from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from .crawler import crawl_products

app = FastAPI()

@app.get("/crawl-products")
def crawl_endpoint():
    """
    해당 엔드포인트 호출 시 크롤링을 수행하고 결과 엑셀 파일을 반환
    """
    excel_file_path = crawl_products()
    return FileResponse(path=excel_file_path, filename="bottega_products.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
