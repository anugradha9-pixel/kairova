from sqlalchemy import create_engine, text
from app.config.settings import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    rows = conn.execute(
        text(
            """
            SELECT
                id,
                email,
                hashed_password
            FROM users
            """
        )
    )

    for row in rows:
        print(row.id)
        print(row.email)
        print(row.hashed_password)
        print("-" * 50)