import psycopg2
import json

# Configure your database connection here
DATABASE = {
    'database': 'rpgdb',
    'user': 'postgres',
    'password': '.',
    'host': '10.0.0.58',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE)
    return conn

def get_slots(character_id, class_id, subclass_id, level):
    if not subclass_id:
        subclass_id = 0
    if not (character_id and class_id and level):
        return {'error': 'Missing required parameters'}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
        -- Query to get available slots
        WITH available_slots AS (
            SELECT 
                generate_series AS level,
                slots::jsonb->>(generate_series - 1) AS slots_available
            FROM 
                spell_slots,
                generate_series(1, 9)
            WHERE 
                class_id = %s 
                AND level = %s
        ),

        -- Query to get used slots
        used_slots AS (
            SELECT 
                spell_slot_level AS level,
                COUNT(*) AS slots_used
            FROM 
                spell_slots_usage 
            WHERE 
                character_id = %s
            GROUP BY 
                spell_slot_level
        )

        -- Combine results using UNION
        SELECT 
            a.level,
            a.slots_available,
            COALESCE(u.slots_used, 0) AS slots_used
            
        FROM 
            available_slots a
        LEFT JOIN 
            used_slots u ON a.level = u.level

        UNION ALL

        SELECT 
            u.level,
            '0' AS slots_available,
            u.slots_used
        FROM 
            used_slots u
        LEFT JOIN 
            available_slots a ON u.level = a.level
        WHERE 
            a.level IS NULL

        ORDER BY level;
        """, (class_id, level, character_id))
        usage = cur.fetchall()

        cur.close()
        conn.close()

        # Format the result into a dictionary
        formatted_result = []
        for row in usage:
            formatted_result.append({
                'level': row[0],
                'slots_available': row[1],
                'slots_used': row[2],
                'slots_remaining':int(row[1]) - int(row[2])
            })

        return {
            'slots': formatted_result
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

# Test the function directly
character_id = 371
class_id = 13
subclass_id = 0
level = 5

result, status_code = get_slots(character_id, class_id, subclass_id, level)

if status_code == 200:
    print("Slots and Usage Information:")
    print(json.dumps(result, indent=4))
else:
    print("Error:")
    print(result)
