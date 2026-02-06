from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple


class CVJobMatcher:
    """CV ve iş ilanı eşleştirme"""
    
    def calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """İki embedding arasındaki cosine similarity hesapla"""
        vec1 = np.array(embedding1).reshape(1, -1)
        vec2 = np.array(embedding2).reshape(1, -1)
        similarity = cosine_similarity(vec1, vec2)[0][0]
        return float(similarity)
    
    def calculate_skill_match(self, cv_skills: List[str], job_skills: List[str]) -> float:
        """CV ve iş ilanı yetenekleri arasındaki eşleşme oranını hesapla"""
        if not job_skills:
            return 0.0
        
        cv_skills_lower = [s.lower() for s in cv_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matched = sum(1 for skill in job_skills_lower if skill in cv_skills_lower)
        return matched / len(job_skills_lower)
    
    def calculate_match_score(
        self,
        cv_embedding: List[float],
        job_embedding: List[float],
        cv_skills: List[str],
        job_skills: List[str]
    ) -> Dict[str, float]:
        """Toplam eşleşme skorunu hesapla"""
        
        # Cosine similarity (embedding benzerliği)
        embedding_similarity = self.calculate_cosine_similarity(cv_embedding, job_embedding)
        
        # Skill match (yetenek eşleşmesi)
        skill_match = self.calculate_skill_match(cv_skills, job_skills)
        
        # Ağırlıklı toplam skor
        # %60 embedding benzerliği + %40 yetenek eşleşmesi
        final_score = (0.6 * embedding_similarity) + (0.4 * skill_match)
        
        return {
            'final_score': round(final_score * 100, 2),  # Yüzde olarak
            'embedding_similarity': round(embedding_similarity * 100, 2),
            'skill_match': round(skill_match * 100, 2)
        }
    
    def rank_jobs_for_cv(
        self,
        cv_embedding: List[float],
        cv_skills: List[str],
        jobs: List[Dict]
    ) -> List[Dict]:
        """CV için iş ilanlarını sırala"""
        ranked_jobs = []
        
        for job in jobs:
            job_embedding = job.get('embedding', [])
            job_skills = job.get('skills', [])
            
            if job_embedding:
                scores = self.calculate_match_score(
                    cv_embedding, job_embedding, cv_skills, job_skills
                )
                ranked_jobs.append({
                    'job_id': job['id'],
                    'title': job['title'],
                    'company': job.get('company', ''),
                    'scores': scores
                })
        
        # Final skora göre sırala
        ranked_jobs.sort(key=lambda x: x['scores']['final_score'], reverse=True)
        
        return ranked_jobs


# Global instance
matcher = CVJobMatcher()