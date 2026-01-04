# Exploitation Hints

**Machine ID:** `c7bf45bf402c8799`
**Variant:** IDOR (Insecure Direct Object Reference)
**Difficulty:** 2/5

## Hints

1. Access control: client_side_only
2. Resource ID type: base64_encoded
3. Authentication: jwt_token
4. ⚠️ Access checks are client-side only
5. 💡 IDs are base64 encoded - try decoding and modifying

## Flag

`HACKFORGE{5577e05acb5c8da6cde03f658ca22d8b}`
