import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import subprocess

class PofficeMasterAdmin:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_user_from_neon(self, email):
        conn = psycopg2.connect(self.db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM "User" WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    def is_master_admin(self, email):
        user = self.get_user_from_neon(email)
        return user and user.get('isAdmin', False)

    def synchronize_admin_access(self, email, password, name):
        """
        Ensures the user has administrative access or at least a mailbox 
        and accounts in all integrated apps.
        """
        if not self.is_master_admin(email):
            return {"status": "error", "message": f"User {email} is not a master admin in Neon."}

        results = {}

        # 1. Sync Mailbox
        try:
            # We use the existing poffice_mail.py script
            # Suppress warnings with -W ignore
            cmd = ["python3", "-W", "ignore", ".agents/skills/poffice-admin/scripts/poffice_mail.py", "create-mailbox", "poffice.online", email.split('@')[0], name, password, "512"]
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
            results["mail"] = json.loads(output)
        except Exception as e:
            results["mail"] = {"status": "error", "message": f"Raw output: {output if 'output' in locals() else 'None'}. Error: {str(e)}"}

        # 2. Sync Seafile
        try:
            cmd = ["python3", "-W", "ignore", ".agents/skills/poffice-admin/scripts/poffice_docs.py", "create-user", email, password, "true"]
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
            results["seafile"] = json.loads(output)
        except Exception as e:
            results["seafile"] = {"status": "error", "message": f"Raw output: {output if 'output' in locals() else 'None'}. Error: {str(e)}"}
        
        # 3. Sync Paperless (Optional: depending on if paperless has per-user admin)
        # For now we just acknowledge the check
        results["paperless"] = {"status": "not_implemented", "message": "Manual token management required for Paperless-ngx admin access."}

        return {"status": "success", "results": results}

if __name__ == "__main__":
    import sys
    # Load DB URL from .env or provided
    DB_URL = os.getenv("DATABASE_URL", "")
    
    manager = PofficeMasterAdmin(DB_URL)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "check":
            # python3 poffice_master_admin.py check email
            email = sys.argv[2]
            print(json.dumps({"isAdmin": manager.is_master_admin(email)}, indent=4))
        elif action == "sync":
            # python3 poffice_master_admin.py sync email password name
            email = sys.argv[2]
            password = sys.argv[3]
            name = sys.argv[4]
            print(json.dumps(manager.synchronize_admin_access(email, password, name), indent=4))
        else:
            print("Unknown action")
    else:
        print("Usage: python3 poffice_master_admin.py <check|sync> <email> [password] [name]")
