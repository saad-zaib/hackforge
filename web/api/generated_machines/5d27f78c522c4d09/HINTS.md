# Exploitation Hints

**Machine ID:** `5d27f78c522c4d09`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: document_management
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/users/delete
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{ebfdde3d693c7e5d6285b7a4d31fa32f}`
