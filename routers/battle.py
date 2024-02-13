from fastapi import APIRouter, HTTPException, status
from schemas.battle import Battle as battle_schema
from models.battle import Battle as battle_model
from config.bd import get_db, Session
from datetime import datetime
import requests
import uuid

router =  APIRouter(prefix='/pokemon-battle', tags=['Pokemon Battle'], responses={404 : {'message' : 'Not found'}})

@router.post('/')
async def create_pokemon_battle(battle_obj : battle_schema):    
    if battle_obj.name_pokemon_a == battle_obj.name_pokemon_b:
        raise HTTPException(status_code=404, detail="Empate tecnico")
    
    try:#instrucción try, atrapa de inicio a fin las lineas que intentaremos ejecutar y que tiene posibilidad de fallar
    #¡inicio try!
        session = get_db()
        db: Session
        for db in session:                      
            battle_obj = battle_schema(**battle_obj.model_dump())
            battle_obj.uuid =  uuid.uuid4()
            battle_obj.created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')                                
            db.add(battle_obj)
            db.commit()
            db.refresh(battle_obj)
            return battle_obj
    #¡fin try!
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
     
@router.get("/", response_model = list[battle_schema])
def get_pokemon_battles():
    try:#instrucción try, atrapa de inicio a fin las lineas que intentaremos ejecutar y que tiene posibilidad de fallar
    #¡inicio try!
        session = get_db()
        db:Session
        for db in session:
            #se usa la instrucción where para buscar por el id y se ejecuta el first para
            #encontrar la primera coincidencia, esto es posible porque el id es un 
            #identificador unico
            r=db.query(battle_model)
            return r
    #¡fin try!
    except Exception as e:#instrucción que nos ayuda a atrapar la excepción que ocurre cuando alguna instrucción dentro de try falla
        #se debe controlar siempre que nos conectamos a una base de datos con un try - except
        #debido a que no podemos controlar la respuesta del servicio externo (en este caso la base de datos)
        #y es muy posible que la conexión falle por lo cual debemos responder que paso
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        #la instrucción raise es similar a la instrucción return, pero en vez de retornar cualquier elemento, retornamos especificamente
        #un error, en este caso el error esta contenido en HTTPException
    
@router.get('/')
async def get_all_pokemons():
    api_url = "https://pokeapi.co/api/v2/pokemon/"
    all_pokemon = requests.get(api_url).json()
    # print(type(all_pokemon['abilities'][0]))
    # print(type(all_pokemon['abilities'][0]))    
    return all_pokemon

@router.get('/{name_pokemon}')
async def get_pokemon(name_pokemon:str):
    try:
        api_url = f"https://pokeapi.co/api/v2/pokemon/{name_pokemon}"
        pokemon = requests.get(api_url).json()
        return pokemon
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
