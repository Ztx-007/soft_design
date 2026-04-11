from fastapi import APIRouter
from fastapi import FastAPI, Query, Depends, Request
from decimal import Decimal
from service import ExchangeRateService
from sqlalchemy.orm import Session
from database import get_db
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
def get_exchange_rate_service(db: Session = Depends(get_db)):
    yield ExchangeRateService(db)

@router.get("/convert")
@limiter.limit("5/minute")
def convert(
            request: Request,
            from_currency:str = Query(...,max_length=3, min_length=3),
            to_currency:str = Query(...,max_length=3, min_length=3), 
            amount: Decimal = Query(...,gt=0),
            service: ExchangeRateService = Depends(get_exchange_rate_service)):
    
    result = service.convert(from_currency, to_currency, amount)
    return result


@router.get("/health") #通常用来监测是否需要重启服务器 是一个api接口
def health():
    return {"status": "OK"}