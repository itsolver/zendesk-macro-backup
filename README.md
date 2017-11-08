# zendesk-triggers-backup

A Python script for backing up Zendesk triggers.

To use:

1. Download make_trigger_backup.py and save to a folder.
2. Replace these placeholder values in make_trigger_backup.py with the correct values:
    - `{your_zendesk_email}`
    - `{your_zendesk_password}`
    - `{your_zendesk_url}`
3. Run `python3 make_trigger_backup.py`.
4. CSV log stored in `_log.csv` with columns: 'File', 'Title', 'Date Created', and 'Date Updated'.
5. JSON backup of individual macros stored in `/date/locale/{filename}.json`.
