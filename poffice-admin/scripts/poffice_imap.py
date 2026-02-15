import imaplib
import email
from email.header import decode_header
import os

class PofficeImap:
    def __init__(self, user, password, imap_server="mail.poffice.online", imap_port=993):
        self.user = user
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port

    def list_emails(self, folder="INBOX", limit=5):
        try:
            # Connect to server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.user, self.password)
            mail.select(folder)

            # Search for all emails
            status, messages = mail.search(None, "ALL")
            if status != "OK":
                return {"status": "error", "message": "Failed to search emails"}

            # Get the list of email IDs
            mail_ids = messages[0].split()
            results = []

            # Fetch the last 'limit' emails
            for i in mail_ids[-limit:]:
                status, data = mail.fetch(i, "(RFC822)")
                if status != "OK":
                    continue

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        from_ = msg.get("From")
                        results.append({
                            "id": i.decode(),
                            "from": from_,
                            "subject": subject,
                            "date": msg.get("Date")
                        })

            mail.close()
            mail.logout()
            return {"status": "success", "emails": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) > 2:
        user = sys.argv[1]
        password = sys.argv[2]
        imap = PofficeImap(user, password)
        print(json.dumps(imap.list_emails(), indent=4))
    else:
        print("Usage: python3 poffice_imap.py <user> <password>")
