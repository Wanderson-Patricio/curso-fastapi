from pydantic import BaseModel


class MoedaResponse(BaseModel):
    cod: str
    name: str
    value: float