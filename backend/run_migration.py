"""
Run database migrations.
"""
import psycopg2
import os

# Connection parameters
connection_params = {
    'host': os.getenv('POSTGRES_HOST', 'ktxn258.duckdns.org'),
    'port': int(os.getenv('POSTGRES_PORT', 6543)),
    'database': 'casaos',  # Store metrics in casaos database
    'user': os.getenv('POSTGRES_USER', 'casaos'),
    'password': os.getenv('POSTGRES_PASSWORD', 'casaos'),
}

def run_migration(migration_file):
    """Run a SQL migration file."""
    print(f"Running migration: {migration_file}")

    with open(migration_file, 'r') as f:
        sql = f.read()

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        cursor.execute(sql)
        connection.commit()

        cursor.close()
        connection.close()

        print(f"[OK] Migration completed successfully")

    except Exception as e:
        print(f"[FAIL] Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration("migrations/001_create_metrics_table.sql")
    print("\nAll migrations completed!")
