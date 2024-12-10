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
    progress = current / total
    block = int(round(bar_length * progress))
    bar = f"[{'#' * block + '-' * (bar_length - block)}]"
    print(f"\r{bar} {current}/{total} products loaded", end="")

# 상품 데이터 추출 함수 (병렬 처리 대상)
def get_product_data(product, i):
    try:
        # 상품명
        product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
        product_name = product_name_elem.text.strip()

        # 상품 링크
        product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
        product_link = product_link_elem.get_attribute("href")

        # 가격
        product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
        product_price = product_price_elem.text.strip()

        # 이미지 URL
        try:
            # 첫 번째: swiper-slide-active를 기준으로 이미지 URL 추출
            product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide.swiper-slide-active img")
            product_image_url = product_image_elem.get_attribute("data-src")
        except:
            try:
                # 두 번째: lazyloaded 클래스를 기준으로 이미지 URL 추출
                product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide img")
                product_image_url = product_image_elem.get_attribute("data-src")
            except:
                # 이미지가 없을 경우 None 처리
                product_image_url = None

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
    
    # Headless 모드로 브라우저 실행
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 이미지 로딩 비활성화
    chrome_prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    driver_path = os.path.abspath("chromedriver")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 크롤링 대상 페이지 설정 + 초기 로딩 대기
    url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
    driver.get(url)
    time.sleep(5)

    # 페이지 상단 필터 컴포넌트에서 전체 상품 수 추출
    max_products = None
    try:
        max_products_elem = driver.find_element(By.CSS_SELECTOR, "div.c-filters__count[data-bind='countProducts']")
        max_products_text = max_products_elem.text.strip()
        max_products = int(max_products_text.split()[0])
        print(f"Total products to load: {max_products}")
    except Exception as e:
        print("Error fetching max product count:", e)

    # 스크롤 액션 실행
    scroll_script = """
    let scrollInterval = setInterval(() => {
        window.scrollBy(0, 100);
        if (document.documentElement.scrollHeight - window.scrollY <= window.innerHeight) {
            clearInterval(scrollInterval);
        }
    }, 200);
    """
    driver.execute_script(scroll_script)

    # 동적 대기
    while True:
        products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
        display_progress(len(products), max_products)
        if max_products and len(products) >= max_products:
            print("\nAll products loaded.")
            break
        time.sleep(7)

    # 모든 상품 리스트 추출
    products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
    print(f"Total products loaded: {len(products)}")

    # 병렬 처리로 상품 데이터 수집
    result = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(get_product_data, product, i) for i, product in enumerate(products, start=1)]
        for future in futures:
            data = future.result()
            if data:
                result.append(data)

    driver.quit()

    # 데이터 저장
    df = pd.DataFrame(result)
    df.to_excel("bottega_products.xlsx", index=False)
    print("Excel file saved: bottega_products.xlsx")

    return "bottega_products.xlsx"
