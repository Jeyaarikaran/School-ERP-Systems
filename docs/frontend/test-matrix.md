# E2E & Device Test Matrix

| Flow | Platform | Devices / Viewports | Network Condition | Result / Evidence |
|---|---|---|---|---|
| Admin: Super Admin Onboarding | Web | Chromium (Desktop) | Normal | Not Verifiable |
| Admin: School Setup | Web | Firefox (Desktop) | Normal | Not Verifiable |
| Admin: Teacher Attendance | Web | WebKit (Tablet) | Normal | Not Verifiable |
| Admin: Principal Dashboard | Web | Chromium (Desktop) | Normal | Not Verifiable |
| Admin: Fee Collection & Close | Web | Chromium (Desktop) | Throttled 3G | Not Verifiable |
| Mobile: Login (Password/OTP) | Android / iOS | Pixel 7, iPhone 13 | Normal | Not Verifiable |
| Mobile: Offline Attendance Drill | Android | Low-end (Android 10) | Airplane Mode | Not Verifiable |
| Mobile: Offline Homework Photo | iOS | iPhone X | Airplane Mode | Not Verifiable |
| Mobile: Push Notification Deep Links | Android / iOS | Various | Background/Killed | Not Verifiable |
| Mobile: Fee Payment (FakeGateway) | Android | Mid-range | High Latency | Not Verifiable |

> **Note:** Tests could not be executed because the `admin/` and `mobile/` codebases are missing from this repository environment.
