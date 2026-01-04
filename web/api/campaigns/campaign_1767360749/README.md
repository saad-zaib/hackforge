# Hackforge Campaign: campaign_1767360749

Generated: 2026-01-02 18:32:29
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `30122d818171a65c`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{0eb3bf4458fa39edb6f4bc25f28fb9c1}`

**Exploitation Hints**:
- Context: export_tool
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `4f1fe9aa9573f3c6`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{0fd976371e805cc580cef2cf79d5acaa}`

**Exploitation Hints**:
- Access control: predictable_token
- Resource ID type: uuid_v4
- Authentication: api_key
- 💡 UUIDs are used but might be predictable or leaked

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
