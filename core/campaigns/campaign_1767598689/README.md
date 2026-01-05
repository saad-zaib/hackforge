# Hackforge Campaign: campaign_1767598689

Generated: 2026-01-05 12:38:09
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `5575ed1245337152`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{b737d46e9fa9d7a0869daebf8137fee2}`

**Exploitation Hints**:
- Context: export_tool
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `9ddc81af04acb0e7`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{285796f3b3e0937f82875e6920ddebfd}`

**Exploitation Hints**:
- Context: document_management
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
