# Exploitation Hints

**Machine ID:** `e87a2daeba4ab60b`
**Variant:** IDOR (Insecure Direct Object Reference)
**Difficulty:** 2/5

## Hints

1. Access control: weak_session_check
2. Resource ID type: base64_encoded
3. Authentication: api_key
4. ⚠️ Session validation is weak
5. 💡 IDs are base64 encoded - try decoding and modifying

## Flag

`HACKFORGE{caea8c4bdabb3861e3efdff750f99c15}`
