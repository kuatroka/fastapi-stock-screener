from typing import Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    """
    Main dashboard and main page
    """
    return templates.TemplateResponse("home.html", {"request": request, "somevar": 2})


@app.post("/stock")
def create_stock(stock: str = "TSLA"):
    """
    Creates a new stock and stores in the database
    """
    return {"code": "success", "message": "Stock created successfully"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
