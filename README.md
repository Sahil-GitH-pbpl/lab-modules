# LabMod (Flask)

## Run

1. Install dependencies:

```bash
py -m pip install -r requirements.txt
```

2. Start app:

```bash
py labmod.py
```

3. Open browser:

```text
http://127.0.0.1:5000
```

## Database

Default MySQL settings are aligned to old PHP project:

- host: `localhost`
- user: `root`
- password: *(empty)*
- database: `creoianw_bhasin`

You can override via environment variables:

- `LABMOD_DB_HOST`
- `LABMOD_DB_PORT`
- `LABMOD_DB_USER`
- `LABMOD_DB_PASSWORD`
- `LABMOD_DB_NAME`
- `LABMOD_SECRET`
