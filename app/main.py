from fastapi import FastAPI
from routers.users import router as user_router
from routers.bulletins import router as bulletin_router


app = FastAPI(
    title="Доска объявлений",
    version="v1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_router)
app.include_router(bulletin_router)








if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
