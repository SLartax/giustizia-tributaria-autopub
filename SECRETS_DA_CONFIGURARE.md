# ⚠️ SECRETS DA CONFIGURARE SU GITHUB

## 📋 Checklist Secrets Obbligatori

Vai su: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Link diretto: https://github.com/SLartax/giustizia-tributaria-autopub/settings/secrets/actions

---

### 🤖 OpenAI (OBBLIGATORI)

| Nome Secret | Valore | Dove trovarlo |
|-------------|--------|---------------|
| `OPENAI_API_KEY` | `sk-proj-...` | https://platform.openai.com/api-keys |
| `OPENAI_MODEL` | `gpt-4o-mini` | Modello consigliato (economico e veloce) |

---

### 📝 WordPress (OBBLIGATORI)

| Nome Secret | Valore | Note |
|-------------|--------|------|
| `WP_BASE_URL` | `https://studiolegaleartax.it` | URL del sito (senza / finale) |
| `WP_USER` | Il tuo username WP | Admin o editor |
| `WP_PASS` | La tua password WP | **NON condividere mai!** |
| `WP_CATEGORY_ID` | `3` | ID della categoria per i post |
| `WP_POST_STATUS` | `draft` oppure `publish` | `draft` per bozze, `publish` per pubblicare subito |

---

### ⚙️ Giustizia Tributaria (OPZIONALI - hanno valori di default)

Questi sono opzionali. Se non li configuri, useranno i valori di default.

| Nome Secret | Valore Default | Descrizione |
|-------------|----------------|-------------|
| `GT_BASE_URL` | `https://bancadatigiurisprudenza.giustiziatributaria.gov.it/` | URL banca dati |
| `GT_SEARCH_PATH` | `ricerca` | Path di ricerca |
| `GT_MAX_ITEMS_PER_RUN` | `15` | Max sentenze da analizzare |
| `GT_MAX_PUBLISH_PER_RUN` | `3` | Max articoli da pubblicare |

---

## 🛠️ Come Aggiungere un Secret

1. Vai su https://github.com/SLartax/giustizia-tributaria-autopub/settings/secrets/actions
2. Clicca **"New repository secret"**
3. Inserisci:
   - **Name**: il nome esatto dalla tabella sopra (es. `OPENAI_API_KEY`)
   - **Secret**: il valore corrispondente
4. Clicca **"Add secret"**
5. Ripeti per tutti i secrets obbligatori

---

## ✅ Verifica Configurazione

Dopo aver configurato i secrets:

1. Vai su **Actions** → **GT AutoPub**
2. Clicca **"Run workflow"** → **"Run workflow"**
3. Attendi l'esecuzione (circa 5-10 minuti)
4. Se tutto va bene, vedrai ✅ verde
5. Controlla i post pubblicati su WordPress

---

## 🔒 Sicurezza

- I secrets sono **criptati** da GitHub
- Non sono mai visibili nei log
- Solo il workflow può accedervi
- **NON committare mai** credenziali nel codice!

---

## ❓ Troubleshooting

### Il workflow fallisce con "OPENAI_API_KEY mancante"
➡️ Verifica di aver aggiunto il secret con nome **esattamente** `OPENAI_API_KEY`

### "JWT Auth fallita"
➡️ Verifica:
- WordPress JWT plugin installato e attivo
- `WP_USER` e `WP_PASS` corretti
- `WP_BASE_URL` corretto (senza / finale)

### "Nessuna sentenza trovata"
➡️ Il sito della giustizia tributaria potrebbe essere temporaneamente non disponibile o aver cambiato struttura

---

## 📞 Supporto

Per problemi:
1. Controlla i log del workflow su GitHub Actions
2. Verifica che tutti i secrets obbligatori siano configurati
3. Testa manualmente l'autenticazione WordPress
