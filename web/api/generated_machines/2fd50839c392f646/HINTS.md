# Exploitation Hints

**Machine ID:** `2fd50839c392f646`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: social_media_profile
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/users/delete
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{9825725e08e6973bae1d37cf48c8331e}`
