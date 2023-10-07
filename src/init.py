import json
import os

directory_path = 'imgs/pass'

# 디렉토리 내부의 모든 파일 삭제
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

directory_path = 'imgs/nonPass'
# 디렉토리 내부의 모든 파일 삭제
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)


# count.json 초기 데이터 생성
count_data = {
    "pass_count": 0,
    "non_pass_count": 0
}

count_json_path = 'count.json'

with open(count_json_path, 'w') as count_json_file:
    json.dump(count_data, count_json_file, indent=4)

# history.json 초기 데이터 생성
history_data = {
    "pass": [],
    "nonPass": []
}

history_json_path = 'history.json'

with open(history_json_path, 'w') as history_json_file:
    json.dump(history_data, history_json_file, indent=4)

print("JSON 파일 초기화 완료")