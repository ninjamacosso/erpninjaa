"""
Script para inicializar o banco de dados com dados padrão
"""
from app import create_app, db
from app.models import Categoria

def init_categorias():
    """Inicializa as categorias padrão"""
    # Categorias de Receita
    categorias_receita = [
        ('Vendas', 'Receitas provenientes de vendas de produtos'),
        ('Serviços', 'Receitas provenientes de prestação de serviços'),
        ('Comissões', 'Receitas de comissões'),
        ('Juros', 'Receitas financeiras'),
        ('Outras Receitas', 'Outras receitas diversas')
    ]

    # Categorias de Despesa
    categorias_despesa = [
        ('Pessoal', 'Despesas com funcionários, salários e encargos'),
        ('Operacional', 'Despesas operacionais como aluguel, energia, etc'),
        ('Marketing', 'Despesas com publicidade e marketing'),
        ('Impostos', 'Despesas com impostos e taxas'),
        ('Financeiras', 'Despesas bancárias e juros'),
        ('Fornecedores', 'Pagamentos a fornecedores'),
        ('Outras Despesas', 'Outras despesas diversas')
    ]

    # Criar categorias de receita
    for nome, descricao in categorias_receita:
        if not Categoria.query.filter_by(nome=nome, tipo='receita').first():
            categoria = Categoria(nome=nome, tipo='receita', descricao=descricao)
            db.session.add(categoria)

    # Criar categorias de despesa
    for nome, descricao in categorias_despesa:
        if not Categoria.query.filter_by(nome=nome, tipo='despesa').first():
            categoria = Categoria(nome=nome, tipo='despesa', descricao=descricao)
            db.session.add(categoria)

    # Commit das alterações
    db.session.commit()

def init_db():
    """Inicializa o banco de dados"""
    app = create_app()
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Inicializar dados
        init_categorias()
        
        print('Banco de dados inicializado com sucesso!')

if __name__ == '__main__':
    init_db() 