import sqlite3

DATABASE_NAME = "token_optimizer.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row 
    return connection

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS optimization_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            optimized_text TEXT NOT NULL,
            original_token_count INTEGER NOT NULL,
            optimized_token_count INTEGER NOT NULL,
            tokens_saved INTEGER NOT NULL,
            savings_percentage REAL NOT NULL,
            model_name TEXT NOT NULL,
            selected_strategy TEXT NOT NULL,
            optimization_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_optimization(result):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO optimization_history (
            original_text,
            optimized_text,
            original_token_count,
            optimized_token_count,
            tokens_saved,
            savings_percentage,
            model_name,
            selected_strategy,
            optimization_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result["original_text"],
        result["optimized_text"],
        result["original_token_count"],
        result["optimized_token_count"],
        result["tokens_saved"],
        result["savings_Percentage"],
        result["model_name"],
        result["selected_strategy"],
        result["optimization_status"]
    ))

    connection.commit()

    record_id = cursor.lastrowid

    connection.close()

    return record_id

def get_optimization_history(limit=50):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM optimization_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    history = [dict(row) for row in rows]
    
    connection.close()

    return history
 