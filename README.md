 
# 🤖 Анонімний Бот

Це Telegram-бот, що забезпечує **анонімний зв’язок між користувачами**. Кожен користувач може надсилати повідомлення іншим, не розкриваючи свою особу.
## ⚙️ Особливості

- Повністю анонімний
- Без використання бази даних — миттєвий відклик
- Шифрування ID через соль (Hashids)


## 🔧 Встановлення

1. Клонуйте репозиторій:
```bash
   git clone https://github.com/Krapka-or-To4ka/AnnonimTGbothttps://github.com/Krapka-or-To4ka/AnnonimTGbot
   cd AnnonimTGbot
```
2.Встановіть залежності:
```bash
pip install -r requirements.txt
```
Створіть .env файл у кореневій директорії з вмістом:
```env
KEY=your_secret_salt
TOKEN=your_telegram_bot_token
```
KEY використовується для шифрування/дешифрування ID користувачів (сіль)
# 🧱 Залежності
```

aiogram==3.20.0.post0 — Telegram бот-фреймворк

python-dotenv==1.1.1 — завантаження змінних середовища з .env

hashids==1.3.1 — обфускація ID користувачів

```