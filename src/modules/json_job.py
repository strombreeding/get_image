import json

def update_count_to_json(is_pass, count):
    # JSON 파일 경로
    json_file_path = "count.json"

    # JSON 파일 열기 및 데이터 읽기
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    if is_pass:
        # "pass_count"를 수정
        json_data['pass_count'] = count
    else:
        # "count"를 수정
        json_data['non_pass_count'] = count

    # 수정된 데이터를 JSON 파일에 다시 씁니다.
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

def get_count_to_json(is_pass):
    # JSON 파일 경로
    json_file_path = 'count.json'

    # JSON 파일 열기 및 데이터 읽기
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    result = 0 
    if is_pass:
        # "pass_count"를 수정
        result = json_data['pass_count']
    else:
        # "count"를 수정
        result = json_data['non_pass_count']

    return result


def in_history_json(is_pass, search):
    # JSON 파일 경로
    json_file_path = 'history.json'

    # JSON 파일 열기 및 데이터 읽기
    with open(json_file_path, 'r') as json_file:
        history_data = json.load(json_file)

    # 검증할 배열 선택
    target_array = history_data["pass"] if is_pass else history_data["nonPass"]

    # 검증할 데이터가 배열에 존재하는지 확인
    exists = any(entry["search"] == search for entry in target_array)

    return exists



def update_history_to_json(is_pass, cnt, search):
    # JSON 파일 경로
    json_file_path = 'history.json'

    # JSON 파일 열기 및 데이터 읽기
    with open(json_file_path, 'r') as json_file:
        history_data = json.load(json_file)

    # "pass" 배열에 새로운 데이터 추가
    if is_pass:
        new_data = {"count": cnt, "search": search}
        history_data["pass"].append(new_data)
    else:
        new_data = {"count": cnt, "search": search}
        history_data["nonPass"].append(new_data)
    # 수정된 데이터를 JSON 파일에 다시 쓰기
    with open(json_file_path, 'w') as json_file:
        json.dump(history_data, json_file, indent=4)

    return print("히스토리 기록")


