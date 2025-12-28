# Bayes spam detector — progetto

Breve descrizione
- API Flask per classificazione spam su SMS e mail.
- Modelli salvati in `models/`; logica in `app/`.

## Quickstart (dev)
### 1. Crea ambiente virtuale e installa dipendenze:
```
python -m venv venv
.\venv\Scripts\activate
source venv/bin/activate
```

### 2. Installazione Dipendenze
```
pip install -r requirements.txt
```

### 3. Configurazione Ambiente (Fondamentale)
Creare il file .env nella root di progetto con le seguenti variabili
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///app.db
```

### 4. Database e Avvio
```
python -m flask db upgrade
flask create-admin -> se si vuole creare utente admin
```

### 5. Avvio
```
flask run
```

Documenti utili
- BACKEND.md — dettagli operativi del backend.
- MODELS.md — convenzioni per artefatti modelli e metadata.

Dove mettere i modelli
- `models/sms/` e `models/mail/` con naming versionato e `model.json`.

Contribuire
- Aggiungi unit/smoke tests per ogni modello e per gli endpoint.
- Mantieni `models/*/model.json` aggiornati.
- Apri PR e richiedi code review da un data scientist per le modifiche di modello.

Contatti / NOTE
- Log principali su stdout/stderr; controlla LOG_LEVEL per debug.
- Non committare modelli o dati sensibili su repo pubblico.
