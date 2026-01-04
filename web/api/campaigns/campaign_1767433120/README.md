# Hackforge Campaign: campaign_1767433120

Generated: 2026-01-03 14:38:40
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `30848b7173c29523`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{43f9192b6dddab5f4c5aecc62380cb26}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `37316311a58e0d83`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{cfe2d08747fbe0467b17d284551cbdd4}`

**Exploitation Hints**:
- Context: social_media_profile
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
