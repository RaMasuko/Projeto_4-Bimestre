from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from app.models.carta_preco import CartaPreco
from app.utils.auth_middleware import login_required

carta_bp = Blueprint('carta', __name__)

@carta_bp.route('/cartas')
@login_required
def index():
    busca = request.args.get('busca', '').strip()
    cartas = CartaPreco.listar_por_usuario(g.usuario.id, busca=busca)
    valor_total = sum(c.preco_estimado for c in cartas)
    return render_template('cartas.html', cartas=cartas, busca=busca, valor_total=valor_total)


@carta_bp.route('/cartas/nova', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        nome_carta = request.form.get('nome_carta', '').strip()
        colecao = request.form.get('colecao', '').strip()
        raridade = request.form.get('raridade', '').strip()
        preco_raw = request.form.get('preco_estimado', '').replace(',', '.').strip()

        if not nome_carta or len(nome_carta) < 2 or len(nome_carta) > 80:
            flash("O nome da carta é obrigatório (entre 2 e 80 caracteres).", "error")
            return render_template('nova_carta.html', nome_carta=nome_carta, colecao=colecao, raridade=raridade, preco_estimado=preco_raw)

        if not colecao:
            flash("Informe a coleção da carta.", "error")
            return render_template('nova_carta.html', nome_carta=nome_carta, colecao=colecao, raridade=raridade, preco_estimado=preco_raw)

        try:
            preco_estimado = float(preco_raw)
            if preco_estimado < 0:
                raise ValueError()
        except ValueError:
            flash("Informe um valor numérico válido e não negativo para o preço.", "error")
            return render_template('nova_carta.html', nome_carta=nome_carta, colecao=colecao, raridade=raridade, preco_estimado=preco_raw)

        nova_carta = CartaPreco(
            nome_carta=nome_carta,
            colecao=colecao,
            raridade=raridade or 'Comum',
            preco_estimado=preco_estimado,
            usuario_id=g.usuario.id
        )
        nova_carta.salvar()
        current_app.logger.info(f"Cotação da carta '{nome_carta}' cadastrada pelo usuário ID {g.usuario.id}")
        flash("Cotação de carta cadastrada com sucesso!", "success")
        return redirect(url_for('carta.index'))

    return render_template('nova_carta.html')


@carta_bp.route('/cartas/<int:carta_id>/editar', methods=['GET', 'POST'])
@login_required
def edit(carta_id):
    carta = CartaPreco.buscar_por_id(carta_id, g.usuario.id)

    if not carta:
        flash("Carta não encontrada ou permissão negada.", "error")
        return redirect(url_for('carta.index'))

    if request.method == 'POST':
        nome_carta = request.form.get('nome_carta', '').strip()
        colecao = request.form.get('colecao', '').strip()
        raridade = request.form.get('raridade', '').strip()
        preco_raw = request.form.get('preco_estimado', '').replace(',', '.').strip()

        if not nome_carta or len(nome_carta) < 2 or len(nome_carta) > 80 or not colecao:
            flash("Preencha nome da carta e coleção corretamente.", "error")
            return render_template('editar_carta.html', carta=carta)

        try:
            preco_estimado = float(preco_raw)
            if preco_estimado < 0:
                raise ValueError()
        except ValueError:
            flash("Informe um valor numérico válido para o preço.", "error")
            return render_template('editar_carta.html', carta=carta)

        carta.nome_carta = nome_carta
        carta.colecao = colecao
        carta.raridade = raridade or 'Comum'
        carta.preco_estimado = preco_estimado
        carta.salvar()
        current_app.logger.info(f"Cotação da carta ID {carta.id} atualizada pelo usuário ID {g.usuario.id}")
        flash("Cotação atualizada com sucesso!", "success")
        return redirect(url_for('carta.index'))

    return render_template('editar_carta.html', carta=carta)


@carta_bp.route('/cartas/<int:carta_id>/excluir', methods=['POST'])
@login_required
def delete(carta_id):
    carta = CartaPreco.buscar_por_id(carta_id, g.usuario.id)

    if not carta:
        flash("Carta não encontrada ou permissão negada.", "error")
        return redirect(url_for('carta.index'))

    nome_removido = carta.nome_carta
    carta.excluir()
    current_app.logger.info(f"Cotação '{nome_removido}' (ID {carta_id}) excluída pelo usuário ID {g.usuario.id}")
    flash("Cotação excluída com sucesso!", "success")
    return redirect(url_for('carta.index'))
