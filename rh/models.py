from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    responsavel = models.ForeignKey('Funcionario', on_delete=models.SET_NULL, null=True, related_name='departamentos_chefiados')
    
    def __str__(self):
        return self.nome

class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=50, choices=[
        ('JR', 'Júnior'),
        ('PL', 'Pleno'),
        ('SR', 'Sênior'),
        ('SP', 'Especialista'),
        ('GR', 'Gerente'),
        ('DR', 'Diretor')
    ])
    
    def __str__(self):
        return f"{self.nome} - {self.get_nivel_display()}"

class Funcionario(models.Model):
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Solteiro(a)'),
        ('C', 'Casado(a)'),
        ('D', 'Divorciado(a)'),
        ('V', 'Viúvo(a)')
    ]
    
    TIPO_CONTRATO_CHOICES = [
        ('CLT', 'CLT'),
        ('PJ', 'Pessoa Jurídica'),
        ('EST', 'Estagiário'),
        ('TMP', 'Temporário')
    ]

    # Informações Pessoais
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL_CHOICES)
    numero_filhos = models.IntegerField(default=0)
    
    # Documentos
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    carteira_trabalho = models.CharField(max_length=20)
    pis = models.CharField(max_length=20)
    
    # Contato
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Informações Profissionais
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    data_admissao = models.DateField()
    tipo_contrato = models.CharField(max_length=3, choices=TIPO_CONTRATO_CHOICES)
    status = models.CharField(max_length=1, choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A')
    
    # Informações Bancárias
    banco = models.CharField(max_length=100)
    agencia = models.CharField(max_length=10)
    conta = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome_completo

class Beneficio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=[
        ('VR', 'Vale Refeição'),
        ('VT', 'Vale Transporte'),
        ('PS', 'Plano de Saúde'),
        ('PO', 'Plano Odontológico'),
        ('SV', 'Seguro de Vida'),
        ('OUT', 'Outros')
    ])
    
    def __str__(self):
        return self.nome

class BeneficioFuncionario(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    beneficio = models.ForeignKey(Beneficio, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    valor_customizado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def valor_atual(self):
        return self.valor_customizado or self.beneficio.valor

class FolhaPagamento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)
    mes_referencia = models.IntegerField()
    ano_referencia = models.IntegerField()
    data_pagamento = models.DateField()
    
    # Rendimentos
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extras = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adicional_noturno = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gratificacoes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Descontos
    inss = models.DecimalField(max_digits=10, decimal_places=2)
    irrf = models.DecimalField(max_digits=10, decimal_places=2)
    faltas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    atrasos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Totais
    total_rendimentos = models.DecimalField(max_digits=10, decimal_places=2)
    total_descontos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['funcionario', 'mes_referencia', 'ano_referencia']
    
    def calcular_inss(self):
        """Cálculo do INSS conforme tabela atual de Angola"""
        salario = self.salario_base
        if salario <= Decimal('35000'):
            return salario * Decimal('0.03')
        elif salario <= Decimal('45000'):
            return salario * Decimal('0.07')
        elif salario <= Decimal('65000'):
            return salario * Decimal('0.08')
        else:
            return salario * Decimal('0.09')
    
    def calcular_irrf(self):
        """Cálculo do IRT (Imposto sobre Rendimento do Trabalho) de Angola"""
        base_calculo = self.salario_base - self.inss
        if base_calculo <= Decimal('35000'):
            return Decimal('0')
        elif base_calculo <= Decimal('45000'):
            return base_calculo * Decimal('0.07')
        elif base_calculo <= Decimal('65000'):
            return base_calculo * Decimal('0.15')
        elif base_calculo <= Decimal('200000'):
            return base_calculo * Decimal('0.20')
        else:
            return base_calculo * Decimal('0.25')
    
    def calcular_totais(self):
        self.total_rendimentos = (
            self.salario_base +
            self.horas_extras +
            self.adicional_noturno +
            self.gratificacoes
        )
        
        self.inss = self.calcular_inss()
        self.irrf = self.calcular_irrf()
        
        self.total_descontos = (
            self.inss +
            self.irrf +
            self.faltas +
            self.atrasos
        )
        
        self.valor_liquido = self.total_rendimentos - self.total_descontos
    
    def save(self, *args, **kwargs):
        self.calcular_totais()
        super().save(*args, **kwargs)

class Ferias(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('AGENDADA', 'Agendada'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada')
    ])
    observacoes = models.TextField(blank=True)

class FaltaLicenca(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=[
        ('FALTA', 'Falta'),
        ('ATESTADO', 'Atestado Médico'),
        ('LICENCA', 'Licença')
    ])
    data_inicio = models.DateField()
    data_fim = models.DateField()
    justificativa = models.TextField()
    documento = models.FileField(upload_to='documentos/faltas/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDENTE', 'Pendente'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada')
    ])

class HoraExtra(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField()
    horas = models.DecimalField(max_digits=4, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=[
        ('NORMAL', '50%'),
        ('DOMINGO', '100%'),
        ('FERIADO', '100%')
    ])
    justificativa = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('PENDENTE', 'Pendente'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada')
    ])
    
    def calcular_valor(self):
        valor_hora = self.funcionario.cargo.salario_base / Decimal('220')  # 220 = horas mensais
        multiplicador = Decimal('1.5') if self.tipo == 'NORMAL' else Decimal('2.0')
        return valor_hora * self.horas * multiplicador

class Treinamento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    instrutor = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    carga_horaria = models.IntegerField()
    local = models.CharField(max_length=200)
    participantes = models.ManyToManyField(Funcionario, through='ParticipacaoTreinamento')
    status = models.CharField(max_length=20, choices=[
        ('AGENDADO', 'Agendado'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado')
    ])

class ParticipacaoTreinamento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    treinamento = models.ForeignKey(Treinamento, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('INSCRITO', 'Inscrito'),
        ('CONFIRMADO', 'Confirmado'),
        ('CONCLUIDO', 'Concluído'),
        ('REPROVADO', 'Reprovado'),
        ('DESISTENTE', 'Desistente')
    ])
    nota = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    certificado = models.FileField(upload_to='certificados/', null=True, blank=True)

class DocumentoRH(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[
        ('CONTRATO', 'Contrato de Trabalho'),
        ('ADVERTENCIA', 'Advertência'),
        ('PROMOCAO', 'Promoção'),
        ('FERIAS', 'Férias'),
        ('OUTROS', 'Outros')
    ])
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='documentos/rh/')
    data_upload = models.DateTimeField(auto_now_add=True)
    data_validade = models.DateField(null=True, blank=True) 