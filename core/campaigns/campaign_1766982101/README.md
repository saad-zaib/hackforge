# Hackforge Campaign: campaign_1766982101

Generated: 2025-12-29 09:21:41
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `3bc05f7751e37e9a`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{f27a52423057c31ce191716475d0e6f0}`

**Exploitation Hints**:
- Context: search_function
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `dcab7899adabf216`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{3a16bb4623c6a1c498525a003b21a496}`

**Exploitation Hints**:
- Access control: timing_vulnerable
- Resource ID type: sequential_numeric
- Authentication: session_cookie
- 💡 Try incrementing/decrementing the ID parameter

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
