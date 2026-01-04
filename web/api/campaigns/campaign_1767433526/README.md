# Hackforge Campaign: campaign_1767433526

Generated: 2026-01-03 14:45:26
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `e0a51b1cd5cf502c`
- **Category**: inj_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{67a9a707e12bef6fb6eef8d9d992d85c}`

**Exploitation Hints**:
- Context: search_function
- Database: mongodb
- Output behavior: blind
- ✓ No input filtering - direct injection possible
- 💡 Try: ' OR '1'='1
- 💡 Blind SQLi - use time-based or boolean techniques
- Flag stored in 'secrets' table

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `55954b3e037653e4`
- **Category**: bac_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{723e1b56a4d5b81f12672e2d39bbfd4d}`

**Exploitation Hints**:
- Access control: none
- Resource ID type: md5_hash
- Authentication: none
- ✓ No access control - direct ID manipulation possible

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
