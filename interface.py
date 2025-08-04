import tkinter as tk
from tkinter import ttk, messagebox as mb, filedialog as fd
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from datetime import date, datetime

# Importando a logica refatorada
from logica import SistemaDeRegistro

# --- Cores ---
co0 = "#2e2d2b"
co1 = "#feffff"
co2 = "#e5e5e5"
co3 = "#00a095"
co4 = "#403d3d"
co5 = "#38576b"
co6 = "#146C94"
co7 = "#ef5350"
co8 = "#263238"
co9 = "#a85585"

class App:
    def __init__(self, master: tk.Tk):
        self.master = master

        # --- TIPOS ---
        self.e_nome: tk.Entry
        self.e_email: tk.Entry
        self.e_telefone: tk.Entry
        self.c_sexo: ttk.Combobox
        self.data_nascimento: DateEntry
        self.e_endereco: tk.Entry
        self.c_curso: ttk.Combobox
        self.arvore_aluno: ttk.Treeview
        self.l_imagem: tk.Label
        self.botao_carregar: tk.Button
        self.e_procurar: tk.Entry

        self.master.title("Sistema de Registro de Alunos")
        self.master.geometry('820x535')
        self.master.configure(background=co1)
        self.master.resizable(width=False, height=False)

        # Instância da lógica do banco de dados
        self.db = SistemaDeRegistro()

        # Variável de estado para o caminho da imagem (gerenciada pela classe)
        self.caminho_da_imagem = ""
        
        # Atributos para PhotoImage que precisam ser mantidos
        self.foto_aluno = None
        self.app_lg_foto = None
        self.img_add = None
        self.img_update = None
        self.img_delete = None

        # Aplica o estilo ttk
        style = ttk.Style(self.master)
        style.theme_use("clam")

        # Chama os métodos para criar a interface
        self._criar_frames()
        self._criar_widgets_logo()
        self._criar_widgets_detalhes()
        self._criar_widgets_botoes()
        self._criar_tabela()

        # Preenche a tabela com os dados iniciais
        self.mostrar_alunos()

    def _criar_frames(self):
        self.frame_logo = tk.Frame(self.master, width=820, height=52, background=co6)
        self.frame_logo.grid(row=0, column=0, columnspan=2)

        self.frame_botoes_e_busca = tk.Frame(self.master, width=280, background=co1)
        self.frame_botoes_e_busca.grid(row=1, column=0, sticky='ns', padx=5, pady=5)

        self.frame_detalhes = tk.Frame(self.master, width=535, background=co1, relief='solid', borderwidth=1)
        self.frame_detalhes.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

        self.frame_tabela = tk.Frame(self.master, background=co1)
        self.frame_tabela.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
        
        # Configura o redimensionamento da janela
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def _criar_widgets_logo(self):
        try:
            app_lg_img = Image.open('logo.png').resize((50, 50))
            self.app_lg_foto = ImageTk.PhotoImage(app_lg_img)
            tk.Label(self.frame_logo, image=self.app_lg_foto, text=" Sistema de Registro de Alunos", compound=tk.LEFT, anchor=tk.NW, font=('Ivy 16 bold'), bg=co6, fg=co1).place(x=5, y=0, relheight=1)
        except FileNotFoundError:
            tk.Label(self.frame_logo, text=" Sistema de Registro de Alunos", anchor=tk.NW, font=('Ivy 16 bold'), bg=co6, fg=co1).place(x=5, y=10)

    def _criar_widgets_detalhes(self):
        # --- Coluna da Esquerda ---
        tk.Label(self.frame_detalhes, text="Nome *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=10, y=10)
        self.e_nome = tk.Entry(self.frame_detalhes, width=30, justify=tk.LEFT, relief='solid')
        self.e_nome.place(x=10, y=35)

        tk.Label(self.frame_detalhes, text="Email *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=10, y=70)
        self.e_email = tk.Entry(self.frame_detalhes, width=30, justify=tk.LEFT, relief='solid')
        self.e_email.place(x=10, y=95)

        tk.Label(self.frame_detalhes, text="Telefone *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=10, y=130)
        self.e_telefone = tk.Entry(self.frame_detalhes, width=20, justify=tk.LEFT, relief='solid')
        self.e_telefone.place(x=10, y=155)

        tk.Label(self.frame_detalhes, text="Sexo *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=170, y=130)
        self.c_sexo = ttk.Combobox(self.frame_detalhes, width=8, font=('Ivy 8 bold'), justify='center')
        self.c_sexo['values'] = ('M', 'F', 'Outro')
        self.c_sexo.place(x=170, y=155)

        # --- Coluna do Meio ---
        tk.Label(self.frame_detalhes, text="Data de Nascimento *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=270, y=10)
        self.data_nascimento = DateEntry(self.frame_detalhes, width=18, justify=tk.LEFT, borderwidth=2, year=date.today().year)
        self.data_nascimento.place(x=270, y=35)

        tk.Label(self.frame_detalhes, text="Endereço *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=270, y=70)
        self.e_endereco = tk.Entry(self.frame_detalhes, width=20, justify=tk.LEFT, relief='solid')
        self.e_endereco.place(x=270, y=95)

        cursos = ['Engenharia Elétrica', 'Finanças', 'Economia', 'Odontologia', 'Psicologia', 'Medicina', 'Música']
        tk.Label(self.frame_detalhes, text="Curso *", anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4).place(x=270, y=130)
        self.c_curso = ttk.Combobox(self.frame_detalhes, width=20, font=('Ivy 8 bold'), values=cursos)
        self.c_curso.place(x=270, y=155)

        # --- Coluna da Direita (Imagem) ---
        self.l_imagem = tk.Label(self.frame_detalhes, bg=co1)
        self.l_imagem.place(x=420, y=10)
        self.botao_carregar = tk.Button(self.frame_detalhes, command=self.escolher_imagem, text="CARREGAR IMAGEM", width=20, compound=tk.CENTER, anchor=tk.CENTER, font=('Ivy 7 bold'))
        self.botao_carregar.place(x=420, y=155)
        self.limpar_campos()

    def _criar_widgets_botoes(self):
        # Frame de busca
        frame_procurar = tk.Frame(self.frame_botoes_e_busca, background=co1, relief='groove', borderwidth=1)
        frame_procurar.pack(fill='x', padx=10, pady=10)
        tk.Label(frame_procurar, text="Procurar Aluno (por ID)", anchor=tk.W, font=('Ivy 10 bold'), bg=co1, fg=co4).pack(fill='x', padx=5)
        
        frame_busca_interno = tk.Frame(frame_procurar, bg=co1)
        frame_busca_interno.pack(fill='x', padx=5, pady=5)
        self.e_procurar = tk.Entry(frame_busca_interno, width=10, justify=tk.CENTER, relief='solid', font=('Ivy 10 bold'))
        self.e_procurar.pack(side='left', padx=5)
        tk.Button(frame_busca_interno, command=self.procurar, text="Procurar", width=9, font=('Ivy 8 bold')).pack(side='left', padx=5)

        # Frame dos botões de ação
        frame_acoes = tk.Frame(self.frame_botoes_e_busca, background=co1)
        frame_acoes.pack(fill='x', padx=10, pady=10)

        try:
            self.img_add = ImageTk.PhotoImage(Image.open('add.png').resize((20, 20)))
            self.img_update = ImageTk.PhotoImage(Image.open('update.png').resize((20, 20)))
            self.img_delete = ImageTk.PhotoImage(Image.open('delete.png').resize((20, 20)))
        except FileNotFoundError:
            self.img_add = self.img_update = self.img_delete = None
        
        tk.Button(frame_acoes, command=self.adicionar, image=self.img_add, text=" Adicionar", width=100, relief='groove', compound=tk.LEFT, anchor=tk.W, font=('Ivy 11')).pack(fill='x', pady=4)
        tk.Button(frame_acoes, command=self.atualizar, image=self.img_update, text=" Atualizar", width=100, relief='groove', compound=tk.LEFT, anchor=tk.W, font=('Ivy 11')).pack(fill='x', pady=4)
        tk.Button(frame_acoes, command=self.deletar, image=self.img_delete, text=" Deletar", width=100, relief='groove', compound=tk.LEFT, anchor=tk.W, font=('Ivy 11')).pack(fill='x', pady=4)

    def _criar_tabela(self):
        lista_cabeca = ['ID', 'Nome', 'Email', 'Telefone', 'Sexo', 'Nascimento', 'Endereço', 'Curso']
        self.arvore_aluno = ttk.Treeview(self.frame_tabela, selectmode='extended', columns=lista_cabeca, show='headings')
        vsb = ttk.Scrollbar(self.frame_tabela, orient='vertical', command=self.arvore_aluno.yview)
        hsb = ttk.Scrollbar(self.frame_tabela, orient='horizontal', command=self.arvore_aluno.xview)
        self.arvore_aluno.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.arvore_aluno.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        self.frame_tabela.grid_rowconfigure(0, weight=1)
        self.frame_tabela.grid_columnconfigure(0, weight=1)
        
        w = [40, 150, 150, 90, 50, 90, 120, 120]
        for i, col in enumerate(lista_cabeca):
            self.arvore_aluno.heading(col, text=col.title(), anchor='center')
            self.arvore_aluno.column(col, width=w[i], anchor='center', minwidth=w[i])
        
        self.arvore_aluno.bind('<Double-1>', self.mostrar_dados_selecionados)

    # --- MÉTODOS DE LÓGICA DA INTERFACE ---

    def limpar_campos(self, limpar_busca=False):
        self.e_nome.delete(0, tk.END)
        self.e_email.delete(0, tk.END)
        self.e_telefone.delete(0, tk.END)
        self.c_sexo.set('')
        self.data_nascimento.set_date(date.today())
        self.e_endereco.delete(0, tk.END)
        self.c_curso.set('')
        self.caminho_da_imagem = ""
        if limpar_busca:
            self.e_procurar.delete(0, tk.END)
        
        try:
            img_padrao = Image.open('logo.png').resize((130, 130))
            self.foto_aluno = ImageTk.PhotoImage(img_padrao)
            self.l_imagem.config(image=self.foto_aluno)
        except FileNotFoundError:
            pass
        self.botao_carregar.config(text="CARREGAR IMAGEM")

    def escolher_imagem(self):
        caminho = fd.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if not caminho:
            return
        
        self.caminho_da_imagem = caminho
        img = Image.open(caminho).resize((130, 130))
        self.foto_aluno = ImageTk.PhotoImage(img)
        self.l_imagem.config(image=self.foto_aluno)
        self.botao_carregar.config(text="TROCAR DE FOTO")

    def mostrar_alunos(self):
        for i in self.arvore_aluno.get_children():
            self.arvore_aluno.delete(i)
        
        lista_dados = self.db.ver_todos_os_estudantes()
        if lista_dados:
            for item in lista_dados:
                self.arvore_aluno.insert('', 'end', values=item)

    def adicionar(self):
        nome = self.e_nome.get().strip()
        email = self.e_email.get().strip()
        telefone = self.e_telefone.get().strip()
        sexo = self.c_sexo.get()
        data = self.data_nascimento.get_date()
        endereco = self.e_endereco.get().strip()
        curso = self.c_curso.get()

        if not all([nome, email, telefone, sexo, endereco, curso]):
            mb.showerror("Erro de Validação", "Por favor, preencha todos os campos obrigatórios.")
            return

        img_para_salvar = self.caminho_da_imagem if self.caminho_da_imagem else "logo.png"
        dados = [nome, email, telefone, sexo, data, endereco, curso, img_para_salvar]

        if self.db.registro_de_estudante(dados):
            mb.showinfo("Sucesso", "Estudante registrado com sucesso!")
            self.limpar_campos()
            self.mostrar_alunos()
        else:
            mb.showerror("Erro no Banco", "Não foi possível registrar o estudante.\nO email informado pode já estar em uso.")

    def atualizar(self):
        try:
            id_aluno = int(self.e_procurar.get())
        except ValueError:
            mb.showerror("Erro", "ID de busca inválido. Por favor, procure um aluno primeiro.")
            return

        nome = self.e_nome.get().strip()
        email = self.e_email.get().strip()
        telefone = self.e_telefone.get().strip()
        sexo = self.c_sexo.get()
        data = self.data_nascimento.get_date()
        endereco = self.e_endereco.get().strip()
        curso = self.c_curso.get()

        if not all([nome, email, telefone, sexo, endereco, curso]):
            mb.showerror("Erro de Validação", "Por favor, preencha todos os campos do formulário.")
            return

        img_para_salvar = self.caminho_da_imagem if self.caminho_da_imagem else "logo.png"
        dados_atualizados = [nome, email, telefone, sexo, data, endereco, curso, img_para_salvar, id_aluno]

        if self.db.atualizar_estudantes(dados_atualizados):
            mb.showinfo("Sucesso", f"Estudante com ID {id_aluno} atualizado com sucesso!")
            self.limpar_campos(limpar_busca=True)
            self.mostrar_alunos()
        else:
            mb.showerror("Erro no Banco", "Não foi possível atualizar o estudante.")

    def procurar(self):
        try:
            id_aluno = int(self.e_procurar.get())
        except ValueError:
            mb.showerror("Erro", "Por favor, digite um ID numérico válido.")
            return

        dados = self.db.procurar_estudante(id_aluno)
        if not dados:
            mb.showerror("Não Encontrado", f"Nenhum aluno com ID {id_aluno} foi encontrado.")
            return
        
        self.limpar_campos()
        
        self.e_nome.insert(0, dados[1])
        self.e_email.insert(0, dados[2])
        self.e_telefone.insert(0, dados[3])
        self.c_sexo.set(dados[4])
        try:
            data_db = datetime.strptime(str(dados[5]), '%Y-%m-%d').date()
            self.data_nascimento.set_date(data_db)
        except (ValueError, TypeError):
            self.data_nascimento.set_date(date.today())
        self.e_endereco.insert(0, dados[6])
        self.c_curso.set(dados[7])
        
        self.caminho_da_imagem = dados[8]
        try:
            img = Image.open(self.caminho_da_imagem).resize((130, 130))
            self.foto_aluno = ImageTk.PhotoImage(img)
            self.l_imagem.config(image=self.foto_aluno)
            self.botao_carregar.config(text="TROCAR DE FOTO")
        except FileNotFoundError:
            mb.showwarning("Aviso", f"Imagem não encontrada no caminho: {self.caminho_da_imagem}")

    def deletar(self):
        try:
            id_aluno = int(self.e_procurar.get())
        except ValueError:
            mb.showerror("Erro", "ID de busca inválido. Por favor, procure um aluno antes de deletar.")
            return

        if mb.askyesno("Confirmar", f"Tem certeza que deseja deletar o estudante com ID {id_aluno}?"):
            if self.db.deletar_estudantes(id_aluno):
                mb.showinfo("Sucesso", "Estudante deletado com sucesso!")
                self.limpar_campos(limpar_busca=True)
                self.mostrar_alunos()
            else:
                mb.showerror("Erro", "Não foi possível deletar o estudante.")

    def mostrar_dados_selecionados(self, _event):
        try:
            item_selecionado = self.arvore_aluno.focus()
            if not item_selecionado: return
            valores = self.arvore_aluno.item(item_selecionado, 'values')
            id_aluno = valores[0]
            self.e_procurar.delete(0, tk.END)
            self.e_procurar.insert(0, id_aluno)
            self.procurar()
        except IndexError:
            pass