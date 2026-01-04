# Hackforge Campaign: campaign_1767240185

Generated: 2026-01-01 09:03:05
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `5173f0f00d6b685e`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{f79253f72d5a8b355ac24059ce61a076}`

**Exploitation Hints**:
- Context: file_processor
- Database: mariadb
- Output behavior: base64_encoded
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `97d3163a0fa7d939`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{dfb72eac1ea0a6bb1df6cc4366c5cd08}`

**Exploitation Hints**:
- Context: e_commerce_order
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/settings
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
