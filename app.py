# Usar venv para rodar o arquvio, e a extensão thunder client para testar as requisições
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, flash # type: ignore


# Dados é outro script com uma estrutura de dados simples
import dados
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minhachave'

def formatar(valor):
    chaves = ["isbn","titulo","autor","genero","ano_publicacao","editora","paginas","status","localizacao"]
    valor = [dict(zip(chaves, tupla)) for tupla in valor]
    return valor

biblioteca = formatar(database.lista_livro())

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/biblioteca', methods=['GET', 'POST'])
def interface_web(message = None, status = None):
    ## função para gerenciamento de interface web
    valor = request.args.get('valor')
    if valor and valor != "":
        return redirect(url_for('pesquisa_livro', valor=valor))
    
    if message and status:
        flash(message, status)
    
    biblioteca = database.lista_livro()
    return render_template('biblioteca.html', biblioteca=formatar(biblioteca))

@app.route('/biblioteca/<valor>', methods=['GET'])
def pesquisa_livro(valor):
    #Lista livors
    if valor:
        biblioteca = database.pesquisar_livro((valor,))
        if biblioteca:
            return render_template('biblioteca.html',biblioteca = formatar(biblioteca)), 200
        else:
            flash('Livro não localizado', 'info')
            return redirect(url_for('interface_web'))
    else:
        return render_template('biblioteca.html',biblioteca = biblioteca), 200

@app.route('/biblioteca/criar', methods=['GET','POST'])
def cria_livro():
    if request.method == 'POST':
        alteracoes = (
            request.form.get('isbn'),
            request.form.get('titulo'),
            request.form.get('autor'),
            request.form.get('genero'),
            request.form.get('ano_publicacao'),
            request.form.get('editora'),
            request.form.get('paginas'),
            request.form.get('status'),
            request.form.get('localizacao')
        )

        alterado = database.criar_livro(alteracoes)
        if alterado > 0:
            flash('Livro criado com sucesso', 'success')
            return redirect(url_for('interface_web'))
        flash('Não foi possível criar um livro', 'error')
        return redirect(url_for('interface_web')) 
    else:
        return render_template('criar_livro.html')

@app.route('/biblioteca/excluir/<isbn>', methods=['POST'])
def exclui_livro(isbn):
    alterado = database.excluir_livro((isbn,))
    if alterado > 0:
        flash('Livro excluido com sucesso', 'success')
    else:
        flash('Livro não encontrado', 'info')
    return redirect(url_for('interface_web'))

@app.route('/biblioteca/atualizar/<isbn>', methods=['GET', 'POST'])
def atualiza_livro(isbn):
    if request.method == 'GET':
        biblioteca = database.pesquisar_livro((isbn,))
        biblioteca = formatar(biblioteca)
        print(biblioteca)
        return render_template('editar_livro.html', livro=biblioteca[0])

    if request.method == 'POST':
        alteracoes = (
            request.form.get('titulo'),
            request.form.get('autor'),
            request.form.get('genero'),
            request.form.get('ano_publicacao'),
            request.form.get('editora'),
            request.form.get('paginas'),
            request.form.get('status'),
            request.form.get('localizacao'),
            request.form.get('isbn')
        )
        alterado = database.editar_livro(alteracoes)
        if alterado > 0:
            flash('Livro alterado com sucesso', 'success')
            return redirect(url_for('interface_web'))
        flash('Livro não localizado', 'info')
        return redirect(url_for('interface_web')) 


# Por padrão o método é GET

# Roda o APP
if __name__ == '__main__':
    app.run(debug=True)