# Laboratory Module Intimation Script

This script checks missed daily form slots and sends a group reminder.

## Behavior
- Grace window: 2 hours after slot time by default (configurable)
- Sample discard reminder: if not filled by 2:00 PM, reminder is sent from the 2:00 PM hourly run
- Runs via cron (recommended hourly)
- Weekly forms are excluded
- Prevents duplicate reminders per day+machine+slot using `form_intimation_log`

## API
- URL default: `http://192.168.0.71:3004/api/messages/send`
- Group default: `120363421649057937`

## Run manually
```bash
python3 "labortry module intimation script/intimation_reminder.py"
```

## Recommended cron (hourly)
```cron
0 * * * * docker exec labmod-ui python "/app/labortry module intimation script/intimation_reminder.py" >> /tmp/lab_form_intimation.log 2>&1
```

## Optional env overrides
- `INTIMATION_ACCOUNT_ID` (**required by your message API**)
- `LABMOD_DB_HOST` (default `127.0.0.1`)
- `LABMOD_DB_PORT` (default `3310`)
- `LABMOD_DB_USER` (default `labmod`)
- `LABMOD_DB_PASSWORD` (default `labmod_pass_123`)
- `LABMOD_DB_NAME` (default `laboratry_module_db`)
- `INTIMATION_API_URL`
- `INTIMATION_GROUP_ID`
- `INTIMATION_GRACE_HOURS` (default `2`)
- `INTIMATION_API_TIMEOUT` (default `10`)
