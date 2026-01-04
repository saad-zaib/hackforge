# Exploitation Hints

**Machine ID:** `c2578a7a765f8d66`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: document_management
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/data/all
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{e3c8b920fac056c0331376ad59cf9eef}`
