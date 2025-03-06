"""
Modelos do módulo financeiro
"""
from datetime import datetime
from app import db

class Categoria(db.Model):
    """Modelo de categoria financeira"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    descricao = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    receitas = db.relationship('Receita', backref='categoria', lazy='dynamic')
    despesas = db.relationship('Despesa', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Receita(db.Model):
    """Modelo de receita"""
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, atrasado
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('receitas', lazy='dynamic'))

    def __repr__(self):
        return f'<Receita {self.descricao}>'

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': float(self.valor),
            'data': self.data.strftime('%Y-%m-%d'),
            'categoria': self.categoria.nome,
            'forma_pagamento': self.forma_pagamento,
            'status': self.status,
            'observacoes': self.observacoes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Despesa(db.Model):
    """Modelo de despesa"""
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, atrasado
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('despesas', lazy='dynamic'))

    def __repr__(self):
        return f'<Despesa {self.descricao}>'

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': float(self.valor),
            'data': self.data.strftime('%Y-%m-%d'),
            'categoria': self.categoria.nome,
            'forma_pagamento': self.forma_pagamento,
            'status': self.status,
            'observacoes': self.observacoes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 