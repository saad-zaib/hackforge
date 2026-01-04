# Hackforge Campaign: campaign_1767433562

Generated: 2026-01-03 14:46:02
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `bd10ca53210fd71c`
- **Category**: inj_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{4d25960b40d0d374093b0e990ff9a642}`

**Exploitation Hints**:
- Context: log_analyzer
- Database: mongodb
- Output behavior: stored_in_db
- ✓ No input filtering - direct injection possible
- 💡 Try: ' OR '1'='1
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `25bb0620cad36f69`
- **Category**: bac_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{62c0f7d0fadbe919c5317c06d65bfbe1}`

**Exploitation Hints**:
- Context: banking_transaction
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/data/all
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
