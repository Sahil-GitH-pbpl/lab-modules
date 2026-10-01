# LabMod (Flask)

## Local Run on Windows

1. Create local config:

```powershell
Copy-Item .env.example .env
```

2. Edit `.env` and set both MySQL database credentials.

3. Start the app:

```powershell
.\run-local.ps1
```

4. Open:

```text
http://127.0.0.1:5006
```

## Manual Run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe labmod.py
```

## Database

This app needs two MySQL databases:

- Main lab module database: configured with `LABMOD_DB_*`
- Login/auth database: configured with `LABMOD_AUTH_DB_*`

Default local settings are for XAMPP/phpMyAdmin:

- host: `127.0.0.1`
- port: `3306`
- user: `root`
- password: empty
- main database: `laboratry_module_db`
- auth database: `hiccup_ticket`

Available environment variables:

- `LABMOD_SECRET`
- `LABMOD_DB_HOST`
- `LABMOD_DB_PORT`
- `LABMOD_DB_USER`
- `LABMOD_DB_PASSWORD`
- `LABMOD_DB_NAME`
- `LABMOD_AUTH_DB_HOST`
- `LABMOD_AUTH_DB_PORT`
- `LABMOD_AUTH_DB_USER`
- `LABMOD_AUTH_DB_PASSWORD`
- `LABMOD_AUTH_DB_NAME`

SQL backfill files in this repository can be imported into the main lab database if the target tables are missing.
