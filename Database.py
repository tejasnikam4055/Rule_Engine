import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='tejas',
            database='rule_engine'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def check_table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.tables 
        WHERE table_schema = 'rule_engine' 
        AND table_name = '{table_name}'
    """)
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    return exists

def create_table(connection):
    if not check_table_exists(connection, 'rules'):
        try:
            cursor = connection.cursor()
            create_table_query = """
            CREATE TABLE rules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rule_string TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            cursor.close()
            print("Table 'rules' created successfully")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
    else:
        print("Table 'rules' already exists, skipping creation.")

def insert_rule(connection, rule_string):
    cursor = connection.cursor()
    query = "INSERT INTO rules (rule_string) VALUES (%s)"
    cursor.execute(query, (rule_string,))
    connection.commit()
    cursor.close()
    print("Rule inserted successfully into 'rules'")

def fetch_rules(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM rules"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Database connection is closed")

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        create_table(conn)  # Create table if it doesn't exist
        # You can insert a rule or fetch rules here if needed
        close_connection(conn)
