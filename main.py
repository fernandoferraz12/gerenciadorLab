import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Configuração do banco de dados SQLite
DB_FILE = "equipamentos.db"


# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tabela Equipamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento TEXT NOT NULL,
            fornecedor TEXT NOT NULL
        )
    ''')

    # Tabela Manutenção
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Manutencao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            ocorrencia TEXT NOT NULL,
            anexo TEXT,
            FOREIGN KEY (equipamento_id) REFERENCES Equipamentos (id)
        )
    ''')

    conn.commit()
    conn.close()


# Função para adicionar um equipamento
def add_equipamento(equipamento, fornecedor):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Equipamentos (equipamento, fornecedor) VALUES (?, ?)", (equipamento, fornecedor))
    conn.commit()
    conn.close()


# Função para obter todos os equipamentos
def get_equipamentos():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Equipamentos")
    equipamentos = cursor.fetchall()
    conn.close()
    return equipamentos


# Função para adicionar manutenção
def add_manutencao(equipamento_id, data, ocorrencia, anexo):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Manutencao (equipamento_id, data, ocorrencia, anexo) VALUES (?, ?, ?, ?)",
        (equipamento_id, data, ocorrencia, anexo)
    )
    conn.commit()
    conn.close()


# Função para obter dados de manutenção
def get_manutencao():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = '''
        SELECT m.id, e.equipamento, m.data, m.ocorrencia, m.anexo
        FROM Manutencao m
        JOIN Equipamentos e ON m.equipamento_id = e.id
    '''
    cursor.execute(query)
    manutencoes = cursor.fetchall()
    conn.close()
    return manutencoes


# Inicializar o banco de dados
init_db()

# Configuração do layout do Streamlit
st.title("Sistema de Manutenção de Equipamentos")

menu = st.sidebar.radio("Menu", ["Equipamentos", "Manutenção", "Visualizar Dados"])

# Seção para gerenciar equipamentos
if menu == "Equipamentos":
    st.header("Cadastro de Equipamentos")

    with st.form("form_equipamento"):
        equipamento = st.text_input("Nome do Equipamento")
        fornecedor = st.text_input("Fornecedor")
        submitted = st.form_submit_button("Adicionar Equipamento")

        if submitted:
            if equipamento and fornecedor:
                add_equipamento(equipamento, fornecedor)
                st.success("Equipamento adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    # Mostrar tabela de equipamentos
    st.subheader("Equipamentos Cadastrados")
    equipamentos = get_equipamentos()
    if equipamentos:
        df_equipamentos = pd.DataFrame(equipamentos, columns=["ID", "Equipamento", "Fornecedor"])
        st.dataframe(df_equipamentos)
    else:
        st.info("Nenhum equipamento cadastrado ainda.")

# Seção para gerenciar manutenção
elif menu == "Manutenção":
    st.header("Cadastro de Manutenção")

    equipamentos = get_equipamentos()
    if equipamentos:
        with st.form("form_manutencao"):
            equipamento_selecionado = st.selectbox("Selecione o Equipamento", [(e[0], e[1]) for e in equipamentos])
            data = st.date_input("Data da Manutenção", datetime.now())
            ocorrencia = st.text_area("Ocorrência")
            anexo = st.file_uploader("Anexar Arquivo", type=["png", "jpg", "pdf", "docx", "xlsx"])
            submitted = st.form_submit_button("Adicionar Manutenção")

            if submitted:
                anexo_path = None
                if anexo:
                    upload_dir = "uploads"
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    anexo_path = os.path.join(upload_dir, anexo.name)
                    with open(anexo_path, "wb") as f:
                        f.write(anexo.getbuffer())

                add_manutencao(equipamento_selecionado[0], data.strftime("%Y-%m-%d"), ocorrencia, anexo_path)
                st.success("Manutenção adicionada com sucesso!")
    else:
        st.warning("Nenhum equipamento cadastrado. Cadastre um equipamento primeiro.")

# Seção para visualizar os dados
elif menu == "Visualizar Dados":
    st.header("Manutenções Registradas")

    manutencoes = get_manutencao()
    if manutencoes:
        df_manutencao = pd.DataFrame(
            manutencoes,
            columns=["ID", "Equipamento", "Data", "Ocorrência", "Anexo"]
        )
        st.dataframe(df_manutencao)
    else:
        st.info("Nenhuma manutenção registrada ainda.")

