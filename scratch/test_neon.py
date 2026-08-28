import os
from sqlalchemy import create_engine, text

# Get the URL from user's request #1
url = "postgresql://neondb_owner:npg_7qhEI2nvQTzC@ep-proud-firefly-au93oo0y-pooler.c-10.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"

engine = create_engine(url)
try:
    with engine.connect() as conn:
        res = conn.execute(text('SELECT column_name FROM information_schema.columns WHERE table_name = \'Mercancia\' OR table_name = \'mercancia\';'))
        print("Columns in Mercancia table:")
        for row in res:
            print(row[0])
            
        print("\nChecking if we can query Mercancia:")
        res2 = conn.execute(text('SELECT count(*) FROM "Mercancia";'))
        print(f"Count: {res2.scalar()}")
        
except Exception as e:
    print(f"Error: {e}")
