# Exploitation Hints

**Machine ID:** `4c0e089556709f33`
**Variant:** IDOR (Insecure Direct Object Reference)
**Difficulty:** 2/5

## Hints

1. Access control: client_side_only
2. Resource ID type: base64_encoded
3. Authentication: none
4. ⚠️ Access checks are client-side only
5. 💡 IDs are base64 encoded - try decoding and modifying

## Flag

`HACKFORGE{be257dd0180291992cc03f5cd2a1a16a}`
