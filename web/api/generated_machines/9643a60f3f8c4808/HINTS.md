# Exploitation Hints

**Machine ID:** `9643a60f3f8c4808`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: e_commerce_order
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/data/all
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{3de065988c5a417d5f67de7872d44414}`
