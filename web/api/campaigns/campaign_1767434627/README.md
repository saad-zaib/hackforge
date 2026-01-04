# Hackforge Campaign: campaign_1767434627

Generated: 2026-01-03 15:03:47
Total Machines: 2

## Machines Overview

### Machine 1: NoSQL Injection
- **Machine ID**: `8bb44835085b9e79`
- **Category**: inj_001
- **Difficulty**: 3/5
- **Flag**: `HACKFORGE{680b342859e82b17b3959c71f0fad9a0}`

**Exploitation Hints**:
- Context: export_tool
- MongoDB NoSQL database
- Parameter: category
- 💡 Try NoSQL operators: $ne, $gt, $regex
- 💡 JSON injection possible in POST body
- Flag stored in 'secrets' collection
- ⚠️ Input validation present - bypass needed

---

### Machine 2: Path Traversal
- **Machine ID**: `55ff626ceefcf2c8`
- **Category**: bac_001
- **Difficulty**: 3/5
- **Flag**: `HACKFORGE{72b3faab375b0c8b82c8eb38fbae4cab}`

**Exploitation Hints**:
- Context: document_management
- File viewing/download functionality present
- Flag location: /var/www/flag.txt
- 💡 Try path traversal: ../ or ..\ sequences
- ⚠️ Filters active: double_encoding_needed, null_byte_possible

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
