import time

import requests
from flask import current_app


class EpicPublicService:
    """Service to fetch document data from EPIC Public API."""

    DOCUMENT_PAGE_SIZE = 100
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds between retries on transient errors

    DEFAULT_DOCUMENT_TYPE_ID = 1
    DEFAULT_SEARCH_PATH = "/api/public/search"

    @classmethod
    def _get_optional_int_config(cls, key):
        value = current_app.config.get(key, "")
        if value in (None, ""):
            return None
        try:
            parsed = int(value)
            return parsed if parsed > 0 else None
        except (TypeError, ValueError):
            current_app.logger.warning("Invalid integer for %s: %r", key, value)
            return None

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
        type_ids = cls._get_document_type_ids()
        current_app.logger.info(
            "EPIC Public fetch starting with base_url=%s search_path=%s configured_type_ids=%s "
            "type_map_size=%s max_pages=%s max_documents=%s",
            current_app.config.get("EPIC_PUBLIC_BASE_URL", "https://projects.eao.gov.bc.ca"),
            current_app.config.get("EPIC_PUBLIC_SEARCH_PATH", cls.DEFAULT_SEARCH_PATH),
            type_ids,
            len(cls._get_document_type_id_map()),
            cls._get_optional_int_config("EPIC_PUBLIC_MAX_PAGES"),
            cls._get_optional_int_config("EPIC_PUBLIC_MAX_DOCUMENTS"),
        )

        if not type_ids:
            current_app.logger.warning(
                "No EPIC Public document type IDs configured; fetching all published PROJECT "
                "documents without a type filter."
            )
            raw_docs = cls._fetch_documents_by_type()
            mapped = cls._map_documents(raw_docs)
            current_app.logger.info(f"Fetched {len(mapped)} documents without type filtering.")
            return mapped

        all_documents = []
        for type_id in type_ids:
            raw_docs = cls._fetch_documents_by_type(type_id)
            mapped = cls._map_documents(raw_docs, type_id)
            all_documents.extend(mapped)
            current_app.logger.info(f"Type {type_id}: {len(mapped)} documents mapped.")

        current_app.logger.info(f"Total documents fetched across all types: {len(all_documents)}")
        return all_documents

    @classmethod
    def _fetch_documents_by_type(cls, type_id=None):
        """Fetch all documents for a single document type, paginating until exhausted.

        Args:
            type_id: Optional EPIC Public document type ID.

        Returns:
            list[dict]: Raw document dicts for this type.
        """
        base_url = current_app.config.get("EPIC_PUBLIC_BASE_URL", "https://projects.eao.gov.bc.ca")
        search_path = current_app.config.get("EPIC_PUBLIC_SEARCH_PATH", cls.DEFAULT_SEARCH_PATH)
        endpoint = f"{base_url}{search_path}"
        page_num = 0
        documents = []
        max_pages = cls._get_optional_int_config("EPIC_PUBLIC_MAX_PAGES")
        max_documents = cls._get_optional_int_config("EPIC_PUBLIC_MAX_DOCUMENTS")

        if type_id:
            current_app.logger.info(f"Fetching documents for type: {type_id}")
        else:
            current_app.logger.info("Fetching documents without type filter")

        while True:
            params = {
                "dataset": "Document",
                "pageNum": page_num,
                "pageSize": cls.DOCUMENT_PAGE_SIZE,
                "projectLegislation": "default",
                "sortBy": "-datePosted",
                "populate": "true",
                "fields": "",
                "fuzzy": "false",
                "and[documentSource]": "PROJECT",
            }
            if type_id:
                params["and[type]"] = type_id

            current_app.logger.info(
                "Requesting EPIC Public documents endpoint=%s type_id=%s page=%s page_size=%s params=%s",
                endpoint,
                type_id,
                page_num,
                cls.DOCUMENT_PAGE_SIZE,
                params,
            )

            data = cls._fetch_page(endpoint, params, type_id, page_num)
            results = data[0].get("searchResults", []) if isinstance(data, list) and data else []
            meta = data[0].get("meta", []) if isinstance(data, list) and data else []
            total = meta[0].get("searchResultsTotal") if meta and isinstance(meta[0], dict) else None

            current_app.logger.info(
                "Received EPIC Public response type_id=%s page=%s result_count=%s reported_total=%s",
                type_id,
                page_num,
                len(results),
                total,
            )

            if not results:
                current_app.logger.warning(
                    "No EPIC Public documents returned for type_id=%s on page=%s. Stopping pagination.",
                    type_id,
                    page_num,
                )
                break

            documents.extend(results)
            current_app.logger.info(
                f"  Type {type_id} | Page {page_num}: fetched {len(results)} documents"
            )

            if max_documents and len(documents) >= max_documents:
                documents = documents[:max_documents]
                current_app.logger.warning(
                    "Stopping EPIC Public fetch early because EPIC_PUBLIC_MAX_DOCUMENTS=%s was reached "
                    "for type_id=%s.",
                    max_documents,
                    type_id,
                )
                break

            if len(results) < cls.DOCUMENT_PAGE_SIZE:
                break

            if max_pages and (page_num + 1) >= max_pages:
                current_app.logger.warning(
                    "Stopping EPIC Public fetch early because EPIC_PUBLIC_MAX_PAGES=%s was reached "
                    "for type_id=%s.",
                    max_pages,
                    type_id,
                )
                break

            page_num += 1

        scope = f"Type {type_id}" if type_id else "Unfiltered search"
        current_app.logger.info(f"  {scope}: {len(documents)} documents total")
        return documents

    @classmethod
    def _fetch_page(cls, endpoint, params, type_id, page_num):
        """Fetch a single page with retry on transient server errors (5xx)."""
        for attempt in range(1, cls.MAX_RETRIES + 1):
            try:
                current_app.logger.info(
                    "Fetching EPIC Public page attempt=%s/%s type_id=%s page=%s",
                    attempt,
                    cls.MAX_RETRIES,
                    type_id,
                    page_num,
                )
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
    def _map_documents(cls, raw_docs, type_id=None):
        """Map raw EPIC Public document records to the format expected by the extractor.

        Args:
            raw_docs: Raw document dicts from the EPIC Public API.
            type_id: The optional EPIC Public type ID used to fetch these docs.

        Returns:
            list[dict]: Mapped documents, skipping any with missing required fields.
        """
        mapped = []
        condition_type_id = cls._get_document_type_id_map().get(type_id, cls.DEFAULT_DOCUMENT_TYPE_ID)
        skipped_missing_document_id = 0
        skipped_missing_project_id = 0

        for item in raw_docs:
            document_id = item.get("_id")
            project = item.get("project") or {}
            project_id = project.get("_id") if isinstance(project, dict) else project

            if not document_id:
                skipped_missing_document_id += 1
                continue

            if not project_id:
                skipped_missing_project_id += 1
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

        current_app.logger.info(
            "Mapped EPIC Public documents type_id=%s mapped=%s skipped_missing_document_id=%s "
            "skipped_missing_project_id=%s condition_type_id=%s",
            type_id,
            len(mapped),
            skipped_missing_document_id,
            skipped_missing_project_id,
            condition_type_id,
        )
        return mapped
