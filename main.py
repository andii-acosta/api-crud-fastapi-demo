from fastapi import FastAPI,Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Optional

app = FastAPI()
app.title = "Api demo FastAPI"
app.version = "0.0.1"

class Movie(BaseModel):
    id : Optional[int] | None=None
    age : str = Field(default="2014",max_length=4)
    category : str = Field(default="Ciencia ficción",max_length=15)
    name : str = Field(default="interestelar",max_length=20)
    

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

@app.get("/",tags=['home'])
def list():
    return JSONResponse({"message": "Hello World"})


@app.get('/movies',tags=['movies'])
def get_movies():
    return movies

@app.get("/movies/{id}",tags=['movies'])
def get_by_id(id : int):
    for item in movies:
        if item['id'] == id :
            return item
    return []

@app.get("/movies/",tags=['movies'])
def get_by_category(category : str):
    mylist = []
    for item in movies:
        if item['category'] == category :
            mylist.append(item)
    
    return mylist


@app.post('/movies',tags=['movies'])
def create(movie : Movie):
    movies.append(movie)
    return movies
    

@app.put('/movies/{id}',tags=["movies"])
def update(id : int, movie : Movie):
    for item in movies:
        if item['id'] == id:
            item['name'] = movie.name
            item['age'] = movie.age
            item['category'] = movie.category
            return item
    return "Pelicula no encontrada."


@app.delete('/movies/{id}',tags=["movies"])
def delete(id : int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    return "Pelicula no encontrada."
    