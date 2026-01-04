# Hackforge Campaign: campaign_1767434635

Generated: 2026-01-03 15:03:55
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `d8b87546abb4409e`
- **Category**: inj_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{d808ca2af8809bd9359b83ce99c98aa0}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `464535d036bd59ea`
- **Category**: bac_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{6dc596d5aa4b44a9a59611414625fc50}`

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
