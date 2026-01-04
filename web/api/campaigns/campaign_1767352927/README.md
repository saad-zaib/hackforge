# Hackforge Campaign: campaign_1767352927

Generated: 2026-01-02 16:22:07
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `86dd2af5c3c23f91`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{b917b4fae2f0fbea778559a6fe0d2289}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `cd5c40bc75237d3d`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{b4cf8a7172b99bb661394e5b61c9fb3c}`

**Exploitation Hints**:
- Access control: none
- Resource ID type: sequential_numeric
- Authentication: session_cookie
- ✓ No access control - direct ID manipulation possible
- 💡 Try incrementing/decrementing the ID parameter

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
