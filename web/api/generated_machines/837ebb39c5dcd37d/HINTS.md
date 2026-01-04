# Exploitation Hints

**Machine ID:** `837ebb39c5dcd37d`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: document_management
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/users/delete
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{a4f7001ea100fcec235c22b1ac47183a}`
