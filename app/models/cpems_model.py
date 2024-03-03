from datetime import datetime
from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "tb_usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(length=100), nullable=True)
    siape = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    nr_telefone = db.Column(db.String(length=30), nullable=False)
    senha = db.Column(db.String(length=60), nullable=False)
    tipo_acesso = db.Column(db.String(length=50), nullable=False)
    # Renomeamos o backref para serem únicos
    processos_responsavel = db.relationship('Processos', foreign_keys='Processos.responsavel_demanda',
                                            backref='responsavel_demanda_user', lazy=True)
    processos_criador = db.relationship('Processos', foreign_keys='Processos.criador_id', backref='criador_processos',
                                        lazy=True)
    processos_conclusao = db.relationship('Processos', foreign_keys='Processos.responsavel_conclusao_demanda',
                                          backref='conclusao_processos', lazy=True)

    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')

    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)


class Processos(db.Model):
    __tablename__ = "tb_processos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nr_processo = db.Column(db.String(50), nullable=False, unique=True)
    nome = db.Column(db.String(200), nullable=True)
    cpf = db.Column(db.String(20), nullable=True)
    tipo_determinacao = db.Column(db.String(60), nullable=False)
    protocolo_pat = db.Column(db.Integer, nullable=True)
    status_pat = db.Column(db.String(20), nullable=True)
    nome_responsavel_pat = db.Column(db.String(80), nullable=True)
    nome_unidade_pat = db.Column(db.String(100), nullable=True)
    nome_servico_pat = db.Column(db.String(100), nullable=True)
    autoridade_coatora = db.Column(db.String(100), nullable=True)
    vara_origem = db.Column(db.String(100), nullable=True)
    fase_demanda = db.Column(db.String(100), nullable=True)
    prioridade_demanda = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.String(1024), nullable=True)
    prazo_dias = db.Column(db.Integer, nullable=True)
    data_intimacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_prazo = db.Column(db.DateTime)
    data_cadastro = db.Column(db.DateTime)
    data_atribuicao = db.Column(db.DateTime)
    data_cumprimento = db.Column(db.DateTime)
    responsavel_demanda = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id'), nullable=True)
    criador_id = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id'), nullable=False)
    responsavel_conclusao_demanda = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id'), nullable=True)
    despacho = db.relationship('Despacho', backref='processo', lazy=True)

    def __repr__(self):
        return f"processos{self.nome}"


class Designados(db.Model):
    __tablename__ = "tb_designados"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_servidor = db.Column(db.String(80), nullable=False)
    siape_servidor = db.Column(db.Integer, nullable=False)
    contato_servidor = db.Column(db.String(20), nullable=False)
    email_servidor = db.Column(db.String(length=50), nullable=False, unique=False)
    unidade_servidor = db.Column(db.String(20), nullable=False)
    gex_servidor = db.Column(db.String(20), nullable=False)
    email_sard_servidor = db.Column(db.String(length=50), nullable=False, unique=False)
    email_gex_servidor = db.Column(db.String(length=50), nullable=False, unique=False)
    afastamento_servidor = db.Column(db.String(length=3), default=False, nullable=False)
    competencias = db.relationship('Competencias', backref='designado', lazy=True)
    siape_id_servidor = db.Column(db.Integer, db.ForeignKey('tb_id_servidores.siape_servidor'))


class Competencias(db.Model):
    __tablename__ = 'tb_competencias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_designado = db.Column(db.Integer, db.ForeignKey('tb_designados.id'))
    competencia = db.Column(db.String(length=100))

class DbRequests(db.Model):
    __tablename__ = "tb_requests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    acao = db.Column(db.String(length=100))
    data_requisicao = db.Column(db.DateTime)
    processo_id = db.Column(db.Integer, db.ForeignKey('tb_processos.id'), nullable=False)
    protocolo_pat = db.Column(db.Integer, nullable=True)
    resposta = db.Column(db.String(length=100))
    id_tarefa = db.Column(db.Integer, nullable=True)
    codigo_unidade = db.Column(db.String(length=30))
    nome_unidade = db.Column(db.String(length=200))
    nome_servico = db.Column(db.String(length=250))
    status_tarefa = db.Column(db.String(length=50))
    interessados = db.Column(db.String(length=100))
    responsaveis = db.Column(db.String(length=100))
    responsaveis_siape = db.Column(db.String(length=100))
    subtarefas_pendentes = db.Column(db.String(length=300))
    processo = db.relationship('Processos', backref='requests', lazy=True)


class IdServidores(db.Model):
    __tablename__ = 'tb_id_servidores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servidor = db.Column(db.Integer, )
    siape_servidor = db.Column(db.Integer, unique=True)  # Garantindo unicidade do siape_servidor
    nome_servidor = db.Column(db.String(length=100))
    designacao = db.relationship('Designados', backref='servidor',
                                 uselist=False)  # Relacionamento inverso para Designados


class Ferias(db.Model):
    __tablename__ = 'tb_ferias'
    id = db.Column(db.Integer, primary_key=True)
    designado_id = db.Column(db.Integer, db.ForeignKey('tb_designados.id'), nullable=False)
    # Períodos aquisitivos
    periodo_1_inicio = db.Column(db.Date, nullable=True)
    periodo_1_fim = db.Column(db.Date, nullable=True)
    periodo_2_inicio = db.Column(db.Date, nullable=True)
    periodo_2_fim = db.Column(db.Date, nullable=True)
    periodo_3_inicio = db.Column(db.Date, nullable=True)
    periodo_3_fim = db.Column(db.Date, nullable=True)
    periodo_4_inicio = db.Column(db.Date, nullable=True)
    periodo_4_fim = db.Column(db.Date, nullable=True)
    # Relacionamento com a tabela Designado
    designado = db.relationship('Designados', backref='ferias')

class Atribuicoes(db.Model):
    __tablename__ = 'tb_atribuicoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_designado = db.Column(db.Integer, db.ForeignKey('tb_designados.id'))
    nome_servico = db.Column(db.String(length=250))
    dt_atribuicao = db.Column(db.Date, nullable=True)

class Despacho(db.Model):
    __tablename__ = 'tb_despacho'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    processo_id = db.Column(db.Integer, db.ForeignKey('tb_processos.id'), nullable=False)
    data_despacho = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.Text, nullable=False)
    responsavel_despacho = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id'), nullable=False)
    responsavel = db.relationship('User', backref='despachos', lazy=True)
