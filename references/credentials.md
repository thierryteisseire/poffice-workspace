# Poffice Credentials & Endpoints

| Service | Endpoint | Admin User | Notes |
|---------|----------|------------|-------|
| Mailcow (Mail/UI) | `https://mail.poffice.online` | `admin` | API Key: `a58bec3fa214d7f3fecc33625f5827dd` |
| Seafile (Cloud) | `https://cloud.poffice.online` | `admin@poffice.online` | Password: `SeafileCloud2025` |
| Paperless (Docs) | `https://docs.poffice.online` | `admin` | Token: `4b0241573134642fa9e92582f445a2f06045ad46` |
| Workspace | `https://workspace.poffice.online` | `admin@poffice.online` | Password: `Poffice2025` |

## API Integration Details

### Mailcow
- **Auth Header**: `X-API-Key: a58bec3fa214d7f3fecc33625f5827dd`
- **Port (Local)**: 8083

### Seafile
- **Auth**: `POST /api2/auth-token/` to get token.

### Paperless
- **Auth Header**: `Authorization: Token 4b0241573134642fa9e92582f445a2f06045ad46`
