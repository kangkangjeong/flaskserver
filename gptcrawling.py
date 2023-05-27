import os
import openai
import json

def get_chatgpt_msg(msg):
    # OpenAI API 인증을 위한 키 설정
    openai.api_key = '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'

    # ChatGPT 모델에 대한 요청 생성
    response = openai.Completion.create(
        engine='text-davinci-003',  # GPT 3.5 Turbo 엔진
        prompt=msg,
        max_tokens=256,  # 반환될 최대 토큰 수
        temperature=0.7,  # 다양성 조절을 위한 온도 설정
        n=3,  # 생성할 응답의 수
        stop=None,  # 응답의 종료 시그널
        timeout=None,  # 요청 제한 시간
    )

    # 가장 높은 점수를 받은 응답 추출
    reply = response.choices[0].text.strip()
    print(reply)
    return reply

def extract_recommendations(reply):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    chrome_driver_path = './installchrome/chromedriver'
    chrome_service = Service(executable_path=chrome_driver_path)
    #웹창열지않고 실행
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # Chrome WebDriver를 사용하여 웹 브라우저 열기
    driver = webdriver.Chrome(options=chrome_options)

    # 구글 이미지 검색 페이지 열기
    driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')
    # driver.implicitly_wait(0.5)
    # 이미지 검색어 입력
    search_query = reply  # 원하는 검색어로 변경
    search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    search_box.send_keys(search_query)
    search_box.submit()

    # 검색 결과에서 첫 번째 이미지 클릭

    first_image = driver.find_element(By.XPATH,'//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    first_image.click()
    # 원본 이미지의 링크 추출
    driver.implicitly_wait(2) #안기다리면 안불러와짐
    original_image = driver.find_element(By.CSS_SELECTOR, 'img.r48jcc.pT0Scc.iPVvYb')
    image_link = original_image.get_attribute('src')
    print("원본 이미지 링크:", image_link)

    # WebDriver 종료
    driver.quit()
    return image_link

# def save_recommendations(image_link):
#     data = {
#         'reply': image_link
#     }
#     folder_path = './gptrecommendimg'
#     file_path = os.path.join(folder_path, 'gpt.json')
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     with open(file_path, 'w') as f:
#         json.dump(data, f)

        
def perform_crawling(gender, temperature, weather):
    search_query = f"I am a {gender}. Today's weather is {temperature}°C {weather}. Please recommend the top Clothing type with color and material and the bottom Clothing type with color and material according to the above situation. The answer is in the form of 'gender:[],top:[], bottom:[]' without any addition."

    reply = get_chatgpt_msg(search_query)
#reply하는형식은은 "gender:male, top:linen shirt, white, cotton, bottom:khaki shorts, beige, cotton" 이렇게 구글이미지 홈페이지에 검색하게된다.

    recommendations = extract_recommendations(reply)
    #검색형태 수정하는버전
    # recommendations = extract_recommendations(reply+'전신샷')
    # save_recommendations(recommendations)

    return {
        'reply': recommendations
    }