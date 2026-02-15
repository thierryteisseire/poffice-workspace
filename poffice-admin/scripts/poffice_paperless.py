import requests
import json
import os

class PaperlessAdmin:
    def __init__(self, token, base_url="https://docs.poffice.online"):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

    def list_documents(self):
        response = requests.get(f"{self.base_url}/api/documents/", headers=self.headers, verify=False)
        return response.json()

    def upload_document(self, file_path, title=None):
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {}
            if title:
                data["title"] = title
            response = requests.post(f"{self.base_url}/api/documents/post_document/", headers={"Authorization": f"Token {self.token}"}, files=files, data=data, verify=False)
            return response.json()

if __name__ == "__main__":
    import sys
    # For Paperless, we need an API token. 
    # Paperless tokens are created in the Django admin or via a POST to /api/token/ (if enabled)
    # For now, we assume the user provides it or we use a known one.
    TOKEN = os.getenv("PAPERLESS_TOKEN")
    if not TOKEN:
        print("Error: PAPERLESS_TOKEN env var required")
        sys.exit(1)
        
    admin = PaperlessAdmin(TOKEN)
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "list":
            print(json.dumps(admin.list_documents(), indent=4))
        elif action == "upload":
            print(json.dumps(admin.upload_document(sys.argv[2]), indent=4))
