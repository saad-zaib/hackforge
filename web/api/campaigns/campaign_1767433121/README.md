# Hackforge Campaign: campaign_1767433121

Generated: 2026-01-03 14:38:41
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `12cb18c8093901c8`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{05fe9caa9c64d5b7e38014186d6965cc}`

**Exploitation Hints**:
- Context: login_form
- MongoDB NoSQL database
- Parameter: username
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `c7bf45bf402c8799`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{5577e05acb5c8da6cde03f658ca22d8b}`

**Exploitation Hints**:
- Access control: client_side_only
- Resource ID type: base64_encoded
- Authentication: jwt_token
- ⚠️ Access checks are client-side only
- 💡 IDs are base64 encoded - try decoding and modifying

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
