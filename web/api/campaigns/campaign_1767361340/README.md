# Hackforge Campaign: campaign_1767361340

Generated: 2026-01-02 18:42:20
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `6c972264e16c825f`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{4a3c80f0ac14fbb226aba711b23139bf}`

**Exploitation Hints**:
- Context: export_tool
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `fb538dc0bd07dcde`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{a47521ffd01424e440605fd9a639f726}`

**Exploitation Hints**:
- Access control: client_side_only
- Resource ID type: predictable_pattern
- Authentication: jwt_token
- ⚠️ Access checks are client-side only

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
