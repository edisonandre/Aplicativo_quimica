from fastapi import FastAPI
from pydantic import BaseModel
from chempy import Substance
from chempy.chemistry import balance_stoichiometry

app = FastAPI()

# Modelo de datos que recibe la API
class ReactionInput(BaseModel):
    reactivos: dict  # {"H2": 2, "O2": 1}
    productos: dict  # {"H2O": 2}
    masa_dada: float
    compuesto_dado: str
    compuesto_objetivo: str

@app.post("/calcular/")
def calcular_estequiometria(data: ReactionInput):
    try:
        # Balanceo
        reac, prod = balance_stoichiometry(set(data.reactivos.keys()), set(data.productos.keys()))

        # Masa molar de cada compuesto
        masas = {}
        for compuesto in list(reac.keys()) + list(prod.keys()):
            masas[compuesto] = Substance.from_formula(compuesto).molar_mass()

        # Conversión de masa dada a moles
        moles_dado = data.masa_dada / masas[data.compuesto_dado]

        # Relación molar
        coef_dado = reac.get(data.compuesto_dado, prod.get(data.compuesto_dado))
        coef_objetivo = reac.get(data.compuesto_objetivo, prod.get(data.compuesto_objetivo))

        moles_objetivo = moles_dado * (coef_objetivo / coef_dado)

        # Masa del compuesto objetivo
        masa_objetivo = moles_objetivo * masas[data.compuesto_objetivo]

        return {
            "moles_objetivo": moles_objetivo,
            "masa_objetivo": masa_objetivo,
            "masas_molares": masas,
            "ecuacion_balanceada": {"reactivos": dict(reac), "productos": dict(prod)}
        }
    except Exception as e:
        return {"error": str(e)}
