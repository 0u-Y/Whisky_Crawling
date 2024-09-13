
from whisky_crawling import collect_whisky_info
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

def create_connection():
    connection = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASS'),
        database = os.getenv('DB_NAME')
    )
    
    return connection



def insert_whisky_info(connection, whisky_data):
    query = """
    INSERT INTO whisky_info(whisky_name, bottling_serie, stated_age, strength)
    VALUES (%s, %s, %s, %s)
    """



    cursor = connection.cursor()
    cursor.executemany(query, whisky_data)
    connection.commit()





if __name__ == "__main__":
    
    conn = create_connection()
    
    
    whisky_data = collect_whisky_info()

    
    data = [
        (whisky['위스키 이름'], whisky['Bottling Serie'], whisky['Stated Age'], whisky['도수']) 
        for whisky in whisky_data
    ]

    insert_whisky_info(conn, data)

    print("DB 저장 완료")

    conn.close()
