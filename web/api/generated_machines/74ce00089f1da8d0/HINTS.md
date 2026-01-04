# Exploitation Hints

**Machine ID:** `74ce00089f1da8d0`
**Variant:** IDOR (Insecure Direct Object Reference)
**Difficulty:** 2/5

## Hints

1. Access control: weak_session_check
2. Resource ID type: sequential_numeric
3. Authentication: api_key
4. ⚠️ Session validation is weak
5. 💡 Try incrementing/decrementing the ID parameter

## Flag

`HACKFORGE{de8cedc82fa199a0aad9a86f98c6a60f}`
