# Hackforge Campaign: campaign_1767434639

Generated: 2026-01-03 15:03:59
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `fa70f64ac7d77159`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{853a99aebb405da2a8f4d0d05cdc1803}`

**Exploitation Hints**:
- Context: log_analyzer
- Database: sqlite
- Output behavior: error_based
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- 💡 Use error-based extraction
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `7a623f50ee5f0deb`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{db76ff38604b01b5f0fff43f09ec32d3}`

**Exploitation Hints**:
- Context: social_media_profile
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/export
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
