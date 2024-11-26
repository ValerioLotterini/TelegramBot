# Django REST Framework API - Telegram Bot


Questo progetto fornisce endpoint api per la registrazione, l'autenticazione e l'invio di un messaggio testo/immagine tramite telegram.
[Collezione Postman - API User Registration](https://www.postman.com/science-observer-42026254/telegrambot/collection/6w42u30/telegram-bot)

## Tecnologie utilizzate

- **Python 3.x**
- **Django 4.x**
- **Django REST Framework**

## Installazione

1. **Clona la repository**:
   ```bash
   git clone https://github.com/ValerioLotterini/TelegramBot
   cd TelegramBot
2. **Crea un ambiente virtuale:**
   ```bash
    python3 -m venv venv
    source venv/bin/activate   # Su Windows usa: venv\Scripts\activate
3. **Installa le dipendenze:**
   ```bash
    pip install -r requirements.txt
4. **Applica le migrazioni:**
   ```bash
    python3 manage.py migrate
5. **Configura file .env:**
   ```bash
    cp .env.example .env # Su Windows usa: copy .env.example .env
6. **Avvia il server di sviluppo:**
   ```bash
    python3 manage.py runserver 