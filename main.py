import psycopg2
from psycopg2 import Error

def list_all_databases():
    """List all databases in PostgreSQL server"""

    # Connection parameters (connect to default postgres database)
    connection_params = {
        'host': 'ktxn258.duckdns.org',
        'port': 6543,
        'database': 'postgres',  # Connect to default postgres database
        'user': 'casaos',
        'password': 'casaos'
    }

    try:
        print("Connecting to PostgreSQL server...")
        print(f"Host: {connection_params['host']}")
        print(f"Port: {connection_params['port']}")
        print("=" * 60)

        # Create connection
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"\n[SUCCESS] Connected successfully!")
        print(f"PostgreSQL version: {db_version[0][:80]}...")
        print("=" * 60)

        # List all databases
        cursor.execute("""
            SELECT
                datname as database_name,
                pg_size_pretty(pg_database_size(datname)) as size,
                datcollate as collation,
                datconnlimit as connection_limit
            FROM pg_database
            WHERE datistemplate = false
            ORDER BY datname;
        """)
        databases = cursor.fetchall()

        print(f"\n[DATABASES] Found {len(databases)} databases:")
        print("-" * 60)
        for db in databases:
            print(f"  Name: {db[0]}")
            print(f"    Size: {db[1]}")
            print(f"    Collation: {db[2]}")
            print(f"    Connection Limit: {db[3]}")
            print("-" * 60)

        cursor.close()
        connection.close()
        print("\n[SUCCESS] Connection closed")

    except Error as e:
        print(f"[ERROR] PostgreSQL error: {e}")
    except Exception as e:
        print(f"[ERROR] Unknown error: {e}")


def check_database_details(db_name):
    """Check tables and details in a specific database"""

    connection_params = {
        'host': 'ktxn258.duckdns.org',
        'port': 6543,
        'database': db_name,
        'user': 'casaos',
        'password': 'casaos'
    }

    try:
        print(f"\n{'=' * 60}")
        print(f"Checking database: {db_name}")
        print("=" * 60)

        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Get list of tables
        cursor.execute("""
            SELECT
                table_name,
                table_type
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()

        if tables:
            print(f"\n[TABLES] Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]} ({table[1]})")

                # Get row count for each table
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
                    count = cursor.fetchone()[0]
                    print(f"    Rows: {count}")
                except Exception as e:
                    print(f"    Rows: Could not count - {e}")
        else:
            print(f"\n[INFO] No tables found in '{db_name}'")

        cursor.close()
        connection.close()

    except Error as e:
        print(f"[ERROR] Cannot connect to database '{db_name}': {e}")
    except Exception as e:
        print(f"[ERROR] Unknown error: {e}")

if __name__ == "__main__":
    # List all databases in the server
    list_all_databases()

    # Check details of specific databases
    print("\n" + "=" * 60)
    print("Checking each database for tables...")
    print("=" * 60)

    # Get list of databases to check
    connection_params = {
        'host': 'ktxn258.duckdns.org',
        'port': 6543,
        'database': 'postgres',
        'user': 'casaos',
        'password': 'casaos'
    }

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;")
        databases = cursor.fetchall()
        cursor.close()
        connection.close()

        # Check each database
        for db in databases:
            check_database_details(db[0])

    except Error as e:
        print(f"[ERROR] {e}")
