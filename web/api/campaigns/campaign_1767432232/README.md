# Hackforge Campaign: campaign_1767432232

Generated: 2026-01-03 14:23:52
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `1e77d4cf4bca6a73`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{dc3a06885d00f763424e46f2f3946cf0}`

**Exploitation Hints**:
- Context: login_form
- MongoDB NoSQL database
- Parameter: username
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `74ce00089f1da8d0`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{de8cedc82fa199a0aad9a86f98c6a60f}`

**Exploitation Hints**:
- Access control: weak_session_check
- Resource ID type: sequential_numeric
- Authentication: api_key
- ⚠️ Session validation is weak
- 💡 Try incrementing/decrementing the ID parameter

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
