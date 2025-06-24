import sqlite3
import os
from typing import List, Tuple, Any, Optional

class SQLiteTutorial:
    def __init__(self, db_name: str = "tutorial.db"):
        """
        Initialize SQLite database connection
        Args:
            db_name: Name of the database file
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✅ Successfully connected to {self.db_name}")
        except sqlite3.Error as e:
            print(f"❌ Error connecting to database: {e}")
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
    
    def create_table(self, table_name: str, columns: str):
        """
        Create a new table
        Args:
            table_name: Name of the table
            columns: SQL column definitions (e.g., "id INTEGER PRIMARY KEY, name TEXT")
        """
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            self.cursor.execute(query)
            self.conn.commit()
            print(f"✅ Table '{table_name}' created successfully")
        except sqlite3.Error as e:
            print(f"❌ Error creating table: {e}")
    
    def insert_data(self, table_name: str, data: dict):
        """
        Insert data into a table
        Args:
            table_name: Name of the table
            data: Dictionary with column names as keys and values as values
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            self.cursor.execute(query, list(data.values()))
            self.conn.commit()
            print(f"✅ Data inserted into '{table_name}' successfully")
        except sqlite3.Error as e:
            print(f"❌ Error inserting data: {e}")
    
    def insert_many(self, table_name: str, columns: List[str], data: List[Tuple]):
        """
        Insert multiple rows of data
        Args:
            table_name: Name of the table
            columns: List of column names
            data: List of tuples containing row data
        """
        try:
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['?' for _ in columns])
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            self.cursor.executemany(query, data)
            self.conn.commit()
            print(f"✅ {len(data)} rows inserted into '{table_name}' successfully")
        except sqlite3.Error as e:
            print(f"❌ Error inserting multiple rows: {e}")
    
    def select_all(self, table_name: str) -> List[Tuple]:
        """
        Select all data from a table
        Args:
            table_name: Name of the table
        Returns:
            List of tuples containing all rows
        """
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print(f"✅ Retrieved {len(results)} rows from '{table_name}'")
            return results
        except sqlite3.Error as e:
            print(f"❌ Error selecting data: {e}")
            return []
    
    def select_where(self, table_name: str, condition: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Select data with a WHERE condition
        Args:
            table_name: Name of the table
            condition: WHERE condition (e.g., "age > ?")
            params: Parameters for the condition
        Returns:
            List of tuples containing matching rows
        """
        try:
            query = f"SELECT * FROM {table_name} WHERE {condition}"
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
            print(f"✅ Retrieved {len(results)} rows from '{table_name}' with condition: {condition}")
            return results
        except sqlite3.Error as e:
            print(f"❌ Error selecting data with condition: {e}")
            return []
    
    def update_data(self, table_name: str, set_values: dict, condition: str, params: Optional[Tuple] = None):
        """
        Update data in a table
        Args:
            table_name: Name of the table
            set_values: Dictionary with column names and new values
            condition: WHERE condition
            params: Parameters for the condition
        """
        try:
            set_clause = ', '.join([f"{col} = ?" for col in set_values.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            
            all_params = list(set_values.values())
            if params:
                all_params.extend(params)
            
            self.cursor.execute(query, all_params)
            self.conn.commit()
            print(f"✅ Data updated in '{table_name}' successfully")
        except sqlite3.Error as e:
            print(f"❌ Error updating data: {e}")
    
    def delete_data(self, table_name: str, condition: str, params: Optional[Tuple] = None):
        """
        Delete data from a table
        Args:
            table_name: Name of the table
            condition: WHERE condition
            params: Parameters for the condition
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            print(f"✅ Data deleted from '{table_name}' successfully")
        except sqlite3.Error as e:
            print(f"❌ Error deleting data: {e}")
    
    def drop_table(self, table_name: str):
        """
        Drop (delete) a table
        Args:
            table_name: Name of the table to drop
        """
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(query)
            self.conn.commit()
            print(f"✅ Table '{table_name}' dropped successfully")
        except sqlite3.Error as e:
            print(f"❌ Error dropping table: {e}")
    
    def get_table_info(self, table_name: str) -> List[Tuple]:
        """
        Get information about table structure
        Args:
            table_name: Name of the table
        Returns:
            List of tuples containing column information
        """
        try:
            query = f"PRAGMA table_info({table_name})"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print(f"✅ Retrieved table info for '{table_name}'")
            return results
        except sqlite3.Error as e:
            print(f"❌ Error getting table info: {e}")
            return []
    
    def execute_custom_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Execute a custom SQL query
        Args:
            query: SQL query string
            params: Parameters for the query
        Returns:
            List of tuples containing results
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = self.cursor.fetchall()
                print(f"✅ Custom query executed successfully, returned {len(results)} rows")
                return results
            else:
                self.conn.commit()
                print("✅ Custom query executed successfully")
                return []
        except sqlite3.Error as e:
            print(f"❌ Error executing custom query: {e}")
            return []

def print_results(results: List[Tuple], title: str = "Results"):
    """Helper function to print query results in a formatted way"""
    print(f"\n📋 {title}:")
    if not results:
        print("No results found")
        return
    
    for i, row in enumerate(results, 1):
        print(f"Row {i}: {row}")

def main():
    """Main tutorial function demonstrating all basic SQLite operations"""
    print("🚀 SQLite3 Tutorial - Basic Functions\n")
    
    # Initialize database
    db = SQLiteTutorial("tutorial.db")
    db.connect()
    
    # 1. Create a table
    print("\n" + "="*50)
    print("1. CREATING A TABLE")
    print("="*50)
    db.create_table("users", """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """)
    
    # 2. Insert single row
    print("\n" + "="*50)
    print("2. INSERTING SINGLE ROW")
    print("="*50)
    db.insert_data("users", {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com"
    })
    
    # 3. Insert multiple rows
    print("\n" + "="*50)
    print("3. INSERTING MULTIPLE ROWS")
    print("="*50)
    users_data = [
        ("Jane Smith", 30, "jane@example.com"),
        ("Bob Johnson", 35, "bob@example.com"),
        ("Alice Brown", 28, "alice@example.com"),
        ("Charlie Wilson", 42, "charlie@example.com")
    ]
    db.insert_many("users", ["name", "age", "email"], users_data)
    
    # 4. Select all data
    print("\n" + "="*50)
    print("4. SELECTING ALL DATA")
    print("="*50)
    all_users = db.select_all("users")
    print_results(all_users, "All Users")
    
    # 5. Select with condition
    print("\n" + "="*50)
    print("5. SELECTING WITH CONDITION")
    print("="*50)
    young_users = db.select_where("users", "age < ?", (30,))
    print_results(young_users, "Users under 30")
    
    # 6. Update data
    print("\n" + "="*50)
    print("6. UPDATING DATA")
    print("="*50)
    db.update_data("users", {"age": 26}, "name = ?", ("John Doe",))
    updated_users = db.select_all("users")
    print_results(updated_users, "Users after update")
    
    # 7. Get table information
    print("\n" + "="*50)
    print("7. TABLE INFORMATION")
    print("="*50)
    table_info = db.get_table_info("users")
    print_results(table_info, "Table Structure")
    
    # 8. Custom query example
    print("\n" + "="*50)
    print("8. CUSTOM QUERY")
    print("="*50)
    custom_result = db.execute_custom_query(
        "SELECT name, age FROM users WHERE age BETWEEN ? AND ? ORDER BY age",
        (25, 35)
    )
    print_results(custom_result, "Users aged 25-35")
    
    # 9. Delete data
    print("\n" + "="*50)
    print("9. DELETING DATA")
    print("="*50)
    db.delete_data("users", "name = ?", ("Charlie Wilson",))
    remaining_users = db.select_all("users")
    print_results(remaining_users, "Users after deletion")
    
    # 10. Drop table (cleanup)
    print("\n" + "="*50)
    print("10. CLEANUP - DROPPING TABLE")
    print("="*50)
    db.drop_table("users")
    
    # Close connection
    db.disconnect()
    
    # Clean up database file
    if os.path.exists("tutorial.db"):
        os.remove("tutorial.db")
        print("✅ Database file cleaned up")

if __name__ == "__main__":
    main() 