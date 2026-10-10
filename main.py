import os
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv(
    "API_KEY",
    "ak_3j68k87w3svcdxm7jlc22jht"
)
EMAIL = os.getenv("EMAIL", "25ds3000005@ds.study.iitm.ac.in")

class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    body: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    totals = defaultdict(float)

    for event in body.events:
        if event.amount > 0:
            totals[event.user] += event.amount

    revenue = sum(totals.values())

    top_user = (
        max(totals, key=totals.get)
        if totals
        else None
    )

    return {
        "email": EMAIL,
        "total_events": len(body.events),
        "unique_users": len(set(e.user for e in body.events)),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }
