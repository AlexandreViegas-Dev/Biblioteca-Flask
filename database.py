import sqlite3
#DDL
def ddl():
    query = """CREATE TABLE IF NOT EXISTS livros (
    isbn TEXT PRIMARY KEY,
    titulo TEXT,
    autor TEXT,
    genero TEXT,
    ano_publicacao INT,
    editora TEXT,
    paginas INT,
    status TEXT,
    localizacao TEXT
    );
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#DML
def dml():
    query = """INSERT INTO livros (isbn, titulo, autor)
    VALUES ('qualquer', 'qualquer titulo', 'qualquer autor');
    """

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def dql():
    query = """SELECT * FROM livros WHERE isbn = 'qualquer';
    """

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    #result = cursor.fetchone() #mostra um registro
    result = cursor.fetchall()
    print(result)
    conn.close()

def dele():
    query = """DROP TABLE livros;
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def lista_livro():
    query = """SELECT * FROM livros ORDER BY titulo"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    #result = cursor.fetchone() #mostra um registro
    result = cursor.fetchall()
    print(result)
    conn.close()
    return(result)

def criar_livro(args):

    query = """INSERT INTO livros VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    linhas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas

def editar_livro(args):
    query = """UPDATE livros SET 
    titulo = ?,
    autor = ?,
    genero = ?,
    ano_publicacao = ?,
    editora = ?,
    paginas = ?,
    status = ?,
    localizacao = ?
    WHERE isbn = ?"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    linhas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas

def pesquisar_livro(args):
    query = f"""SELECT * FROM livros WHERE isbn = ?;
    """

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall() #mostra um registro
    conn.close()
    return result

def excluir_livro(args):
    query = """DELETE FROM livros WHERE isbn = ?"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    linhas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas

if __name__ == '__main__':
    pesquisar_livro(("978-6555945638",))