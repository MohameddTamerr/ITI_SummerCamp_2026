# AI Text Detector — FastAPI Backend

A simple REST API that detects whether a given text is **AI-generated** or **Human-written**.

---

## Project Structure

```
project/
├── main.py           ← FastAPI app (this is the server)
├── model.joblib      ← your trained sklearn pipeline  ← YOU ADD THIS
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Drop your trained model here
#    The file must be named exactly:  model.joblib

# 3. Start the server
uvicorn main:app --reload --port 8000
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Classify a text |

### POST `/predict`

**Request body:**
```json
{
  "text": "The impact of artificial intelligence on modern society..."
}
```

**Response:**
```json
{
  "label": 1,
  "category": "AI-generated",
  "confidence": 94.7
}
```

- `label` → `0` = Human, `1` = AI-generated
- `category` → human-readable string
- `confidence` → model confidence in % (0–100)

---

## Interactive Docs

Once the server is running, open:

- **Swagger UI** → http://127.0.0.1:8000/docs
- **ReDoc**       → http://127.0.0.1:8000/redoc

---

## Frontend Integration

```javascript
const API_URL = "http://127.0.0.1:8000";

async function detectText(text) {
  const res = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return await res.json();
  // { label: 1, category: "AI-generated", confidence: 94.7 }
}
```
