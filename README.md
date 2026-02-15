# Poffice Admin Skill

Administration and automation suite for the **Poffice** ecosystem (Mailcow, Seafile, Paperless-ngx, SOGo).

## 🚀 Overview

The `poffice-admin` skill provides a comprehensive set of Python scripts and documentation to manage a self-hosted office stack. It enables automation of user provisioning, mail management, document generation, and calendar orchestration.

---

## 🛠 Features & Functions

### 1. Mail & User Management (`poffice_mail.py`)
- **List Domains**: Retrieve all domains managed by the Mailcow instance.
- **Create Mailbox**: Provision new email accounts with specific quotas and settings.
- **Send Email**: Send plain text emails via SMTP with TLS support.

### 2. Cloud Storage Management (`poffice_docs.py`)
- **User Provisioning**: Create, list, and delete Seafile users.
- **Library Management**: Create and list Seafile libraries (repositories).
- **File Operations**: Programmatic upload and download of files to/from the cloud.

### 3. Document Archiving (`poffice_paperless.py`)
- **List Documents**: Query the Paperless-ngx archive for stored documents.
- **Upload Document**: Direct ingestion of files into the Paperless-ngx processing pipeline.

### 4. Calendar Orchestration (`poffice_calendar.py`)
- **CRUD Operations**: Add, List, Update, and Delete events via CalDAV.
- **Meeting Invites**: Generate and send official `.ics` meeting invitations to participants.
- **SOGo Integration**: Fully compatible with the SOGo groupware suite.

### 5. Document Generation (`poffice_gen.py`)
- **Word (.docx)**: Create and update Word documents with headings and paragraphs.
- **Excel (.xlsx)**: Generate spreadsheets from python data structures.
- **PDF**: Create professional PDF reports programmatically.

### 6. Email Interaction (`poffice_imap.py`)
- **Read Mail**: List and fetch recent emails from any IMAP folder (e.g., INBOX).
- **Header Parsing**: Extracts Subject, From, and Date for automation triggers.

### 7. Master Admin Sync (`poffice_master_admin.py`)
- **Neon Integration**: Interfaces with Neon PostgreSQL to check "Master Admin" status.
- **Cross-App Sync**: Automatically provisions a user across Mail and Seafile once they are verified as an admin in the central Neon database.

---

## 📂 Repository Structure

```text
poffice-admin/
├── SKILL.md             # Core skill description and triggers
├── scripts/             # Python automation scripts
│   ├── poffice_mail.py
│   ├── poffice_docs.py
│   ├── poffice_calendar.py
│   └── ...
└── references/          # API references and credential templates
```

## 📋 Usage

Most scripts can be run directly via CLI:

```bash
# Example: Create a mailbox
python3 scripts/poffice_mail.py create-mailbox example.com user "John Doe" "password123"

# Example: Create a PDF report
python3 scripts/poffice_gen.py create-pdf report.pdf "Monthly Summary" "All systems operational."
```

## 🔐 Configuration

Credentials should be managed via environment variables or the `references/credentials.md` template.
- `MAILCOW_API_KEY`
- `SEAFILE_ADMIN_EMAIL` / `SEAFILE_ADMIN_PASSWORD`
- `PAPERLESS_TOKEN`
- `DATABASE_URL` (Neon PostgreSQL)
