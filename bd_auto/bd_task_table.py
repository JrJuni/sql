import sqlite3
import os

def get_db_connection(db_name='sales_data_task.db'):
    """데이터베이스 연결을 생성하고 커넥션과 커서 객체를 반환합니다."""
    # 현재 스크립트 파일의 디렉토리를 가져옵니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, db_name)
    conn = sqlite3.connect(db_path)
    # 딕셔너리 형태로 결과를 받기 위해 row_factory 설정
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    return conn, cursor

def setup_database(db_name='sales_data_task.db'):
    """'tasks' 테이블을 생성합니다. current_status의 기본값을 'To Do'로 변경합니다."""
    try:
        conn, cursor = get_db_connection(db_name=db_name)
        # 'IF NOT EXISTS'를 추가하여 테이블이 이미 있을 경우 오류를 방지합니다.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT NOT NULL,
            company_name TEXT NOT NULL,
            contact_person TEXT NOT NULL,
            contact_email TEXT,
            contact_phone TEXT,
            task_description TEXT NOT NULL,
            current_status TEXT NOT NULL DEFAULT 'To Do',
            due_date TEXT,
            assignee TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        print("데이터베이스와 테이블이 준비되었습니다.")

    except sqlite3.Error as e:
        print(f"데이터베이스 오류: {e}")
    finally:
        if conn:
            conn.close()

# 함수 호출하여 실행
if __name__ == '__main__':
    setup_database(db_name='test001.db')