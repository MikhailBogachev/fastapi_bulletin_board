from fastapi import FastAPI


app = FastAPI(
    title="Доска объявлений",
    version="v1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
