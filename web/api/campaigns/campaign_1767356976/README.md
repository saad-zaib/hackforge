# Hackforge Campaign: campaign_1767356976

Generated: 2026-01-02 17:29:36
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `b8f8d690543fe1ce`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{697337dff51139e13a4dd20c14e7b205}`

**Exploitation Hints**:
- Context: login_form
- Shell: sh
- Command structure: single_command
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `9c0d31cdda071277`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{826466d25559b5bf90fc84e43eb6b162}`

**Exploitation Hints**:
- Context: banking_transaction
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
