# check_creator_table.py

from sqlalchemy import create_engine
from sqlalchemy import inspect

engine = create_engine(
    "postgresql+psycopg2://postgres:MyNewPassword123!@localhost:5432/makermint"
)

inspector = inspect(engine)

columns = inspector.get_columns("creators")

for col in columns:
    print(col["name"], col["type"])