"""
Modelo de perfil
"""
from datetime import datetime
from app import db

class Profile(db.Model):
    """Modelo de perfil do usuário ou empresa"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Informações básicas
    name = db.Column(db.String(100))
    type = db.Column(db.String(20))  # 'personal' ou 'business'
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    
    # Informações adicionais para empresas
    company_name = db.Column(db.String(100))
    company_registration = db.Column(db.String(50))  # CNPJ/NIF
    company_type = db.Column(db.String(50))
    industry = db.Column(db.String(100))
    website = db.Column(db.String(200))
    
    # Campos de controle
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_complete = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Profile {self.name}>'

    def to_dict(self):
        """Converte o perfil para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'company_name': self.company_name if self.type == 'business' else None,
            'company_registration': self.company_registration if self.type == 'business' else None,
            'company_type': self.company_type if self.type == 'business' else None,
            'industry': self.industry if self.type == 'business' else None,
            'website': self.website if self.type == 'business' else None,
            'is_complete': self.is_complete
        } 