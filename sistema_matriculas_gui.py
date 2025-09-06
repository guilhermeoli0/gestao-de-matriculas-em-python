# sistema_matriculas_gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# --- ARQUIVOS DE DADOS ---
ARQUIVO_ALUNOS = "alunos.txt"
ARQUIVO_CURSOS = "cursos.txt"
ARQUIVO_TURMAS = "turmas.txt"
ARQUIVO_MATRICULAS = "matriculas.txt"

# --- LISTAS PARA ARMAZENAR DADOS ---
alunos = []
cursos = []
turmas = []
matriculas = []

# --- FUNÇÕES PARA CARREGAR DADOS DOS ARQUIVOS ---
def carregar_dados():
    if os.path.exists(ARQUIVO_ALUNOS):
        with open(ARQUIVO_ALUNOS, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(" | ")
                    aluno = {
                        "id": int(partes[0]),
                        "nome": partes[1],
                        "cpf": partes[2],
                        "rg": partes[3],
                        "nascimento": partes[4]
                    }
                    alunos.append(aluno)

    if os.path.exists(ARQUIVO_CURSOS):
        with open(ARQUIVO_CURSOS, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(" | ")
                    curso = {
                        "id": int(partes[0]),
                        "nome": partes[1],
                        "carga_horaria": partes[2]
                    }
                    cursos.append(curso)

    if os.path.exists(ARQUIVO_TURMAS):
        with open(ARQUIVO_TURMAS, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(" | ")
                    curso_encontrado = None
                    for c in cursos:
                        if c["nome"] == partes[2]:
                            curso_encontrado = c
                            break
                    if not curso_encontrado:
                        curso_encontrado = {"id": 0, "nome": partes[2], "carga_horaria": "0"}

                    turma = {
                        "id": int(partes[0]),
                        "nome": partes[1],
                        "curso": curso_encontrado,
                        "horario": partes[3],
                        "professor": partes[4],
                        "limite": int(partes[5]),
                        "alunos": []
                    }
                    turmas.append(turma)

    if os.path.exists(ARQUIVO_MATRICULAS):
        with open(ARQUIVO_MATRICULAS, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(" | ")
                    aluno_id = int(partes[1])
                    turma_id = int(partes[2])

                    aluno = None
                    for a in alunos:
                        if a["id"] == aluno_id:
                            aluno = a
                            break

                    turma = None
                    for t in turmas:
                        if t["id"] == turma_id:
                            turma = t
                            break

                    if aluno and turma:
                        turma["alunos"].append(aluno)
                        matriculas.append({"aluno_id": aluno_id, "turma_id": turma_id})

# --- FUNÇÕES PARA SALVAR DADOS ---
def salvar_aluno_txt(aluno):
    with open(ARQUIVO_ALUNOS, "a", encoding="utf-8") as f:
        f.write(f"{aluno['id']} | {aluno['nome']} | {aluno['cpf']} | {aluno['rg']} | {aluno['nascimento']}\n")

def salvar_curso_txt(curso):
    with open(ARQUIVO_CURSOS, "a", encoding="utf-8") as f:
        f.write(f"{curso['id']} | {curso['nome']} | {curso['carga_horaria']}\n")

def salvar_turma_txt(turma):
    with open(ARQUIVO_TURMAS, "a", encoding="utf-8") as f:
        f.write(f"{turma['id']} | {turma['nome']} | {turma['curso']['nome']} | {turma['horario']} | {turma['professor']} | {turma['limite']}\n")

def salvar_matricula_txt(aluno_id, turma_id):
    with open(ARQUIVO_MATRICULAS, "a", encoding="utf-8") as f:
        f.write(f"{len(matriculas)+1} | {aluno_id} | {turma_id}\n")

# --- FUNÇÕES DE AÇÃO ---
def cadastrar_aluno():
    nome = simpledialog.askstring("Cadastro", "Nome do aluno:")
    if not nome: return
    cpf = simpledialog.askstring("Cadastro", "CPF:")
    if not cpf: return
    rg = simpledialog.askstring("Cadastro", "RG:")
    nascimento = simpledialog.askstring("Cadastro", "Data de nascimento (ex: 01/01/2000):")

    for a in alunos:
        if a["cpf"] == cpf:
            messagebox.showerror("Erro", "CPF já cadastrado!")
            return

    novo_id = len(alunos) + 1
    aluno = {"id": novo_id, "nome": nome, "cpf": cpf, "rg": rg, "nascimento": nascimento}
    alunos.append(aluno)
    salvar_aluno_txt(aluno)
    messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado!")

def cadastrar_curso():
    nome = simpledialog.askstring("Curso", "Nome do curso:")
    if not nome: return
    carga = simpledialog.askstring("Curso", "Carga horária (horas):") or "0"

    for c in cursos:
        if c["nome"].lower() == nome.lower():
            messagebox.showerror("Erro", "Curso já existe!")
            return

    novo_id = len(cursos) + 1
    curso = {"id": novo_id, "nome": nome, "carga_horaria": carga}
    cursos.append(curso)
    salvar_curso_txt(curso)
    messagebox.showinfo("Sucesso", f"Curso '{nome}' cadastrado!")

def criar_turma():
    if len(cursos) == 0:
        messagebox.showwarning("Atenção", "Cadastre um curso primeiro!")
        return

    curso_nomes = [c["nome"] for c in cursos]
    curso_escolhido = simpledialog.askstring("Turma", f"Escolha um curso:\n" + "\n".join(curso_nomes))
    curso = None
    for c in cursos:
        if c["nome"] == curso_escolhido:
            curso = c
            break
    if not curso:
        messagebox.showerror("Erro", "Curso inválido!")
        return

    nome_turma = simpledialog.askstring("Turma", "Nome da turma (ex: Turma A):")
    horario = simpledialog.askstring("Turma", "Horário das aulas:")
    professor = simpledialog.askstring("Turma", "Nome do professor:")
    try:
        limite = int(simpledialog.askstring("Turma", "Limite de alunos (padrão 30):") or "30")
    except:
        limite = 30

    novo_id = len(turmas) + 1
    turma = {
        "id": novo_id,
        "nome": nome_turma,
        "curso": curso,
        "horario": horario,
        "professor": professor,
        "limite": limite,
        "alunos": []
    }
    turmas.append(turma)
    salvar_turma_txt(turma)
    messagebox.showinfo("Sucesso", f"Turma '{nome_turma}' criada!")

def matricular_aluno():
    if len(alunos) == 0:
        messagebox.showwarning("Atenção", "Nenhum aluno cadastrado.")
        return
    if len(turmas) == 0:
        messagebox.showwarning("Atenção", "Nenhuma turma criada.")
        return

    aluno_nomes = [f"{a['id']} - {a['nome']}" for a in alunos]
    aluno_str = simpledialog.askstring("Matrícula", f"Escolha o aluno:\n" + "\n".join(aluno_nomes))
    try:
        aluno_id = int(aluno_str.split(" - ")[0])
    except:
        messagebox.showerror("Erro", "Selecione um aluno válido.")
        return

    aluno = None
    for a in alunos:
        if a["id"] == aluno_id:
            aluno = a
            break
    if not aluno:
        messagebox.showerror("Erro", "Aluno não encontrado.")
        return

    turma_desc = []
    for t in turmas:
        vagas = t["limite"] - len(t["alunos"])
        status = "✅" if vagas > 0 else "❌"
        turma_desc.append(f"{t['id']} - {t['nome']} ({t['curso']['nome']}) - {status}")
    
    turma_str = simpledialog.askstring("Matrícula", f"Escolha a turma:\n" + "\n".join(turma_desc))
    try:
        turma_id = int(turma_str.split(" - ")[0])
    except:
        messagebox.showerror("Erro", "Selecione uma turma válida.")
        return

    turma = None
    for t in turmas:
        if t["id"] == turma_id:
            turma = t
            break
    if not turma:
        messagebox.showerror("Erro", "Turma não encontrada.")
        return

    if len(turma["alunos"]) >= turma["limite"]:
        messagebox.showerror("Erro", "Turma está cheia!")
        return

    if aluno in turma["alunos"]:
        messagebox.showwarning("Atenção", "Aluno já matriculado!")
        return

    turma["alunos"].append(aluno)
    salvar_matricula_txt(aluno_id, turma_id)
    messagebox.showinfo("Sucesso", f"{aluno['nome']} matriculado na turma {turma['nome']}!")

def listar_alunos():
    if not alunos:
        msg = "Nenhum aluno cadastrado."
    else:
        msg = "📋 ALUNOS CADASTRADOS:\n\n"
        for a in alunos:
            msg += f"ID: {a['id']} | {a['nome']} | CPF: {a['cpf']}\n"
    messagebox.showinfo("Alunos", msg)

def listar_cursos():
    if not cursos:
        msg = "Nenhum curso cadastrado."
    else:
        msg = "📘 CURSOS CADASTRADOS:\n\n"
        for c in cursos:
            msg += f"ID: {c['id']} | {c['nome']} | Carga: {c['carga_horaria']}h\n"
    messagebox.showinfo("Cursos", msg)

def listar_turmas():
    if not turmas:
        msg = "Nenhuma turma criada."
    else:
        msg = "🏫 TURMAS:\n\n"
        for t in turmas:
            vagas = t["limite"] - len(t["alunos"])
            msg += f"ID: {t['id']} | {t['nome']} | Curso: {t['curso']['nome']}\n"
            msg += f"  Horário: {t['horario']} | Professor: {t['professor']}\n"
            msg += f"  Alunos: {len(t['alunos'])}/{t['limite']} | Vagas: {vagas}\n\n"
    messagebox.showinfo("Turmas", msg)

# --- INTERFACE GRÁFICA COM DESIGN MELHORADO ---
def main():
    carregar_dados()

    janela = tk.Tk()
    janela.title("🎓 Sistema de Gestão de Matrículas")
    janela.geometry("500x600")
    janela.resizable(True, True)  # Permite redimensionar nas direções horizontal e vertical
    janela.configure(bg="#f8f9fa")

    # --- Título Principal ---
    frame_top = tk.Frame(janela, bg="#343a40", height=80)
    frame_top.pack(fill="x")
    frame_top.pack_propagate(False)

    titulo = tk.Label(
        frame_top,
        text="Sistema de Matrículas",
        font=("Helvetica", 18, "bold"),
        bg="#343a40",
        fg="white"
    )
    subtitulo = tk.Label(
        frame_top,
        text="©2025 Todos os direitos reservados - Programado por Jorge Oliveira",
        font=("Helvetica", 10),
        bg="#343a40",
        fg="#cccccc"
    )
    titulo.pack(pady=10)
    subtitulo.pack()

    # --- Frame dos Botões ---
    frame_botoes = tk.Frame(janela, bg="#f8f9fa")
    frame_botoes.pack(pady=20, padx=20, fill="both", expand=True)

    # Estilo dos botões
    botoes = [
        ("➕ Cadastrar Aluno", cadastrar_aluno),
        ("📘 Cadastrar Curso", cadastrar_curso),
        ("🏫 Criar Turma", criar_turma),
        ("👥 Matricular Aluno", matricular_aluno),
        ("📋 Listar Alunos", listar_alunos),
        ("📚 Listar Cursos", listar_cursos),
        ("🏫 Listar Turmas", listar_turmas),
    ]

    for texto, comando in botoes:
        btn = tk.Button(
            frame_botoes,
            text=texto,
            command=comando,
            font=("Segoe UI", 11),
            bg="#007BFF",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            relief="flat",
            height=2,
            width=25
        )
        btn.pack(pady=8, ipadx=10)

    # --- RODAPÉ ---
    frame_rodape = tk.Frame(janela, bg="#343a40", height=40)
    frame_rodape.pack(side="bottom", fill="x")

    label_rodape = tk.Label(
        frame_rodape,
        text="©2025 Todos os direitos reservados - Programado por Jorge Oliveira",
        font=("Segoe UI", 9),
        bg="#343a40",
        fg="#cccccc"
    )
    label_rodape.pack(pady=10)

    # --- Mensagem inicial ---
    total_alunos = len(alunos)
    total_cursos = len(cursos)
    total_turmas = len(turmas)
    janela.after(100, lambda: messagebox.showinfo(
        "Bem-vindo!",
        f"Sistema carregado com sucesso!\n"
        f"Alunos: {total_alunos} | Cursos: {total_cursos} | Turmas: {total_turmas}"
    ))

    # Inicia a interface
    janela.mainloop()

# --- EXECUTA O PROGRAMA ---
if __name__ == "__main__":
    main()