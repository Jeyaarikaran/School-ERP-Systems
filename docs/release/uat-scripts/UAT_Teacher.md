# UAT Script: Teacher Role

**Prerequisites**:
- Logged in as Teacher (e.g., `teacher1@demo.school`)
- Assigned to Class 10, Section A.

| Step | Action | Expected Result | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Navigate to Attendance | Shows Class 10A roster. | [ ] | |
| 2 | Mark attendance (offline drill) | Disable internet. Mark 3 students absent. Click save. | [ ] | Should show "Queued" UI |
| 3 | Reconnect | Enable internet. | [ ] | Syncs in background within 10s |
| 4 | Assign Homework | Upload a photo of the board. | [ ] | Upload succeeds, compression works |
| 5 | View substitution | Check dashboard for substituted classes. | [ ] | Shows correct period and room |

> **Note:** Tamil labels must be verified by a native speaker. Test environment missing, so execution is pending.
