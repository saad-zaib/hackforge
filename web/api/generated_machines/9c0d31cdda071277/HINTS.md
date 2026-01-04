# Exploitation Hints

**Machine ID:** `9c0d31cdda071277`
**Variant:** Missing Function Level Access Control
**Difficulty:** 2/5

## Hints

1. Context: banking_transaction
2. Regular user has limited access
3. 💡 Admin functions might not check authorization properly
4. Try accessing: /api/admin/users/delete
5. ⚠️ Some endpoints may not validate user role

## Flag

`HACKFORGE{826466d25559b5bf90fc84e43eb6b162}`
