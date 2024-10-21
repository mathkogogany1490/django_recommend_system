# import mysql.connector as conn
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def connect_field():
    fields = {
        "host": "3.36.78.179",
        "username": "kogo1490",
        "password": "math1106",
        "database": "mydb",
        "port": 3306
    }
    return fields
def postgres_connect_field():
    fields = {
        "host": "52.79.160.194",
        "username": "kogo1490",
        "password": "math1106",
        "database": "mydb",
        "port": 5432
    }
    return fields

def bring_dataframe_from_table(table, flag):
    if flag == "postgres":
        fields = postgres_connect_field()
        conn = f"postgresql+psycopg2://{fields['username']}:{fields['password']}@{fields['host']}:{fields['port']}/{fields['database']}"
    elif flag == "mysql":
        fields = connect_field()
        conn = f"mysql+mysqlconnector://{fields['username']}:{fields['password']}@{fields['host']}:{fields['port']}/{fields['database']}"
    try:
        engine = create_engine(conn)
        query = f"select * from {table}"
        df = pd.read_sql(query, con=engine)
    except SQLAlchemyError as e:
        # 에러 처리 및 로그 출력
        print(f"Error while inserting data: {e}")
        return
    else:
        engine.dispose()
        print("Data selected and connection closed!!!")
    return df

def insert_data_into_table(df, table):
    # connecting fields
    fields = connect_field()
    # MySQL 연결 문자열 생성
    conn = f"mysql+mysqlconnector://{fields['username']}:{fields['password']}@{fields['host']}:{fields['port']}/{fields['database']}"

      # 예외 처리를 통한 안전한 MySQL 연결 및 데이터 삽입
    try:
        # with 문으로 engine 자동 종료 처리
        with create_engine(conn).connect() as connection:

            # DataFrame 데이터를 MySQL 테이블에 삽입
            df.to_sql(table, con=connection, if_exists='append', chunksize=1000, index=False)
            print(f"Data inserted successfully into table {table}.")
    except SQLAlchemyError as e:
        # 에러 처리 및 로그 출력
        print(f"Error while inserting data: {e}")
    else:
        print("Data inserted and connection closed!!!")