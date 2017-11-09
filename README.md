# zendesk-triggers-backup

A Python script for backing up Zendesk triggers. Works with 2-Factor Authentication enabled if you use an API token.

To use:

1. Download make_trigger_backup.py and save to a folder.
2. Run `python3 make_trigger_backup.py`.
3. Input Zendesk credentials:
    - zendesk subdomain
    - {zendesk_email}/token or {zendesk_email}
    - {api_key} or {zendesk_password}
4. CSV log stored in `_log.csv` with columns: 'File', 'Title', 'Date Created', and 'Date Updated'.
5. JSON backup of individual triggers stored in `/date/locale/{filename}.json`.
