from fastapi import FastAPI,Body,Path,Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Optional,List

from starlette.requests import Request
from jwt_manager import create_token,valid_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Api demo FastAPI"
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
        auth = await super().__call__(request)
        data = valid_token(auth.credentials)
        if data["email"] != "admin@admin.com":
            raise HTTPException(status_code=403,detail="Credentials invalid")


class User(BaseModel):
    email: str
    password: str
    
    
class Movie(BaseModel):
    id : Optional[int] | None=None
    age : str = Field(max_length=4)
    category : str = Field(max_length=25)
    name : str = Field(max_length=50)
    
    class Config:
        shema_extra = {
            "example": {
                "id": 1,
                "age":"2014",
                "name":"interestelar",
                "category":"Ciencia ficción"
            }
        }
    

movies = [
    {
        "name":"pelicula 1",
        "id":1,
        "age":"1994",
        "category":"terror"
    },
    {
        "name":"pelicula 2",
        "id":2,
        "age":"1995",
        "category":"accion"
    },
    {
        "name":"pelicula 1",
        "id":3,
        "age":"1996",
        "category":"terror"
    },
    {
        "name":"pelicula 2",
        "id":4,
        "age":"1997",
        "category":"accion"
    }
]


@app.post('/login',tags=['auth'])
def login(user: User):
    if user.email == "admin@admin.com" and user.password == "123456":
        token : str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    

@app.get("/",tags=['home'],response_model=dict, status_code=200)
def main() -> dict:
    return JSONResponse(status_code=200, content={"message": "Welcome, this is an API created for Learn FastAPI crud"})


@app.get('/movies',tags=['movies'],response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)


@app.get("/movies/{id}",tags=['movies'],response_model=Movie, status_code=200)
def get_by_id(id : int = Path(ge=1)) -> Movie:
    for item in movies:
        if item['id'] == id :
            return JSONResponse(status_code=200,content=item)
    return JSONResponse(content=[])


@app.get("/movies/",tags=['movies'],response_model=List[Movie], status_code=200)
def get_by_category(category : str = Query(min_length=3, max_length=25)) -> List[Movie]:
    mylist = []
    for item in movies:
        if item['category'] == category :
            mylist.append(item)
    
    return JSONResponse(status_code=200,content=mylist)


@app.post('/movies',tags=['movies'],response_model=dict, status_code=201)
def create(movie : Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"create success."})
    

@app.put('/movies/{id}',tags=["movies"],response_model=dict, status_code=201)
def update(id : int, movie : Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['name'] = movie.name
            item['age'] = movie.age
            item['category'] = movie.category
            return JSONResponse(status_code=201,content={"message":"update success."})
    
    return JSONResponse(status_code=404,content={"message":"Movie not found."})


@app.delete('/movies/{id}',tags=["movies"],response_model=dict, status_code=201)
def delete(id : int = Path(ge=1)) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(status_code=201,content={"message":"delete success."})
    return JSONResponse(status_code=404,content={"message":"Movie not found."})
    