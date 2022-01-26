from typing import Optional
import yfinance
from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from models import Stock

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


class StockRequest(BaseModel):
    symbol: str
    # price: float = Optional[float]
    # forward_pe: float
    # forward_eps: float
    # dividend_yield: float
    # ma50: float
    # ma200: float


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
    forward_pe: Optional[str] = None,
    dividend_yield: Optional[str] = None,
    ma50: Optional[str] = None,
    ma200: Optional[str] = None,
):
    """
    Main dashboard and main page
    """
    stocks = db.query(Stock)
    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe >= float(forward_pe))
    if dividend_yield:
        stocks = stocks.filter(Stock.dividend_yield >= float(dividend_yield))
    if ma50 == "on":
        stocks = stocks.filter(Stock.price >= Stock.ma50)
    if ma200 == "on":
        stocks = stocks.filter(Stock.price >= Stock.ma200)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "stocks": stocks,
            "forward_pe": forward_pe,
            "dividend_yield": dividend_yield,
            "ma50": ma50,
            "ma200": ma200,
        },
    )


def fetch_stock_data(symbol: str):
    db = SessionLocal()
    stock = Stock()
    # stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    yahoo_data = yfinance.Ticker(symbol)

    stock.symbol = yahoo_data.info["symbol"]

    if yahoo_data.info["twoHundredDayAverage"]:
        stock.ma200 = yahoo_data.info["twoHundredDayAverage"]

    if yahoo_data.info["fiftyDayAverage"]:
        stock.ma50 = yahoo_data.info["fiftyDayAverage"]

    stock.price = yahoo_data.info["previousClose"]

    if yahoo_data.info["forwardPE"]:
        stock.forward_pe = yahoo_data.info["forwardPE"]

    if yahoo_data.info["forwardEps"]:
        stock.forward_eps = yahoo_data.info["forwardEps"]
    if yahoo_data.info["dividendYield"]:
        stock.dividend_yield = yahoo_data.info["dividendYield"] * 100

    db.add(stock)
    db.commit()


@app.post("/stock")
async def create_stock(
    stock_request: StockRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Creates a new stock and stores in the database
    """
    # stock = Stock()
    # stock.symbol = stock_request.symbol
    # db.add(stock)
    # db.commit()
    background_tasks.add_task(fetch_stock_data, stock_request.symbol)

    return {"code": "success", "message": "Stock created successfully"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
