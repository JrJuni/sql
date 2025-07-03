import sqlite3

def get_db_connection(db_name='sales_mobi_2025.db'):
    """데이터베이스 연결을 생성하고 커넥션 객체를 반환합니다."""
    # (실제 환경에서는 db_name을 설정 파일에서 가져오는 것이 좋습니다)
    conn = sqlite3.connect(db_name)
    # 외래 키 제약 조건을 활성화합니다.
    conn.execute("PRAGMA foreign_keys = ON;")
    # 결과를 딕셔너리처럼 사용할 수 있도록 row_factory를 설정합니다.
    conn.row_factory = sqlite3.Row
    return conn

def setup_database(db_name='sales_mobi_2025.db'):
    """
    모든 테이블(contacts, categories, tasks, projects 등)의 스키마를 정의하고 생성합니다.
    이 함수는 프로그램 시작 시 한 번만 호출됩니다.
    """
    print("데이터베이스 설정 확인 및 초기화 시작...")
    try:
        conn = get_db_connection(db_name)
        cursor = conn.cursor()

        # 1. 연락처 테이블 (contacts)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            age INTEGER,
            department TEXT,
            position TEXT,
            notes TEXT
        )
        ''')

        # 2. 카테고리 테이블 (categories)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')
        
        # 3. 프로젝트 테이블 (projects)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            start_date TEXT,
            end_date TEXT
        )
        ''')

        # 4. 업무 테이블 (tasks) - 다른 테이블을 참조하는 외래 키 포함
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT NOT NULL,
            task_description TEXT NOT NULL,
            current_status TEXT NOT NULL DEFAULT 'To Do',
            due_date TEXT,
            assignee TEXT NOT NULL,
            contact_id INTEGER,
            category_id INTEGER,
            project_id INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE SET NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
        )
        ''')
        
        # 5. 프로젝트-참가자 연결 테이블 (다대다 관계)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_participants (
            project_id INTEGER,
            contact_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
            FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
            PRIMARY KEY (project_id, contact_id)
        )
        ''')
        
        # 6. 프로젝트-기술 연결 테이블 (다대다 관계)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_technologies (
            project_id INTEGER,
            technology_name TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
            PRIMARY KEY (project_id, technology_name)
        )
        ''')

        conn.commit()
        print("데이터베이스 스키마가 성공적으로 준비되었습니다.")
    except sqlite3.Error as e:
        print(f"데이터베이스 설정 중 오류 발생: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    setup_database(db_name='sales_mobi_2025.db')