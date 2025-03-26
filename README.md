# IIBS Api - Interactive Information Board System

Wala lng pasikat lng ako

## Environment Variables

To run this project, add the following environment variables to your `.env` file:

```plaintext
DATABASE_URL=postgresql://username:password@localhost:5432/db_name
JWT_SECRET_KEY=
JWT_REFRESH_KEY=
```

- Database name should be iibs

- If the database name is not iibs, you need to configure the `alembic.ini` file. Find this line of code and change it, you can copy the `DATABASE_URL` from your `env` file and paste it.

```
sqlalchemy.url = postgresql://miria:hades2801@localhost:5432/iibs_db
```

You can generate a random hex key using the following command:

```bash
openssl rand -hex 32
```

## Installation

1. Create your virtual enviroment first:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- Linux/macOS
  ```bash
  source venv/bin/activate
  ```
- Windows
  ```bash
  venv\Scripts\Activate
  ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

- Note: Ensure you have `pip` installed on your system before running the installation command.

4. Run the project:
   ```bash
    uvicorn main:app --reload
   ```

## Documentation

Once you've installed and started the API, you can view the available routes in the documentation:

[API Documentation](http://127.0.0.1:8000/docs)
