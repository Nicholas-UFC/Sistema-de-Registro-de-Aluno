import sqlite3


class SistemaDeRegistro:
    def __init__(self, db_name="estudantes.db"):
        """
        Inicializa a classe, definindo o nome do arquivo do banco de dados.
        """
        self.db_name = db_name
        self._create_table()

    def _execute_query(
        self, query, params=(), commit=False, fetchone=False, fetchall=False
    ):
        """
        Método auxiliar privado para executar todas as consultas de forma segura.
        Ele gerencia a conexão, o cursor, os erros, o commit e a busca de dados.
        """
        try:
            # O uso de 'with' garante que a conexão será fechada automaticamente.
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                # 'with conn:' já faz o commit em caso de sucesso ou rollback em caso de erro.
                if commit:
                    pass

                if fetchone:
                    return cursor.fetchone()

                if fetchall:
                    return cursor.fetchall()

                # Retorna True para operações de escrita (INSERT, UPDATE, DELETE) bem-sucedidas.
                return True

        except sqlite3.Error as e:
            # Em caso de erro, imprime no console para depuração e retorna False.
            print(f"Erro no Banco de Dados: {e}")
            return False

    def _create_table(self):
        query = """CREATE TABLE IF NOT EXISTS estudantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL, -- Garante que cada email seja único
                    telefone TEXT NOT NULL,
                    sexo TEXT NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    curso TEXT NOT NULL,
                    picture TEXT NOT NULL)"""
        self._execute_query(query)

    def registro_de_estudante(self, estudante_data):
        """Insere um novo estudante no banco de dados."""
        query = "INSERT INTO estudantes (nome, email, telefone, sexo, data_nascimento, endereco, curso, picture) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        return self._execute_query(query, estudante_data, commit=True)

    def ver_todos_os_estudantes(self):
        """Retorna todos os estudantes ordenados por nome."""
        query = "SELECT * FROM estudantes ORDER BY nome"
        return self._execute_query(query, fetchall=True)

    def procurar_estudante(self, id):
        """Busca um estudante pelo seu ID."""
        query = "SELECT * FROM estudantes WHERE id=?"
        return self._execute_query(query, (id,), fetchone=True)

    def atualizar_estudantes(self, novos_valores):
        """Atualiza os dados de um estudante existente."""
        query = "UPDATE estudantes SET nome=?, email=?, telefone=?, sexo=?, data_nascimento=?, endereco=?, curso=?, picture=? WHERE id=?"
        return self._execute_query(query, novos_valores, commit=True)

    def deletar_estudantes(self, id):
        """Deleta um estudante pelo seu ID."""
        query = "DELETE FROM estudantes WHERE id=?"
        return self._execute_query(query, (id,), commit=True)
