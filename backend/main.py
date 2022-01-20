from email.policy import HTTP
from urllib import response
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import fetch_all_todos, fetch_one_todo, create_todo, update_todo, remove_todo
from models import Todo

# Instantiate APP object
app = FastAPI()

origins = ['https://localhost:3000',
           'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
    
)

# Test Server
@app.get("/")
def read_root():
    return {"PING:PONG"}

# HTTP Operations (POST/GET/PUT/DELETE)
@app.get("/api/todo")
async def get_all_todo_entries():
    # Fetch Response
    response = await fetch_all_todos() 
    if not response:
        raise HTTPException(404)
    else:
        return response

@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):
    # Fetch Response
    try:
        response = await fetch_one_todo(title)
        # Sanity Check
        if not response:
            raise HTTPException(404, f'Record with (ID:{title}) does not Exist.')
        else:
            return response
    except Exception as e:
        raise HTTPException(404, e.args)

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    # Fetch Response
    response = await create_todo(todo.dict())
    # Sanity Check
    if not response:
        raise HTTPException(404, "Error Occured during Creation OR the Endpoint does not exist")
    else:
        return response
    
@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title: str, description: str):
    # Fetch Response
    response = await update_todo(title=title, desc=description)
    # Sanity Check
    if not response:
        raise HTTPException(404, "Bad request / Record not found")
    else:
        return response
    
@app.delete("/api/todo{title}")
async def delete_todo(title):
    # Fetch Response
    response = await remove_todo(title)
    # Sanity Check
    if not response:
        raise HTTPException(404, f"No matching record exists for title: {title}")
    else:
        return f"Successfully deleted item {title}"

### NOTE: XML Responses can be returned via the Response object
### available in fastapi. There is no use case for this here, but
### it is reasonably easy to implement to use with legacy (SOAP) api(s)

### Since the request/response cycle is asynchronous,
### implementing multi threading for this application is
### severe overkill, but an example of a potential usage will be included

