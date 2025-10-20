# vk_news_publisher_fixed_v2.py
import gspread
from google.oauth2.service_account import Credentials
import requests
import time
import logging
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vk_publisher.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VKNewsPublisher:
    def __init__(self):
        self.VK_GROUP_ID = "-свой вкгруппа айди, в начале всегда минус"
        self.VK_GROUP_TOKEN = "свой вкгруппа токен"
        self.GOOGLE_SHEET_ID = "свой гуглтаблицы айди"
        
        self.sheet = self._init_google_sheets()
        
    def _init_google_sheets(self):
        """Инициализация Google Sheets"""
        try:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_key(self.GOOGLE_SHEET_ID)
            
            # Пробуем найти лист
            for sheet_name in ["AI News Hub", "News", "Лист1", "Sheet1"]:
                try:
                    return spreadsheet.worksheet(sheet_name)
                except:
                    continue
            
            available_sheets = [ws.title for ws in spreadsheet.worksheets()]
            raise Exception(f"Доступные листы: {available_sheets}")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации Google Sheets: {e}")
            raise

    def publish_to_vk(self, post_text: str) -> Dict[str, Any]:
        """Публикация поста в VK с улучшенной обработкой"""
        try:
            # Вариант 1: Стандартная публикация
            url = "https://api.vk.com/method/wall.post"
            params = {
                "owner_id": self.VK_GROUP_ID,
                "from_group": 1,
                "message": post_text,
                "access_token": self.VK_GROUP_TOKEN,
                "v": "5.131"
            }
            
            response = requests.post(url, params=params, timeout=30)
            data = response.json()
            
            if "response" in data:
                post_id = data["response"]["post_id"]
                logger.info(f"✅ Пост опубликован! ID: {post_id}")
                
                # Проверяем, что пост действительно на стене
                self.verify_post_on_wall(post_id)
                return {"success": True, "post_id": post_id}
                
            else:
                error = data.get("error", {})
                error_code = error.get("error_code")
                error_msg = error.get("error_msg", "Unknown error")
                
                logger.warning(f"⚠️ Ошибка публикации: {error_msg} (код: {error_code})")
                
                # Обработка специфических ошибок
                if error_code == 214:  # Доступ к добавлению записи запрещен
                    logger.info("🔄 Пробуем альтернативный метод публикации...")
                    return self.publish_alternative_method(post_text)
                else:
                    return {"success": False, "error": error_msg}
                    
        except Exception as e:
            logger.error(f"❌ Ошибка при публикации в VK: {e}")
            return {"success": False, "error": str(e)}

    def publish_alternative_method(self, post_text: str) -> Dict[str, Any]:
        """Альтернативный метод публикации"""
        try:
            # Иногда помогает публикация без from_group
            url = "https://api.vk.com/method/wall.post"
            params = {
                "owner_id": self.VK_GROUP_ID,
                "message": post_text,
                "access_token": self.VK_GROUP_TOKEN,
                "v": "5.131"
            }
            
            response = requests.post(url, params=params, timeout=30)
            data = response.json()
            
            if "response" in data:
                post_id = data["response"]["post_id"]
                logger.info(f"✅ Пост опубликован (альтернативный метод)! ID: {post_id}")
                return {"success": True, "post_id": post_id}
            else:
                return {"success": False, "error": data.get("error", {}).get("error_msg", "Unknown error")}
                
        except Exception as e:
            logger.error(f"❌ Ошибка альтернативного метода: {e}")
            return {"success": False, "error": str(e)}

    def verify_post_on_wall(self, post_id: int):
        """Проверяет, что пост действительно появился на стене"""
        try:
            time.sleep(2)  # Даем время на публикацию
            
            url = "https://api.vk.com/method/wall.getById"
            params = {
                "posts": f"{self.VK_GROUP_ID}_{post_id}",
                "access_token": self.VK_GROUP_TOKEN,
                "v": "5.131"
            }
            
            response = requests.post(url, params=params, timeout=30)
            data = response.json()
            
            if "response" in data and len(data["response"]) > 0:
                post = data["response"][0]
                logger.info(f"🔍 Пост проверен: ID {post_id}, текст: {post.get('text', '')[:50]}...")
            else:
                logger.warning(f"⚠️ Пост {post_id} не найден при проверке")
                
        except Exception as e:
            logger.warning(f"⚠️ Не удалось проверить пост {post_id}: {e}")

    def format_post(self, title: str, summary: str, url: str) -> str:
        """Форматирование поста"""
        post_text = f"📰 {title}\n\n{summary}\n\n🔗 Источник: {url}\n\n#AI #Новости #Технологии"
        
        if len(post_text) > 4000:
            post_text = post_text[:3990] + "..."
            
        return post_text

    def find_status_column_index(self, headers: list) -> int:
        """Находит индекс колонки Status"""
        for col_name in ["Status", "Статус", "status"]:
            try:
                return headers.index(col_name) + 1
            except ValueError:
                continue
        raise ValueError(f"Колонка 'Status' не найдена. Доступные: {headers}")

    def update_status(self, row_index: int, status: str = "Published"):
        """Обновляет статус статьи"""
        try:
            headers = self.sheet.row_values(1)
            status_col = self.find_status_column_index(headers)
            self.sheet.update_cell(row_index, status_col, status)
            logger.info(f"✅ Статус обновлен для строки {row_index}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка обновления статуса: {e}")
            return False

    def process_news(self):
        """Основной метод обработки"""
        try:
            logger.info("=== Начало обработки новостей ===")
            
            records = self.sheet.get_all_records()
            logger.info(f"📊 Загружено записей: {len(records)}")
            
            processed_count = 0
            success_count = 0
            
            for i, row in enumerate(records, start=2):
                try:
                    status = row.get("Status", "")
                    relevance_score = row.get("RelevanceScore", 0)
                    
                    if status != "Processed":
                        continue
                    
                    try:
                        relevance = float(relevance_score)
                    except (ValueError, TypeError):
                        relevance = 0.0
                    
                    if relevance <= 0.7:
                        continue
                    
                    processed_count += 1
                    
                    title = row.get("Title", "").strip()
                    summary = row.get("Summary", "").strip()
                    url = row.get("URL", "").strip()
                    
                    if not title or not url:
                        continue
                    
                    logger.info(f"📝 Обработка [{processed_count}]: {title}")
                    
                    post_text = self.format_post(title, summary, url)
                    result = self.publish_to_vk(post_text)
                    
                    if result["success"]:
                        self.update_status(i)
                        success_count += 1
                    
                    time.sleep(2)  # Увеличиваем паузу между постами
                    
                except Exception as e:
                    logger.error(f"❌ Ошибка обработки строки {i}: {e}")
                    continue
            
            logger.info("=== Обработка завершена ===")
            logger.info(f"📈 Обработано: {processed_count}")
            logger.info(f"✅ Успешно: {success_count}")
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}")
            raise

def main():
    try:
        publisher = VKNewsPublisher()
        publisher.process_news()
    except Exception as e:
        logger.error(f"❌ Не удалось запустить публикатор: {e}")
        exit(1)

if __name__ == "__main__":

    main()
