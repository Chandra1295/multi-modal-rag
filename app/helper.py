
import os
import uuid
import streamlit as st
from dotenv import load_dotenv
import logging
from pathlib import Path
import sqlite3
from types import SimpleNamespace
import time
from datetime import datetime

load_dotenv()

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.file_processed = 0
        self.total_cleaned = 0
        
    def log_processing_time(self, filename, size_mb):
        elapsed = time.time() - self.start_time
        self.file_processed += 1
        logging.info(
            f"PROCESSED: {filename} ({size_mb:.1f}MB) in {elapsed:.2f}s | "
            f"Total files: {self.file_processed}"
        )
        
    def log_cleanup(self, bytes_freed):
        self.total_cleaned += bytes_freed
        logging.info(
            f"CLEANUP: Freed {bytes_freed/1e6:.2f}MB | "
            f"Total freed: {self.total_cleaned/1e6:.2f}MB"
        )

# Initialize monitor
monitor = SystemMonitor()

# Configure logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.handlers.RotatingFileHandler(
            "logs/app.log", 
            maxBytes=1e6, 
            backupCount=3
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_cookie_manager():
    """Safe cookie manager initialization with duplicate key prevention"""
    if "cookie_manager" not in st.session_state:
        try:
            # Initialize cookie manager
            cookie_password = os.getenv("COOKIE_PASSWORD", "default_secret_key")
            cookies = EncryptedCookieManager(
                prefix="my_cookie_prefix",
                password=cookie_password
            )
            
            # Verify cookie manager is ready
            if not hasattr(cookies, 'ready'):
                raise AttributeError("CookieManager missing 'ready' attribute")
                
            # Wait for cookies to be ready (with timeout)
            max_wait_time = 5  # seconds
            start_time = time.time()
            while not cookies.ready():
                if time.time() - start_time > max_wait_time:
                    raise TimeoutError("CookieManager not ready within timeout")
                time.sleep(0.1)
            
            st.session_state.cookie_manager = cookies
            logger.info("Cookie manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Cookie init failed: {str(e)}")
            # Fallback to session state
            st.session_state.cookie_manager = SimpleNamespace(
                get=lambda x: st.session_state.get(x),
                __setitem__=lambda k, v: st.session_state.__setitem__(k, v),
                ready=lambda: True,
                save=lambda: None
            )
    
    return st.session_state.cookie_manager

def get_persistent_user_id():
    """Get or create a persistent user ID that survives app restarts"""
    # Initialize database connection
    db_path = "user_data.db"
    conn = None
    
    try:
        # Connect to SQLite database (creates if not exists)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persistent_user (
                id TEXT PRIMARY KEY
            )
        """)
        conn.commit()
        
        # First try to get from session state
        if "user_id" in st.session_state:
            return st.session_state.user_id
        
        # Try to get from database
        cursor.execute("SELECT id FROM persistent_user LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            st.session_state.user_id = user_id
            logger.info(f"Retrieved persistent user ID from database: {user_id}")
            return user_id
        
        # Generate new ID if none exists
        new_id = str(uuid.uuid4())
        st.session_state.user_id = new_id
        
        # Save to database
        cursor.execute("INSERT INTO persistent_user (id) VALUES (?)", (new_id,))
        conn.commit()
        logger.info(f"Created new persistent user ID: {new_id}")
        
        return new_id
        
    except Exception as e:
        logger.error(f"Error in persistent user ID system: {str(e)}")
        # Fallback to session state with new ID
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
        return st.session_state.user_id
        
    finally:
        if conn:
            conn.close()

# Alias for backward compatibility
get_or_create_user_id = get_persistent_user_id