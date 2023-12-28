from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, BooleanField, SelectField, \
    TextAreaField, HiddenField
from wtforms.validators import Email, DataRequired


def remove_whitespace(form, field):
    if field.data:
        field.data = field.data.replace(" ", "").replace("\t", "").replace("\n", "")


class ProcessosForm(FlaskForm):
    nr_processo_form = StringField(label="Número do Processo Judicial", validators=[DataRequired(), remove_whitespace])
    impetrante_form = StringField(label="Impetrante", validators=[DataRequired()])
    cpf_form = StringField(label="Cpf")
    tipo_determinacao_form = SelectField('Tipo de Determinação',
                                         choices=[('Cumprimento de Sentença', 'Cumprimento de Sentença'),
                                                  ('Prestação de Informações', 'Prestação de Informações')],
                                         validators=[DataRequired()])
    protocolo_pat_form = IntegerField(label="Protocolo PAT")
    status_pat_form = StringField(label="Status PAT")
    nome_responsavel_pat_form = StringField(label="Nome responsável PAT")
    nome_servico_pat_form = StringField(label="Nome do Serviço PAT")
    autoridade_coatora_form = StringField(label="Autoridade Coatora")
    vara_origem_form = StringField(label="Vara de Origem")
    fase_demanda_form = StringField(label="Fase da Demanda")
    prioridade_demanda_form = SelectField(label='Prioridade',
                                          choices=[('Normal', 'Normal'),
                                                   ('Urgente', 'Urgente')])
    data_intimacao_form = DateField(label="Data da Intimação Judicial")
    prazo_demanda_form = IntegerField(label="Prazo da Demanda", validators=[DataRequired()])
    data_fim_prazo_form = DateField(label="Data Final da Demanda", format='%d/%m/%Y')
    data_cadastro_demanda_form = DateField(label="Data cadastro da Demanda")
    data_atribuicao_demanda_form = DateField(label="Data atribuicao da Demanda")
    data_cumprimento_demanda_form = DateField(label="Data de cumprimento da Demanda")
    responsavel_demanda_form = StringField(label="Responsável pela Demanda")
    responsavel_conclusao_demanda_form = StringField(label="Responsável pela Demanda")
    observacoes_form = StringField(label="Observações")


class UsuariosForm(FlaskForm):
    nome_form = StringField(label="Usuário")
    siape_form = IntegerField(label="Siape")
    email_form = StringField(label="Email", validators=[Email(), DataRequired()])
    nr_telefone_form = StringField(label="Telefone")
    senha_form = PasswordField(label="Senha")
    tipo_acesso_form = SelectField('Tipo de Acesso',
                                   choices=[('Estagiário', 'Estagiário'), ('Terceirizado', 'Terceirizado'),
                                            ('Servidor', 'Servidor'), ('Gestor', 'Gestor')])


class DesignadosForm(FlaskForm):
    nome_servidor_form = StringField(label="Nome do Servidor")
    siape_servidor_form = IntegerField(label="SIAPE do Servidor")
    contato_servidor_form = StringField(label="Contato do Servidor")
    email_servidor_form = StringField(label="Email do Servidor")
    unidade_servidor_form = StringField(label="Unidade do Servidor")
    gex_servidor_form = StringField(label="GEX do Servidor")
    email_sard_servidor_form = StringField(label="Email SARH do Servidor")
    email_gex_servidor_form = StringField(label="Email GEX do Servidor")
    afastamento_servidor_form = BooleanField(label="Afastamento do Servidor")
    quantidade_form = IntegerField(label="Quantidade")


class FeriasForm(FlaskForm):
    designado_id = IntegerField(label="Designado ID")
    periodo_1_inicio = DateField(label="Período 1 - Data de Início")
    periodo_1_fim = DateField(label="Período 1 - Data de Fim")
    periodo_2_inicio = DateField(label="Período 2 - Data de Início")
    periodo_2_fim = DateField(label="Período 2 - Data de Fim")
    periodo_3_inicio = DateField(label="Período 3 - Data de Início")
    periodo_3_fim = DateField(label="Período 3 - Data de Fim")
    periodo_4_inicio = DateField(label="Período 4 - Data de Início")
    periodo_4_fim = DateField(label="Período 4 - Data de Fim")


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    # usuario = StringField(label="Usuario", validators=[DataRequired()])
    senha = StringField(label="Senha", validators=[DataRequired()])
    submit = SubmitField(label="Login", validators=[DataRequired()])


class DespachoForm(FlaskForm):
    texto = TextAreaField('Despacho', validators=[DataRequired()])
    submit = SubmitField('Adicionar Despacho')


class Atualiza_Fase(FlaskForm):
    fase_form = SelectField('Fase',
                            choices=[('Aguardando conclusão Subtarefa', 'Aguardando conclusão Subtarefa'), (
                                'Aguardando realização de Perícia Médica agendada',
                                'Aguardando realização de Perícia Médica agendada'), (
                                         'Aguardando Parecer da Àrea Técnica',
                                         'Aguardando Parecer da Àrea Técnica'),
                                     ('Aguardando providências a cargo da GEX',
                                      'Aguardando providências a cargo da GEX'), (
                                         'Aguardando conclusão pelo(a) servidor(a)',
                                         'Aguardando conclusão pelo(a) servidor(a)'), (
                                         'Aguardando Cumprimento de Exigências pel(a) Segurado(a)',
                                         'Aguardando Cumprimento de Exigências pel(a) Segurado(a)'),
                                     ('Aguardando peticionamento', 'Aguardando peticionamento'),
                                     ('Em análise', 'Em análise'), ('Finalizado', 'Finalizado')])
    submit = SubmitField('Atualiza Andamento')


class Finaliza_Processo(FlaskForm):
    id_processo = HiddenField()
    submit = SubmitField('Finaliza')


class AdicionarCompetencia(FlaskForm):
    add_competencia_servidor_form = SelectField('Serviço', choices=[
        ('Acerto para Integração - SIBE', 'Acerto para Integração - SIBE'),
        ('Acertos para análise', 'Acertos para análise'),
        ('Acertos para Marcação de Perícia Médica', 'Acertos para Marcação de Perícia Médica'),
        ('Acréscimo de 25%', 'Acréscimo de 25%'),
        ('Alterar Local ou Forma de Pagamento', 'Alterar Local ou Forma de Pagamento'),
        ('Análise de Acórdão', 'Análise de Acórdão'),
        ('Aposentadoria da Pessoa com Deficiência por Tempo de Contribuição',
         'Aposentadoria da Pessoa com Deficiência por Tempo de Contribuição'),
        ('Aposentadoria por Idade Rural', 'Aposentadoria por Idade Rural'),
        ('Aposentadoria por Idade Urbana', 'Aposentadoria por Idade Urbana'),
        ('Aposentadoria por Tempo de Contribuição', 'Aposentadoria por Tempo de Contribuição'),
        ('Apuração de Irregularidade - MOB Digital', 'Apuração de Irregularidade - MOB Digital'),
        ('Atualizar Cadastro e/ou Benefício', 'Atualizar Cadastro e/ou Benefício'),
        ('Atualizar Procurador e Representante Legal', 'Atualizar Procurador e Representante Legal'),
        ('Atualizar Vínculos e Remunerações e Código de Pagamento',
         'Atualizar Vínculos e Remunerações e Código de Pagamento'),
        ('Auxílio-Acidente', 'Auxílio-Acidente'),
        ('Auxílio-Doença - Rural (Acerto Pós-perícia)', 'Auxílio-Doença - Rural (Acerto Pós-perícia)'),
        ('Auxílio-Doença - Urbano (Acerto Pós-perícia)', 'Auxílio-Doença - Urbano (Acerto Pós-perícia)'),
        ('Auxílio-Reclusão Urbano', 'Auxílio-Reclusão Urbano'),
        ('Benefício Assistencial à Pessoa com Deficiência', 'Benefício Assistencial à Pessoa com Deficiência'),
        ('Benefício Assistencial ao Idoso', 'Benefício Assistencial ao Idoso'),
        ('Certidão de Tempo de Contribuição', 'Certidão de Tempo de Contribuição'),
        ('Cópia de Processo', 'Cópia de Processo'),
        ('Cópia de Processo - Entidade Conveniada', 'Cópia de Processo - Entidade Conveniada'),
        ('Cumprimento de Acórdão com Implantação de Benefício', 'Cumprimento de Acórdão com Implantação de Benefício'),
        ('Cumprimento de Acórdão com Implantação de Benefício/BI',
         'Cumprimento de Acórdão com Implantação de Benefício/BI'),
        ('Cumprimento de Acórdão com Implantação de Benefício/LOAS',
         'Cumprimento de Acórdão com Implantação de Benefício/LOAS'),
        ('Cumprimento de Acórdão sem Implantação de Benefício', 'Cumprimento de Acórdão sem Implantação de Benefício'),
        ('Emissão de Certidão de Tempo de Contribuição - CTC', 'Emissão de Certidão de Tempo de Contribuição - CTC'),
        ('Encaminhamentos do Processo de Apuração - MOB', 'Encaminhamentos do Processo de Apuração - MOB'),
        ('Instrução de Processo de Recurso', 'Instrução de Processo de Recurso'),
        ('Isenção de Imposto de Renda', 'Isenção de Imposto de Renda'),
        ('Marcação, Remarcação, Cancelamento e Consulta de Agendamento',
         'Marcação, Remarcação, Cancelamento e Consulta de Agendamento'),
        ('Pagamento de Benefício Não Recebido', 'Pagamento de Benefício Não Recebido'),
        ('Pagamento de Valor não Recebido até a Data do Óbito do Beneficiário',
         'Pagamento de Valor não Recebido até a Data do Óbito do Beneficiário'),
        ('Pensão por Morte Rural', 'Pensão por Morte Rural'),
        ('Pensão por Morte Urbana', 'Pensão por Morte Urbana'),
        ('Reativar Benefício', 'Reativar Benefício'),
        ('Reativar BPC após Atualização do CADÚnico', 'Reativar BPC após Atualização do CADÚnico'),
        ('Recurso - Cumprimento de Diligência', 'Recurso - Cumprimento de Diligência'),
        ('Renovar Declaração de Cárcere/Reclusão', 'Renovar Declaração de Cárcere/Reclusão'),
        ('Revisão', 'Revisão'),
        ('Revisão - Entidade Conveniada', 'Revisão - Entidade Conveniada'),
        ('Revisão de Certidão de Tempo de Contribuição', 'Revisão de Certidão de Tempo de Contribuição'),
        ('Revisão Extraordinária', 'Revisão Extraordinária'),
        ('Salário-Maternidade Rural', 'Salário-Maternidade Rural'),
        ('Salário-Maternidade Urbano', 'Salário-Maternidade Urbano'),
        ('Solicitar Desistência/Encerramento/Renúncia de Benefício',
         'Solicitar Desistência/Encerramento/Renúncia de Benefício'),
        ('Solicitar Emissão de Pagamento não Recebido', 'Solicitar Emissão de Pagamento não Recebido'),
    ])
    submit = SubmitField('Adicionar Competencia')


class FormDeletarCompetencia(FlaskForm):
    id_competencia = HiddenField()  # Campo oculto para armazenar o ID da competência a ser excluída
    submit = SubmitField('Confirmar Exclusão')  # Botão para confirmar a exclusão


class FormInativarServidor(FlaskForm):
    id_servidor = HiddenField()


class FormReativarServidor(FlaskForm):
    id_servidor = HiddenField()
