# 1안
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     # 크롬 옵션 설정 (headless 모드 필요 시 주석 해제)
#     chrome_options = Options()
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    
#     # 드라이버 실행 (chromedriver 경로 필요)
#     # driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
#     service = Service('./chromedriver')
#     driver = webdriver.Chrome(service=service, options=chrome_options)
    
#     # 타겟 URL
#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
    
#     time.sleep(3)  # 초기 로딩 대기
    
#     # 페이지 끝까지 스크롤하여 모든 상품 정보 로딩
#     # 마지막 스크롤 위치 기록
#     last_height = driver.execute_script("return document.body.scrollHeight")
    
#     while True:
#         # 페이지 맨 아래로 스크롤
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(3)  # 로딩 대기
        
#         # 새로운 스크롤 높이 확인
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             # 더 이상 새로운 컨텐츠가 없으면 스크롤 중지
#             break
#         last_height = new_height
    
#     # 상품 리스트 가져오기
#     # 상품 요소: 사이트 구조에 따라 변경 필요.
#     # 본 예시는 class명 'product-grid-card'를 기준으로 삼음
#     products = driver.find_elements(By.CLASS_NAME, "product-grid-card")
    
#     result = []
#     for product in products:
#         try:
#             # 상품명, 링크, 가격, 이미지 정보 추출
#             # HTML 구조에 따라 By.XPATH나 By.CSS_SELECTOR 수정 필요
#             product_link_elem = product.find_element(By.CSS_SELECTOR, 'a.product-grid-card__link')
#             product_link = product_link_elem.get_attribute('href')
            
#             product_name_elem = product.find_element(By.CSS_SELECTOR, '.product-grid-card__title')
#             product_name = product_name_elem.text.strip()
            
#             product_price_elem = product.find_element(By.CSS_SELECTOR, '.product-grid-card__price')
#             product_price = product_price_elem.text.strip()
            
#             product_image_elem = product.find_element(By.CSS_SELECTOR, '.product-grid-card__image img')
#             product_image_url = product_image_elem.get_attribute('src')
            
#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             # 개별 상품 파싱 실패시 무시 혹은 로그 기록
#             print("Error parsing product:", e)

#     driver.quit()
    
#     # DataFrame으로 만들고 엑셀 저장
#     df = pd.DataFrame(result)
#     df.to_excel("products.xlsx", index=False)
    
#     return "products.xlsx"

# 2안
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     chrome_options = Options()
#     # chrome_options.add_argument('--headless')  # 필요에 따라 주석 해제
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    
#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)  # 초기 로딩 대기

#     # 무한 스크롤 진행
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(3)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

#     # 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print("Found", len(products), "products")

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL
#             # 실제 이미지 URL은 data-src 속성에 있음
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__imagecontainer img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print("Error parsing product:", e)

#     driver.quit()

#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("products.xlsx", index=False)
#     print("Excel file saved: products.xlsx")

#     return "products.xlsx"

# 3안
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     chrome_options = Options()
#     # 필요시 headless 모드
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    
#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)  # 초기 로딩 대기

#     # 무한 스크롤 구현: 상품 개수 증가를 기준으로 스크롤 계속
#     scroll_count = 0
#     old_count = 0
#     while True:
#         products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#         new_count = len(products)
#         print(f"Scroll {scroll_count}: Found {new_count} products so far.")

#         # 더 많은 상품이 로드되었으면 스크롤 지속
#         if new_count > old_count:
#             old_count = new_count
#             scroll_count += 1
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(20)  # 로딩 대기
#         else:
#             # 상품 개수가 늘어나지 않으면 모든 상품 로딩 완료로 판단
#             print("No new products loaded. Stopping scroll.")
#             break

#     # 스크롤 완료 후 최종 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print("Final product count:", len(products))

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL (data-src 속성 사용)
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__imagecontainer img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print("Error parsing product:", e)

#     driver.quit()

#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("products.xlsx", index=False)
#     print("Excel file saved: products.xlsx")

#     return "products.xlsx"

# 4안
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     chrome_options = Options()
#     # 필요시 headless 모드
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    
#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)  # 초기 로딩 대기

#     # 무한 스크롤 구현: 상품 개수 증가를 기준으로 스크롤 계속
#     scroll_count = 0
#     old_count = 0
#     max_scrolls = 100  # 최대 스크롤 횟수 설정
#     while scroll_count < max_scrolls:
#         products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#         new_count = len(products)
#         print(f"Scroll {scroll_count}: Found {new_count} products so far.")

#         # 더 많은 상품이 로드되었으면 스크롤 지속
#         if new_count > old_count:
#             old_count = new_count
#             scroll_count += 1
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(100)  # 로딩 대기 시간 조정
#         else:
#             # 상품 개수가 늘어나지 않으면 모든 상품 로딩 완료로 판단
#             print("No new products loaded. Stopping scroll.")
#             break

#     # 스크롤 완료 후 최종 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print("Final product count:", len(products))

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL (data-src 속성 사용)
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__imagecontainer img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print("Error parsing product:", e)

#     driver.quit()

#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("products.xlsx", index=False)
#     print("Excel file saved: products.xlsx")

#     return "products.xlsx"

# 5안
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     chrome_options = Options()
#     # 필요시 headless 모드
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    
#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(100)  # 초기 로딩 대기

#     # 무한 스크롤 구현: 일정 픽셀만큼 반복적으로 스크롤
#     scroll_pause_time = 3  # 스크롤 후 대기 시간
#     scroll_increment = 500  # 한 번에 스크롤할 픽셀 수
#     max_scrolls = 200  # 최대 스크롤 횟수
#     scroll_count = 0

#     while scroll_count < max_scrolls:
#         # 현재 위치에서 일정 픽셀만큼 아래로 스크롤
#         driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
#         time.sleep(scroll_pause_time)  # 로딩 대기
#         scroll_count += 1

#         # 새로운 상품이 로드되었는지 확인
#         products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#         print(f"Scroll {scroll_count}: Found {len(products)} products so far.")

#         # 더 이상 새로운 상품이 로드되지 않으면 중지
#         if scroll_count > 1 and len(products) == old_count:
#             print("No new products loaded. Stopping scroll.")
#             break

#         old_count = len(products)

#     # 스크롤 완료 후 최종 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print("Final product count:", len(products))

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL (data-src 속성 사용)
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__imagecontainer img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print("Error parsing product:", e)

#     driver.quit()

#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("products.xlsx", index=False)
#     print("Excel file saved: products.xlsx")

#     return "products.xlsx"

# 6안
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from threading import Thread

# def scroll_repeatedly(driver, scroll_increment, scroll_pause_time, max_scrolls, stop_flag):
#     """지정된 간격으로 스크롤을 반복하는 함수."""
#     scroll_count = 0
#     while scroll_count < max_scrolls and not stop_flag['stop']:
#         driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
#         print(f"Scrolled {scroll_count + 1} times.")
#         time.sleep(scroll_pause_time)
#         scroll_count += 1

# def crawl_products():
#     chrome_options = Options()
#     # 필요시 headless 모드
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')

#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)  # 초기 로딩 대기

#     scroll_pause_time = 1  # 스크롤 후 대기 시간
#     scroll_increment = 200  # 한 번에 스크롤할 픽셀 수
#     max_scrolls = 1000  # 최대 스크롤 횟수
#     stop_flag = {'stop': False}  # 스크롤 중지를 위한 플래그

#     # 스크롤을 별도 스레드에서 실행
#     scroll_thread = Thread(target=scroll_repeatedly, args=(driver, scroll_increment, scroll_pause_time, max_scrolls, stop_flag))
#     scroll_thread.start()

#     result = []
#     old_count = 0

#     while scroll_thread.is_alive():
#         # 새로운 상품 로드 상태 확인
#         products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#         new_count = len(products)
#         print(f"Currently loaded products: {new_count}")

#         # 더 이상 새로운 상품이 로드되지 않을 경우 스크롤 중지
#         if new_count == old_count:
#             stop_flag['stop'] = True
#             break
#         old_count = new_count
#         time.sleep(3)  # 대기하며 상태 확인

#     # 스크롤 완료 후 최종 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print("Final product count:", len(products))

#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL (data-src 속성 사용)
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__imagecontainer img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print("Error parsing product:", e)

#     driver.quit()

#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("products.xlsx", index=False)
#     print("Excel file saved: products.xlsx")

#     return "products.xlsx"

# 7안 - 모두 정상 작동 BUT 스크롤 완료 대기시간이 너무 김
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     chrome_options = Options()
#     # 필요시 headless 모드
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')

#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     # 크롤링 대상 페이지 설정 + 초기 로딩 대기
#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)

#     # JavaScript로 setInterval을 실행하여 스크롤 액션 실행 + 스크롤 완료를 기다리기 위해 충분히 대기
#     scroll_script = """
#     let scrollInterval = setInterval(() => {
#         window.scrollBy(0, 100);
#         if (document.documentElement.scrollHeight - window.scrollY <= window.innerHeight) {
#             clearInterval(scrollInterval);
#         }
#     }, 200);
#     """
#     driver.execute_script(scroll_script)
#     time.sleep(1000)

#     # 모든 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print(f"Total products loaded: {len(products)}")

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL
#             # product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide img")
#             # product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide:nth-child(1) img")
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide.swiper-slide-active img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print("Error parsing product:", e)

#     driver.quit()

#     # 타겟 페이지 상품 크롤링 결과 Excel 저장
#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("bottega_products.xlsx", index=False)
#     print("Excel file saved: bottega_products.xlsx")

#     return "bottega_products.xlsx"

# 8안 - 크롤링 정상 작동하나 소요시간 오래 걸림
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def crawl_products():
#     chrome_options = Options()
#     # 필요시 headless 모드
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')

#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     # 크롤링 대상 페이지 설정 + 초기 로딩 대기
#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)

#     # 전체 상품 수 추출
#     max_products = None
#     try:
#         max_products_elem = driver.find_element(By.CSS_SELECTOR, "div.c-filters__count[data-bind='countProducts']")
#         max_products_text = max_products_elem.text.strip()
#         max_products = int(max_products_text.split()[0])  # "546 제품"에서 숫자 546 추출
#         print(f"Maximum products to load: {max_products}")
#     except Exception as e:
#         print("Error fetching max product count:", e)

#     # JavaScript로 setInterval을 실행하여 스크롤 액션 실행
#     scroll_script = """
#     let scrollInterval = setInterval(() => {
#         window.scrollBy(0, 100);
#         if (document.documentElement.scrollHeight - window.scrollY <= window.innerHeight) {
#             clearInterval(scrollInterval);
#         }
#     }, 200);
#     """
#     driver.execute_script(scroll_script)

#     # 조건부 대기: 로드된 상품 수가 최대 상품 수에 도달할 때까지 대기
#     while True:
#         products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#         print(f"Currently loaded products: {len(products)}")
#         if max_products and len(products) >= max_products:
#             print("All products loaded.")
#             break
#         time.sleep(2)

#     # 모든 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print(f"Total products loaded: {len(products)}")

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL
#             product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide.swiper-slide-active img")
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print(f"Error parsing product {i}: {e}")

#     driver.quit()

#     # 타겟 페이지 상품 크롤링 결과 Excel 저장
#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("bottega_products.xlsx", index=False)
#     print("Excel file saved: bottega_products.xlsx")

#     return "bottega_products.xlsx"

# 9안 - 3분 8초, 5분 15초, 9분 40초
# import time
# import os
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# # 터미널에 프로그레스 바를 출력하는 함수
# def display_progress(current, total, bar_length=40):
#     progress = current / total
#     block = int(round(bar_length * progress))
#     bar = f"[{'#' * block + '-' * (bar_length - block)}]"
#     print(f"\r{bar} {current}/{total} products loaded", end="")

# # 크롤링 로직 함수
# def crawl_products():
#     chrome_options = Options()
    
#     # 4번. Headless 모드로 브라우저 실행 (UI 렌더링 제거로 속도 향상)
#     chrome_options.add_argument('--headless')  
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')

#     # 5번. 이미지 로딩 비활성화 (네트워크 대역폭 절약 및 로딩 속도 향상)
#     chrome_prefs = {"profile.managed_default_content_settings.images": 2}
#     chrome_options.add_experimental_option("prefs", chrome_prefs)

#     driver_path = os.path.abspath("chromedriver")
#     service = Service(driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     # 크롤링 대상 페이지 설정 + 초기 로딩 대기
#     url = "https://www.bottegaveneta.com/ko-kr/search?cgid=women-bags"
#     driver.get(url)
#     time.sleep(5)

#     # 페이지 상단 필터 컴포넌트에서 전체 상품 수 추출
#     max_products = None
#     try:
#         max_products_elem = driver.find_element(By.CSS_SELECTOR, "div.c-filters__count[data-bind='countProducts']")
#         max_products_text = max_products_elem.text.strip()
#         max_products = int(max_products_text.split()[0])  # "546 제품"에서 숫자 546 추출
#         print(f"Total products to load: {max_products}")
#     except Exception as e:
#         print("Error fetching max product count:", e)

#     # 3번. 스크롤 단위를 크게 설정하여 반복 횟수 줄이기
#     scroll_script = """
#     let scrollInterval = setInterval(() => {
#         window.scrollBy(0, 100);
#         if (document.documentElement.scrollHeight - window.scrollY <= window.innerHeight) {
#             clearInterval(scrollInterval);
#         }
#     }, 200);
#     """
#     driver.execute_script(scroll_script)

#     # 1번. 조건부 대기: 상품 로드 완료까지 동적 대기 (불필요한 고정 대기 시간 제거)
#     while True:
#         products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#         # print(f"Currently loaded products: {len(products)}")
#         display_progress(len(products), max_products)
#         if max_products and len(products) >= max_products:
#             print("All products loaded.")
#             break
#         time.sleep(7)  # 대기 간격 조정

#     # 모든 상품 리스트 추출
#     products = driver.find_elements(By.CSS_SELECTOR, "article.c-product")
#     print(f"Total products loaded: {len(products)}")

#     result = []
#     for i, product in enumerate(products, start=1):
#         print(f"---- Product {i} ----")
#         try:
#             # 상품명
#             product_name_elem = product.find_element(By.CSS_SELECTOR, "h2.c-product__name")
#             product_name = product_name_elem.text.strip()
#             print("Product Name:", product_name)

#             # 상품 링크
#             product_link_elem = product.find_element(By.CSS_SELECTOR, "a.c-product__link.c-product__focus")
#             product_link = product_link_elem.get_attribute("href")
#             print("Product Link:", product_link)

#             # 가격
#             product_price_elem = product.find_element(By.CSS_SELECTOR, "p.c-price__value--current")
#             product_price = product_price_elem.text.strip()
#             print("Product Price:", product_price)

#             # 이미지 URL
#             # product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide.swiper-slide-active img")
#             try:
#                 # 첫 번째: swiper-slide-active를 기준으로 이미지 URL 추출
#                 product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide.swiper-slide-active img")
#                 product_image_url = product_image_elem.get_attribute("data-src")
#             except:
#                 try:
#                     # 두 번째: lazyloaded 클래스를 기준으로 이미지 URL 추출
#                     # product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__image.lazyloaded")
#                     product_image_elem = product.find_element(By.CSS_SELECTOR, ".c-product__carousel--slide img")
#                     product_image_url = product_image_elem.get_attribute("data-src")
#                 except:
#                     product_image_url = None  # 이미지가 없을 경우 None 처리
#             product_image_url = product_image_elem.get_attribute("data-src")
#             print("Product Image URL:", product_image_url)

#             result.append({
#                 '상품명': product_name,
#                 '가격': product_price,
#                 '상품 링크': product_link,
#                 '이미지 URL': product_image_url
#             })
#         except Exception as e:
#             print(f"Error parsing product {i}: {e}")

#     driver.quit()

#     # 타겟 페이지 상품 크롤링 결과 Excel 저장
#     df = pd.DataFrame(result)
#     print("DataFrame preview:\n", df.head())
#     df.to_excel("bottega_products.xlsx", index=False)
#     print("Excel file saved: bottega_products.xlsx")

#     return "bottega_products.xlsx"

# 10안
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
                product_image_url = None  # 이미지가 없을 경우 None 처리

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
        max_products = int(max_products_text.split()[0])  # "546 제품"에서 숫자 546 추출
        print(f"Total products to load: {max_products}")
    except Exception as e:
        print("Error fetching max product count:", e)

    # 스크롤 실행
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
    with ThreadPoolExecutor(max_workers=8) as executor:  # 최대 8개의 스레드 사용
        futures = [executor.submit(get_product_data, product, i) for i, product in enumerate(products, start=1)]
        for future in futures:
            data = future.result()
            if data:
                result.append(data)

    driver.quit()

    # 데이터 저장
    df = pd.DataFrame(result)
    print("DataFrame preview:\n", df.head())
    df.to_excel("bottega_products.xlsx", index=False)
    print("Excel file saved: bottega_products.xlsx")

    return "bottega_products.xlsx"
