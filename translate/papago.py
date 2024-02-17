# Let's start translating the JSON file using the Papago API
#코드 실행 시 python papago.py -d [번역하고 싶은 json 파일 path] 로 실행
#translate 함수 안에 CLIENT_ID, CLIENT_SECRET에 자신의 네이버 API 정보 입력

import requests
import json
import argparse
import time

parser = argparse.ArgumentParser(description='Translate JSON file and add fields')
parser.add_argument('-d', '--json-file', type=str, required=True, help='Path to the JSON file')

args = parser.parse_args()

# JSON 파일 경로
json_file_path = args.json_file
 
#main translation function
def translate(text, source='ko', target='en'):
    CLIENT_ID, CLIENT_SECRET = 'ID입력', 'SECRET입력'
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'Content-Type': 'application/json',
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    data = {'source': 'ko', 'target': 'en', 'text': text}
    response = requests.post(url, json.dumps(data), headers=headers)
    rescode = response.status_code
    #print(rescode)
    #만약 에러 코드 뜨면 중단하고 터미널에 에러 메세지 출력
    if rescode != 200:
        raise Exception(response.json())
    else:
        return response.json()['message']['result']['translatedText']


def translate_and_add_fields(json_data):
    for key, value in json_data.items():
        if 'big_category_eng' not in value:
            big_category_translated = translate(value['big_category'])
            value['big_category_eng'] = big_category_translated
            time.sleep(0.5)
        if 'small_category_eng' not in value:
            small_category_translated = translate(value['small_category'])
            value['small_category_eng'] = small_category_translated
            time.sleep(0.5)
        if 'item_hashtags_eng' not in value:
            item_hashtags_translated = [translate(tag) for tag in value['item_hashtags']]
            value['item_hashtags_eng'] = item_hashtags_translated
            time.sleep(0.5)
    
    return json_data

# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Read the JSON file
json_data = read_json_file(json_file_path)
translated_data = translate_and_add_fields(json_data)

# Update the JSON file with the translated data (in the same file)
def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Update the JSON file with the translated data (in the same file)
write_json_file(translated_data, json_file_path)