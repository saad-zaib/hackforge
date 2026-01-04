# Hackforge Campaign: campaign_1767241522

Generated: 2026-01-01 09:25:22
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `047a18058a2c3425`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{e8d8bf2d6a004c530f06f706032adb89}`

**Exploitation Hints**:
- Context: whois_lookup
- Database: mariadb
- Output behavior: logged_to_file
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `a3e3729517e44d32`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{66429da1fdbf3db5dcc30d475207a4f6}`

**Exploitation Hints**:
- Context: e_commerce_order
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/data/all
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
