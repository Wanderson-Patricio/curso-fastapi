from fastapi import APIRouter
from typing import List

from ..models import MoedaResponse

router: APIRouter = APIRouter(prefix='/moedas')

@router.get('/')
def listar_moedas() -> List[MoedaResponse]:
    return [
        MoedaResponse(
            cod = 'BRL',
            name = 'Real Brasileiro',
            value = 0.1613
        ),
        MoedaResponse(
            cod = 'USD',
            name = 'Dólar Americano',
            value = 1.0
        )
    ]

@router.post('/', response_model=MoedaResponse, status_code=201)
def cadastrar_moeda(moeda: MoedaResponse) -> MoedaResponse:
    return MoedaResponse(
        cod=moeda.cod + ' novo',
        name=moeda.name,
        value=moeda.value
    )