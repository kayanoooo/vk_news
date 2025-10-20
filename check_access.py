# check_sheets_access.py
import gspread
from google.oauth2.service_account import Credentials
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_sheets_access():
    """Проверка доступа к Google Sheets"""
    try:
        # Настройки
        GOOGLE_SHEET_ID = "13Mh3PmXGB0_cfXj8f_wiDdn186HRJ638NuNT4pCcTqA"
        
        # Авторизация
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
        client = gspread.authorize(creds)
        
        logger.info("✅ Успешная авторизация в Google API")
        
        # Пробуем открыть таблицу
        try:
            spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)
            logger.info(f"✅ Таблица найдена: {spreadsheet.title}")
        except gspread.SpreadsheetNotFound:
            logger.error("❌ Таблица не найдена. Проверьте GOOGLE_SHEET_ID")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка доступа к таблице: {e}")
            return False
        
        # Получаем список всех листов
        worksheets = spreadsheet.worksheets()
        logger.info("📋 Доступные листы в таблице:")
        for i, ws in enumerate(worksheets):
            logger.info(f"  {i+1}. '{ws.title}' (id: {ws.id})")
        
        # Пробуем найти лист "AI News Hub"
        target_sheet_name = "AI News Hub"
        try:
            worksheet = spreadsheet.worksheet(target_sheet_name)
            logger.info(f"✅ Лист '{target_sheet_name}' найден!")
            
            # Проверяем структуру данных
            records = worksheet.get_all_records()
            logger.info(f"📊 Найдено записей: {len(records)}")
            
            if records:
                logger.info("📝 Структура данных:")
                for key, value in records[0].items():
                    logger.info(f"  - {key}: {value}")
            else:
                logger.warning("⚠️ Лист пустой или нет данных")
                
            return True
            
        except gspread.WorksheetNotFound:
            logger.error(f"❌ Лист '{target_sheet_name}' не найден!")
            logger.info("Доступные листы:")
            for ws in worksheets:
                logger.info(f"  - '{ws.title}'")
            return False
            
    except FileNotFoundError:
        logger.error("❌ Файл credentials.json не найден")
        return False
    except Exception as e:
        logger.error(f"❌ Общая ошибка: {e}")
        return False

if __name__ == "__main__":
    check_sheets_access()