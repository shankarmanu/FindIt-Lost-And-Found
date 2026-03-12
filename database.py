import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'items.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create the items table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            emoji TEXT NOT NULL,
            name TEXT NOT NULL,
            desc TEXT NOT NULL,
            loc TEXT NOT NULL,
            date TEXT NOT NULL,
            cat TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    
    # Check if we need to seed the database with sample data
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM items')
    row = cursor.fetchone()
    
    if row['count'] == 0:
        sample_items = [
            ('lost', '📱', 'iPhone 15 Pro – Space Black', 'Lost near Times Square subway entrance. Has a red case with initials "J.M." scratched on the back.', 'Times Square, NYC', 'Mar 10, 2026', 'Mobile', 'john@example.com'),
            ('found', '🐾', 'Golden Retriever – Male, 3yrs', 'Found wandering near Riverside Park. Friendly, wearing a blue collar but no tag. Currently safe with finder.', 'Riverside Park, NYC', 'Mar 11, 2026', 'Pet', '555-0102'),
            ('lost', '👜', 'Brown Leather Wallet', 'Lost at Grand Central Terminal during rush hour. Contains cash, 3 credit cards, and a library card with my name.', 'Grand Central, NYC', 'Mar 9, 2026', 'Wallet', 'jane@example.com'),
            ('found', '🔑', 'Keychain – 4 keys & fob', 'Found on a bench in Bryant Park. Silver keychain with a small Eiffel Tower charm. Turned in to park security.', 'Bryant Park, NYC', 'Mar 12, 2026', 'Keys', 'security@example.com'),
            ('lost', '🪪', 'Passport + Driver''s License', 'Lost my passport and license in a blue document folder near JFK Airport baggage claim. Extremely urgent.', 'JFK Airport, NYC', 'Mar 8, 2026', 'ID', 'urgent@example.com'),
            ('found', '🧳', 'Black Samsonite Carry-On', 'Found in Penn Station. Has a yellow luggage tag but no contact info. Stored at the station lost & found.', 'Penn Station, NYC', 'Mar 11, 2026', 'Bag', 'station@example.com')
        ]
        
        conn.executemany('''
            INSERT INTO items (type, emoji, name, desc, loc, date, cat, contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_items)
        
    conn.commit()
    conn.close()

def get_all_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(ix) for ix in items]

def add_item(item_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (type, emoji, name, desc, loc, date, cat, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item_data['type'],
        item_data['emoji'],
        item_data['name'],
        item_data['desc'],
        item_data['loc'],
        item_data['date'],
        item_data['cat'],
        item_data['contact']
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
