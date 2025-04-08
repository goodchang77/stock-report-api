from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/company")
def get_company_info(ticker: str = Query(...)):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        return {
            "company": info.get("shortName", ""),
            "ticker": ticker,
            "marketCap": info.get("marketCap", 0),
            "eps": info.get("trailingEps", 0),
            "grossMargins": float(info.get("grossMargins", 0)) * 100 if info.get("grossMargins") else None,
            "peRatio": info.get("trailingPE", 0),
            "industry": info.get("industry", ""),
            "sector": info.get("sector", ""),
            "country": info.get("country", "")
        }

    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker
        }
