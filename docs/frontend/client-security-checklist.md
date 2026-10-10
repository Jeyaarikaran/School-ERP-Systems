# Client Security Checklist (Web & Mobile)

## Admin Web (BFF Architecture)
- [ ] **CSP Configured**: No `unsafe-inline` scripts.
- [ ] **Security Headers**: HSTS, X-Content-Type-Options, X-Frame-Options.
- [ ] **Cookies**: httpOnly, Secure, SameSite=Strict on all tokens.
- [ ] **No Local Secrets**: Tokens not stored in localStorage/sessionStorage.
- [ ] **SRI (Subresource Integrity)**: Configured for external scripts.
- [ ] **XSS Prevention**: `dangerouslySetInnerHTML` banned in linter.

## Mobile (Flutter)
- [ ] **Secure Storage**: Tokens use `flutter_secure_storage`.
- [ ] **No Hardcoded Secrets**: Bundle scanned, `--dart-define` used correctly.
- [ ] **Obfuscation**: Release builds use obfuscation (`--obfuscate`).
- [ ] **Logging Disabled**: No `debugPrint` or raw `print` in release mode.
- [ ] **Network Security**: Cleartext traffic disabled (Android Network Security Config / iOS ATS).
- [ ] **FLAG_SECURE**: Enabled for Results, Fees, and Privacy screens on Android.
- [ ] **Deep Links Validated**: Parameters not trusted, backend queried for scope.

> **Note:** MASVS L1 mapping and verification require the compiled bundles which are missing from this environment.
