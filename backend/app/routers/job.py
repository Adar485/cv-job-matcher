from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models.user import User
from app.models.cv import CV
from app.models.job import Job, Skill, JobSkill, Match
from app.schemas.job import JobCreate, JobResponse, JobDetail
from app.utils.auth import get_current_user
from app.services.nlp_engine import nlp_engine
from app.services.matcher import matcher

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Yeni iş ilanı oluştur"""
    job_text = f"{job_data.title} {job_data.description} {job_data.requirements or ''}"
    
    skills = nlp_engine.extract_skills(job_text)
    
    try:
        embedding = nlp_engine.get_embedding(job_text)
    except Exception as e:
        embedding = []
    
    new_job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        description=job_data.description,
        requirements=job_data.requirements,
        embedding=json.dumps(embedding)
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    for skill_data in skills:
        skill = db.query(Skill).filter(Skill.name == skill_data['name']).first()
        if not skill:
            skill = Skill(name=skill_data['name'], normalized_name=skill_data['name'].lower())
            db.add(skill)
            db.commit()
            db.refresh(skill)
        
        job_skill = JobSkill(
            job_id=new_job.id,
            skill_id=skill.id,
            importance=skill_data['confidence']
        )
        db.add(job_skill)
    
    db.commit()
    
    return new_job


@router.get("/", response_model=List[JobResponse])
def get_all_jobs(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Tüm iş ilanlarını listele"""
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobDetail)
def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db)
):
    """İş ilanı detayını getir"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="İş ilanı bulunamadı"
        )
    return job


@router.get("/{job_id}/skills")
def get_job_skills(
    job_id: int,
    db: Session = Depends(get_db)
):
    """İş ilanındaki yetenekleri getir"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="İş ilanı bulunamadı"
        )
    
    skills = []
    for job_skill in job.skills:
        skills.append({
            'name': job_skill.skill.name,
            'importance': job_skill.importance
        })
    
    return {'job_id': job_id, 'skills': skills}


@router.post("/{cv_id}/match")
def match_cv_with_jobs(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """CV'yi tüm iş ilanlarıyla eşleştir"""
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV bulunamadı"
        )
    
    cv_embedding = json.loads(cv.embedding) if cv.embedding else []
    cv_skills = [cs.skill.name for cs in cv.skills]
    
    if not cv_embedding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CV henüz işlenmemiş"
        )
    
    jobs = db.query(Job).all()
    
    results = []
    for job in jobs:
        job_embedding = json.loads(job.embedding) if job.embedding else []
        job_skills = [js.skill.name for js in job.skills]
        
        if job_embedding:
            scores = matcher.calculate_match_score(
                cv_embedding, job_embedding, cv_skills, job_skills
            )
            
            match_record = Match(
                cv_id=cv.id,
                job_id=job.id,
                similarity_score=scores['final_score'],
                skill_match_score=scores['skill_match']
            )
            db.add(match_record)
            
            results.append({
                'job_id': job.id,
                'job_title': job.title,
                'company': job.company,
                'location': job.location,
                'final_score': scores['final_score'],
                'embedding_similarity': scores['embedding_similarity'],
                'skill_match': scores['skill_match'],
                'matched_skills': [s for s in cv_skills if s.lower() in [js.lower() for js in job_skills]]
            })
    
    db.commit()
    
    results.sort(key=lambda x: x['final_score'], reverse=True)
    
    return {
        'cv_id': cv_id,
        'total_jobs': len(results),
        'matches': results
    }


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """İş ilanını sil"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="İş ilanı bulunamadı"
        )
    
    db.delete(job)
    db.commit()
    
    return {"message": "İş ilanı başarıyla silindi"}