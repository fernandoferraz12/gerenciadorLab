import sqlite3
import streamlit as st

# 📌 Criar banco de dados e tabela (caso não existam)
def create_database():
    conn = sqlite3.connect("crud_app.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links_menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 📌 Funções CRUD
def get_all_links():
    conn = sqlite3.connect("crud_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM links_menu ORDER BY id ASC")
    links = cursor.fetchall()
    conn.close()
    return links

def add_link(nome, url):
    conn = sqlite3.connect("crud_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links_menu (nome, url) VALUES (?, ?)", (nome, url))
    conn.commit()
    conn.close()

def delete_link(link_id):
    conn = sqlite3.connect("crud_app.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM links_menu WHERE id = ?", (link_id,))
    conn.commit()
    conn.close()

# 📌 Interface do Streamlit
def config_links():
    st.title("🔗 Configuração de Links do Menu")

    # 🛠️ Criar o banco de dados caso ainda não exista
    create_database()

    # 📌 Formulário para adicionar novo link
    with st.form(key="form_add_link"):
        nome = st.text_input("Nome do Botão")
        url = st.text_input("URL do Link")

        col1, col2 = st.columns([1, 8])
        with col1:
            salvar_button = st.form_submit_button("Salvar", type="primary")
        with col2:
            fechar_button = st.form_submit_button("Fechar")

    if salvar_button:
        if nome and url:
            add_link(nome, url)
            st.success("✅ Link adicionado com sucesso!")
            st.rerun()
        else:
            st.error("⚠️ Preencha todos os campos!")

    if fechar_button:
        st.rerun()

    # 📌 Exibir os links salvos
    st.subheader("📄 Links Cadastrados")
    links = get_all_links()

    if not links:
        st.info("📌 Nenhum link cadastrado. Adicione novos links acima.")
    else:
        for link in links:
            col1, col2 = st.columns([7, 1])
            with col1:
                st.markdown(f"🔗 [{link[1]}]({link[2]})")
            with col2:
                if st.button("🗑️", key=f"delete_{link[0]}"):
                    delete_link(link[0])
                    st.warning("❌ Link removido!")
                    st.rerun()

if __name__ == "__main__":
    config_links()
