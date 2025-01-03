from fastapi import APIRouter, HTTPException
from typing import Optional
from pymongo.collection import Collection

from ..models import MoedaResponse
from ..config import PyMongoConnector

router: APIRouter = APIRouter(prefix='/conversao')
db_name: str = 'conversor'
col_name: str = 'moedas'
col: Collection = PyMongoConnector().get_collection(db_name, col_name)

default_coin: str = 'USD'

@router.get('/')
def conversor(cod1: Optional[str] = None, cod2: Optional[str] = None):
    if cod1 is None:
        raise HTTPException(status_code=400, detail={
            'message': 'É necessário informar pelo menos para conversão.',
            'status': 400
        })
    cod2 = cod2 if cod2 is not None else default_coin

    coin1: MoedaResponse = MoedaResponse.from_json(
        col.find_one({'cod': cod1}, {'_id': 0}))
    coin2: MoedaResponse = MoedaResponse.from_json(
        col.find_one({'cod': cod2}, {'_id': 0}))

    ratio: float = coin1.value / coin2.value
    return [
        {
            'message': f'Conversão de {cod1} -> {cod2}',
            'ratio': round(ratio, 4)
        },
        {
            'message': f'Conversão de {cod2} -> {cod1}',
            'ratio': round(1 / ratio, 4)
        }
    ]
