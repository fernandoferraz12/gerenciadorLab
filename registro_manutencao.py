import sqlite3
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def registro_manutencao():
    st.subheader("Registro de Manutenção")

    # **Criar pasta para uploads**
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # **Criar tabela no banco de dados**
    def create_database():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS manutencoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipamento TEXT NOT NULL,
                data_manutencao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                horas_parado INTEGER NOT NULL,
                os TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # **CRUD - Manutenção**
    def add_manutencao(equipamento, data_manutencao, tipo, horas_parado, os_path):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO manutencoes (equipamento, data_manutencao, tipo, horas_parado, os)
            VALUES (?, ?, ?, ?, ?)
        ''', (equipamento, data_manutencao, tipo, horas_parado, os_path))
        conn.commit()
        conn.close()

    def get_all_manutencoes():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM manutencoes ORDER BY id DESC')
        records = cursor.fetchall()
        conn.close()
        return records

    def update_manutencao(record_id, equipamento, data_manutencao, tipo, horas_parado, os_path):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE manutencoes
            SET equipamento = ?, data_manutencao = ?, tipo = ?, horas_parado = ?, os = ?
            WHERE id = ?
        ''', (equipamento, data_manutencao, tipo, horas_parado, os_path, record_id))
        conn.commit()
        conn.close()

    def delete_manutencao(record_id):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM manutencoes WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    # **Criar tabelas**
    create_database()

    # **Buscar equipamentos disponíveis**
    def get_equipamentos():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT equipamento FROM equipamentos ORDER BY equipamento')
        equipamentos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return equipamentos

    # **Gerenciar estado**
    if "show_form_manutencao" not in st.session_state:
        st.session_state.show_form_manutencao = False
    if "edit_mode_manutencao" not in st.session_state:
        st.session_state.edit_mode_manutencao = False
    if "record_id_manutencao" not in st.session_state:
        st.session_state.record_id_manutencao = None

    # **Botão para abrir o formulário**
    if st.button("NOVA MANUTENÇÃO", key="new_manutencao"):
        st.session_state.show_form_manutencao = True
        st.session_state.edit_mode_manutencao = False
        st.session_state.record_id_manutencao = None

        # Resetar campos
        st.session_state.equipamento = ""
        st.session_state.data_manutencao = None
        st.session_state.tipo = ""
        st.session_state.horas_parado = 0
        st.session_state.os = None

    # **Exibir Formulário**
    if st.session_state.show_form_manutencao or st.session_state.edit_mode_manutencao:
        st.subheader("Cadastro de Manutenção" if not st.session_state.edit_mode_manutencao else "Editar Manutenção")

        with st.form(key="form_manutencao", clear_on_submit=False):
            equipamento = st.selectbox("Equipamento", [""] + get_equipamentos(),
                                       index=([""] + get_equipamentos()).index(st.session_state.get("equipamento", ""))
                                       if st.session_state.edit_mode_manutencao else 0)

            data_manutencao = st.date_input("Data da Manutenção",
                                            value=st.session_state.get("data_manutencao", None))

            tipo = st.selectbox("Tipo", ["", "PREVENTIVA", "CORRETIVA"],
                                index=["", "PREVENTIVA", "CORRETIVA"].index(st.session_state.get("tipo", ""))
                                if st.session_state.edit_mode_manutencao else 0)

            horas_parado = st.number_input("Horas Parado", min_value=0, value=st.session_state.get("horas_parado", 0))

            os_uploaded = st.file_uploader("Anexar OS (PDF ou Imagem)", type=["pdf", "jpg", "jpeg", "png"])
            os_path = st.session_state.get("os", None)

            # **Salvar arquivo**
            if os_uploaded:
                os_path = os.path.join(UPLOAD_FOLDER, os_uploaded.name)
                with open(os_path, "wb") as f:
                    f.write(os_uploaded.getbuffer())

            # ✅ Permitir que o usuário baixe o arquivo salvo


            col1, col2 = st.columns([1, 1])
            with col1:
                salvar_button = st.form_submit_button("Salvar", type="primary")

            # ✅ Garantir que sempre há um botão de submissão
            fechar_button = st.form_submit_button("Fechar") if not st.session_state.edit_mode_manutencao else None

            if salvar_button:
                formatted_date = data_manutencao.strftime("%d/%m/%Y") if data_manutencao else ""

                if st.session_state.edit_mode_manutencao:
                    update_manutencao(st.session_state.record_id_manutencao, equipamento, formatted_date, tipo, horas_parado, os_path)
                    st.success("Registro atualizado com sucesso!")
                else:
                    add_manutencao(equipamento, formatted_date, tipo, horas_parado, os_path)
                    st.success("Manutenção registrada com sucesso!")

                st.session_state.show_form_manutencao = False
                st.session_state.edit_mode_manutencao = False
                st.rerun()

            if fechar_button:
                st.session_state.show_form_manutencao = False
                st.session_state.edit_mode_manutencao = False
                st.rerun()

        # ✅ Exibir o botão de download fora do st.form()
        if st.session_state.get("os"):
            os_path = st.session_state["os"]
            file_name = os_path.split("/")[-1]  # Obtém apenas o nome do arquivo

            with open(os_path, "rb") as file:
                st.download_button(
                    label=f"⬇️ Baixar {file_name}",  # 🔥 Nome dinâmico do arquivo
                    data=file,
                    file_name=file_name,
                    mime="application/octet-stream"
                )

    # **Filtros**
    st.subheader("Filtros")
    col1, col2, col3 = st.columns(3)

    with col1:
        filtro_equipamento = st.text_input("Filtrar por Equipamento:")
    with col2:
        filtro_tipo = st.selectbox("Filtrar por Tipo:", ["", "PREVENTIVA", "CORRETIVA"], index=0)
    with col3:
        filtro_data = st.date_input("Filtrar por Data:", value=None)

    # **Aplicar filtros**
    df_filtrado = pd.DataFrame(get_all_manutencoes(), columns=[
        "ID", "Equipamento", "Data Manutenção", "Tipo", "Horas Parado", "OS"
    ])


    ## parte nova ate aqui

    # **Aplicar filtros**
    if not df_filtrado.empty:
        if filtro_equipamento:
            df_filtrado = df_filtrado[df_filtrado["Equipamento"].str.contains(filtro_equipamento, case=False, na=False)]
        if filtro_data:
            df_filtrado = df_filtrado[df_filtrado["Data Manutenção"] == filtro_data.strftime("%d/%m/%Y")]
        if filtro_tipo:
            df_filtrado = df_filtrado[df_filtrado["Tipo"] == filtro_tipo]
        
    # **Verificar se há registros após aplicar filtros**
    if df_filtrado.empty:
        st.info("Nenhum registro encontrado.")
    else:
        st.subheader("Registros de Manutenção")

        # ✅ **Cabeçalho da tabela**
        st.markdown("""
           <div style="display: flex; font-weight: bold; padding: 10px 5px; border-bottom: 2px solid #ddd;">
               <div style="flex: 2;">Equipamento</div>
               <div style="flex: 2;">Data Manutenção</div>
               <div style="flex: 2;">Tipo</div>
               <div style="flex: 2;">Horas Parado</div>
               <div style="flex: 1.5; text-align: center;">Ações</div>
           </div>
           """, unsafe_allow_html=True)

        # **Exibir registros**
        for index, row in df_filtrado.iterrows():
            background_color = "#f9f9f9" if index % 2 == 0 else "#ffffff"

            cols = st.columns([7, 1, 1])
            with cols[0]:
                os_link = f'<a href="{row["OS"]}" target="_blank">📎 Ver OS</a>' if row["OS"] else "Nenhum"

                st.markdown(f"""
                       <div style="background-color: {background_color}; padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #ddd;">
                           <div style="flex: 2;">{row['Equipamento']}</div>
                           <div style="flex: 2;">{row['Data Manutenção']}</div>
                           <div style="flex: 2;">{row['Tipo']}</div>
                           <div style="flex: 2;">{row['Horas Parado']} horas</div>
                       </div>
                   """, unsafe_allow_html=True)

            with cols[1]:
                if st.button("✏️", key=f"edit_manutencao_{index}"):
                    st.session_state.update({

                        "equipamento": row["Equipamento"],
                        "data_manutencao": datetime.strptime(row["Data Manutenção"], "%d/%m/%Y").date(),
                        "tipo": row["Tipo"],
                        "horas_parado": row["Horas Parado"],
                        "os": row["OS"],  # ✅ OS só aparece no formulário ao editar
                        "show_form_manutencao": True,
                        "edit_mode_manutencao": True
                    })
                    st.rerun()

            with cols[2]:
                if st.button("🗑️", key=f"delete_manutencao_{index}"):
                    delete_manutencao(row["ID"])
                    st.warning("Registro deletado!")
                    st.rerun()


