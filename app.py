# Usar venv para rodar o arquvio, e a extensão thunder client para testar as requisições
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, flash # type: ignore


# Dados é outro script com uma estrutura de dados simples
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minhachave'

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/biblioteca', methods=['GET', 'POST'])
def interface_web():
    ## função para gerenciamento de interface web
    valor = request.args.get('valor')
    if valor and valor != "":
        return redirect(url_for('pesquisa_livro', valor=valor))
    biblioteca = dados.carregar_do_arquivo()
    return render_template('biblioteca.html', biblioteca=biblioteca)

@app.route('/biblioteca/<valor>', methods=['GET'])
def pesquisa_livro(valor):
    #Lista livors
    if valor:
        biblioteca = dados.carregar_do_arquivo()
        biblioteca = [livro for livro in biblioteca if livro['isbn'] == valor or livro['titulo'].replace(" ", "_") == valor]
        return render_template('biblioteca.html',biblioteca = biblioteca), 200
    else:
        return render_template('biblioteca.html',biblioteca = biblioteca), 200

@app.route('/biblioteca/criar', methods=['GET','POST'])
def cria_livro():
    if request.method == 'POST':
        novo_livro = {
            'isbn': request.form.get('isbn'),
            'titulo': request.form.get('titulo'),
            'autor': request.form.get('autor'),
            'titulo': request.form.get('titulo'),
            'genero': request.form.get('genero'),
            'ano_publicado': request.form.get('ano_publicado'),
            'editora': request.form.get('editora'),
            'paginas': request.form.get('paginas'),
            'status': request.form.get('status'),
            'localizacao': request.form.get('localizacao')
        }

        for l in biblioteca:
           if l['isbn'] == novo_livro['isbn']:
                return jsonify("Livro já cadastrado"), 200
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return render_template('biblioteca.html', biblioteca=biblioteca)
    else:
        return render_template('criar_livro.html')

@app.route('/biblioteca/excluir/<isbn>', methods=['POST'])
def exclui_livro(isbn):
    biblioteca = dados.carregar_do_arquivo()
    biblioteca = [livro for livro in biblioteca if livro['isbn'] != isbn]
    dados.salvar_no_arquivo(biblioteca)
    return redirect(url_for(interface_web))

@app.route('/biblioteca/atualizar/<isbn>', methods=['GET', 'POST'])
def atualiza_livro(isbn):
    if request.method == 'GET':
        biblioteca = dados.carregar_do_arquivo()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                biblioteca = livro
        return render_template('editar_livro.html', livro=biblioteca)

    if request.method == 'POST':
        biblioteca = dados.carregar_do_arquivo()
        alteracoes = {
            'isbn': request.form.get('isbn'),
            'titulo': request.form.get('titulo'),
            'autor': request.form.get('autor'),
            'titulo': request.form.get('titulo'),
            'genero': request.form.get('genero'),
            'ano_publicacao': request.form.get('ano_publicacao'),
            'editora': request.form.get('editora'),
            'paginas': request.form.get('paginas'),
            'status': request.form.get('status'),
            'localizacao': request.form.get('localizacao')
        }
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                for key, value in alteracoes.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                flash('Livro alterado com sucesso', 'sucess')
                return render_template('biblioteca.html', biblioteca=biblioteca)
        flash('Livro não localizado', 'info')
        return render_template('biblioteca.html', biblioteca=biblioteca)


# Por padrão o método é GET

# Roda o APP
if __name__ == '__main__':
    app.run(debug=True)