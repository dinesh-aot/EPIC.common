from epic_cron.services.clamav_service import ClamAVService


class VirusScanner:
    """Service to test file scanning with ClamAV."""

    @staticmethod
    def scan_file_from_path(file_path: str):
        print(f"🧪 Scanning file: {file_path}")
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            clam = ClamAVService()
            infected, info = clam.scan_bytes(data)

            if infected is True:
                print(f"Virus detected: {info}")
            elif infected is False:
                print("File is clean.")
            else:
                print(f"Scan failed or unknown result: {info}")
        except Exception as e:
            print(f"Error scanning file: {e}")
