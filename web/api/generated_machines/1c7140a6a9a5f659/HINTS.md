# Exploitation Hints

**Machine ID:** `1c7140a6a9a5f659`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: banking_transaction
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/export
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{a3df8676239556ebf71811c7019088e1}`
