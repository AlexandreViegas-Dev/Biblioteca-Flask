from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, flash # type: ignore


# Dados é outro script com uma estrutura de dados simples
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minhachave'

@app.route('/<nome>')
def meu_nome(nome=None):
    return render_template('meunome.html', nome=nome)

@app.route('/name')
def namedefault():
    return "Olá, eu não sou o Goku!"

# um nome entre <> indica uma variável, que será passada para o programa
@app.route('/name/<nome>', methods = ['GET', 'POST'])
def name(nome):
    return f"Olá, eu não sou o {nome}!"

@app.route('/biblioteca/<isbn>', methods=['GET', 'DELETE', 'PUT'])
def manipula_livro(isbn=None):
    #Lista livors
    if request.method == 'GET':
        print("Get")
        if isbn:
            for l in biblioteca:
                if l['isbn'] == isbn:
                    return jsonify(l)
            return jsonify("message: livro não localizado"), 404
        else:
            return render_template('biblioteca.html',biblioteca = biblioteca), 200

    #insere livro
    elif request.method == 'POST':
        print("Post")
        novo_livro = request.get_json()
        for l in biblioteca:
            if l['isbn'] == novo_livro['isbn']:
                return jsonify("Livro já cadastrado"), 200
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("Livro cadastrado com sucesso"), 201

    #Deleta livros
    elif request.method == 'DELETE':
        print("Delete")
        for l in biblioteca:
            if l['isbn'] == isbn:
                biblioteca.remove(l)
                dados.salvar_no_arquivo(biblioteca)
                return render_template('biblioteca.html',biblioteca = biblioteca), 200
            return jsonify("message: livro não localizado"), 404

    #Alteração de livros
    elif request.method == 'PUT':
        alteracoes = request.get_json()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                for key, value in alteracoes.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("mensagem: livro alterado com sucesso"), 200
        return jsonify("message: livro não localizado"), 404
    else:
        return 'Solicitação não aceita', 503