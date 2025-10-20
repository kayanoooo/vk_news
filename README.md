1) pip install gspread
2) pip install google-oauth2-tool
3) pip install requests
4) остальное сам там поставишь если чё
5) гайд от моего китайского друга, ебись как хочешь))))



Настройка Google Sheets
   
1.1. Создание Google Cloud Project

  1. Перейдите на Google Cloud Console
  
  2. Создайте новый проект
  
  3. Включите Google Sheets API:

    APIs & Services → Library → поиск "Google Sheets API" → Enable

1.2. Создание Service Account

  1. APIs & Services → Credentials → Create Credentials → Service Account
  
  2. Заполните:

    Name: news-distributor

    Description: "For VK news distribution"

  3. Нажмите "Create and Continue"

  4. Роль: "Viewer" (или кастомная роль)

  5. Нажмите "Done"

1.3. Создание ключа доступа

  1. Найдите созданный service account в списке

  2. Нажмите на
     
    email → Keys → Add Key → Create New Key

  3. Выберите JSON формат

  4. Скачайте файл и сохраните как credentials.json в корне проекта (просто смени скачанный на тот, который в проекте)

1.4. Настройка Google Sheets таблицы

  1. Создайте таблицу с названием "AI News Hub"

  2. Структура колонок:

    | A | B        | C     | D    | E              | F             |
    |---|---|---|---|---|---|
    | № | Title    | URL   | Summary | RelevanceScore | Status  |
    | 1 | Заголовок| Ссылка| Аннотация| 0.85         | Processed |

  3. Дайте доступ service account:

    Поделитесь таблицей

    Email: your-service-account@project-id.iam.gserviceaccount.com

    Права: "Редактор"

  4. Получите Sheet ID из URL таблицы:

    https://docs.google.com/spreadsheets/d/ВАШ_SHEET_ID/edit#gid=0


Настройка VK группы
   
2.1. Получение ключа доступа группы

  1. Перейдите в управление вашей группой VK

  2. Управление → Настройки → Дополнительно → Работа с API

  3. Нажмите "Создать ключ"

  4. Выберите права:

    ✅ Управление записями на стене (wall)

    ✅ Доступ в любое время

  5. Скопируйте созданный ключ

2.2. Получение Group ID

  1. Откройте вашу группу VK

  2. Из URL скопируйте ID:

    https://vk.com/public123456 → ID = 123456

    https://vk.com/club123456 → ID = 123456

2.3. Важные настройки группы

  1. В настройках группы убедитесь, что:

    ✅ Стена: Открытая

    ✅ Возможность публикации: Открытая

    ❌ Комментарии перед публикацией: Выключено

    ✅ Разрешить доступ к API


