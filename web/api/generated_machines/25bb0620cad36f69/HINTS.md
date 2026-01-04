# Exploitation Hints

**Machine ID:** `25bb0620cad36f69`
**Variant:** Missing Function Level Access Control
**Difficulty:** 1/5

## Hints

1. Context: banking_transaction
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/data/all
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{62c0f7d0fadbe919c5317c06d65bfbe1}`
