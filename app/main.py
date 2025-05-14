from fastapi import FastAPI
from routes import user, todo_list

app = FastAPI(title="Task Manager API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager API!"}

# Routers
app.include_router(user.router)
app.include_router(todo_list.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)