# test_db.py

from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:MyNewPassword123!@localhost:5432/makermint"
)

with engine.connect() as conn:
    print(conn.execute(text("select current_user")).scalar())