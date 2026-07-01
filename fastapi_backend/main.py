from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .schemas import PredictionRecordOut
from .services import obtener_predicciones
from .routers.predictions import router as predictions_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Caregiver Overload Prediction System', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(predictions_router, prefix='/api/v1', tags=['predictions'])


@app.get('/health')
def health():
    return {'status': 'ok'}
