from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from typing import List, Dict
import re


class NLPEngine:
    """BERT tabanlı NLP işlemleri"""
    
    def __init__(self):
        self.model_name = "dbmdz/bert-base-turkish-cased"
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        
        # Yaygın teknik yetenekler listesi
        self.skill_keywords = [
            # Programlama dilleri
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'go', 'rust', 'typescript',
            # Web teknolojileri
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
            # Veritabanları
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
            # DevOps & Cloud
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'gitlab', 'github', 'ci/cd', 'linux',
            # Veri bilimi & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            # Diğer
            'git', 'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'unit test', 'jira'
        ]
    
    def load_model(self):
        """BERT modelini yükle"""
        if not self.is_loaded:
            print("BERT modeli yükleniyor...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            self.model.eval()
            self.is_loaded = True
            print("Model yüklendi!")
    
    def get_embedding(self, text: str) -> List[float]:
        """Metin için BERT embedding oluştur"""
        self.load_model()
        
        # Metni tokenize et
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Embedding oluştur
        with torch.no_grad():
            outputs = self.model(**inputs)
            # [CLS] token'ının embedding'ini al
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        
        return embedding.tolist()
    
    def extract_skills(self, text: str) -> List[Dict]:
        """Metinden yetenekleri çıkar"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill in text_lower:
                # Skill'in kaç kez geçtiğini say
                count = text_lower.count(skill)
                confidence = min(1.0, 0.5 + (count * 0.1))
                found_skills.append({
                    'name': skill,
                    'confidence': confidence
                })
        
        # Confidence'a göre sırala
        found_skills.sort(key=lambda x: x['confidence'], reverse=True)
        
        return found_skills
    
    def extract_skills_from_job(self, description: str, requirements: str = "") -> List[Dict]:
        """İş ilanından yetenekleri çıkar"""
        combined_text = f"{description} {requirements}"
        return self.extract_skills(combined_text)


# Global instance
nlp_engine = NLPEngine()