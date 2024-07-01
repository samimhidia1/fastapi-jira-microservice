import psycopg2
from psycopg2 import sql
from core.database import get_db_connection, return_db_connection

def create_epic(epic):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        insert_query = sql.SQL("""
            INSERT INTO epics (id, summary, description, project_key, custom_fields)
            VALUES (%s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (epic.id, epic.summary, epic.description, epic.project_key, epic.custom_fields))
        connection.commit()
    except Exception as error:
        print("Error while creating epic:", error)
    finally:
        cursor.close()
        return_db_connection(connection)

def get_epic(epic_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        select_query = sql.SQL("SELECT * FROM epics WHERE id = %s")
        cursor.execute(select_query, (epic_id,))
        result = cursor.fetchone()
        if result:
            return Epic(*result)
    except Exception as error:
        print("Error while retrieving epic:", error)
    finally:
        cursor.close()
        return_db_connection(connection)
    return None

def update_epic(epic):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        update_query = sql.SQL("""
            UPDATE epics
            SET summary = %s, description = %s, project_key = %s, custom_fields = %s
            WHERE id = %s
        """)
        cursor.execute(update_query, (epic.summary, epic.description, epic.project_key, epic.custom_fields, epic.id))
        connection.commit()
    except Exception as error:
        print("Error while updating epic:", error)
    finally:
        cursor.close()
        return_db_connection(connection)

def delete_epic(epic_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        delete_query = sql.SQL("DELETE FROM epics WHERE id = %s")
        cursor.execute(delete_query, (epic_id,))
        connection.commit()
    except Exception as error:
        print("Error while deleting epic:", error)
    finally:
        cursor.close()
        return_db_connection(connection)
