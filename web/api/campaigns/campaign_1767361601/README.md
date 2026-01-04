# Hackforge Campaign: campaign_1767361601

Generated: 2026-01-02 18:46:41
Total Machines: 2

## Machines Overview

### Machine 1: SQL Injection
- **Machine ID**: `86e6c8c9ab8f2581`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{9e6d197fe06d9134db66d7bee9b5e6bd}`

**Exploitation Hints**:
- Context: whois_lookup
- Database: sqlite
- Output behavior: error_based
- ⚠️ Filters active: space, semicolon
- 💡 Try: ' OR '1'='1
- 💡 Use error-based extraction
- Flag stored in 'secrets' table

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `5d27f78c522c4d09`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{ebfdde3d693c7e5d6285b7a4d31fa32f}`

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
