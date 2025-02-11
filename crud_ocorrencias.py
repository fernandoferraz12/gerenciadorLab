import sqlite3
import streamlit as st
from datetime import datetime
import pandas as pd
import io

def crud_ocorrencias():
    st.subheader("Ocorrências")

    # Criar banco de dados e tabela
    def create_database():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aberto_por TEXT NOT NULL,
                ocorrencia TEXT NOT NULL,
                data TEXT NOT NULL,
                acao_imediata TEXT NOT NULL,
                avaliado_supervisao TEXT, 
                avaliado_por TEXT, 
                observacoes_supervisao TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # Funções CRUD
    def add_record(aberto_por, ocorrencia, data, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ocorrencias (aberto_por, ocorrencia, data, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (aberto_por, ocorrencia, data, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao))
        conn.commit()
        conn.close()

    def update_record(record_id, aberto_por, ocorrencia, data, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ocorrencias
            SET aberto_por = ?, ocorrencia = ?, data = ?, acao_imediata = ?, 
                avaliado_supervisao = ?, avaliado_por = ?, observacoes_supervisao = ?
            WHERE id = ?
        ''', (aberto_por, ocorrencia, data, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao, record_id))
        conn.commit()
        conn.close()

    def get_all_records():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ocorrencias ORDER BY id DESC')
        records = cursor.fetchall()
        conn.close()
        return records

    def delete_record(record_id):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ocorrencias WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    # Função para gerar e baixar Excel
    def generate_excel():
        df = pd.DataFrame(get_all_records(), columns=[
            "ID", "Aberto por", "Ocorrência", "Data", "Ação Imediata",
            "Avaliado pela Supervisão", "Avaliado por", "Observações da Supervisão"
        ])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Ocorrências")
        output.seek(0)

        return output


    # Criar banco de dados
    create_database()

    # **Resetar o formulário corretamente**
    def reset_form():
        st.session_state.update({
            "show_form": False,
            "edit_mode": False,
            "record_id": None,
            "aberto_por": "",
            "ocorrencia": "",
            "data": None,
            "acao_imediata": "",
            "avaliado_supervisao": "",
            "avaliado_por": "",
            "observacoes_supervisao": ""
        })

    # Inicializar o estado do formulário se não existir
    if "show_form" not in st.session_state:
        reset_form()

    # Criar layout dos botões
    col1, col2 = st.columns([2, 8])  # Ajusta o tamanho das colunas

    with col1:
        if st.button("➕ NOVA OCORRÊNCIA", key="new_occurrence"):
            reset_form()
            st.session_state.show_form = True

    with col2:
        st.download_button(
            label="📥 Exportar Excel",
            data=generate_excel(),
            file_name="ocorrencias.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    # **Exibir o formulário logo abaixo do botão "NOVA OCORRÊNCIA"**
    if st.session_state.show_form:
        st.subheader("Cadastro de Ocorrência" if not st.session_state.edit_mode else "Editar Ocorrência")

        with st.form(key="form_ocorrencia", clear_on_submit=False):
            aberto_por = st.text_input("Aberto por", value=st.session_state.aberto_por)
            ocorrencia = st.text_area("Ocorrência", value=st.session_state.ocorrencia)
            data_input = st.date_input("Data (opcional)", value=st.session_state.data if st.session_state.data else None)
            acao_imediata = st.text_area("Ação Imediata", value=st.session_state.acao_imediata)
            avaliado_supervisao = st.selectbox("Avaliado pela Supervisão?", ["", "SIM", "NÃO"], index=["", "SIM", "NÃO"].index(st.session_state.avaliado_supervisao) if st.session_state.avaliado_supervisao else 0)
            avaliado_por = st.text_input("Avaliado por", value=st.session_state.avaliado_por)
            observacoes_supervisao = st.text_area("Observações da Supervisão", value=st.session_state.observacoes_supervisao)

            col1, col2 = st.columns([1, 8])
            with col1:
                salvar_button = st.form_submit_button("Salvar", type="primary")
            with col2:
                fechar_button = None
                if not st.session_state.edit_mode:
                    fechar_button = st.form_submit_button("Fechar")


            if salvar_button:
                formatted_date = data_input.strftime("%d/%m/%Y") if data_input else ""
                if st.session_state.edit_mode:
                    update_record(st.session_state.record_id, aberto_por, ocorrencia, formatted_date, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao)
                    st.success("Registro atualizado com sucesso!")
                else:
                    add_record(aberto_por, ocorrencia, formatted_date, acao_imediata, avaliado_supervisao, avaliado_por, observacoes_supervisao)
                    st.success("Ocorrência adicionada com sucesso!")

                reset_form()
                st.rerun()

            if fechar_button:
                reset_form()
                st.rerun()

    # **Filtros**
    st.subheader("Filtros")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        filtro_aberto_por = st.text_input("Aberto por:")
    with col2:
        filtro_ocorrencia = st.text_input("Ocorrência:")
    with col3:
        filtro_data = st.date_input("Data:", value=None)
    with col4:
        filtro_acao_imediata = st.text_input("Ação Imediata:")
    with col5:
        filtro_avaliado_supervisao = st.selectbox("Avaliado:", ["", "SIM", "NÃO"], index=0)

    # **Aplicar filtros nos registros**
    df_filtrado = pd.DataFrame(get_all_records(), columns=[
        "ID", "Aberto por", "Ocorrência", "Data", "Ação Imediata", "Avaliado pela Supervisão", "Avaliado por",
        "Observações da Supervisão"
    ])



    # Aplicar filtros
    if not df_filtrado.empty:
        if filtro_aberto_por:
            df_filtrado = df_filtrado[df_filtrado["Aberto por"].str.contains(filtro_aberto_por, case=False, na=False)]
        if filtro_ocorrencia:
            df_filtrado = df_filtrado[df_filtrado["Ocorrência"].str.contains(filtro_ocorrencia, case=False, na=False)]
        if filtro_data:
            df_filtrado = df_filtrado[df_filtrado["Data"] == filtro_data.strftime("%d/%m/%Y")]
        if filtro_acao_imediata:
            df_filtrado = df_filtrado[
                df_filtrado["Ação Imediata"].str.contains(filtro_acao_imediata, case=False, na=False)]
        if filtro_avaliado_supervisao:
            df_filtrado = df_filtrado[df_filtrado["Avaliado pela Supervisão"] == filtro_avaliado_supervisao]

    # **Verificar se há registros após aplicar filtros**
    if df_filtrado.empty:
        st.info("Nenhum registro encontrado.")

    # **Cabeçalho da Tabela**



    # novo cabeçalho
    st.markdown(

        """
            <style>
                .header-container {
                    display: flex;
                    font-weight: bold;
                    padding: 5px;
                    border-bottom: 2px solid #ddd;
                    text-align: left;
                }
                .header-item {
                    padding: 5px;
                    white-space: nowrap;
                    flex-grow: 1;
                    text-overflow: ellipsis;
                    overflow: hidden;
                }
            </style>
            <div class="header-container">
                <div class="header-item" style="flex: 2.3; text-align: left;">Aberto por</div>
                <div class="header-item" style="flex: 2.5; text-align: left;">Ocorrência</div>
                <div style="flex: 1;"></div>  <!-- Espaço invisível para empurrar a Data -->
                <div class="header-item" style="flex: 3.5; text-align: left;">Data</div> 
                <div class="header-item" style="flex: 4; text-align: left;">Ação Imediata</div>
                <div class="header-item" style="flex: 5.5; text-align: left;">Avaliado</div>
            </div>
            """,
        unsafe_allow_html=True
    )

    # **Exibir registros**
    for index, row in df_filtrado.iterrows():
        cols = st.columns([8, 1, 1])
        with cols[0]:
            st.markdown(
                f"""
                <div style="padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #ddd; 
                            height: 50px; overflow: hidden; align-items: center;">
                    <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Aberto por']}</div>
                    <div style="flex: 3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Ocorrência']}</div>
                    <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Data']}</div>
                    <div style="flex: 3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Ação Imediata']}</div>
                    <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Avaliado pela Supervisão']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[1]:
            if st.button("✏️", key=f"edit_{index}"):
                st.session_state.update({
                    "edit_mode": True,
                    "show_form": True,
                    "record_id": row["ID"],
                    "aberto_por": row["Aberto por"],
                    "ocorrencia": row["Ocorrência"],

                    "data": datetime.strptime(row["Data"], "%d/%m/%Y").date() if row["Data"] else None,

                    "acao_imediata": row["Ação Imediata"],
                    "avaliado_supervisao": row["Avaliado pela Supervisão"],
                    "avaliado_por": row["Avaliado por"],
                    "observacoes_supervisao": row["Observações da Supervisão"]
                })
                st.rerun()


        with cols[2]:
            if st.button("🗑️", key=f"delete_{index}"):
                delete_record(row["ID"])
                st.warning("Registro deletado!")
                st.rerun()
