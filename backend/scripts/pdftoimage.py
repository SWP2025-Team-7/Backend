from pdf2image import convert_from_bytes
from PIL import ImageFilter, ImageEnhance
import io

async def pdf_bytes_to_png(pdf_bytes: bytes) -> bytes:
    # Конвертация первой страницы PDF → PIL Image с 300 DPI
    image = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1)
    page = image[0]

    # 2. Преобразование в градации серого
    gray = page.convert('L')

    # 3. Удаление шума (медианный фильтр)
    denoised = gray.filter(ImageFilter.MedianFilter(size=3))

    # 4. Усиление контраста
    enhancer = ImageEnhance.Contrast(denoised)
    enhanced = enhancer.enhance(2.0)

    # 5. Бинаризация (пороговая обработка)
    threshold = 128
    binary = enhanced.point(lambda p: 255 if p > threshold else 0, 'L')

    # Сохранение в PNG в буфер
    buffer = io.BytesIO()
    binary.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer.getvalue()
