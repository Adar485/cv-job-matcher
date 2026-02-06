from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base

# Modelleri import et (tabloların oluşması için gerekli)
from app.models.user import User
from app.models.cv import CV
from app.models.job import Job, Skill, CVSkill, JobSkill, Match

# Router'ları import et
from app.routers.auth import router as auth_router
from app.routers.cv import router as cv_router
from app.routers.job import router as jobs_router

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

# FastAPI uygulaması
app = FastAPI(
    title=settings.APP_NAME,
    description="CV ve İş İlanı Eşleştirme API'si",
    version="1.0.0"
)

# CORS ayarları (React frontend için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth_router)
app.include_router(cv_router)
app.include_router(jobs_router)


@app.get("/")
def root():
    return {
        "message": "CV Job Matcher API'sine Hoş Geldiniz!",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
