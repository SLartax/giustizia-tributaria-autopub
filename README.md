# Giustizia Tributaria AutoPub

Sistema automatizzato per prelevare, selezionare e commentare sentenze della giustizia tributaria italiana, con pubblicazione automatica su WordPress.

## 📌 Funzionalità

1. **Scraping automatico** dalla [Banca Dati Giustizia Tributaria](https://bancadatigiurisprudenza.giustiziatributaria.gov.it/)
2. **Selezione intelligente** delle sentenze favorevoli al contribuente (tramite regole + AI)
3. **Commento automatico** generato con OpenAI
4. **Pubblicazione su WordPress** tramite API JWT
5. **Esecuzione schedulata** via GitHub Actions (ogni giorno alle 06:10 CET)

## 🛠️ Setup

### 1. Prerequisiti

- Account OpenAI con API key
- WordPress con plugin JWT Authentication installato e configurato
- Repository GitHub

### 2. Configurazione File

#### Sostituire `aeo_jwt_auth.py`

**IMPORTANTE**: Il file `aeo_jwt_auth.py` attuale è uno stub. 
Devi sostituirlo con il tuo modulo completo che include:
- Autenticazione JWT WordPress
- Metodo `post_exists_by_slug(slug)`
- Metodo `publish_post(...)` completo

#### Completare `giustizia_tributaria_autopub.py`

Il file placeholder deve essere sostituito con il codice completo fornito da ChatGPT nella conversazione originale.

### 3. Configurare GitHub Secrets

Vai su: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Aggiungi i seguenti secrets:

#### OpenAI
- `OPENAI_API_KEY`: La tua API key OpenAI (es. `sk-...`)
- `OPENAI_MODEL`: Modello da usare (es. `gpt-4o-mini`)

#### WordPress
- `WP_BASE_URL`: URL del tuo sito (es. `https://studiolegaleartax.it`)
- `WP_USER`: Username WordPress
- `WP_PASS`: Password WordPress
- `WP_CATEGORY_ID`: ID categoria per i post (es. `3`)
- `WP_POST_STATUS`: Stato post (es. `draft` o `publish`)

#### Giustizia Tributaria (opzionali)
- `GT_BASE_URL`: Default `https://bancadatigiurisprudenza.giustiziatributaria.gov.it/`
- `GT_SEARCH_PATH`: Default `ricerca`
- `GT_MAX_ITEMS_PER_RUN`: Max sentenze da analizzare (es. `15`)
- `GT_MAX_PUBLISH_PER_RUN`: Max articoli da pubblicare (es. `3`)

### 4. Attivare GitHub Actions

Il workflow è già configurato in `.github/workflows/gt_autopub.yml`.

Per eseguirlo manualmente:
1. Vai su **Actions**
2. Seleziona **GT AutoPub**
3. Clicca **Run workflow**

L'esecuzione automatica avviene ogni giorno alle 06:10 CET.

## 📝 Struttura Repository

```
.
├── .github/
│   └── workflows/
│       └── gt_autopub.yml          # Workflow GitHub Actions
├── giustizia_tributaria_autopub.py # Script principale
├── aeo_jwt_auth.py                 # Modulo auth WordPress (da completare)
├── requirements.txt                # Dipendenze Python
├── .env.example                    # Template variabili ambiente
└── README.md
```

## 📄 Licenza e Note Legali

⚠️ **DISCLAIMER**: 
- Questo script deve rispettare i termini di utilizzo della banca dati
- Implementa rate limiting per evitare sovraccarichi
- I contenuti generati hanno finalità esclusivamente informative

## 👨‍💻 Autore

Creato da Studio Legale Artax - 2026
