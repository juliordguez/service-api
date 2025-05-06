from fastapi import FastAPI

app = FastAPI()

@app.get("/usuario")
async def get_usuario():
    return {"usuario": {"id": 1, "nombre": "Juan Pérez"}}

@app.get("/usuarios")
async def get_usuarios():
    return {
        "usuarios": [
            {"id": 1, "nombre": "Juan Pérez"},
            {"id": 2, "nombre": "Ana Gómez"},
            {"id": 3, "nombre": "Carlos López"}
        ]
    }

@app.get("/casas")
async def get_casas():
    return {
        "casas": [
            {"id": 1, "direccion": "Calle 1 #123"},
            {"id": 2, "direccion": "Calle 2 #456"},
            {"id": 3, "direccion": "Calle 3 #789"}
        ]
    }

@app.get("/fraccionamientos")
async def get_fraccionamientos():
    return {
        "fraccionamientos": [
            {"id": 1, "nombre": "Fracc. Las Palmas"},
            {"id": 2, "nombre": "Fracc. El Mirador"},
            {"id": 3, "nombre": "Fracc. Monteverde"}
        ]
    }


@app.get("/roles")
async def get_roles():
    return {
        "roles": [
            {"id": 1, "rol": "admin"},
            {"id": 2, "rol": "usuario"},
            {"id": 3, "rol": "vigilante"}
        ]
    }

