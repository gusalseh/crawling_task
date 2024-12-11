import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor

# 터미널에 프로그레스 바를 출력하는 함수
def display_progress(current, total, bar_length=40):
    progress = current / total # 진행 비율 계산
    block = int(round(bar_length * progress)) # 진행 상태를 바 형태로 변환
    bar = f"[{'#' * block + '-' * (bar_length - block)}]" # 바 생성
    print(f"\r{bar} {current}/{total} products loaded", end="") # 터미널 출력

# 상품 데이터 추출 함수 (병렬 처리 대상)
def get_product_data(product, i):
    try:
        # h2 태그의 c-product__name 선택자로 상품명 추출
        product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
        product_name = product_name_elem.text.strip()

        # a태그의 c-product__link & c-product__focus 선택자로 상품 링크 URL 추출
        product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
        product_link = product_link_elem.get_attribute("href")

        # p태그의 c-price__value--current 선택자로 상품 가격 추출
        product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
        product_price = product_price_elem.text.strip()

        try:
            # swiper-slide-active 선택자로 이미지 URL 추출
            product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide.swiper-slide-active img")
            product_image_url = product_image_elem.get_attribute("data-src")
        except:
            try:
                # 상단 선택자가 없는 상품의 경우 예외 처리
                # c-product__carousel--slide 선택자를 기준으로 이미지 URL 추출
                product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide img")
                product_image_url = product_image_elem.get_attribute("data-src")
            except:
                # 이미지가 없을 경우 None 처리
                product_image_url = None

        # 추출한 데이터를 딕셔너리 형태로 반환
        return {
            '상품명': product_name,
            '가격': product_price,
            '상품 링크': product_link,
            '이미지 URL': product_image_url
        }
    except Exception as e:
        print(f"Error parsing product {i}: {e}")
        return None

# 크롤링 로직 함수
def crawl_products():
    chrome_options = Options()
    
    # Selenium 옵션 설정
    chrome_options.add_argument('--headless') # 브라우저 UI를 표시하지 않음
    chrome_options.add_argument('--no-sandbox') # 리눅스 호환성을 위한 설정
    chrome_options.add_argument('--disable-dev-shm-usage') # 공유 메모리 크기 제한 해제

    # 이미지 로딩 비활성화
    chrome_prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    # 크롬 드라이버 경로 설정 및 초기화
    driver_path = os.path.abspath("chromedriver") # 현재 디렉토리의 크롬 드라이버 경로
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options) # 드라이버 초기화

    # 크롤링 대상 URL 설정 및 접속
    url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags" # 크롤링 대상 페이지 설정
    driver.get(url) # 웹 페이지 열기
    time.sleep(5) # 초기 로딩 시간 대기


    # 페이지 상단 필터 컴포넌트에서 전체 상품 수 추출하여 max_products 변수 저장
    max_products = None
    try:
        # 상품 수가 표시된 HTML 요소에서 해당 텍스트 데이터의 숫자만 추출
        max_products_elem = driver.find_element(By.CSS_SELECTOR, "div.c-filters__count[data-bind='countProducts']")
        max_products_text = max_products_elem.text.strip()
        max_products = int(max_products_text.split()[0])
        print(f"Total products to load: {max_products}")
    except Exception as e:
        print("Error fetching max product count:", e)

    # 스크롤 액션 정의
    # 0.2초 간격으로 100px씩 스크롤하고, 더 이상 스크롤할 내용이 없을 때 멈춤
    scroll_script = """
    let scrollInterval = setInterval(() => {
        window.scrollBy(0, 100);
        if (document.documentElement.scrollHeight - window.scrollY <= window.innerHeight) {
            clearInterval(scrollInterval);
        }
    }, 200);
    """
    # 스크롤 액션 실행
    driver.execute_script(scroll_script)

    # 모든 상품이 로드될 때까지 대기
    while True:
        # article.c-product 선택자 기준으로 각 상품을 나타내는 HTML 요소를 동적으로 타겟팅
        products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
        display_progress(len(products), max_products) # 현재 진행 상태 출력
        if max_products and len(products) >= max_products: # 현재 로드된 상품 의 수와 총 상품 수를 비교하여 모든 상품이 로드되었는지 확인
            print("\nAll products loaded.")
            break
        time.sleep(7)

    # article.c-product 선택자 기준으로 모든 상품 리스트 추출하여 products 변수 저장
    products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
    print(f"Total products loaded: {len(products)}")

    # 병렬 처리로 상품 데이터 수집
    result = []
    with ThreadPoolExecutor(max_workers=8) as executor: # 8개의 스레드를 가진 스레드 풀 관리 객체 executor 지정
        # get_product_data 함수와 해당 함수의 매개변수(product-상품요소, i-상품번호)로 함수 작동을 하도록 하는 병렬 작업 생성
        # enumerate 메소드를 사용하여 각 상품과 인덱스 동시에 반환
        futures = [executor.submit(get_product_data, product, i) for i, product in enumerate(products, start=1)]
        for future in futures:
            data = future.result()
            if data:
                result.append(data)

    driver.quit()

    # 결과 데이터를 Pandas DataFrame으로 변환 및 저장
    df = pd.DataFrame(result)
    df.to_excel("bottega_products.xlsx", index=False)
    print("Excel file saved: bottega_products.xlsx")

    return "bottega_products.xlsx"
