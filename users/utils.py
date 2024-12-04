import json

def load_club_data():
    with open('club.json', 'r', encoding='utf-8') as file:
        return json.load(file)

club_data = load_club_data()

def get_club(code):
        for club in club_data:
            if club['code'] == code:
                return club['name']
        return None

def handle_request(code):
    name = get_club_name(code)
    if name:
        return {'name': name}
    else:
        return {'error': '해당 코드의 동아리를 찾을 수 없습니다.'}
