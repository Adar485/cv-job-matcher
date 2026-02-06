from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import json

from app.database import get_db
from app.models.user import User
from app.models.cv import CV
from app.models.job import Skill, CVSkill
from app.schemas.cv import CVResponse, CVDetail
from app.utils.auth import get_current_user
from app.services.cv_parser import cv_parser
from app.services.nlp_engine import nlp_engine

router = APIRouter(prefix="/api/cv", tags=["CV"])

# Upload klasörü
UPLOAD_DIR = "uploads/cvs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=CVResponse)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """CV dosyası yükle ve analiz et"""
    # Dosya uzantısı kontrolü
    allowed_extensions = [".pdf"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Şu anda sadece PDF dosyaları kabul edilmektedir"
        )
    
    # Dosyayı kaydet
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # CV'yi parse et
    try:
        parsed_data = cv_parser.parse_cv(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CV işlenirken hata oluştu: {str(e)}"
        )
    
    # Yetenekleri çıkar
    skills = nlp_engine.extract_skills(parsed_data['raw_text'])
    
    # BERT embedding oluştur
    try:
        embedding = nlp_engine.get_embedding(parsed_data['raw_text'])
    except Exception as e:
        embedding = []
    
    # Veritabanına kaydet
    new_cv = CV(
        user_id=current_user.id,
        file_path=file_path,
        file_name=file.filename,
        raw_text=parsed_data['raw_text'],
        parsed_data=json.dumps(parsed_data, ensure_ascii=False),
        embedding=json.dumps(embedding)
    )
    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)
    
    # Yetenekleri kaydet
    for skill_data in skills:
        # Skill var mı kontrol et
        skill = db.query(Skill).filter(Skill.name == skill_data['name']).first()
        if not skill:
            skill = Skill(name=skill_data['name'], normalized_name=skill_data['name'].lower())
            db.add(skill)
            db.commit()
            db.refresh(skill)
        
        # CV-Skill ilişkisi
        cv_skill = CVSkill(
            cv_id=new_cv.id,
            skill_id=skill.id,
            confidence_score=skill_data['confidence']
        )
        db.add(cv_skill)
    
    db.commit()
    
    return new_cv


@router.get("/", response_model=List[CVResponse])
def get_my_cvs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Kullanıcının CV'lerini listele"""
    cvs = db.query(CV).filter(CV.user_id == current_user.id).all()
    return cvs


@router.get("/{cv_id}", response_model=CVDetail)
def get_cv_detail(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """CV detayını getir"""
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV bulunamadı"
        )
    return cv


@router.get("/{cv_id}/skills")
def get_cv_skills(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """CV'deki yetenekleri getir"""
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV bulunamadı"
        )
    
    skills = []
    for cv_skill in cv.skills:
        skills.append({
            'name': cv_skill.skill.name,
            'confidence': cv_skill.confidence_score
        })
    
    return {'cv_id': cv_id, 'skills': skills}


@router.delete("/{cv_id}")
def delete_cv(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """CV sil"""
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV bulunamadı"
        )
    
    # Dosyayı sil
    if cv.file_path and os.path.exists(cv.file_path):
        os.remove(cv.file_path)
    
    # Veritabanından sil
    db.delete(cv)
    db.commit()
    
    return {"message": "CV başarıyla silindi"}