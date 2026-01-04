# Hackforge Campaign: campaign_1767358725

Generated: 2026-01-02 17:58:45
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `67b4e02428bd76dc`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{3dc4df9db48b0186da7397dd3a432224}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `745565f578956a3e`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{5667b96bd75ed25e4cfc6099769b14f9}`

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
