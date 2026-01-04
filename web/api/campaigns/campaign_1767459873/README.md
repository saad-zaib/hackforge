# Hackforge Campaign: campaign_1767459873

Generated: 2026-01-03 22:04:33
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `6d0d5dbf81245a0e`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{38fb1f7bfbee0f94a21268825e4309a9}`

**Exploitation Hints**:
- Context: export_tool
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `1c7140a6a9a5f659`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{a3df8676239556ebf71811c7019088e1}`

**Exploitation Hints**:
- Context: banking_transaction
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
