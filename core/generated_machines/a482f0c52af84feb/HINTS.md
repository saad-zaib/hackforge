# Exploitation Hints

**Machine ID:** `a482f0c52af84feb`
**Variant:** IDOR (Insecure Direct Object Reference)
**Difficulty:** 2/5

## Hints

1. Access control: client_side_only
2. Resource ID type: uuid_v4
3. Authentication: jwt_token
4. ⚠️ Access checks are client-side only
5. 💡 UUIDs are used but might be predictable or leaked

## Flag

`HACKFORGE{b12e4c0b801b24eeb45bdb869f66204d}`
