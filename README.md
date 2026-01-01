# Vodouš API (Webová část)
Webová aplikace pro učení slovíček cizího jazyka postavená pomocí **Streamlit**.  
Slouží jako frontend nad vlastním REST API (FastAPI), které zajišťuje logiku procvičování.

## Funkce
- Flashcard
-- Jednoduché hádání slovíčka


## Technologie
- Python 3.13+
- Streamlit
- FastAPI (backend API)

## Rychlý start

### Instalace
```bash
git clone <repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### .env
```
APP_BASE_URL - adresa webu
FAST_API_URL_BASE - adresa API služby
FAST_API_URL_RANDOM_WORD - adresa pro náhodné slovíčko ("/word/random/{id_seed}")
```

### Spuštění
```
streamlit run app.py
```
Poběží na adrese http://127.0.0.1:8501
