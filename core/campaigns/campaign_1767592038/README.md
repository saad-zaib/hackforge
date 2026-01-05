# Hackforge Campaign: campaign_1767592038

Generated: 2026-01-05 10:47:18
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `54b4f6bb081d8b6a`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{0bb50a5ab599ce95fcdd0a7a3cc06e86}`

**Exploitation Hints**:
- Context: log_analyzer
- Database: sqlite
- Output behavior: stored_in_db
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `6ccf3ef1194ae044`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{5b9417cbcd05eb524346ec3fd947f2bb}`

**Exploitation Hints**:
- Context: social_media_profile
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/users/delete
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
