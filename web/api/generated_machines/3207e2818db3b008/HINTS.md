# Exploitation Hints

**Machine ID:** `3207e2818db3b008`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: e_commerce_order
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/data/all
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{bf19206998f6b5499c4ac30ec7c0961f}`
