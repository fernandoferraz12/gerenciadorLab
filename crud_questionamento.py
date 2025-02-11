import sqlite3
import streamlit as st
from datetime import datetime
import pandas as pd
import io

def crud_questionamento():
    st.subheader("Questionamento de Exames")

    def generate_excel():
        df_export = pd.DataFrame(get_all_records(), columns=[
            "ID", "Data", "Aberto por", "Questionado por", "Clínica/Local", "Código do Paciente",
            "Exame", "Questionamento", "Avaliado por", "Ação Aplicada"
        ])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Questionamentos")
        output.seek(0)

        return output

    # Função para criar o banco de dados e a tabela
    def create_database():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questionamentos_exames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                aberto_por TEXT NOT NULL,
                questionado_por TEXT NOT NULL,
                clinica_local TEXT NOT NULL,
                cod_paciente TEXT NOT NULL,
                exame TEXT NOT NULL,
                questionamento TEXT NOT NULL,
                avaliado_por TEXT NOT NULL,
                acao_aplicada TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    # Função para adicionar um registro
    def add_record(data, aberto_por, questionado_por, clinica_local, cod_paciente, exame, questionamento, avaliado_por, acao_aplicada):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO questionamentos_exames (data, aberto_por, questionado_por, clinica_local, cod_paciente, exame, questionamento, avaliado_por, acao_aplicada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data, aberto_por, questionado_por, clinica_local, cod_paciente, exame, questionamento, avaliado_por, acao_aplicada))
        conn.commit()
        conn.close()

    # Função para buscar todos os registros
    def get_all_records():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questionamentos_exames ORDER BY id DESC')
        records = cursor.fetchall()
        conn.close()
        return records

    # Função para atualizar um registro
    def update_record(record_id, data, aberto_por, questionado_por, clinica_local, cod_paciente, exame, questionamento, avaliado_por, acao_aplicada):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE questionamentos_exames
            SET data = ?, aberto_por = ?, questionado_por = ?, clinica_local = ?, cod_paciente = ?, exame = ?, questionamento = ?, avaliado_por = ?, acao_aplicada = ?
            WHERE id = ?
        ''', (data, aberto_por, questionado_por, clinica_local, cod_paciente, exame, questionamento, avaliado_por, acao_aplicada, record_id))
        conn.commit()
        conn.close()

    # Função para deletar um registro
    def delete_record(record_id):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM questionamentos_exames WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()



    # Criação do banco de dados e da tabela
    create_database()

    # Gerenciar o estado para exibição do formulário
    if "show_form_questionamento" not in st.session_state:
        st.session_state.show_form_questionamento = False

    if "edit_mode_questionamento" not in st.session_state:
        st.session_state.edit_mode_questionamento = False

    if "record_id_questionamento" not in st.session_state:
        st.session_state.record_id_questionamento = None

    # Gerenciar o estado dos campos
    fields = [
        "data", "aberto_por", "questionado_por", "clinica_local",
        "cod_paciente", "exame", "questionamento", "avaliado_por", "acao_aplicada"
    ]
    for field in fields:
        if field not in st.session_state:
            st.session_state[field] = "" if field != "data" else None

    # Botão para exibir o formulário
    # Criar layout dos botões
    col1, col2 = st.columns([2, 6])  # Ajusta o tamanho das colunas

    with col1:
        if st.button("➕ NOVO QUESTIONAMENTO", key="new_questionamento"):
            st.session_state.show_form_questionamento = True
            st.session_state.edit_mode_questionamento = False
            st.session_state.record_id_questionamento = None

    with col2:
        st.download_button(
            label="📥 Exportar Excel",
            data=generate_excel(),
            file_name="questionamentos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )








    # Exibe o formulário se necessário
    if st.session_state.show_form_questionamento or st.session_state.edit_mode_questionamento:
        st.subheader("Cadastro de Questionamento" if not st.session_state.edit_mode_questionamento else "Editar Questionamento")

        with st.form(key="form_questionamento", clear_on_submit=False):
            data_input = st.date_input("Data", value=st.session_state.data if st.session_state.data else None)
            aberto_por = st.text_input("Aberto por", value=st.session_state.aberto_por)
            questionado_por = st.text_input("Questionado por", value=st.session_state.questionado_por)
            clinica_local = st.text_input("Clínica/Local", value=st.session_state.clinica_local)
            cod_paciente = st.text_input("Código do Paciente", value=st.session_state.cod_paciente)
            exame = st.text_input("Exame", value=st.session_state.exame)
            questionamento = st.text_area("Questionamento", value=st.session_state.questionamento)
            avaliado_por = st.text_input("Avaliado por", value=st.session_state.avaliado_por)
            acao_aplicada = st.text_area("Ação Aplicada", value=st.session_state.acao_aplicada)

            col1, col2 = st.columns([1, 8])
            with col1:
                salvar_button = st.form_submit_button("Salvar", type="primary")
            with col2:

                fechar_button = None
                if not st.session_state.edit_mode_questionamento:
                    fechar_button = st.form_submit_button("Fechar")



            if salvar_button:
                if not data_input:
                    st.error("Por favor, selecione uma data válida!")
                else:
                    formatted_date = data_input.strftime("%d/%m/%Y")
                    if st.session_state.edit_mode_questionamento:
                        update_record(
                            st.session_state.record_id_questionamento,
                            formatted_date, aberto_por, questionado_por, clinica_local, cod_paciente, exame,
                            questionamento, avaliado_por, acao_aplicada
                        )
                        st.success("Registro atualizado com sucesso!")
                    else:
                        add_record(
                            formatted_date, aberto_por, questionado_por, clinica_local, cod_paciente, exame,
                            questionamento, avaliado_por, acao_aplicada
                        )
                        st.success("Registro adicionado com sucesso!")

                    st.session_state.show_form_questionamento = False
                    st.session_state.edit_mode_questionamento = False
                    st.session_state.record_id_questionamento = None
                    for field in fields:
                        st.session_state[field] = "" if field != "data" else None
                    st.rerun()

            if fechar_button:
                st.session_state.show_form_questionamento = False
                st.session_state.edit_mode_questionamento = False
                st.rerun()

    # Filtros
    st.subheader("Filtros")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filtro_data = st.date_input("Data:", value=None)
    with col2:
        filtro_clinica = st.text_input("Clínica/Local:")
    with col3:
        filtro_cod_paciente = st.text_input("Cod. Paciente:")
    with col4:
        filtro_exame = st.text_input("Exame:")

    # Aplica os filtros ao DataFrame
    df_filtrado = pd.DataFrame(get_all_records(), columns=[
        "ID", "Data", "Aberto por", "Questionado por", "Clínica/Local", "Código do Paciente",
        "Exame", "Questionamento", "Avaliado por", "Ação Aplicada"
    ])

    if not df_filtrado.empty:
        if filtro_data:
            filtro_data_formatada = filtro_data.strftime("%d/%m/%Y")
            df_filtrado = df_filtrado[df_filtrado["Data"] == filtro_data_formatada]

        if filtro_clinica:
            df_filtrado = df_filtrado[df_filtrado["Clínica/Local"].str.contains(filtro_clinica, case=False, na=False)]
        if filtro_cod_paciente:
            df_filtrado = df_filtrado[df_filtrado["Código do Paciente"].str.contains(filtro_cod_paciente, case=False, na=False)]
        if filtro_exame:
            df_filtrado = df_filtrado[df_filtrado["Exame"].str.contains(filtro_exame, case=False, na=False)]

        df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"], errors="coerce").dt.strftime("%d/%m/%Y")

        # Cabeçalho
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; font-weight: bold; padding: 10px 5px; border-bottom: 2px solid #ddd;">
                <div style="flex: 1;">Data</div>
                <div style="flex: 1;">Clínica</div>
                <div style="flex: 1;">Cod. do Paciente</div>
                <div style="flex: 1;">Exame</div>
                <div style="flex: 2; text-align: center;">Ações</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        for index, row in df_filtrado.iterrows():
            background_color = "#f9f9f9" if index % 2 == 0 else "#ffffff"

            cols = st.columns([8, 1, 1])
            with cols[0]:
                st.markdown(
                    f"""
                    <div style="background-color: {background_color}; padding: 10px; display: flex; align-items: center; 
                                border-bottom: 1px solid #ddd; height: 50px; overflow: hidden;">
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Data']}</div>
                        <div style="flex: 3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Clínica/Local']}</div>
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Código do Paciente']}</div>
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Exame']}</div>
                        <div style="flex: 2; text-align: center; height: 50px; line-height: 50px;">-</div>  <!-- Apenas um espaço vazio para manter alinhamento -->
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with cols[1]:
                if st.button("✏️", key=f"edit_questionamento_{index}"):
                    st.session_state.edit_mode_questionamento = True
                    st.session_state.record_id_questionamento = row["ID"]
                    st.session_state.data = datetime.strptime(row["Data"], "%d/%m/%Y").date()
                    st.session_state.aberto_por = row["Aberto por"]
                    st.session_state.questionado_por = row["Questionado por"]
                    st.session_state.clinica_local = row["Clínica/Local"]
                    st.session_state.cod_paciente = row["Código do Paciente"]
                    st.session_state.exame = row["Exame"]
                    st.session_state.questionamento = row["Questionamento"]
                    st.session_state.avaliado_por = row["Avaliado por"]
                    st.session_state.acao_aplicada = row["Ação Aplicada"]
                    st.session_state.show_form_questionamento = True
                    st.rerun()

            with cols[2]:
                if st.button("🗑️", key=f"delete_questionamento_{index}"):
                    delete_record(row["ID"])
                    st.warning("Registro deletado!")
                    st.rerun()


    else:
        st.info("Nenhum registro encontrado.")
