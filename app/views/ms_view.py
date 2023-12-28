from datetime import datetime, timedelta
from urllib.parse import quote_plus
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from sqlalchemy import func, or_
import pytz
from app import app
from app import db
from app.forms import ms_form
from app.forms.ms_form import LoginForm, DespachoForm, Atualiza_Fase, AdicionarCompetencia, FormDeletarCompetencia, \
    FormInativarServidor, FormReativarServidor, Finaliza_Processo
from app.models import cpems_model
from app.models.cpems_model import Processos, User, Despacho, Designados, IdServidores, Competencias, DbRequests
import html
import time
import pandas as pd

# Exemplo de DataFrame
data = {
    'Nome': ['João', 'Maria', 'José'],
    'Idade': [25, 30, 28],
    'Cidade': ['São Paulo', 'Rio de Janeiro', 'Salvador']
}

df = pd.DataFrame(data)


@app.route('/exibir-dataframe')
def exibir_dataframe():
    # Convertendo o DataFrame para HTML
    df_html = df.to_html(classes='table table-striped')

    # Renderiza o template e passa o HTML para a página
    return render_template('exibir_dataframe.html', dataframe=df_html)


@app.route("/", methods=["GET", "POST"])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        usuario_logado = User.query.filter_by(email=form_login.email.data).first()  # Alterado para 'email'
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form_login.senha.data):
            login_user(usuario_logado)
            flash(f'Sucesso! Seu login é: {usuario_logado.email}', category='success')  # Alterado para 'email'
            return redirect(url_for('home'))
        else:
            flash('Falha no login. Verifique seu e-mail e senha.', category='danger')

    return render_template("login/login.html", form_login=form_login)


@app.route("/logout", methods={"GET", "POST"})
@login_required
def page_logout():
    logout_user()
    flash("Logout realizado com sucesso.", category='info')
    return redirect(url_for("login"))


@app.route("/base", methods={"GET", "POST"})
@login_required
def base():
    return render_template("base.html")


@app.route("/home", methods={"GET", "POST"})
@login_required
def home():
    processos = Processos.query.filter(
        or_(Processos.fase_demanda != 'Finalizado', Processos.fase_demanda == None)).all()
    urgentes = Processos.query.filter(Processos.prioridade_demanda == 'Urgente').count()
    finalizados = Processos.query.filter(Processos.fase_demanda == 'Finalizado').count()
    tarefas_sem_responsavel = Processos.query.filter(
        or_(Processos.nome_responsavel_pat == None, Processos.nome_responsavel_pat == '')).count()
    meus_processos = cpems_model.Processos.query.filter(
        cpems_model.Processos.responsavel_demanda == current_user.id).order_by(cpems_model.Processos.id).all()

    status_atualizado = {}
    tarefas_pendentes = 0
    tarefas_concluídas = 0

    for processo in processos:
        info_mais_recente = DbRequests.query.filter_by(processo_id=processo.id).order_by(
            DbRequests.data_requisicao.desc()).first()
        if info_mais_recente:
            status_atualizado[processo.id] = {
                'status_tarefa': info_mais_recente.status_tarefa,
                'codigo_unidade': info_mais_recente.codigo_unidade,
                'nome_servico': info_mais_recente.nome_servico,
                'responsaveis': info_mais_recente.responsaveis
            }
            # Conta as tarefas pendentes ou em exigência
            if info_mais_recente.status_tarefa in ['PENDENTE', 'EM EXIGENCIA']:
                tarefas_pendentes += 1
            elif info_mais_recente.status_tarefa in ['CONCLUIDA']:
                tarefas_concluídas += 1
        else:
            status_atualizado[processo.id] = {
                'status_tarefa': '',
                'codigo_unidade': '',
                'nome_servico': '',
                'responsaveis': ''
            }

    return render_template("home/home.html", processos=processos, meus_processos=meus_processos,
                           tarefas_pendentes=tarefas_pendentes, tarefas_concluídas=tarefas_concluídas,
                           tarefas_sem_responsavel=tarefas_sem_responsavel, urgentes=urgentes, finalizados=finalizados,
                           status_atualizado=status_atualizado)


@app.route("/painel-de-controle")
@login_required
def painel_de_controle():
    return render_template("painel_de_controle/painel-de-controle.html")


@app.route("/tarefas-pendentes")
@login_required
def tarefas_pendentes():
    processos = Processos.query.filter(
        or_(Processos.fase_demanda != 'Finalizado', Processos.fase_demanda == None)).all()

    status_atualizado = {}
    for processo in processos:
        info_mais_recente = DbRequests.query.filter_by(processo_id=processo.id).order_by(
            DbRequests.data_requisicao.desc()).first()
        if info_mais_recente:
            status_atualizado[processo.id] = {
                'status_tarefa': info_mais_recente.status_tarefa,
                'codigo_unidade': info_mais_recente.codigo_unidade,
                'nome_servico': info_mais_recente.nome_servico,
                'responsaveis': info_mais_recente.responsaveis
            }
        else:
            status_atualizado[processo.id] = {
                'status_tarefa': '',
                'codigo_unidade': '',
                'nome_servico': '',
                'responsaveis': ''
            }

    return render_template("tabelas/tarefas_pendentes.html", processos=processos, status_atualizado=status_atualizado)


@app.route("/tarefas-concluidas")
@login_required
def tarefas_concluidas():
    processos = Processos.query.filter(
        or_(Processos.fase_demanda != 'Finalizado', Processos.fase_demanda == None)).all()

    status_atualizado = {}
    for processo in processos:
        info_mais_recente = DbRequests.query.filter_by(processo_id=processo.id).order_by(
            DbRequests.data_requisicao.desc()).first()
        if info_mais_recente:
            status_atualizado[processo.id] = {
                'status_tarefa': info_mais_recente.status_tarefa,
                'codigo_unidade': info_mais_recente.codigo_unidade,
                'nome_servico': info_mais_recente.nome_servico,
                'responsaveis': info_mais_recente.responsaveis
            }
        else:
            status_atualizado[processo.id] = {
                'status_tarefa': '',
                'codigo_unidade': '',
                'nome_servico': '',
                'responsaveis': ''
            }

    return render_template("tabelas/tarefas_concluidas.html", processos=processos, status_atualizado=status_atualizado)


@app.route("/tarefas-sem-responsavel")
@login_required
def tarefas_sem_responsavel():
    processos = Processos.query.filter(
        or_(Processos.fase_demanda != 'Finalizado', Processos.fase_demanda == None)).all()

    status_atualizado = {}
    for processo in processos:
        info_mais_recente = DbRequests.query.filter_by(processo_id=processo.id).order_by(
            DbRequests.data_requisicao.desc()).first()
        if info_mais_recente:
            status_atualizado[processo.id] = {
                'status_tarefa': info_mais_recente.status_tarefa,
                'codigo_unidade': info_mais_recente.codigo_unidade,
                'nome_servico': info_mais_recente.nome_servico,
                'responsaveis': info_mais_recente.responsaveis
            }
        else:
            status_atualizado[processo.id] = {
                'status_tarefa': '',
                'codigo_unidade': '',
                'nome_servico': '',
                'responsaveis': ''
            }

    return render_template("tabelas/tarefas_sem_responsavel.html", processos=processos,
                           status_atualizado=status_atualizado)


@app.route("/processos-finalizados")
@login_required
def processos_finalizados():
    processos = Processos.query.filter(Processos.fase_demanda == 'Finalizado').all()
    print(processos)
    return render_template("tabelas/processos_finalizados.html", processos=processos)


@app.route("/designados", methods={"GET", "POST"})
@login_required
def designados():
    tb_designados_servico = Designados.query.all()
    tb_designados_cadastro = Designados.query.all()
    form_inativar_servidor = FormInativarServidor()
    form_reativar_servidor = FormReativarServidor()

    # Consulta ao banco de dados para contar os servidores
    gex_stats = db.session.query(
        Designados.gex_servidor,
        Designados.afastamento_servidor,
        db.func.count(Designados.id).label('count')
    ).group_by(Designados.gex_servidor, Designados.afastamento_servidor).all()

    # Processamento dos dados
    gex_data = {}
    for gex, afastamento, count in gex_stats:
        if gex not in gex_data:
            gex_data[gex] = {'Sim': 0, 'Não': 0, 'Total': 0}
        if afastamento == 'Sim':
            gex_data[gex]['Sim'] += count
        elif afastamento == 'Não':
            gex_data[gex]['Não'] += count
        gex_data[gex]['Total'] += count  # Adiciona a contagem ao total

    # Lógica para contar a quantidade de servidores por serviço de cada GEX.
    competencias_stats = db.session.query(Competencias.competencia,
                                          db.func.count(Competencias.id_designado).label('count')).join(
        Designados).group_by(Competencias.competencia).order_by(db.desc('count')).all()
    competencias_data = {comp: count for comp, count in competencias_stats}

    return render_template("designados/designados.html", competencias_data=competencias_data,
                           tb_designados_servico=tb_designados_servico,
                           tb_designados_cadastro=tb_designados_cadastro, form_inativar_servidor=form_inativar_servidor,
                           form_reativar_servidor=form_reativar_servidor, gex_data=gex_data)


@app.route("/usuarios")
@login_required
def usuarios():
    tb_usuarios = User.query.all()
    return render_template("usuarios/usuarios.html", tb_usuarios=tb_usuarios)


@app.route("/cadastro_servidor", methods={"GET", "POST"})
@login_required
def cadastrar_designado():
    form_designados = ms_form.DesignadosForm()
    print("aqui")
    if form_designados.validate_on_submit():
        print("aqui")
        nome_servidor = form_designados.nome_servidor_form.data
        siape_servidor = form_designados.siape_servidor_form.data
        contato_servidor = form_designados.contato_servidor_form.data
        email_servidor = form_designados.email_servidor_form.data
        unidade_servidor = form_designados.unidade_servidor_form.data
        gex_servidor = form_designados.gex_servidor_form.data
        email_sard_servidor = form_designados.email_sard_servidor_form.data
        email_gex_servidor = form_designados.email_gex_servidor_form.data
        afastamento_servidor = form_designados.afastamento_servidor_form.data
        objeto_designados = cpems_model.Designados(nome_servidor=nome_servidor,
                                                   siape_servidor=siape_servidor,
                                                   contato_servidor=contato_servidor, email_servidor=email_servidor,
                                                   unidade_servidor=unidade_servidor, gex_servidor=gex_servidor,
                                                   email_sard_servidor=email_sard_servidor,
                                                   email_gex_servidor=email_gex_servidor,
                                                   afastamento_servidor=afastamento_servidor)
        try:
            db.session.add(objeto_designados)
            db.session.commit()
            flash(f"Servidor {form_designados.nome_servidor_form.data} cadastrado com sucesso!", category="success")
            return redirect(url_for('cadastrar_designado'))
        except SQLAlchemyError as e:
            flash(f"Erro ao cadastrar Servidor {e}", category="danger")
            db.session.rollback()  # Reverte a transação em caso de erro

    return render_template("cadastro_servidor/cadastro-servidor.html", form_designados=form_designados)


@app.route("/editar-servidor/<int:id>", methods=["POST", "GET"])
@login_required
def editar_servidor(id):
    servidor = cpems_model.Designados.query.get_or_404(id)  # Busca o processo pelo ID
    form_designados = ms_form.DesignadosForm(
        obj=servidor)  # Cria um formulário e preenche com os dados do processo existente
    if form_designados.validate_on_submit():
        try:
            servidor.nome_servidor = form_designados.nome_servidor_form.data
            servidor.siape_servidor = form_designados.siape_servidor_form.data
            servidor.contato_servidor = form_designados.contato_servidor_form.data
            servidor.email_servidor = form_designados.email_servidor_form.data
            servidor.unidade_servidor = form_designados.unidade_servidor_form.data
            servidor.gex_servidor = form_designados.gex_servidor_form.data
            servidor.email_sard_servidor = form_designados.email_sard_servidor_form.data
            servidor.email_gex_servidor = form_designados.email_gex_servidor_form.data
            print("teste2")
            db.session.commit()
            flash(f"Servidor {servidor.nome_servidor} editado com sucesso!", category="success")
        except SQLAlchemyError as e:
            flash(f"Erro ao editar servidor: {e}", category="danger")
            db.session.rollback()
    return render_template("cadastro_servidor/editar-servidor.html", form_designados=form_designados, servidor=servidor)


@app.route("/configurar-competencias/<int:id>", methods=["POST", "GET"])
@login_required
def configurar_competencias(id):
    servidor = cpems_model.Designados.query.get_or_404(id)
    competencias = servidor.competencias
    form_designados = ms_form.DesignadosForm(obj=servidor)
    form_add_competencias = AdicionarCompetencia()
    form_deletar_competencia = FormDeletarCompetencia()

    if form_add_competencias.validate_on_submit():
        try:
            adicionar_competencia(form_add_competencias.add_competencia_servidor_form.data, servidor)
            flash("Serviço incluído com sucesso", category="success")
            return redirect(url_for('configurar_competencias', id=id))
        except IntegrityError as e:
            flash("Erro ao adicionar Serviço: Violação de integridade de dados", category="danger")
            db.session.rollback()
        except Exception as e:
            flash("Erro ao adicionar Serviço. Tente novamente mais tarde.", category="danger")
            db.session.rollback()

    return render_template("designados/configurar_competencias.html",
                           form_designados=form_designados,
                           servidor=servidor,
                           competencias=competencias,
                           form_add_competencias=form_add_competencias,
                           form_deletar_competencia=form_deletar_competencia)


def adicionar_competencia(competencia, servidor):
    nova_competencia = Competencias(competencia=competencia, designado=servidor)
    db.session.add(nova_competencia)
    db.session.commit()


@app.route("/excluir-competencia/<int:id>", methods=["POST"])
@login_required
def excluir_competencia(id):
    form_deletar_competencia = FormDeletarCompetencia()
    try:
        competencia = Competencias.query.get_or_404(id)
        db.session.delete(competencia)
        db.session.commit()
        flash("Serviço excluído com sucesso", category="success")
    except:
        db.session.rollback()
        flash("Erro ao excluir serviço", category="danger")
    return redirect(url_for('configurar_competencias', form_deletar_competencia=form_deletar_competencia,
                            id=competencia.id_designado))


@app.route("/inativar-servidor/<int:id>", methods=["POST"])
@login_required
def inativar_servidor(id):
    form_inativar_servidor = FormInativarServidor()
    designado = cpems_model.Designados.query.get_or_404(id)
    designado.afastamento_servidor = "Sim"
    db.session.commit()
    flash("Servidor inativado com sucesso", category="success")
    return redirect(url_for('designados'))


@app.route("/reativar-servidor/<int:id>", methods=["POST"])
@login_required
def reativar_servidor(id):
    form_reativar_servidor = FormReativarServidor()
    designado = cpems_model.Designados.query.get_or_404(id)
    designado.afastamento_servidor = "Não"
    db.session.commit()
    flash("Servidor reativado com sucesso", category="success")
    return redirect(url_for('designados'))


@app.route("/dashboard")
@login_required
def dashboard():
    # Por exemplo: data = db.session.query(...).all()
    # Por exemplo: chart_data = [ ... ]

    chart_data = {
        'labels': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
        'lineData': [12, 19, 3, 5, 2, 3, 9],
        'pieData': [10, 20, 30, 40],
        'pieLabels': ['Eletrônicos', 'Livros', 'Vestuário', 'Outros'],
        'barData': [21, 15, 7, 8, 12, 9, 4]
    }

    # Transformar os dados em listas separadas para o gráfico de linha
    results = db.session.query(func.count(Processos.id), func.date(Processos.data_cadastro)).group_by(
        func.date(Processos.data_cadastro)).all()
    entrada_processos = [{'Quantidade de Processos': count, 'Data': date.strftime('%d/%m/%Y')} for count, date in
                         results]
    line_labels = [data['Data'] for data in entrada_processos]
    line_data = [data['Quantidade de Processos'] for data in entrada_processos]
    chart_data['labels'] = line_labels
    chart_data['lineData'] = line_data

    # Transformar os dados em listas separadas para o gráfico de Pizza
    results = db.session.query(Processos.tipo_determinacao, func.count(Processos.id)).group_by(
        Processos.tipo_determinacao).all()
    tipo_determinacao = [{'Tipo': html.unescape(tipo), 'Quantidade de Processos': count} for tipo, count in results]
    pie_labels = [data['Tipo'] for data in tipo_determinacao]
    pie_data = [data['Quantidade de Processos'] for data in tipo_determinacao]
    chart_data['pieLabels'] = pie_labels
    chart_data['pieData'] = pie_data

    return render_template("dashboard/dashboard.html", chart_data=chart_data, entrada_processos=entrada_processos,
                           tipo_determinacao=tipo_determinacao)


@app.route("/sql_alchemy")
@login_required
def sql_alchemy():
    data = Processos.query.all()
    # Convertendo os objetos para um formato serializável
    processed_data = [{'Id Processo': processo.id, 'Numero do Processo': processo.nr_processo} for processo in data]

    # Consulta para contar processos protocolados por dia
    results = db.session.query(func.count(Processos.id), func.date(Processos.data_cadastro)).group_by(
        func.date(Processos.data_cadastro)).all()
    entrada_processos = [{'Quantidade de Processos': count, 'Data': date.strftime('%d/%m/%Y')} for count, date in
                         results]

    results = db.session.query(Processos.tipo_determinacao, func.count(Processos.id)).group_by(
        Processos.tipo_determinacao).all()
    tipo_determinacao = [{'Tipo': tipo, 'Quantidade de Processos': count} for tipo, count in results]
    for item in tipo_determinacao:
        item['Tipo'] = html.unescape(item['Tipo'])

    id_servidor = (IdServidores.query.filter_by(siape_servidor=545670).with_entities(IdServidores.id_servidor).scalar())

    if id_servidor is not None:
        print(f"O id_servidor para siape  é: {id_servidor}")
    else:
        print("Não foi encontrado um id_servidor para o siape.")

    # novo_designado = Designados(
    #     servico_servidor='BPC',
    #     nome_servidor='RICARDO ALVES DE OLIVEIRA',
    #     siape_servidor=2035843,
    #     contato_servidor='123456789',
    #     email_servidor='novo@servidor.com',
    #     unidade_servidor='Unidade XYZ',
    #     gex_servidor='GEX XYZ',
    #     email_sard_servidor='sard@novo.com',
    #     email_gex_servidor='gex@novo.com',
    #     afastamento_servidor=False,
    #     quantidade=1,
    #     #id_servidor=666  # Substitua com o ID existente do servidor
    # )
    #
    # db.session.add(novo_designado)
    # db.session.commit()

    # servidor = Designados.query.filter_by(id=344).first()
    #
    # # Adicionar as competências para o servidor
    # competencia_1 = Competencias(competencia='Aposentadoria por Idade Rural', designado=servidor)
    # competencia_2 = Competencias(competencia='Auxílio-Reclusão Urbano', designado=servidor)
    # competencia_3 = Competencias(competencia='Emissão de Certidão de Tempo de Contribuição - CTC', designado=servidor)
    #
    # # Adicionar as competências ao banco de dados
    # db.session.add(competencia_1)
    # db.session.add(competencia_2)
    # db.session.add(competencia_3)
    # db.session.commit()

    return jsonify(tipo_determinacao)


@app.route("/detalhar-processo/<int:id>", methods={"GET", "POST"})
@login_required
def detalhar_processo(id):
    processo = cpems_model.Processos.query.get_or_404(id)
    form = DespachoForm()
    form_atualiza_fase = Atualiza_Fase()
    form_finaliza = Finaliza_Processo()
    atualizacoes = DbRequests.query.filter(DbRequests.processo_id == id).all()

    if form.validate_on_submit():
        data_despacho = datetime.now()
        responsavel_despacho = current_user.id
        despacho = Despacho(processo_id=id, texto=form.texto.data, data_despacho=data_despacho,
                            responsavel_despacho=responsavel_despacho)
        db.session.add(despacho)
        db.session.commit()
        flash('Despacho adicionado com sucesso!', 'success')
        return redirect(url_for('detalhar_processo', id=id))
    return render_template("detalhar_processo/detalhar-processo.html", processo=processo, form=form,
                           form_atualiza_fase=form_atualiza_fase, atualizacoes=atualizacoes,
                           form_finaliza=form_finaliza)


@app.route("/atualiza-fase-processo/<int:id>", methods={"GET", "POST"})
@login_required
def atualiza_fase_processo(id):
    processo = cpems_model.Processos.query.get_or_404(id)
    form_atualiza_fase = Atualiza_Fase()

    if form_atualiza_fase.validate_on_submit():
        processo.fase_demanda = form_atualiza_fase.fase_form.data
        db.session.commit()
        flash('Andamento atualizado com sucesso!', 'success')
        return redirect(url_for('detalhar_processo', id=id))
    return render_template("detalhar_processo/detalhar-processo.html", processo=processo,
                           form_atualiza_fase=form_atualiza_fase)


@app.route("/whatsapp/<int:siape>/<string:nome_servico>/<string:protocolo_pat>/<int:processo_id>", methods=["GET"])
@login_required
def whatsapp(siape, nome_servico, protocolo_pat,processo_id):
    servidor = Designados.query.filter_by(siape_servidor=siape).first()
    nome_servico_formatado = quote_plus(nome_servico)
    protocolo_pat_formatado = quote_plus(protocolo_pat)
    if servidor and servidor.contato_servidor:
        numero_telefone = servidor.contato_servidor.replace(" ", "")
        responsavel = servidor.nome_servidor.replace(" ", "+")
        whatsapp_url = f"https://api.whatsapp.com/send?phone=+55{numero_telefone}&text=Ol%C3%A1+%2A{responsavel}%2A%2C%0A%0AGostaria+de+inform%C3%A1-lo%28a%29+que+a+tarefa+de+%2A{nome_servico_formatado}%2A%2C+n%C3%BAmero+%2A{protocolo_pat_formatado}%2A%2C+relacionada+ao+%2AMandado+de+Seguran%C3%A7a%2A%2C+est%C3%A1+atualmente+sob+sua+responsabilidade.+Caso+voc%C3%AA+esteja+legalmente+impedido%28a%29+de+analis%C3%A1-la+devido+a+algum+afastamento%2C+por+favor%2C+responda+a+esta+mensagem+informando+sobre+essa+situa%C3%A7%C3%A3o."
        return redirect(whatsapp_url)
    else:
        flash("Servidor não encontrado ou sem contato registrado", category="danger")
        return redirect(url_for('detalhar_processo', id=processo_id))




@app.route("/finaliza-processo/<int:id>", methods={"GET", "POST"})
@login_required
def finaliza_processo(id):
    processo = cpems_model.Processos.query.get_or_404(id)
    form_finaliza = Finaliza_Processo()

    if form_finaliza.validate_on_submit():
        processo.responsavel_conclusao_demanda = current_user.id
        processo.data_cumprimento = datetime.now()
        processo.fase_demanda = "Finalizado"
        db.session.commit()
        flash('Processo Finalizado com sucesso!', 'success')
        return redirect(url_for('detalhar_processo', id=id))
    return render_template("detalhar_processo/detalhar-processo.html", processo=processo, form_finaliza=form_finaliza)


@app.route("/puxar_processo", methods={"GET", "POST"})
@login_required
def puxar_processo():
    processo = cpems_model.Processos.query.filter(cpems_model.Processos.responsavel_demanda.is_(None)).order_by(
        cpems_model.Processos.id).first()
    processo.responsavel_demanda = current_user.id
    processo.data_atribuicao = datetime.now()
    db.session.commit()
    flash('Responsável atribuído com sucesso!', 'success')
    return redirect(url_for('detalhar_processo', id=processo.id))


@app.route("/request/<int:id>", methods={"GET", "POST"})
@login_required
def request_tarefa(id):
    processo = cpems_model.Processos.query.get_or_404(id)
    fuso_horario_local = pytz.timezone('America/Sao_Paulo')
    data_requisicao = datetime.now(fuso_horario_local)

    nova_requisicao = DbRequests(
        data_requisicao=data_requisicao,
        processo_id=processo.id,
        protocolo_pat=processo.protocolo_pat,
        responsaveis_siape=0
    )
    db.session.add(nova_requisicao)
    db.session.commit()
    return jsonify({'processo_id': processo.id})


@app.route("/cadastro-usuario", methods={"GET", "POST"})
@login_required
def page_cadastro_usuario():
    form_usuario = ms_form.UsuariosForm()
    if form_usuario.validate_on_submit():
        objeto_usuario = cpems_model.User(
            usuario=form_usuario.nome_form.data,
            siape=form_usuario.siape_form.data,
            email=form_usuario.email_form.data,
            nr_telefone=form_usuario.nr_telefone_form.data,
            senhacrip=form_usuario.senha_form.data,
            tipo_acesso=form_usuario.tipo_acesso_form.data)
        try:
            db.session.add(objeto_usuario)
            db.session.commit()
            flash(f"Usuário {form_usuario.nome_form.data} cadastrado com sucesso!", category="success")
            return redirect(url_for('page_cadastro_usuario'))
        except SQLAlchemyError as e:
            flash(f"Erro ao cadastrar Usuário {e}", category="danger")
            db.session.rollback()  # Reverte a transação em caso de erro
    else:
        pass
    return render_template("cadastro_usuario/cadastro-usuario.html", form_usuario=form_usuario)


@app.route("/cadastrar-processo", methods={"GET", "POST"})
@login_required
def page_cadastrar_processo():
    form = ms_form.ProcessosForm()
    if form.validate_on_submit():
        numero_do_processo = form.nr_processo_form.data
        impetrante = form.impetrante_form.data
        cpf = form.cpf_form.data
        tipo_de_determinacao = form.tipo_determinacao_form.data
        prioridade_demanda = form.prioridade_demanda_form.data
        protocolo_pat = form.protocolo_pat_form.data
        autoridade = form.autoridade_coatora_form.data
        vara = form.vara_origem_form.data
        prazo = form.prazo_demanda_form.data
        data_intimacao = form.data_intimacao_form.data
        data_prazo = data_intimacao + timedelta(days=prazo)
        data_cadastro = datetime.now()
        id_criador = current_user.id
        objeto_processo = cpems_model.Processos(nr_processo=numero_do_processo, nome=impetrante, cpf=cpf,
                                                tipo_determinacao=tipo_de_determinacao,
                                                prioridade_demanda=prioridade_demanda, protocolo_pat=protocolo_pat,
                                                autoridade_coatora=autoridade,
                                                vara_origem=vara, data_cadastro=data_cadastro, criador_id=id_criador,
                                                prazo_dias=prazo, data_prazo=data_prazo)
        try:
            db.session.add(objeto_processo)
            db.session.commit()
            flash(f"Processo {objeto_processo.nr_processo} cadastrado com sucesso!", category="success")
            return redirect(url_for('page_cadastrar_processo'))
        except IntegrityError as e:
            error_message = str(e)
            if "Duplicate entry" in error_message:
                flash("Erro: Processo duplicado. Verifique se o processo já existe.", category="danger")
            else:
                flash(f"Erro ao cadastrar Processo: {error_message}", category="danger")
            db.session.rollback()  # Reverte a transação em caso de erro
        except DataError as e:
            flash(f"Erro:{e}", category="danger")
            db.session.rollback()  # Reverte a transação em caso de erro

    return render_template("cadastro_processo/cadastrar-processo.html", form=form)


@app.route("/editar-processo/<int:id>", methods=["POST", "GET"])
@login_required
def editar_processo(id):
    processo = cpems_model.Processos.query.get_or_404(id)
    form = ms_form.ProcessosForm(obj=processo)

    if request.method == 'GET':
        form.tipo_determinacao_form.data = processo.tipo_determinacao
        form.prioridade_demanda_form.data = processo.prioridade_demanda

    if form.validate_on_submit():
        processo.nr_processo = form.nr_processo_form.data
        processo.nome = form.impetrante_form.data
        processo.cpf = form.cpf_form.data
        processo.tipo_determinacao = form.tipo_determinacao_form.data
        processo.prioridade_demanda = form.prioridade_demanda_form.data
        processo.protocolo_pat = form.protocolo_pat_form.data
        processo.autoridade_coatora = form.autoridade_coatora_form.data
        processo.vara_origem = form.vara_origem_form.data
        processo.prazo_dias = form.prazo_demanda_form.data

        try:
            db.session.commit()
            flash(f"Processo {processo.nr_processo} atualizado com sucesso!", category="success")
            return redirect(url_for('detalhar_processo', id=id))  # Redireciona para outra página após a edição
        except IntegrityError as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash("Erro: Não foi possível atualizar o processo.", category="danger")
        except DataError as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash(f"Erro:{e}", category="danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao editar processo: {e}", "danger")

    return render_template("editar-processo/editar-processo.html", form=form, processo=processo)
