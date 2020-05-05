from fastapi import FastAPI
from pydantic import BaseModel
import datetime as dt

from calcul_droite import calc_droite

app = FastAPI()

class Droite(BaseModel):
    date: dt.datetime
    lat_est_s:str
    lat_est_h: int
    lat_est_m: float
    long_est_s: str
    long_est_h: int
    long_est_m: float



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/calc/")
def read_item(droite: Droite):
    hc, Z = calc_droite(droite.date, 
                       (droite.long_est_s, droite.long_est_h, droite.long_est_m),
                       (droite.lat_est_s, droite.lat_est_h, droite.lat_est_m))


    return {"date": droite.date, "hc": hc, "Z": Z}