# Hackforge Campaign: campaign_1767434573

Generated: 2026-01-03 15:02:53
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `f4b43c22695c82a4`
- **Category**: inj_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{1c46e352f114ccc0151796aa8c058a03}`

**Exploitation Hints**:
- Context: login_form
- MongoDB NoSQL database
- Parameter: username
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `f16e3508768865d9`
- **Category**: bac_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{3c34565bbcbe3e025fb8a2f379cc8486}`

**Exploitation Hints**:
- Access control: timing_vulnerable
- Resource ID type: uuid_v4
- Authentication: jwt_token
- 💡 UUIDs are used but might be predictable or leaked

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
