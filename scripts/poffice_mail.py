import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class PofficeMail:
    def __init__(self, api_key, base_url="https://mail.poffice.online"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }

    def get_domains(self):
        # We use http to the container IP if on host, but here we use the public URL
        # For the script to be robust, we allow overriding the base_url
        response = requests.get(f"{self.base_url}/api/v1/get/domain/all", headers=self.headers, verify=False)
        return response.json()

    def create_mailbox(self, domain, local_part, name, password, quota=3072):
        data = {
            "address": f"{local_part}@{domain}",
            "name": name,
            "domain": domain,
            "local_part": local_part,
            "password": password,
            "password2": password,
            "quota": quota,
            "active": "1"
        }
        response = requests.post(f"{self.base_url}/api/v1/add/mailbox", headers=self.headers, json=data, verify=False)
        return response.json()

    def send_email(self, smtp_user, smtp_pass, to_email, subject, body, smtp_server="mail.poffice.online", smtp_port=587):
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            text = msg.as_string()
            server.sendmail(smtp_user, to_email, text)
            server.quit()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Example usage
    import sys
    # For testing, we can provide the API key as en env var
    API_KEY = os.getenv("MAILCOW_API_KEY", "a58bec3fa214d7f3fecc33625f5827dd")
    client = PofficeMail(API_KEY)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "list-domains":
            print(json.dumps(client.get_domains(), indent=4))
        elif action == "create-mailbox":
            # python3 poffice_mail.py create-mailbox domain user name pass [quota]
            domain = sys.argv[2]
            user = sys.argv[3]
            name = sys.argv[4]
            passwd = sys.argv[5]
            quota = int(sys.argv[6]) if len(sys.argv) > 6 else 3072
            print(json.dumps(client.create_mailbox(domain, user, name, passwd, quota), indent=4))
