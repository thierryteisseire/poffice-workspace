# Mailcow API Reference (v1)

Documentation available at: `https://mail.poffice.online/api/` (if enabled)

### Common Endpoints

#### GET /api/v1/get/mailbox/all
Returns list of all mailboxes.

#### POST /api/v1/add/mailbox
Body:
```json
{
  "address": "user@domain.com",
  "name": "Full Name",
  "domain": "domain.com",
  "local_part": "user",
  "password": "password",
  "password2": "password",
  "quota": 3072,
  "active": 1
}
```
