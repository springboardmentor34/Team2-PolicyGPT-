from fastapi import FastAPI

app = FastAPI(
    title="PolicyGPT API",
    description="Government Policy & Public Scheme Intelligence Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to PolicyGPT API"
    }