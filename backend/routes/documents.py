from fastapi import APIRouter, Body, HTTPException
from starlette.status import  HTTP_200_OK
from pydantic import BaseModel
from typing import Any, Dict
import httpx


from backend.scripts.pdftoimage import pdf_bytes_to_png

router = APIRouter(prefix="/documents")

# Pydantic-модель запроса от тг-бота, здесь описаны все поля и их типы. 
# Когда придет запрос, то FastAPI автоматически проверит, что в теле есть именно эти поля, нужного типа, и создаст объект payload этого класса.
class DocumentUploadRequest(BaseModel):
    userId: int
    file_in_bytes: str  # bytes, encoding=latin-1

# Pydantic-модель ответа вашему боту
class DocumentExtractResponse(BaseModel):
    extracted_data: Dict[str, Any]

@router.post("/upload",
             response_model=DocumentExtractResponse, # Благодаря этому FastAPI будет возвращать объект этого класса
             status_code=HTTP_200_OK)
# Body(..., embed=True)

# Body - говорит FastAPI взять данные из http запроса и передать их сюда(в данном случае в payload).

# ... означает что это будет обязательный параметр»; если тело пустое или невалидное, будет 422 Unprocessable Entity. 
# Если вместо ... вы указали бы какое-то значение по умолчанию (например, None или {}), то тело перестало бы быть строго обязательным.

# С embed=True FastAPI ждёт, что эти поля будут «запакованы» под ключом, совпадающим с именем параметра (payload), то есть:
#{
#  "payload": {
#    "userId": 123,
#    "file_in_bytes": "…"
#  }
#}
# Еще один уровень вложенности чтобы к примеру возвращать не отдельно userId и file_in_bytes, а вместе в payload

async def upload_document(payload: DocumentUploadRequest=Body(..., embed=True)):
    # Теперь к полям можно обращатсья как payload.userId и payload.file_in_bytes
    
    pdf_bytes = payload.file_in_bytes.encode("latin-1") # Делаем из байтов обратно pdf файл
    
    png_bytes = await pdf_bytes_to_png(pdf_bytes) # Конвертируем pdf в png с "хорошим качеством"
    
    try:
        # Открываем асинхронный HTTP-клиент с таймаутом 30 секунд
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Готовим тело multipart-запроса: ключ "document" как в ноде Webhook n8n,
            # значение — кортеж (имя файла, байты, MIME-тип)
            files = {"document": 
                        ("document.png", png_bytes, "image/png")}
            
            # Создаем POST-запрос на https://bot.techaas.tech/webhook-test/data-extract, передаем то, что подготовили выше
            resp = await client.post("https://bot.techaas.tech/webhook-test/data-extract", files=files)
            
            # Метод raise_for_status() проверяет этот код:
            # - Если код в диапазоне 200–299 (успешные ответы), он ничего не делает и позволяет дальше работать с resp.
            # Если код вне этого диапазона (например, 400 Bad Request, 404 Not Found, 500 Internal Server Error и т. д.),
            # он выбрасывает исключение httpx.HTTPStatusError.
            resp.raise_for_status()
            
            # Парсим то, что пришло от n8n в JSON
            try:
                extracted = resp.json()
            except ValueError as e:
                # неверный JSON от n8n
                raise HTTPException(
                status_code=502,
                detail=f"Invalid JSON in response from extraction service: {e}"
            )
            
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error while executing n8n: {e}")

    # Потом преобразуется в объект класса DocumentExtractResponse
    return {"extracted_data": extracted}
    
    

