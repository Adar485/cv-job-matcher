import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional


class CVParser:
    """CV dosyalarından metin çıkarma ve ayrıştırma"""
    
    def __init__(self):
        # Bölüm başlıkları (Türkçe ve İngilizce)
        self.section_headers = {
            'education': ['eğitim', 'education', 'öğrenim', 'akademik'],
            'experience': ['deneyim', 'experience', 'iş deneyimi', 'work experience', 'tecrübe'],
            'skills': ['yetenekler', 'skills', 'beceriler', 'teknik beceriler', 'technical skills'],
            'languages': ['diller', 'languages', 'yabancı dil'],
            'projects': ['projeler', 'projects'],
            'certificates': ['sertifikalar', 'certificates', 'certifications'],
            'summary': ['özet', 'summary', 'profil', 'profile', 'hakkımda', 'about me']
        }
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """PDF dosyasından metin çıkar"""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF okuma hatası: {str(e)}")
    
    def extract_email(self, text: str) -> Optional[str]:
        """Metinden email adresi çıkar"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Metinden telefon numarası çıkar"""
        phone_pattern = r'(\+90|0)?[\s.-]?(\d{3})[\s.-]?(\d{3})[\s.-]?(\d{2})[\s.-]?(\d{2})'
        match = re.search(phone_pattern, text)
        if match:
            return ''.join(match.groups()[1:])
        return None
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Metni bölümlere ayır"""
        sections = {}
        text_lower = text.lower()
        
        # Her bölüm için başlangıç pozisyonunu bul
        section_positions = []
        for section_name, headers in self.section_headers.items():
            for header in headers:
                pos = text_lower.find(header)
                if pos != -1:
                    section_positions.append((pos, section_name, header))
                    break
        
        # Pozisyona göre sırala
        section_positions.sort(key=lambda x: x[0])
        
        # Bölümleri çıkar
        for i, (pos, section_name, header) in enumerate(section_positions):
            start = pos + len(header)
            if i + 1 < len(section_positions):
                end = section_positions[i + 1][0]
            else:
                end = len(text)
            sections[section_name] = text[start:end].strip()
        
        return sections
    
    def parse_cv(self, file_path: str) -> Dict:
        """CV'yi tam olarak ayrıştır"""
        raw_text = self.extract_text_from_pdf(file_path)
        
        parsed_data = {
            'raw_text': raw_text,
            'email': self.extract_email(raw_text),
            'phone': self.extract_phone(raw_text),
            'sections': self.extract_sections(raw_text)
        }
        
        return parsed_data


# Global instance
cv_parser = CVParser()