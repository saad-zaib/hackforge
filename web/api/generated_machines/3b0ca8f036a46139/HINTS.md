# Exploitation Hints

**Machine ID:** `3b0ca8f036a46139`
**Variant:** IDOR (Insecure Direct Object Reference)
**Difficulty:** 2/5

## Hints

1. Access control: client_side_only
2. Resource ID type: base64_encoded
3. Authentication: basic_auth
4. ⚠️ Access checks are client-side only
5. 💡 IDs are base64 encoded - try decoding and modifying

## Flag

`HACKFORGE{17fa12cf89e25fa2fb3be347869416d1}`
