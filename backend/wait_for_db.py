import os
import time
import psycopg2


def wait_for_db(url, retries=30, delay=2):
    for i in range(retries):
        try:
            conn = psycopg2.connect(url)
            conn.close()
            print("Database available")
            return
        except Exception as e:
            print(f"Waiting for database ({i+1}/{retries})... {e}")
            time.sleep(delay)
    raise RuntimeError("Timed out waiting for the database")


if __name__ == '__main__':
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL not set')
    wait_for_db(database_url)
