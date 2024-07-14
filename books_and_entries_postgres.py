import psycopg2
import json
import os

def get_db_connection():
    return psycopg2.connect(
        dbname="rpgdb",
        user="postgres",
        password=".",  # Replace with your actual password
        host="localhost"
    )

def insert_books_and_entries(json_file):
    conn = get_db_connection()
    cur = conn.cursor()

    with open(json_file, 'r') as f:
        data = json.load(f)
        for book in data['book']:
            # Insert book metadata into books table
            cur.execute(
                """
                INSERT INTO source_books (name, source, cover_url, published, author)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (book['name'], book['source'], book['coverUrl'], book['published'], book.get('author'))
            )
            book_id = cur.fetchone()[0]

            for chapter in book['contents']:
                # Insert chapter data into chapters table
                ordinal_type = chapter['ordinal']['type'] if 'ordinal' in chapter else None
                ordinal_identifier = chapter['ordinal'].get('identifier') if 'ordinal' in chapter and 'identifier' in chapter['ordinal'] else None

                cur.execute(
                    """
                    INSERT INTO chapters (book_id, name, ordinal_type, ordinal_identifier)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (book_id, chapter['name'], ordinal_type, ordinal_identifier)
                )
                chapter_id = cur.fetchone()[0]

                if 'headers' in chapter:
                    for header in chapter['headers']:
                        if isinstance(header, dict):
                            header_text = header['header']
                            depth = header.get('depth', 0)
                        else:
                            header_text = header
                            depth = 0

                        # Insert header data into headers table
                        cur.execute(
                            """
                            INSERT INTO headers (chapter_id, header, depth)
                            VALUES (%s, %s, %s);
                            """,
                            (chapter_id, header_text, depth)
                        )

    conn.commit()
    cur.close()
    conn.close()

# File path of the JSON file
json_file = './src/books/books.json'

insert_books_and_entries(json_file)
