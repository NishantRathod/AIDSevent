"""
Sample data generator for KnowledgeShare
Run this to populate the database with test data for demonstration
"""

import sqlite3
from werkzeug.security import generate_password_hash

def create_sample_data():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    
    print("Creating sample users...")
    
    # Sample users (password for all: "password123")
    sample_users = [
        ("Alice Johnson", "alice@example.com", generate_password_hash("password123"), 150, "Computer Science student passionate about algorithms"),
        ("Bob Smith", "bob@example.com", generate_password_hash("password123"), 120, "Math enthusiast sharing calculus notes"),
        ("Charlie Brown", "charlie@example.com", generate_password_hash("password123"), 100, "Physics major with lots of study materials"),
        ("Diana Prince", "diana@example.com", generate_password_hash("password123"), 90, "Engineering student helping others"),
        ("Ethan Hunt", "ethan@example.com", generate_password_hash("password123"), 80, "Chemistry researcher")
    ]
    
    try:
        for user in sample_users:
            try:
                cur.execute("INSERT INTO users(name, email, password, tokens, bio) VALUES(?,?,?,?,?)", user)
                user_id = cur.lastrowid
                cur.execute("INSERT INTO token_history(user_id, change, reason) VALUES(?,50,'Welcome Bonus')", (user_id,))
                print(f"✓ Created user: {user[0]}")
            except sqlite3.IntegrityError:
                print(f"✗ User {user[0]} already exists")
        
        print("\nCreating sample PDFs...")
        
        # Sample PDFs (note: actual files won't exist, but database entries will)
        sample_pdfs = [
            ("Data Structures Complete Guide", "Computer Science", "Comprehensive notes covering arrays, linked lists, trees, and graphs", "sample1.pdf", 1, 45, 23),
            ("Calculus I Lecture Notes", "Mathematics", "Complete calculus notes from MIT OpenCourseWare", "sample2.pdf", 2, 38, 19),
            ("Physics: Mechanics Fundamentals", "Physics", "Classical mechanics covering Newton's laws and applications", "sample3.pdf", 3, 32, 15),
            ("Organic Chemistry Basics", "Chemistry", "Introduction to organic chemistry with reactions", "sample4.pdf", 5, 28, 12),
            ("Python Programming Tutorial", "Computer Science", "Beginner-friendly Python guide with examples", "sample5.pdf", 1, 52, 31),
            ("Linear Algebra Notes", "Mathematics", "Matrix operations, eigenvalues, and vector spaces", "sample6.pdf", 2, 41, 22),
            ("Quantum Physics Introduction", "Physics", "Modern physics concepts and quantum mechanics basics", "sample7.pdf", 3, 25, 10),
            ("Engineering Mechanics", "Engineering", "Statics and dynamics for engineering students", "sample8.pdf", 4, 19, 8),
            ("Database Systems Guide", "Computer Science", "SQL, normalization, and database design principles", "sample9.pdf", 1, 36, 18),
            ("Statistics and Probability", "Mathematics", "Statistical analysis methods and probability theory", "sample10.pdf", 2, 30, 14)
        ]
        
        for pdf in sample_pdfs:
            try:
                cur.execute("""INSERT INTO pdfs(title, subject, description, filename, uploader_id, views, downloads) 
                              VALUES(?,?,?,?,?,?,?)""", pdf)
                print(f"✓ Created PDF: {pdf[0]}")
            except sqlite3.IntegrityError:
                print(f"✗ PDF {pdf[0]} already exists")
        
        con.commit()
        print("\n✅ Sample data created successfully!")
        print("\nTest Credentials:")
        print("Email: alice@example.com | Password: password123")
        print("Email: bob@example.com | Password: password123")
        print("Email: charlie@example.com | Password: password123")
        print("Email: diana@example.com | Password: password123")
        print("Email: ethan@example.com | Password: password123")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    print("=" * 60)
    print("KnowledgeShare - Sample Data Generator")
    print("=" * 60)
    print("\nThis will create sample users and PDFs for testing.")
    print("Note: Actual PDF files won't be created, only database entries.\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        create_sample_data()
    else:
        print("Cancelled.")
