# PRD — Calendar Availability Consolidator

## 1. Project Title

**Calendar Availability Consolidator — Phase 1 MVP**

---

### 2. Objective

Create a local command-line utility that calculates consolidated free time across multiple Google Calendars within a user-defined time window.

The system must:

* evaluate availability only from events marked as `busy`,
* merge occupied intervals across selected calendars,
* calculate total free time,
* and return all available time blocks within the requested interval.

The tool is intended for personal productivity planning and scheduling analysis.

---

## 3. Functional Logic

### 3.1 Execution Input

The script is executed manually from the command line.

The user provides:

* start datetime,
* end datetime

Example:

```bash
python availability.py \
  --start "2026-05-07 09:00" \
  --end "2026-05-07 18:00" \
```


**Validation:** If the duration between `Start_DateTime` and `End_DateTime` exceeds 24 hours, the system must trigger a terminal error.

---

### 3.2 Configuration Source

The system uses a local configuration file containing:

* Google Calendar IDs

Retrieve all events from the calendar IDs defined in the local configuration file.

Example conceptual structure:

```yaml
calendars:
  - primary@group.calendar.google.com
  - engineering@group.calendar.google.com
  - personal@group.calendar.google.com
```

---

### 3.3 Authentication

The script authenticates locally against the user’s Google account using OAuth credentials.

Authentication tokens are stored locally in environment variables.

No cloud-side persistence is required.

---

### 3.4 Availability Query Logic

The system queries Google Calendar availability using only:

* selected calendars,
* provided time window.

Only events marked as `busy` are considered unavailable time.

The following event types are ignored:

* all-day events,
* free events,
* tentative events,
* working location entries,
* canceled events.

Recurring events are treated as normal occupied intervals if returned as busy by Google Calendar.

**Threshold:** Any gap $\ge$ 5 minutes is classified as "Available." Any gap < 5 minutes is discarded.

---

### 3.5 Busy Interval Consolidation

All busy intervals from all selected calendars are merged into a single consolidated unavailable timeline.

Overlapping or adjacent intervals must collapse into one continuous interval.

Example:

```text
Calendar A: 09:00-10:00
Calendar B: 09:30-11:00

Merged:
09:00-11:00
```

---

### 3.6 Free Time Calculation

The system computes free blocks as the inverse of merged busy intervals within the requested window.

Example:

```text
Window:
09:00-18:00

Busy:
10:00-11:00
13:00-14:30

Free:
09:00-10:00
11:00-13:00
14:30-18:00
```

---

### 3.7 Output Format

The script outputs:

1. Total free time
2. Individual free blocks
3. Duration per block

Example:

```text
Total free time: 5h 30m

Available blocks:
09:00-10:00 (1h)
11:00-13:00 (2h)
14:30-17:00 (2h 30m)
```

---

## 4. Data Flow

```text
CLI Input
    ↓
Load Local Configuration
    ↓
Resolve Calendar IDs
    ↓
Authenticate with Google
    ↓
Query free/busy API
    ↓
Collect busy intervals
    ↓
Merge intervals
    ↓
Calculate free blocks
    ↓
Render console output
```

---

## 5. Edge Cases & Error Handling

### 5.1 Invalid Calendar IDs

If a calendar ID:

* does not exist,
* is inaccessible,
* or returns an authorization error,

the system:

* ignores that calendar,
* logs a warning,
* continues execution.

---

### 5.2 Empty Calendar list

If the list of calendars in the configuration file to zero valid calendars:

* execution fails,
* user receives an explicit error message.

---

### 5.3 No Busy Events

If no busy intervals exist:

* the entire requested window is returned as available.

---

### 5.4 Fully Occupied Window

If busy intervals cover the entire window:

* total free time is `0`,
* no free blocks are returned.

---

### 5.5 Overlapping Busy Intervals

Overlapping or touching intervals must merge before availability calculations.

---

### 5.6 Timezone Handling

The system always uses the user’s current local timezone.

Convert all event timestamps and the input window to the local system timezone.

No manual timezone override is required for MVP.

---

### 5.7 Invalid Time Window

If:

* start >= end,
* malformed datetime input,
* or unsupported format,

execution fails with validation feedback.

---

### 5.8 Configuration Errors

If the configuration file is missing the system must abort and specify it was not found.

If it contains malformed Calendar IDs, those should be ignored.

---

## 6. Success Criteria

The MVP is considered successful when:

1. User can define arbitrary time windows.
2. User can define calendars via the configuration file.
3. Busy intervals from all calendars are merged correctly.
4. Total free time is accurate.
5. Free blocks are displayed chronologically.
6. Invalid calendars do not abort execution.
7. The sum of `Total Available Time` + `Consolidated Busy Time` + `Discarded Gaps (<5m)` must equal the total duration of the Input Window.
8. Availability is reported with minute-level accuracy.

---

## 7. Future Roadmap

### Phase 2

* Export results to JSON/CSV.
* Interactive TUI selection of calendar groups.
* Minimum block duration filtering.
* Human-readable summaries (“largest free block”).

### Phase 3

* Automatic daily availability reports.
* Slack/Telegram integrations.
* Scheduling recommendation engine.
* Conflict density analytics.

### Phase 4

* Multi-user shared availability intersection.
* GUI/Web interface.
* Real-time availability daemon.
* Google Meet scheduling integration.
