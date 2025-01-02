from fastapi import APIRouter, HTTPException
from typing import Dict, List
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from ..models import MoedaResponse
from ..config import PyMongoConnector

router: APIRouter = APIRouter(prefix='/moedas')
db_name: str = 'conversor'
col_name: str = 'moedas'
col: Collection = PyMongoConnector().get_collection(db_name, col_name)

@router.get('/')
def list_coins(offset: int = 0, limit: int = 5) -> List[MoedaResponse]:
    all_coins: Cursor = col.find({}, {'_id': 0}).skip(offset).limit(limit)
    return [MoedaResponse.from_json(coin) for coin in all_coins]

@router.get('/{cod:str}')
def get_coin(cod: str) -> MoedaResponse:
    coin: Dict = col.find_one({"cod": cod}, {'_id': 0})
    if coin is None:
        raise HTTPException(status_code=404, detail={
                "Message": "Moeda não encontrada",
                "cod": cod}
            )
    return MoedaResponse.from_json(coin)

@router.post('/', response_model=Dict, status_code=201)
def register_coin(moeda: MoedaResponse) -> Dict:
    col.insert_one(moeda.to_json())
    return {'message': 'Moeda inserida com sucesso',
            'moeda': moeda}