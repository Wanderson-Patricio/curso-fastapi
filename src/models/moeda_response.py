from pydantic import BaseModel
from typing import Dict

class MoedaResponse(BaseModel):
    cod: str
    name: str
    value: float

    def from_json(json: Dict) -> "MoedaResponse":
        return MoedaResponse(
            cod = json.get('cod'),
            name = json.get('name'),
            value = json.get('value')
        )
    
    def to_json(self) -> Dict:
        return {
            'cod': self.cod,
            'name': self.name,
            'value': self.value
        }
