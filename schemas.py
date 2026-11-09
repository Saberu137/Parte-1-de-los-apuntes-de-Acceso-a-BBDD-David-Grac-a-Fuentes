from pydantic import BaseModel

class TareaCrear(BaseModel):
    titulo: str


# Lo que la API devuelve
class TareaLeer(BaseModel):
    id: int
    titulo: str
    completada: bool
