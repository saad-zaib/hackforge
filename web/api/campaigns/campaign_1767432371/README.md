# Hackforge Campaign: campaign_1767432371

Generated: 2026-01-03 14:26:11
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `81e1cbcaffdc99d5`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{f67322cd2e83e3a807f6d7c41f94cbde}`

**Exploitation Hints**:
- Context: login_form
- Database: mongodb
- Output behavior: stored_in_db
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `2fd50839c392f646`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{9825725e08e6973bae1d37cf48c8331e}`

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
