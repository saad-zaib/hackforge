# Hackforge Campaign: campaign_1767432239

Generated: 2026-01-03 14:23:59
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `de0f2adb4d7c97e6`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{5cead86d7a5780d435954068f0ea901b}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `b38dd191d959139c`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{40a74a4a9c0e8d171249c6cb0110fe69}`

**Exploitation Hints**:
- Context: banking_transaction
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
