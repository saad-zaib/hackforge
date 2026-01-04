# Exploitation Hints

**Machine ID:** `cfd9e344a2d7391a`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: document_management
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/users/delete
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{b27c72484e0ace2c5b70d0f34a92b67c}`
