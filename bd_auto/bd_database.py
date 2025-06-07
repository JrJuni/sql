import sqlite3

def create_database():
    """
    영업 관리 시스템을 위한 초기 데이터베이스와 테이블을 생성합니다.
    """
    # 'sales_data.db' 파일로 데이터베이스에 연결합니다. 파일이 없으면 새로 생성됩니다.
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()

    # 1. 법인 정보 테이블 (Companies)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL UNIQUE,
            industry TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. 담당자 정보 테이블 (Contacts)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            FOREIGN KEY (company_id) REFERENCES Companies (id)
        )
    ''')

    # 3. 커뮤니케이션 기록 테이블 (Interactions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            interaction_date DATE NOT NULL,
            channel TEXT,
            summary TEXT NOT NULL,
            is_response_needed BOOLEAN DEFAULT FALSE,
            is_completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (contact_id) REFERENCES Contacts (id)
        )
    ''')

    # 4. 구매 내역 테이블 (Purchases)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            purchase_date DATE NOT NULL,
            license_info TEXT,
            FOREIGN KEY (company_id) REFERENCES Companies (id)
        )
    ''')

    # 변경사항을 저장하고 연결을 닫습니다.
    conn.commit()
    conn.close()
    print("'sales_data.db' 데이터베이스와 테이블이 성공적으로 생성되었습니다.")

if __name__ == '__main__':
    create_database()