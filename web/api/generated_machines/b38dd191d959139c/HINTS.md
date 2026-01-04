# Exploitation Hints

**Machine ID:** `b38dd191d959139c`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: banking_transaction
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/data/all
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{40a74a4a9c0e8d171249c6cb0110fe69}`
