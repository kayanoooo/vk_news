# debug_filter.py
import gspread
from google.oauth2.service_account import Credentials
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_filtering():
    """Отладка фильтрации записей"""
    
    # Настройки
    GOOGLE_SHEET_ID = "13Mh3PmXGB0_cfXj8f_wiDdn186HRJ638NuNT4pCcTqA"
    
    try:
        # Авторизация
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)
        
        # Находим лист
        sheet = None
        for sheet_name in ["AI News Hub", "News", "Лист1", "Sheet1"]:
            try:
                sheet = spreadsheet.worksheet(sheet_name)
                logger.info(f"✅ Используем лист: '{sheet_name}'")
                break
            except:
                continue
        
        if not sheet:
            available_sheets = [ws.title for ws in spreadsheet.worksheets()]
            logger.error(f"❌ Лист не найден. Доступные: {available_sheets}")
            return
        
        # Получаем все записи
        records = sheet.get_all_records()
        logger.info(f"📊 Всего записей в таблице: {len(records)}")
        
        if not records:
            logger.info("ℹ️ Таблица пустая")
            return
        
        # Показываем структуру первой записи
        logger.info("📋 Структура данных (первая запись):")
        for key, value in records[0].items():
            logger.info(f"   '{key}': '{value}' (тип: {type(value).__name__})")
        
        # Анализируем все записи
        logger.info("\n🔍 Анализ всех записей:")
        processed_count = 0
        skipped_count = 0
        
        for i, row in enumerate(records, start=2):
            status = row.get("Status", "")
            relevance_score = row.get("RelevanceScore", 0)
            title = row.get("Title", "").strip()
            
            logger.info(f"\n--- Строка {i} ---")
            logger.info(f"Title: '{title}'")
            logger.info(f"Status: '{status}' (ожидается: 'Processed')")
            logger.info(f"RelevanceScore: '{relevance_score}' (тип: {type(relevance_score).__name__})")
            
            # Проверяем условия фильтрации
            status_ok = status == "Processed"
            
            try:
                relevance = float(relevance_score)
                relevance_ok = relevance > 0.7
            except (ValueError, TypeError) as e:
                relevance = 0.0
                relevance_ok = False
                logger.info(f"RelevanceScore конвертация: ошибка ({e})")
            
            logger.info(f"Status OK: {status_ok}")
            logger.info(f"RelevanceScore OK: {relevance_ok} ({relevance} > 0.7 = {relevance_ok})")
            
            if status_ok and relevance_ok:
                processed_count += 1
                logger.info(f"✅ Будет обработана!")
            else:
                skipped_count += 1
                logger.info(f"❌ Пропущена")
        
        logger.info(f"\n📈 ИТОГО:")
        logger.info(f"Всего записей: {len(records)}")
        logger.info(f"Будет обработано: {processed_count}")
        logger.info(f"Пропущено: {skipped_count}")
        
        # Показываем примеры пропущенных записей
        if processed_count == 0 and len(records) > 0:
            logger.info(f"\n🔎 Примеры пропущенных записей:")
            for i, row in enumerate(records[:5], start=2):  # первые 5 записей
                status = row.get("Status", "")
                relevance_score = row.get("RelevanceScore", 0)
                
                status_reason = "Status не 'Processed'" if status != "Processed" else ""
                
                try:
                    relevance = float(relevance_score)
                    relevance_reason = "RelevanceScore <= 0.7" if relevance <= 0.7 else ""
                except:
                    relevance_reason = "RelevanceScore не число"
                
                reasons = [r for r in [status_reason, relevance_reason] if r]
                reason_text = ", ".join(reasons) if reasons else "неизвестно"
                
                logger.info(f"Строка {i}: '{row.get('Title', '')}' - {reason_text}")
                
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    debug_filtering()