from sqlalchemy import inspect

from app.db.session import engine

inspector = inspect(engine)

print("\nCREATORS TABLE COLUMNS\n")

for column in inspector.get_columns("creators"):
    print(column["name"])