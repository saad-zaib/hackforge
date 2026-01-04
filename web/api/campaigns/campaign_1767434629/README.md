# Hackforge Campaign: campaign_1767434629

Generated: 2026-01-03 15:03:49
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `87c1b436f6b3e8dd`
- **Category**: inj_001
- **Difficulty**: 3/5
- **Flag**: `HACKFORGE{8eba84c029b11e6d21804e5194e75d64}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection
- ⚠️ Input validation present - bypass needed

---

### Machine 2: Vertical Privilege Escalation
- **Machine ID**: `be49b5e0cc3bf8d8`
- **Category**: bac_001
- **Difficulty**: 3/5
- **Flag**: `HACKFORGE{07c3c58e9150efd0e484084bd27d9a99}`

**Exploitation Hints**:
- Context: document_management
- You are: user1 (role: user)
- Target: Admin panel access
- 💡 JWT token may contain role claim that can be modified
- ⚠️ Try to access /admin or modify your privileges

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
