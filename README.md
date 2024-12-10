# crawling_task

## 📖 프로젝트 설명

**crawling_task**는 Selenium을 사용하여 Bottega Veneta 웹사이트에서 상품 정보를 크롤링하고, 데이터를 정리하여 Excel 파일로 저장하는 프로젝트입니다. 이 스크립트는 Python 기반으로 작성되었으며, 크롬 드라이버를 통해 웹 브라우저를 자동화합니다.

---

## 🚀 기능

1. **상품 정보 크롤링**:

   - 상품명
   - 가격
   - 상품 링크
   - 이미지 URL

2. **주요 라이브러리**:

   - selenium: 웹 브라우저를 자동화하여 데이터 크롤링
   - pandas: 데이터를 정리하고 Excel 파일로 저장
   - fastapi: API 서버를 구성

3. **결과 저장**:

   - 크롤링한 데이터를 정리하여 `bottega_products.xlsx`로 저장

4. **동적 로딩 처리**:

   - 무한 스크롤을 자동화하여 동적으로 로드되는 상품 정보 추출

5. **병렬 처리**:
   - 크롤링 속도를 높이기 위해 병렬 처리 활용

---

## 📦 설치 및 실행

### 1. Python 설치

- Python 3.8 이상이 필요합니다.
- [Python 다운로드](https://www.python.org/downloads)

### 2. 가상 환경 설정

가상 환경을 생성하고 활성화하세요.

#### macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 크롬 드라이버 설치

- 나의 브라우저에 맞는 크롬 드라이버 버전이 필요합니다.
- [크롬 드라이버 다운로드](https://developer.chrome.com/docs/chromedriver/downloads?hl=ko)
- 다운로드 받은 크롬 브라우저를 프로젝트 루트 디텍토리에 저장해주세요.

### 5. 서버 실행

프로젝트 루트 디렉토리에서 다음 명령어를 실행하세요.

```bash
uvicorn app.main:app --reload
```

### 6. 크롤링 API 호출

- 브라우저를 열고 http://localhost:8000/docs로 이동합니다.
- Swagger UI가 로드되면, /crawl_products 엔드포인트를 찾습니다:
- 경로: http://localhost:8000/docs#/default/crawl_endpoint_crawl_products_get
- Try it out 버튼을 클릭합니다.
- Execute 버튼을 클릭하여 크롤링을 실행합니다.

### 7. 크롤링 결과 파일

크롤링 결과가 프로젝트 루트 디렉토리에 bottega_products.xlsx 파일명으로 저장됩니다.
