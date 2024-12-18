from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from bs4 import BeautifulSoup


def web_parser():
    # 크롬 드라이버 설정 (ChromeDriver 경로를 지정해 주세요)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 백그라운드 실행
    chrome_options.add_argument("--no-sandbox")  # 리소스 보호 비활성화 (일부 환경에서 권장)
    chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 공유 비활성화 (일부 환경에서 권장)

    driver = webdriver.Chrome(options=chrome_options)

    # 웹 페이지 열기
    url = 'https://www.kopo.ac.kr/jungsu/content.do?menu=247'  # 크롤링할 웹 페이지의 URL로 변경해야 합니다.
    driver.get(url)

    # 페이지가 로드될 시간을 기다림
    time.sleep(0.5)  # 필요에 따라 조정

    try:
        # <div class="meal_box"> 요소 찾기
        meal_box = driver.find_element(By.CLASS_NAME, "meal_box")
        meal_box_html = meal_box.get_attribute("outerHTML")



        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(meal_box_html, "html.parser")

        # 1. 식사 시간표 추출
        result = ""

        # 1. 식사 시간표 추출
        time_table = soup.find("table", class_="tbl_table time")
        if time_table:
            result += "식사 시간표:\n"
            for row in time_table.find("tbody").find_all("tr"):
                times = [col.text.strip() for col in row.find_all("td")]
                result += f"  아침: {times[0]}, 점심: {times[1]}, 저녁: {times[2]}\n"

        # 2. 식단 정보 추출
        menu_table = soup.find("table", class_="tbl_table menu")
        if menu_table:
            result += "\n식단 정보:\n"
            for row in menu_table.find("tbody").find_all("tr"):
                date = row.find("td").text.strip()  # 날짜
                meals = [col.text.strip().replace("\n", ", ") for col in row.find_all("td")[1:]]
                result += f"{date}:\n"
                result += f"  - 조식: {meals[0]}\n"
                result += f"  - 중식: {meals[1]}\n"
                result += f"  - 석식: {meals[2]}\n"

        # 결과 출력
        pprint(result)
        return result

    except Exception as e:
        print("오류 발생:", e)

    # 드라이버 닫기
    driver.quit()
