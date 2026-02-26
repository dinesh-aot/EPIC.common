from epic_cron.services.clamav_service import ClamAVService


class VirusScanner:
    """Service to test file scanning with ClamAV."""

    @staticmethod
    def scan_file_from_path(file_path: str):
        print(f"Scanning file: {file_path}")
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            clam = ClamAVService()
            infected, info = clam.scan_bytes(data)

            if infected is True:
                current_app.logger.warning(f"Virus detected: {info}")
            elif infected is False:
                current_app.logger.info("File is clean.")
            else:
                current_app.logger.warning(f"Scan failed or unknown result: {info}")
        except Exception as e:
            current_app.logger.error(f"Error scanning file: {e}")
