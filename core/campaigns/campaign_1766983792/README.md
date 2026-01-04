# Hackforge Campaign: campaign_1766983792

Generated: 2025-12-29 09:49:52
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `cffe83e967363abe`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{43719b5348da55836fe36c3d6940845b}`

**Exploitation Hints**:
- Context: log_analyzer
- Database: mongodb
- Output behavior: stored_in_db
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `f8300556ea105720`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{abce71c3a7d3b93ba8b04c34367fb969}`

**Exploitation Hints**:
- Context: document_management
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/users/delete
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
