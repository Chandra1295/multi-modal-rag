import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Load environment
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dbname": os.getenv("DB_NAME")
}

logger = logging.getLogger(__name__)

def get_db_connection():
    """Establishes database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.debug("Database connection established")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def create_chat_table():
    """Ensures chat table exists"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    context TEXT,
                    source_file TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_user_id ON chat_history(user_id);
            """)
            conn.commit()
            logger.info("Chat table verified/created")
    except Exception as e:
        logger.error(f"Table creation failed: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def save_chat(user_id, question, answer, context=None, source_file=None):
    """Saves chat to database"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_history 
                (user_id, question, answer, context, source_file)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, question, answer, context, source_file))
            conn.commit()
            logger.debug(f"Chat saved for user {user_id}")
    except Exception as e:
        logger.error(f"Save chat failed: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def get_chat_history(user_id, limit=20):
    """Retrieves chat history for user"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT question, answer, context, source_file, 
                       to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp
                FROM chat_history
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT %s
            """, (user_id, limit))
            results = cur.fetchall()
            logger.debug(f"Retrieved {len(results)} records for user {user_id}")
            return results
    except Exception as e:
        logger.error(f"Get history failed: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()