import time

import requests
from flask import current_app


class EpicPublicService:
    """Service to fetch document data from EPIC Public API."""

    DOCUMENT_PAGE_SIZE = 100
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds between retries on transient errors

    DEFAULT_DOCUMENT_TYPE_ID = 1

    @classmethod
    def _get_document_type_id_map(cls):
        """Return the document type ID map from EPIC_PUBLIC_DOCUMENT_TYPE_ID_MAP config.

        Format: comma-separated "epicId:conditionTypeId" pairs.
        Example: "5cf00c03a266b7e1877504d1:3,5cf00c03a266b7e1877504d5:1"
        """
        configured = current_app.config.get("EPIC_PUBLIC_DOCUMENT_TYPE_ID_MAP", "")
        result = {}
        for pair in configured.split(","):
            pair = pair.strip()
            if ":" not in pair:
                continue
            epic_id, _, cond_id = pair.partition(":")
            epic_id = epic_id.strip()
            cond_id = cond_id.strip()
            if epic_id and cond_id.isdigit():
                result[epic_id] = int(cond_id)
        return result

    @classmethod
    def _get_document_type_ids(cls):
        """Return the list of document type IDs to fetch, from config or the type map keys."""
        configured = current_app.config.get("EPIC_PUBLIC_DOCUMENT_TYPE_IDS", "")
        if configured:
            return [t.strip() for t in configured.split(",") if t.strip()]
        return list(cls._get_document_type_id_map().keys())

    @classmethod
    def fetch_all_documents(cls):
        """Fetch all documents across all configured document types.

        Returns:
            list[dict]: Combined list of mapped document dicts from all types.
        """
        all_documents = []
        for type_id in cls._get_document_type_ids():
            raw_docs = cls._fetch_documents_by_type(type_id)
            mapped = cls._map_documents(raw_docs, type_id)
            all_documents.extend(mapped)
            current_app.logger.info(f"Type {type_id}: {len(mapped)} documents mapped.")

        current_app.logger.info(f"Total documents fetched across all types: {len(all_documents)}")
        return all_documents

    @classmethod
    def _fetch_documents_by_type(cls, type_id):
        """Fetch all documents for a single document type, paginating until exhausted.

        Args:
            type_id: EPIC Public document type ID.

        Returns:
            list[dict]: Raw document dicts for this type.
        """
        base_url = current_app.config.get("EPIC_PUBLIC_BASE_URL", "https://projects.eao.gov.bc.ca")
        endpoint = f"{base_url}/api/public/search"
        page_num = 0
        documents = []

        current_app.logger.info(f"Fetching documents for type: {type_id}")

        while True:
            params = {
                "dataset": "Document",
                "pageNum": page_num,
                "pageSize": cls.DOCUMENT_PAGE_SIZE,
                "projectLegislation": "default",
                "sortBy": "-datePosted,",
                "populate": "true",
                "fields": "",
                "fuzzy": "true",
                "and[documentSource]": "PROJECT",
                "and[type]": type_id,
            }

            data = cls._fetch_page(endpoint, params, type_id, page_num)
            results = data[0].get("searchResults", []) if isinstance(data, list) and data else []

            if not results:
                break

            documents.extend(results)
            current_app.logger.info(
                f"  Type {type_id} | Page {page_num}: fetched {len(results)} documents"
            )

            if len(results) < cls.DOCUMENT_PAGE_SIZE:
                break

            page_num += 1

        current_app.logger.info(f"  Type {type_id}: {len(documents)} documents total")
        return documents

    @classmethod
    def _fetch_page(cls, endpoint, params, type_id, page_num):
        """Fetch a single page with retry on transient server errors (5xx)."""
        for attempt in range(1, cls.MAX_RETRIES + 1):
            try:
                response = requests.get(endpoint, params=params, timeout=60)
                response.raise_for_status()
                return response.json()
            except requests.HTTPError as e:
                if response.status_code < 500:
                    current_app.logger.error(
                        f"HTTP {response.status_code} fetching type={type_id} page={page_num}: {e}"
                    )
                    raise
                if attempt < cls.MAX_RETRIES:
                    current_app.logger.warning(
                        f"HTTP {response.status_code} on type={type_id} page={page_num} "
                        f"(attempt {attempt}/{cls.MAX_RETRIES}), retrying in {cls.RETRY_DELAY}s..."
                    )
                    time.sleep(cls.RETRY_DELAY)
                else:
                    current_app.logger.error(
                        f"HTTP {response.status_code} on type={type_id} page={page_num} "
                        f"after {cls.MAX_RETRIES} attempts: {e}"
                    )
                    raise
            except requests.RequestException as e:
                current_app.logger.error(
                    f"Request error fetching type={type_id} page={page_num}: {e}"
                )
                raise

    @classmethod
    def _map_documents(cls, raw_docs, type_id):
        """Map raw EPIC Public document records to the format expected by the extractor.

        Args:
            raw_docs: Raw document dicts from the EPIC Public API.
            type_id: The EPIC Public type ID used to fetch these docs.

        Returns:
            list[dict]: Mapped documents, skipping any with missing required fields.
        """
        mapped = []
        condition_type_id = cls._get_document_type_id_map().get(type_id, cls.DEFAULT_DOCUMENT_TYPE_ID)

        for item in raw_docs:
            document_id = item.get("_id")
            project = item.get("project") or {}
            project_id = project.get("_id") if isinstance(project, dict) else project

            if not document_id or not project_id:
                continue

            mapped.append({
                "document_id": str(document_id),
                "document_label": item.get("displayName"),
                "document_file_name": item.get("documentFileName"),
                "date_issued": item.get("datePosted"),
                "act": item.get("legislation"),
                "project_id": str(project_id),
                "document_type_id": condition_type_id,
            })

        return mapped
