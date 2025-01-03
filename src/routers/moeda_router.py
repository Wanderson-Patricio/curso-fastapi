from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List, Optional, Union
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
    coin: Union[Dict, None] = col.find_one({'cod': cod}, {'_id': 0})
    if coin is None:
        raise HTTPException(status_code=404, detail={
            'Message': f'Moeda não encontrada. Código: {cod}',
            'status': 404}
        )
    return MoedaResponse.from_json(coin)


@router.post('/', response_model=Dict, status_code=201)
def register_coin(moeda: MoedaResponse) -> Dict:
    col.insert_one(moeda.to_json())
    return {'message': 'Moeda inserida com sucesso',
            'moeda': moeda}


@router.patch('/{cod:str}', response_model=Dict, status_code=200)
def update_coin(cod: str, parameters: Optional[Dict[str, Any]] = None) -> Dict:
    coin: Union[Dict, None] = col.find_one({'cod': cod}, {'_id': 0})
    if coin is None:
        raise HTTPException(status_code=404, detail={
            'Message': f'Moeda não encontrada. Código: {cod}',
            'status': 404}
        )

    if parameters is None:
        raise HTTPException(status_code=400, detail={
            'message': 'Não foram passados parâmetros para atualização',
            'status': 400}
        )

    old_coin: MoedaResponse = MoedaResponse.from_json(
        col.find_one({'cod': cod}, {'_id': 0}))
    col.find_one_and_update({'cod': cod}, {'$set': parameters})
    new_coin: MoedaResponse = MoedaResponse.from_json(
        col.find_one({'cod': cod}, {'_id': 0}))

    return {
        'message': f'Moeda {cod} atualizada com sucesso',
        'before': old_coin,
        'after': new_coin
    }


@router.delete('/{cod:str}')
def delete_coin(cod: str) -> Dict:
    coin: Union[Dict, None] = col.find_one({'cod': cod}, {'_id': 0})
    if coin is None:
        raise HTTPException(status_code=404, detail={
            'Message': f'Moeda não encontrada. Código: {cod}',
            'status': 404}
        )

    coin: MoedaResponse = MoedaResponse.from_json(col.find_one(coin))
    col.delete_one({'cod': cod})
    return {
        'message': 'Moeda deletada com sucesso',
        'coin': coin
    }
