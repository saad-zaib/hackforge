# Hackforge Campaign: campaign_1767459890

Generated: 2026-01-03 22:04:51
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `5e7e74825a6ab13c`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{a6fe5c5278bf8033d88576f7ae2ba243}`

**Exploitation Hints**:
- Context: search_function
- Database: mariadb
- Output behavior: stored_in_db
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `469852811c1c3455`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{41be9c0bc14b8eabd5d895915620e0f4}`

**Exploitation Hints**:
- Context: banking_transaction
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
