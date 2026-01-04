# Hackforge Campaign: campaign_1767357304

Generated: 2026-01-02 17:35:04
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `611352cd036933d3`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{741c7c6ef798d255de6dc2cc598da825}`

**Exploitation Hints**:
- Context: login_form
- Database: mariadb
- Output behavior: blind
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- 💡 Blind SQLi - use time-based or boolean techniques
- Flag stored in 'secrets' table

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `1adf41a2a1245c21`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{667e986e1972bf93fcbc5b9652dccdbb}`

**Exploitation Hints**:
- Access control: predictable_token
- Resource ID type: predictable_pattern
- Authentication: jwt_token

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
