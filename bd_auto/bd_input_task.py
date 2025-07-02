import sqlite3
import os
from datetime import datetime

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

def setup_database():
    """'tasks' 테이블을 생성합니다. current_status의 기본값을 'To Do'로 변경합니다."""
    try:
        conn, cursor = get_db_connection()
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

def get_user_input(prompt_text, default_value="", required=True):
    """사용자로부터 입력을 받고, 필수 값인 경우 비어있지 않은지 확인합니다."""
    prompt = f"{prompt_text} (기본값: {default_value})" if default_value else prompt_text
    while True:
        user_input = input(f"{prompt}: ").strip()
        if user_input:
            return user_input
        # default_value가 None이 아닌 경우(빈 문자열 포함) 기본값을 반환
        if default_value is not None:
            return default_value
        if required:
            print("이 값은 필수입니다. 다시 입력해주세요.")
        else:
            return ""

def get_status_input(default_value):
    """사용자로부터 정해진 상태 값 중 하나를 입력받습니다."""
    status_options = ['To Do', 'In Progress', 'Done', 'Pending']
    # 입력 옵션을 title-case로 통일하여 비교 (e.g., 'to do' -> 'To Do')
    status_options_lower = [opt.lower() for opt in status_options] 
    prompt = f"진행 상태 ({', '.join(status_options)}, 기본값: {default_value})"
    
    while True:
        user_input = input(f"{prompt}: ").strip()
        if not user_input:
            return default_value
        
        if user_input.lower() in status_options_lower:
            # 일관된 데이터 저장을 위해 Title Case로 변환하여 반환
            return user_input.title()
            
        print(f"잘못된 입력입니다. [{', '.join(status_options)}] 중 하나를 입력해주세요.")

def insert_task():
    """사용자로부터 입력받은 데이터로 'tasks' 테이블에 새로운 레코드를 삽입합니다."""
    print("\n=== [1] 새로운 영업 활동 추가 ===")
    task_date = get_user_input("날짜", default_value=datetime.now().strftime('%Y-%m-%d'))
    company_name = get_user_input("회사명 (필수)")
    contact_person = get_user_input("담당자 (필수)")
    contact_email = get_user_input("이메일 (선택)", default_value="", required=False)
    contact_phone = get_user_input("연락처 (선택)", default_value="", required=False)
    task_description = get_user_input("주요 내용 (필수)")
    current_status = get_status_input(default_value="To Do")
    due_date = get_user_input("마감일 (YYYY-MM-DD, 선택)", default_value="", required=False)
    assignee = get_user_input("담당 직원 (필수)")

    try:
        conn, cursor = get_db_connection()
        sql = '''
        INSERT INTO tasks (task_date, company_name, contact_person, contact_email, contact_phone, task_description, current_status, due_date, assignee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        task_data = (task_date, company_name, contact_person, contact_email, contact_phone, task_description, current_status, due_date, assignee)
        cursor.execute(sql, task_data)
        conn.commit()
        print("\n✅ 데이터가 성공적으로 추가되었습니다!")
    except sqlite3.Error as e:
        print(f"\n❌ 데이터 삽입 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

def view_tasks():
    """'tasks' 테이블의 모든 레코드를 조회하여 출력합니다."""
    print("\n=== [2] 전체 영업 활동 조회 ===")
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        if not tasks:
            print("조회할 데이터가 없습니다.")
            return
        
        for task in tasks:
            print("-" * 20)
            print(f"ID: {task['id']}")
            print(f"  - 날짜: {task['task_date']}, 마감일: {task['due_date'] or 'N/A'}")
            print(f"  - 회사: {task['company_name']} ({task['contact_person']})")
            print(f"  - 연락처: {task['contact_phone'] or 'N/A'}, 이메일: {task['contact_email'] or 'N/A'}")
            print(f"  - 내용: {task['task_description']}")
            print(f"  - 상태: {task['current_status']}, 담당: {task['assignee']}")
            print(f"  - 생성: {task['created_at']}, 최종 수정: {task['updated_at']}")
        print("-" * 20)

    except sqlite3.Error as e:
        print(f"\n❌ 데이터 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

def update_task():
    """기존 레코드를 ID로 찾아 모든 필드를 수정합니다. `updated_at`을 여기서 갱신합니다."""
    print("\n=== [3] 영업 활동 수정 ===")
    task_id = input("수정할 활동의 ID를 입력하세요: ").strip()
    if not task_id.isdigit():
        print("올바른 ID를 입력해주세요.")
        return

    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            print(f"ID {task_id}에 해당하는 활동을 찾을 수 없습니다.")
            return

        print("\n--- 기존 데이터를 불러왔습니다. 수정할 내용을 입력하세요. (변경 없으면 Enter) ---")
        task_date = get_user_input("날짜", default_value=task['task_date'])
        company_name = get_user_input("회사명", default_value=task['company_name'])
        contact_person = get_user_input("담당자", default_value=task['contact_person'])
        contact_email = get_user_input("이메일", default_value=task['contact_email'], required=False)
        contact_phone = get_user_input("연락처", default_value=task['contact_phone'], required=False)
        task_description = get_user_input("주요 내용", default_value=task['task_description'])
        current_status = get_status_input(default_value=task['current_status'])
        due_date = get_user_input("마감일 (YYYY-MM-DD)", default_value=task['due_date'], required=False)
        assignee = get_user_input("담당 직원", default_value=task['assignee'])
        
        # 여기서 updated_at 값을 직접 설정합니다.
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = '''
        UPDATE tasks SET
            task_date = ?, company_name = ?, contact_person = ?,
            contact_email = ?, contact_phone = ?, task_description = ?,
            current_status = ?, due_date = ?, assignee = ?,
            updated_at = ?
        WHERE id = ?
        '''
        update_data = (
            task_date, company_name, contact_person, contact_email, contact_phone, 
            task_description, current_status, due_date, assignee, updated_at, task_id
        )
        cursor.execute(sql, update_data)
        conn.commit()
        print(f"\n✅ ID {task_id} 활동이 성공적으로 수정되었습니다!")

    except sqlite3.Error as e:
        print(f"\n❌ 데이터 수정 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

def delete_task():
    """기존 레코드를 ID로 찾아 삭제합니다."""
    print("\n=== [4] 영업 활동 삭제 ===")
    task_id = input("삭제할 활동의 ID를 입력하세요: ").strip()
    if not task_id.isdigit():
        print("올바른 ID를 입력해주세요.")
        return

    try:
        conn, cursor = get_db_connection()
        # 삭제 전에 해당 데이터가 있는지 확인합니다.
        cursor.execute("SELECT id, company_name FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            print(f"ID {task_id}에 해당하는 활동을 찾을 수 없습니다.")
            return

        # 사용자에게 정말 삭제할 것인지 다시 한번 확인합니다.
        confirm = input(f"ID {task['id']} ({task['company_name']}) 활동을 정말로 삭제하시겠습니까? (y/n): ").strip().lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            print(f"\n✅ ID {task_id} 활동이 성공적으로 삭제되었습니다!")
        else:
            print("삭제를 취소했습니다.")

    except sqlite3.Error as e:
        print(f"\n❌ 데이터 삭제 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()


# 메인 실행 블록
if __name__ == '__main__':
    setup_database()
    
    while True:
        print("\n--- 영업 활동 관리 ---")
        print("1. 활동 추가")
        print("2. 전체 활동 조회")
        print("3. 활동 수정")
        print("4. 활동 삭제")
        print("5. 종료")
        choice = input("원하는 작업의 번호를 입력하세요: ").strip()

        if choice == '1':
            insert_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            update_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3, 4, 5 중 하나를 입력하세요.")
