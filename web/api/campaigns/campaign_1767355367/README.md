# Hackforge Campaign: campaign_1767355367

Generated: 2026-01-02 17:02:47
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `c671c8f4d7abaf05`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{0a54adf5e1f5d9dc472e631b1a28bd31}`

**Exploitation Hints**:
- Context: export_tool
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `b08006419f1313ca`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{13e95faee2dab5384aad3b2b3103f74b}`

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
