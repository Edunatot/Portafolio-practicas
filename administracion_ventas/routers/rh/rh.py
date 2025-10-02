from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()
app = FastAPI()

class RH(BaseModel):
    nombre: str
    edad: int
    correo: str
    celular: str
    experiencia: int
    nivel_ed: int
    horarios: str
    presentacion: int
    conocimiento: int
    comunicacion: int
    resolucion: int

aplicantes = []
perfil_ideal = {
    "experiencia": 1,
    "nivel_ed": 3,
    "presentacion": 7,
    "horarios":"y",
    "conocimiento": 7,
    "comunicacion": 6,
    "resolucion": 8
}

def aprobado(apl: RH):
    return (apl.experiencia >= perfil_ideal["experiencia"] and
            apl.nivel_ed >= perfil_ideal["nivel_ed"] and
            apl.presentacion >= perfil_ideal["presentacion"] and
            apl.conocimiento >= perfil_ideal["conocimiento"] and
            apl.comunicacion >= perfil_ideal["comunicacion"] and
            apl.resolucion >= perfil_ideal["resolucion"])

@router.post("/aplicantes")
def registrar_aplicante(aplicante: RH):
    aprob = aprobado(aplicante)
    aplicantes.append({"data": aplicante, "aprobado": aprob})
    return {"mensaje": "Aplicante registrado", "aprobado": aprob}

@router.get("/aplicantes")
def listar_aplicantes():
    return aplicantes

@app.get("/")
def rh_home():
    return FileResponse(Path("routers/rh/rh.html"))

