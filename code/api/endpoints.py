import repository.db as db

from fastapi import FastAPI
import routers.esgreporting as esgreporting
import routers.authroutes as authroutes

db.Base.metadata.create_all(bind=db.engine)
app = FastAPI()
app.include_router(esgreporting.router)
app.include_router(authroutes.router)


import datetime
@app.get("/ping")
def get_ping():
    return {"ping": datetime.datetime.now()}