from datetime import datetime
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from services.bulletin_service import get_bulletins as get_bulletins_from_db
from routers import users


app = FastAPI(
    title="Доска объявлений",
    version="v1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(users.router)


class BulletinSchema(BaseModel):
    #id: int
    name: str
    description: str
    #created_at: datetime
    type: str
    author: str = 'test'



@app.post("/bulletins/")
async def add_bulletin(
    bullet: BulletinSchema,
    session: AsyncSession = Depends(get_session)
):
    pass


@app.get("/bulletins", response_model=list[BulletinSchema])
async def get_bulletins(session: AsyncSession = Depends(get_session)):
    bulletins = await get_bulletins_from_db(session)
    return bulletins

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
