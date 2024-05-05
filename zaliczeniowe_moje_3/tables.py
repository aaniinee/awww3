from sqlalchemy import create_engine, inspect

# Set up database
engine = create_engine('sqlite:///db.sqlite3')

# Get table information
inspector = inspect(engine)
tables = inspector.get_table_names()

print(tables)