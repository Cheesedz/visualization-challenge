# visualization-challenge

Project for joining ISE code challenge

# Setup

## Web

- Install pnpm

```bash
    npm install -g pnpm@latest
```

- Install dependcies

```bash
    cd web
    pnpm i
```

- Run in development environment

```bash
    pnpm dev
```

## API

- Install dependencies

```bash
    cd api
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```

- Set up environment variables

```bash
    GROQ_API_KEY=
    GROQ_MODEL_NAME=llama-3.1-8b-instant
```

- Run API

```bash
    uvicorn app.main:app --reload
```
