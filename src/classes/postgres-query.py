import psycopg2
from psycopg2 import sql

# Database credentials
db = "rpgdb"
username = "postgres"
passw = "."
hostname = "localhost"

def get_spell_slots(class_id,subclass_id,level):
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname=db,
        user=username,
        password=".",
        host=hostname
    )

    # Create a cursor object
    cur = conn.cursor()

    print(class_id,subclass_id, level)

    if subclass_id == None:
        subclass_id = 0
        query = """
        SELECT slots FROM spell_slots WHERE class_id = %s and level = %s;
        """
    else:    # Define your query
        query = """
        SELECT slots FROM spell_slots WHERE class_id = %s and subclass_id = %s and level = %s;
        """
   
    # Execute the query
    cur.execute(query, (class_id,subclass_id, level))

    # Fetch all the results
    result = cur.fetchall()
    # Assuming there's always at least one result
    if result:
        data = result[0][0]
    else:
        data = None

    # Close the cursor and connection
    cur.close()
    conn.close()

    return data

# Example usage
spell_slots = get_spell_slots(10,20, 3)
print(spell_slots)

#Add Subclass Check??