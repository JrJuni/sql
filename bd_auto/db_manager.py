import sqlite3
from datetime import datetime
from db_setup import get_db_connection

# --- 데이터 조회(Read) 함수들 ---
def get_all_contacts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY person_name")
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_all_projects_with_details():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY name")
    projects = cursor.fetchall()
    
    project_details = []
    for p in projects:
        # 참가자 목록 조회
        cursor.execute("""
            SELECT c.person_name, c.company_name FROM contacts c
            JOIN project_participants pp ON c.id = pp.contact_id
            WHERE pp.project_id = ?
        """, (p['id'],))
        participants = cursor.fetchall()
        
        # 기술 목록 조회
        cursor.execute("SELECT technology_name FROM project_technologies WHERE project_id = ?", (p['id'],))
        technologies = cursor.fetchall()
        
        project_details.append({
            'project': p,
            'participants': participants,
            'technologies': technologies
        })
        
    conn.close()
    return project_details

# --- 데이터 생성(Create) 함수들 ---
def add_contact(details):
    sql = '''INSERT INTO contacts (person_name, company_name, email, phone, age, department, position, notes)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (details['person_name'], details['company_name'], details['email'], 
                             details['phone'], details['age'], details['department'], 
                             details['position'], details['notes']))
        conn.commit()
        print(f"✅ 연락처 '{details['person_name']}'님이 성공적으로 추가되었습니다!")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"❌ 오류: 해당 이메일({details['email']})을 가진 연락처가 이미 존재합니다.")
    except sqlite3.Error as e:
        print(f"❌ 데이터 삽입 중 오류 발생: {e}")
    finally:
        if conn: conn.close()
    return None

def add_project(details):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 트랜잭션 시작
        cursor.execute("BEGIN")
        
        # 1. 프로젝트 기본 정보 추가
        cursor.execute("INSERT INTO projects (name, start_date, end_date) VALUES (?, ?, ?)", 
                       (details['name'], details['start_date'], details['end_date']))
        project_id = cursor.lastrowid
        
        # 2. 참가자 정보 추가
        for contact_id in details['participant_ids']:
            cursor.execute("INSERT INTO project_participants (project_id, contact_id) VALUES (?, ?)", 
                           (project_id, contact_id))
            
        # 3. 기술 정보 추가
        for tech in details['technologies']:
            cursor.execute("INSERT INTO project_technologies (project_id, technology_name) VALUES (?, ?)", 
                           (project_id, tech))
            
        conn.commit()
        print(f"✅ 프로젝트 '{details['name']}'이(가) 성공적으로 추가되었습니다!")
    except sqlite3.Error as e:
        conn.rollback() # 오류 발생 시 트랜잭션 롤백
        print(f"❌ 프로젝트 추가 중 오류 발생: {e}")
    finally:
        if conn: conn.close()

# 여기에 update_task, delete_task 등의 다른 데이터 관리 함수들을 추가할 수 있습니다.