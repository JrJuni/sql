from datetime import datetime
import db_setup
import db_manager

# --- 사용자 인터페이스(UI) 및 입력 처리 헬퍼 함수 ---
def get_user_input(prompt_text, default_value=None, required=True):
    """사용자로부터 입력을 받는 범용 함수."""
    prompt = f"{prompt_text} (기본값: {default_value})" if default_value is not None else prompt_text
    while True:
        user_input = input(f"{prompt}: ").strip()
        if user_input: return user_input
        if default_value is not None: return default_value
        if required: print("이 값은 필수입니다. 다시 입력해주세요.")
        else: return ""

def select_contact_from_list(is_multiple=False):
    """사용자가 목록에서 연락처를 선택하거나 새로 추가하도록 돕는 UI 함수."""
    while True: # 새 연락처 추가 후 목록을 다시 보여주기 위해 루프 사용
        contacts = db_manager.get_all_contacts()
        
        if not contacts:
            print("\n현재 등록된 연락처가 없습니다.")
            choice = input("지금 새 연락처를 추가하시겠습니까? (y/n): ").strip().lower()
            if choice == 'y':
                run_add_contact_flow()
                continue # 연락처 추가 후 루프를 다시 시작하여 목록을 보여줍니다.
            else:
                return None # 사용자가 추가를 원치 않으면 None을 반환합니다.
        
        print("\n--- 연락처 목록 ---")
        for c in contacts:
            print(f"  ID {c['id']}: {c['person_name']} ({c['company_name']})")
        
        prompt = "연결할 연락처의 ID를 입력하세요"
        if is_multiple: prompt += " (쉼표로 구분)"
        prompt += " (또는 'new'를 입력하여 새로 추가)"

        ids_str = input(f"{prompt}: ").strip().lower()

        if ids_str == 'new':
            run_add_contact_flow()
            continue # 새 연락처 추가 후 목록을 다시 보여주기 위해 루프를 다시 시작합니다.

        selected_ids = [int(i.strip()) for i in ids_str.split(',') if i.strip().isdigit()]
        
        if not selected_ids:
            print("올바른 ID나 'new'를 입력해주세요.")
            continue

        # 유효성 검사 (실제 존재하는 ID인지 확인)
        valid_ids = [c['id'] for c in contacts]
        if all(sid in valid_ids for sid in selected_ids):
            return selected_ids if is_multiple else selected_ids[0]
        else:
            print("목록에 없는 ID가 포함되어 있습니다. 다시 입력해주세요.")

# --- 메뉴 실행 함수 ---

def run_add_contact_flow():
    """연락처 추가 과정을 진행하는 함수."""
    print("\n=== 새 연락처 추가 ===")
    contact_details = {
        'person_name': get_user_input("이름 (필수)"),
        'company_name': get_user_input("회사명 (필수)"),
        'email': get_user_input("이메일 (선택)", default_value="", required=False),
        'phone': get_user_input("전화번호 (선택)", default_value="", required=False),
        'age': get_user_input("연령 (선택)", default_value="", required=False),
        'department': get_user_input("부서 (선택)", default_value="", required=False),
        'position': get_user_input("직급 (선택)", default_value="", required=False),
        'notes': get_user_input("특이사항 (선택)", default_value="", required=False)
    }
    db_manager.add_contact(contact_details)

def run_add_project_flow():
    """프로젝트 추가 과정을 진행하는 함수."""
    print("\n=== 새 프로젝트 추가 ===")
    project_details = {
        'name': get_user_input("프로젝트명 (필수)"),
        'start_date': get_user_input("시작일 (YYYY-MM-DD)", default_value=datetime.now().strftime('%Y-%m-%d')),
        'end_date': get_user_input("마감일 (YYYY-MM-DD, 선택)", required=False)
    }
    
    participant_ids = select_contact_from_list(is_multiple=True)
    if not participant_ids:
        print("참가자가 선택되지 않아 프로젝트 생성을 취소합니다.")
        return
    project_details['participant_ids'] = participant_ids

    tech_str = get_user_input("관련 기술 (쉼표로 구분)")
    project_details['technologies'] = [tech.strip() for tech in tech_str.split(',') if tech.strip()]

    db_manager.add_project(project_details)

def run_view_projects_flow():
    """프로젝트 목록을 조회하고 출력하는 함수."""
    print("\n=== 전체 프로젝트 목록 ===")
    project_details = db_manager.get_all_projects_with_details()
    if not project_details:
        print("저장된 프로젝트가 없습니다.")
        return
        
    for detail in project_details:
        p = detail['project']
        participants = detail['participants']
        technologies = detail['technologies']
        
        print("-" * 25)
        print(f"ID: {p['id']} | 프로젝트명: {p['name']}")
        print(f"  기간: {p['start_date']} ~ {p['end_date'] or '진행중'}")
        
        participant_list = [f"{part['person_name']}({part['company_name']})" for part in participants]
        print(f"  참가자: {', '.join(participant_list) if participant_list else '없음'}")

        tech_list = [tech['technology_name'] for tech in technologies]
        print(f"  관련 기술: {', '.join(tech_list) if tech_list else '없음'}")
    print("-" * 25)


# --- 메인 실행 블록 ---
def main():
    # 프로그램 시작 시 데이터베이스 구조 확인 및 생성
    db_setup.setup_database(db_name='sales_mobi_2025.db')

    while True:
        print("\n--- 영업 및 프로젝트 관리 시스템 ---")
        print("1. 프로젝트 추가")
        print("2. 전체 프로젝트 조회")
        print("3. 연락처 추가")
        # 여기에 다른 메뉴들을 추가할 수 있습니다.
        print("9. 종료")
        choice = input("원하는 작업의 번호를 입력하세요: ").strip()

        if choice == '1':
            run_add_project_flow()
        elif choice == '2':
            run_view_projects_flow()
        elif choice == '3':
            run_add_contact_flow()
        elif choice == '9':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력하세요.")

if __name__ == '__main__':
    main()
