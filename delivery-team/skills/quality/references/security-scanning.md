# Inline Security Scanning

## Purpose

Detect common security vulnerabilities in code during the Development stage (Stage 6) without requiring external scanning tools. These checks run after each story's code is written, before DoD validation.

---

## Check Triggers

1. After each story's code is written (post-Write/Edit in Development stage)
2. Before DoD validation begins
3. On demand via the `security-scan` command

The QA Engineer reviews all files created or modified for the current story against the patterns below.

---

## Severity Levels

| Severity | Meaning | Pipeline Behavior |
|----------|---------|-------------------|
| **Critical** | Exploitable vulnerability; must fix before DoD | Blocks DONE status — story cannot pass DoD |
| **Warning** | Potential vulnerability; likely needs fixing | Flags in DoD report; reviewer decides |
| **Info** | Best practice violation; low risk | Noted in DoD report; does not block |

---

## Security Check Categories

### 1. Hardcoded Secrets (Critical)

Detect API keys, passwords, tokens, and credentials embedded in source code.

**Patterns to scan for:**

| Pattern | Regex | Language |
|---------|-------|----------|
| AWS access key | `AKIA[0-9A-Z]{16}` | Any |
| Generic API key assignment | `(?i)(api[_-]?key\|apikey\|secret[_-]?key)\s*[:=]\s*["'][^"']{8,}["']` | Any |
| Password assignment | `(?i)(password\|passwd\|pwd)\s*[:=]\s*["'][^"']+["']` | Any |
| Private key header | `-----BEGIN (RSA\|EC\|DSA\|OPENSSH) PRIVATE KEY-----` | Any |
| JWT token | `eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}` | Any |
| Connection string with password | `(?i)(mongodb\|postgres\|mysql\|redis):\/\/[^:]+:[^@]+@` | Any |
| GitHub token | `gh[pousr]_[A-Za-z0-9_]{36,}` | Any |

**Fix suggestion:** Move secrets to environment variables or a secrets manager. Reference them via `os.environ`, `process.env`, or equivalent.

### 2. SQL Injection (Critical)

Detect string concatenation or interpolation in SQL queries.

**Patterns:**

| Language | Vulnerable Pattern | Safe Alternative |
|----------|-------------------|-----------------|
| Python | `f"SELECT * FROM users WHERE id = {user_id}"` | `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))` |
| Python | `"SELECT * FROM users WHERE id = " + user_id` | Use parameterized queries |
| JavaScript | `` `SELECT * FROM users WHERE id = ${userId}` `` | Use parameterized queries or ORM |
| Go | `fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)` with `db.Query()` | `db.Query("SELECT * FROM users WHERE id = $1", userID)` |
| Java | `"SELECT * FROM users WHERE id = " + userId` | Use `PreparedStatement` |

**Regex:** `(?i)(execute\|query\|raw)\s*\(.*(%s\|%d\|\$\{|\+\s*\w+|format\().*(?:SELECT\|INSERT\|UPDATE\|DELETE\|DROP)`

### 3. Cross-Site Scripting — XSS (Warning)

Detect unescaped user input rendered in HTML.

**Patterns:**

| Language/Framework | Vulnerable Pattern | Safe Alternative |
|-------------------|-------------------|-----------------|
| JavaScript | `element.innerHTML = userInput` | `element.textContent = userInput` |
| JavaScript | `document.write(userInput)` | Use DOM APIs with text nodes |
| React | `dangerouslySetInnerHTML={{__html: userInput}}` | Use JSX text interpolation |
| Python/Jinja | `{{ user_input \| safe }}` | `{{ user_input }}` (auto-escaped) |
| Go/html | `template.HTML(userInput)` | Use default template escaping |

### 4. Insecure Deserialization (Critical)

Detect use of unsafe deserialization functions on untrusted data.

**Patterns:**

| Language | Dangerous Function | Safe Alternative |
|----------|-------------------|-----------------|
| Python | `pickle.loads()`, `pickle.load()` | Use `json.loads()` or validate before deserializing |
| Python | `eval()`, `exec()` | Never use on user input; use `ast.literal_eval()` for literals |
| JavaScript | `eval()`, `Function()` constructor | Use `JSON.parse()` for data; avoid dynamic code execution |
| Java | `ObjectInputStream.readObject()` | Use allow-lists for deserialization; prefer JSON |
| PHP | `unserialize()` | Use `json_decode()` |

### 5. Path Traversal (Warning)

Detect user input used in file system operations without validation.

**Patterns:**

| Language | Vulnerable Pattern | Safe Alternative |
|----------|-------------------|-----------------|
| Python | `open(user_input)`, `os.path.join(base, user_input)` without validation | Validate with `os.path.realpath()` and check prefix |
| JavaScript | `fs.readFile(userInput)` | Resolve and validate against allowed directory |
| Go | `os.Open(userInput)` | Use `filepath.Clean()` and validate prefix |

**Key check:** Does the code verify that the resolved path stays within the intended directory? Look for `..` traversal prevention.

### 6. Exposed Credentials in Config (Critical)

Detect secrets in configuration files that may be committed to version control.

**Files to check:** `*.env`, `*.yml`, `*.yaml`, `*.json`, `*.toml`, `*.ini`, `*.cfg`, `*.conf`

**Patterns:**
- Files named `.env` containing `KEY=value` with sensitive-looking values
- YAML/JSON with keys like `password`, `secret`, `token`, `api_key` containing non-placeholder values
- Config files not listed in `.gitignore`

**Fix suggestion:** Add sensitive config files to `.gitignore`. Use `.env.example` with placeholder values.

### 7. Deprecated or Weak Cryptography (Info)

| Pattern | Issue | Recommendation |
|---------|-------|---------------|
| `md5(`, `hashlib.md5` | MD5 is cryptographically broken | Use SHA-256 or bcrypt for passwords |
| `sha1(`, `hashlib.sha1` | SHA-1 is deprecated for security use | Use SHA-256+ |
| `DES`, `3DES`, `RC4` | Weak/deprecated ciphers | Use AES-256-GCM |
| `Math.random()` for security | Not cryptographically secure | Use `crypto.getRandomValues()` or `secrets` module |

---

## Output Format

Security scan results are reported as a findings table:

```markdown
## Security Scan Results — [Story ID]

**Files scanned:** 12
**Findings:** 3 (1 critical, 1 warning, 1 info)

| # | File | Line | Severity | Category | Description | Fix Suggestion |
|---|------|------|----------|----------|-------------|---------------|
| 1 | src/auth.py | 42 | Critical | Hardcoded Secret | API key literal in source code | Move to environment variable |
| 2 | src/user.py | 87 | Warning | XSS | `innerHTML` assignment with user-controlled value | Use `textContent` instead |
| 3 | src/crypto.py | 15 | Info | Weak Crypto | MD5 used for hashing | Replace with SHA-256 |

### Required Actions (before DoD)
- [ ] Fix finding #1 (Critical — blocks DoD)

### Recommended Actions
- [ ] Review finding #2 (Warning — likely needs fixing)

### Notes
- Finding #3 is informational — address in a future cleanup story if desired
```

---

## Integration with Empirical Validation

Some security findings cannot be fully verified through static inspection:

- **Runtime injection testing**: SQL injection with actual payloads requires runtime verification
- **Authentication bypass**: Verifying that auth checks work requires a running application
- **CORS misconfiguration**: Requires runtime HTTP inspection

These findings should be marked as requiring empirical validation (CODE_COMPLETE) and carried forward to UAT as mandatory test cases.

---

## Language-Specific Quick Reference

### Python
- `pickle.loads()`, `pickle.load()` — insecure deserialization
- `eval()`, `exec()` — code injection
- `os.system()`, `subprocess.call(shell=True)` — command injection
- `yaml.load()` without `Loader=SafeLoader` — YAML deserialization attack
- `hashlib.md5()`, `hashlib.sha1()` — weak hashing

### JavaScript / TypeScript
- `eval()`, `Function()`, `setTimeout(string)` — code injection
- `innerHTML`, `outerHTML`, `document.write()` — XSS
- `child_process.exec(userInput)` — command injection
- `JSON.parse()` of untrusted WebSocket data without schema validation

### Go
- `sql.Query()` with `fmt.Sprintf` — SQL injection
- `os.Open(userInput)` without path validation — path traversal
- `template.HTML()` — XSS (bypasses template escaping)
- `net/http` without TLS — unencrypted transport

### Java
- `Runtime.exec()` with string concatenation — command injection
- `ObjectInputStream.readObject()` — insecure deserialization
- `Statement` instead of `PreparedStatement` — SQL injection
- `X509TrustManager` that accepts all certificates — TLS bypass
