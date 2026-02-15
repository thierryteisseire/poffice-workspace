import requests
import json
import os

class SeafileAdmin:
    def __init__(self, username, password, base_url="https://cloud.poffice.online"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.token = self._get_token()
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

    def _get_token(self):
        response = requests.post(f"{self.base_url}/api2/auth-token/", data={
            "username": self.username,
            "password": self.password
        }, verify=False)
        if response.status_code == 200:
            return response.json()["token"]
        else:
            raise Exception(f"Failed to get Seafile token: {response.text}")

    def create_user(self, email, password, is_admin=False):
        # Admin endpoint to create user
        data = {
            "email": email,
            "password": password,
            "is_staff": "true" if is_admin else "false"
        }
        # Use v2.1 for better admin control
        response = requests.post(f"{self.base_url}/api/v2.1/admin/users/", headers=self.headers, json=data, verify=False)
        return response.json()

    def list_users(self):
        # Use v2.1 admin endpoint
        response = requests.get(f"{self.base_url}/api/v2.1/admin/users/", headers=self.headers, verify=False)
        return response.json()

    def delete_user(self, email):
        # Use v2.1 admin endpoint
        response = requests.delete(f"{self.base_url}/api/v2.1/admin/users/{email}/", headers=self.headers, verify=False)
        return response.json() if response.content else {"status": "ok"}

    def list_repos(self):
        response = requests.get(f"{self.base_url}/api2/repos/", headers=self.headers, verify=False)
        return response.json()

    def create_repo(self, name):
        # Note: creates a repo for the current user
        response = requests.post(f"{self.base_url}/api2/repos/", headers=self.headers, json={"name": name}, verify=False)
        return response.json()

    def list_files(self, repo_id, path="/"):
        response = requests.get(f"{self.base_url}/api2/repos/{repo_id}/dir/?p={path}", headers=self.headers, verify=False)
        return response.json()

    def upload_file(self, repo_id, file_path, target_path="/"):
        # 1. Get upload link
        response = requests.get(f"{self.base_url}/api2/repos/{repo_id}/upload-link/", headers=self.headers, verify=False)
        upload_url = response.json() # This is the direct string of the URL
        
        # 2. Upload file
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {
                'file': (filename, f),
                'parent_dir': (None, target_path)
            }
            # Upload doesn't use the standard json headers
            upload_response = requests.post(upload_url, headers={"Authorization": f"Token {self.token}"}, files=files, verify=False)
            return upload_response.text

    def download_file(self, repo_id, file_path, save_as):
        # 1. Get download link
        response = requests.get(f"{self.base_url}/api2/repos/{repo_id}/file/?p={file_path}", headers=self.headers, verify=False)
        download_url = response.json() # Direct string
        
        # 2. Download content
        r = requests.get(download_url, verify=False)
        with open(save_as, 'wb') as f:
            f.write(r.content)
        return save_as

if __name__ == "__main__":
    import sys
    # Example usage
    USER = os.getenv("SEAFILE_ADMIN_EMAIL", "")
    PASS = os.getenv("SEAFILE_ADMIN_PASSWORD", "")
    
    admin = SeafileAdmin(USER, PASS)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "list-users":
            print(json.dumps(admin.list_users(), indent=4))
        elif action == "create-user":
            # python3 poffice_docs.py create-user email pass [is_admin]
            is_admin = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
            print(json.dumps(admin.create_user(sys.argv[2], sys.argv[3], is_admin), indent=4))
        elif action == "delete-user":
            # python3 poffice_docs.py delete-user email
            print(json.dumps(admin.delete_user(sys.argv[2]), indent=4))
        elif action == "list-repos":
            print(json.dumps(admin.list_repos(), indent=4))
        elif action == "create-repo":
            # python3 poffice_docs.py create-repo name
            print(json.dumps(admin.create_repo(sys.argv[2]), indent=4))
        elif action == "list-files":
            # python3 poffice_docs.py list-files repo_id [path]
            path = sys.argv[3] if len(sys.argv) > 3 else "/"
            print(json.dumps(admin.list_files(sys.argv[2], path), indent=4))
        elif action == "upload":
            # python3 poffice_docs.py upload repo_id file_path [target_path]
            target = sys.argv[4] if len(sys.argv) > 4 else "/"
            print(admin.upload_file(sys.argv[2], sys.argv[3], target))
        elif action == "download":
            # python3 poffice_docs.py download repo_id file_path save_as
            print(admin.download_file(sys.argv[2], sys.argv[3], sys.argv[4]))
