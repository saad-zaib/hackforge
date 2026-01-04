# Exploitation Hints

**Machine ID:** `13c0c424cf469df0`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: whois_lookup
2. Shell: dash
3. Command structure: command_substitution
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{642d4488744c3167ea9cf7b1a4ab1430}`
