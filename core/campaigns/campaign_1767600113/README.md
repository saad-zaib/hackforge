# Hackforge Campaign: campaign_1767600113

Generated: 2026-01-05 13:01:53
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `573cb4bfb74cff1c`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{18626a831b90773416a1397de8f3b0c2}`

**Exploitation Hints**:
- Context: login_form
- MongoDB NoSQL database
- Parameter: username
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `b9b78cd772ccd4e8`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{cfee4f675260fb2060015584fc40043b}`

**Exploitation Hints**:
- Context: banking_transaction
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
