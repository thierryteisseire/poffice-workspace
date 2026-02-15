---
name: poffice-admin
description: "Administration and automation for the Poffice suite (Mailcow, Seafile, Paperless-ngx). Use for: (1) Creating and managing mail accounts, (2) Sending and receiving emails, (3) Managing calendars and invites (via SOGo), (4) managing documents (Seafile/Paperless), (5) Creating and updating Word, Excel, and PDF documents, (6) Creating and sending calendar events and invites, (7) Automating office workflows."
---

# Poffice Admin Skill

This skill provides the necessary tools and workflows to manage the Poffice infrastructure.

## Core Capabilities

1. **User & Mail Management**: Create mailboxes, manage domains, and send/receive emails.
2. **Document Management**: Sync files via Seafile and archive documents via Paperless-ngx.
3. **Calendar Management**: Full CRUD management of events (List, Add, Update, Delete) in SOGo (attached to Mailcow) and sending email invites with .ics attachments.
4. **Document Creation**: Generate and update Word (.docx), Excel (.xlsx), and PDF documents programmatically.

## Quick Reference Scripts

The following scripts are available in the `scripts/` directory:

- `poffice_mail.py`: Mailbox creation and email sending.
- `poffice_docs.py`: Seafile user and repo management.
- `poffice_paperless.py`: Document ingestion and listing.
- `poffice_gen.py`: Document creation and update (Word, Excel, PDF).
- `poffice_calendar.py`: Calendar event creation and email invites.

### Typical Workflows

#### Creating a New Office User
To create a fully provisioned user (Mail + Cloud storage):
1. Run `python3 scripts/poffice_mail.py create-mailbox domain.com user_name "Full Name" password`
2. Run `python3 scripts/poffice_docs.py create-user user@domain.com password`

#### Creating and Archiving a Report
1. Use `poffice_gen.py` to create a PDF or Excel report.
2. Use `poffice_paperless.py` to upload the generated file for long-term archiving.
3. Use `poffice_mail.py` to email the report to the team.

#### Scheduling a Meeting and Sending Invites
1. Use `poffice_calendar.py add` to put the event on your own calendar.
2. Use `poffice_calendar.py invite` to send the official invitation to participants.
3. Optionally, use `poffice_gen.py` to create a meeting agenda PDF and attach it to an email using `poffice_mail.py`.

#### Managing Existing Events
1. Use `poffice_calendar.py list` to see upcoming events.
2. Use `poffice_calendar.py delete [UID]` to remove an event.
3. Update events using the `update_event` method in `poffice_calendar.py`.

#### Sending a System Invite
Use `poffice_mail.py send-email` to notify users about account creation or meetings.

## Service Access & Credentials

See [references/credentials.md](references/credentials.md) for API keys and endpoint information.

## Calendar (SOGo)
Calendar management is handled through SOGo. 
- **URL**: `https://mail.poffice.online/SOGo`
- **CalDAV**: `https://mail.poffice.online/SOGo/dav/`
To send invites programmatically, use standard `ics` generation and send via `poffice_mail.py`.

## Documentation
- **Mailcow API**: [references/mailcow_api.md](references/mailcow_api.md)
- **Seafile API**: [references/seafile_api.md](references/seafile_api.md)
- **Paperless API**: [references/paperless_api.md](references/paperless_api.md)
