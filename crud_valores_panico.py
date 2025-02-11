import sqlite3
import streamlit as st
from datetime import datetime
import pandas as pd
import io

def crud_valores_panico():
    st.subheader("Valores de Pânico")

    # **Criar banco de dados e tabelas**
    def create_database():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()

        # Criar tabela de comunicação de valores de pânico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comunicacoes_panico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comunicado_por TEXT NOT NULL,
                cod_paciente TEXT NOT NULL,
                exame TEXT NOT NULL,
                valor_panico TEXT NOT NULL,
                resultado_paciente TEXT NOT NULL,
                unidade TEXT NOT NULL,
                comunicado_para TEXT NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                observacoes TEXT
            )
        ''')

        # Criar tabela de valores de pânico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valores_panico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parametro TEXT NOT NULL,
                valor_panico TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    # **CRUD - Comunicação de Valores de Pânico**
    def add_comunicacao(comunicado_por, cod_paciente, exame, valor_panico, resultado_paciente, unidade, comunicado_para, data, hora, observacoes):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()

        # Garantir que a data esteja no formato correto antes de inserir
        formatted_date = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")

        cursor.execute('''
            INSERT INTO comunicacoes_panico (comunicado_por, cod_paciente, exame, valor_panico, resultado_paciente, unidade, comunicado_para, data, hora, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (comunicado_por, cod_paciente, exame, valor_panico, resultado_paciente, unidade, comunicado_para, formatted_date, hora, observacoes))
        conn.commit()
        conn.close()

    def get_all_comunicacoes():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM comunicacoes_panico ORDER BY id DESC')
        records = cursor.fetchall()
        conn.close()

        # Convertendo para DataFrame e ajustando a coluna "Data"
        df = pd.DataFrame(records, columns=[
            "ID", "Comunicado por", "Cod/Paciente", "Exame", "Valor de Pânico",
            "resultado_paciente", "Unidade", "Comunicado para", "Data", "Hora", "Observações"
        ])

        if not df.empty:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime("%d/%m/%Y")  # Ajusta o formato da data

        return df

    def delete_comunicacao(record_id):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM comunicacoes_panico WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    # **CRUD - Valores de Pânico**
    def add_valor_panico(parametro, valor_panico):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO valores_panico (parametro, valor_panico)
            VALUES (?, ?)
        ''', (parametro, valor_panico))
        conn.commit()
        conn.close()

    def update_comunicacao(record_id, comunicado_por, cod_paciente, exame, valor_panico, resultado_paciente, unidade,
                           comunicado_para, data, hora, observacoes):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()

        # ✅ Converter a data para o formato correto antes de atualizar o banco de dados
        formatted_date = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")

        cursor.execute('''
            UPDATE comunicacoes_panico
            SET comunicado_por = ?, cod_paciente = ?, exame = ?, valor_panico = ?, resultado_paciente = ?, unidade = ?, 
                comunicado_para = ?, data = ?, hora = ?, observacoes = ?
            WHERE id = ?
        ''', (
            comunicado_por, cod_paciente, exame, valor_panico, resultado_paciente, unidade, comunicado_para,
            formatted_date, hora, observacoes, record_id
        ))

        conn.commit()
        conn.close()

    def get_all_valores_panico():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM valores_panico ORDER BY id DESC')

        records = cursor.fetchall()
        conn.close()
        return records

    def delete_valor_panico(record_id):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM valores_panico WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()



    def generate_excel():
        df = pd.DataFrame(get_all_comunicacoes(), columns=[
            "ID", "Comunicado por", "Cod/Paciente", "Exame", "Valor de Pânico",
            "resultado_paciente", "Unidade", "Comunicado para", "Data", "Hora", "Observações"
        ])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Ocorrências")
        output.seek(0)

        return output

    # **Criar tabelas**
    create_database()

    # **Gerenciar estado**
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if "show_valores_panico" not in st.session_state:
        st.session_state.show_valores_panico = False

    # **Botões para abrir formulários**
    col1,col2, col3 = st.columns([4, 3,8])
    with col1:
        if st.button("➕ INSERIR COMUNICAÇÃO"):
            st.session_state.update({
                "show_form": True,
                "show_valores_panico": False,
                "edit_mode": False,
                "record_id_comunicacao": None,
                "comunicado_por": "",
                "cod_paciente": "",
                "exame": "",
                "valor_panico": "",
                "resultado_paciente": "",
                "unidade": "",
                "comunicado_para": "",
                "data": None,
                "hora": None,
                "observacoes": ""
            })


    with col2:
        st.download_button(
            label="📥 Exportar Excel",
            data=generate_excel(),
            file_name="questionamentos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col3:
        if st.button("TABELA DE VALORES"):
            st.session_state.show_valores_panico = not st.session_state.show_valores_panico

    #parte inserida na tentativa##############################################
    if st.session_state.show_valores_panico:
        st.subheader("Tabela de Valores de Pânico")

        with st.form(key="form_valores_panico", clear_on_submit=True):  # 🟢 clear_on_submit ativa a limpeza automática
            parametro = st.text_input("Parâmetro")
            valor_panico = st.text_input("Valor de Pânico")

            col1, col2 = st.columns([1, 1])
            with col1:
                salvar_button = st.form_submit_button("Salvar", type="primary")
            with col2:
                fechar_button = st.form_submit_button("Fechar")

            if salvar_button:
                add_valor_panico(parametro, valor_panico)
                st.success("Valor de Pânico registrado com sucesso!")

                # 🔄 Mantém o formulário aberto e recarrega a página
                st.session_state.show_valores_panico = True
                st.rerun()

            if fechar_button:
                st.session_state.show_valores_panico = False
                st.rerun()

            if fechar_button:
                st.session_state.show_valores_panico = False
                st.rerun()

        #colocar os filtros



        # **Exibir tabela de valores de pânico**
        df_valores = pd.DataFrame(get_all_valores_panico(), columns=["ID", "Parâmetro", "Valor de Pânico"])
        if not df_valores.empty:
            for index, row in df_valores.iterrows():
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.markdown(f"""
                        <div style="padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #ddd;">
                            <div style="flex: 3;">{row['Parâmetro']}</div>
                            <div style="flex: 2;">{row['Valor de Pânico']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    if st.button("✏️", key=f"edit_valor_{index}"):
                        st.session_state.show_valores_panico = True
                with cols[2]:
                    if st.button("🗑️", key=f"delete_valor_{index}"):
                        delete_valor_panico(row["ID"])
                        st.warning("Registro deletado!")
                        st.rerun()


    # **Formulário - Comunicação de Valores de Pânico**
    if st.session_state.show_form:
        st.subheader("Editar Comunicação" if st.session_state.edit_mode else "Inserir Comunicação")

        exames = pd.DataFrame(get_all_valores_panico(), columns=["ID", "Parâmetro", "Valor de Pânico"])
        exames_dict = dict(zip(exames["Parâmetro"], exames["Valor de Pânico"]))

        # **Selecionar Exame - Atualiza dinamicamente**
        exame_selecionado = st.selectbox(
            "Exame", options=[""] + list(exames_dict.keys()),
            index = ([""] + list(exames_dict.keys())).index(st.session_state.exame) if st.session_state.get("exame") else 0

        )

        # **Obter Valor de Pânico correspondente**
        valor_panico = exames_dict.get(st.session_state.exame, "Nenhum valor disponível")
        st.markdown(f"**Valor de Pânico:** {valor_panico}")

        with st.form(key="form_comunicacao", clear_on_submit=False):
            comunicado_por = st.text_input("Comunicado por", value=st.session_state.get("comunicado_por", ""))
            cod_paciente = st.text_input("Cod/Paciente", value=st.session_state.get("cod_paciente", ""))
            resultado_paciente = st.text_input("Resultado do Paciente",
                                               value=st.session_state.get("resultado_paciente", ""))
            unidade = st.text_input("Unidade", value=st.session_state.get("unidade", ""))
            comunicado_para = st.text_input("Comunicado para", value=st.session_state.get("comunicado_para", ""))
            data = st.date_input("Data", value=st.session_state.get("data", None))
            hora = st.time_input("Hora", value=datetime.strptime(st.session_state.get("hora", "00:00"),
                                                                 "%H:%M").time() if st.session_state.get(
                "hora") else None)
            observacoes = st.text_area("Observações", value=st.session_state.get("observacoes", ""))

            col1, col2 = st.columns([1, 8])
            with col1:
                salvar_button = st.form_submit_button("Salvar", type="primary")
            with col2:
                fechar_button = None  # Inicializa sem botão
                if not st.session_state.edit_mode:  # Só exibe o botão se NÃO estiver editando
                    fechar_button = st.form_submit_button("Fechar")


            if salvar_button:
                if not data:  # Se a data não estiver preenchida
                    st.error("⚠️ Por favor, selecione uma data antes de salvar!")
                else:
                    formatted_date = data.strftime("%d/%m/%Y")
                    formatted_time = hora.strftime("%H:%M") if hora else ""

                    if st.session_state.edit_mode:
                        update_comunicacao(
                            st.session_state.record_id_comunicacao, comunicado_por, cod_paciente, exame_selecionado,
                            valor_panico, resultado_paciente, unidade, comunicado_para, formatted_date, formatted_time,
                            observacoes
                        )
                        st.success("Registro atualizado com sucesso!")
                    else:
                        add_comunicacao(comunicado_por, cod_paciente, exame_selecionado, valor_panico,
                                        resultado_paciente, unidade, comunicado_para, formatted_date, formatted_time,
                                        observacoes)
                        st.success("Comunicação registrada com sucesso!")

                    st.session_state.show_form = False
                    st.session_state.edit_mode = False
                    st.rerun()

            if fechar_button:
                st.session_state.show_form = False
                st.rerun()

    # **Tabela de Registros de Comunicação**
    st.subheader("Registros de Comunicações")

    #parte colada
    # **Filtros**
    st.subheader("Filtros")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        filtro_data = st.date_input("Data:", value=None)

    with col2:
        filtro_cod_paciente = st.text_input("Cod. Paciente:")
    with col3:
        filtro_exame = st.text_input("Exame:")
    with col4:
        filtro_unidade = st.text_input("Unidade:")
    with col5:
        filtro_comunicado_para = st.text_input("Comunicado Para:")

    # **Carregar todos os registros antes de aplicar filtros**
    df_filtrado = pd.DataFrame(get_all_comunicacoes(), columns=[
        "ID", "Comunicado por", "Cod/Paciente", "Exame", "Valor de Pânico", "resultado_paciente",
        "Unidade", "Comunicado para", "Data", "Hora", "Observações"
    ])


    # **Aplicar filtros**
    # **Aplicar filtros**
    if not df_filtrado.empty:

        df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"], errors="coerce").dt.strftime("%d/%m/%Y")

        if filtro_data:
            filtro_data_formatada = filtro_data.strftime("%d/%m/%Y")  # Formata corretamente para DD/MM/YYYY
            df_filtrado = df_filtrado[df_filtrado["Data"].dt.strftime("%d/%m/%Y") == filtro_data_formatada]

        if filtro_cod_paciente:
            df_filtrado = df_filtrado[
                df_filtrado["Cod/Paciente"].str.contains(filtro_cod_paciente, case=False, na=False)]

        if filtro_exame:
            df_filtrado = df_filtrado[df_filtrado["Exame"].str.contains(filtro_exame, case=False, na=False)]

        if filtro_unidade:
            df_filtrado = df_filtrado[df_filtrado["Unidade"].str.contains(filtro_unidade, case=False, na=False)]

        if filtro_comunicado_para:
            df_filtrado = df_filtrado[
                df_filtrado["Comunicado para"].str.contains(filtro_comunicado_para, case=False, na=False)]

        # **Converter a coluna "Data" para o formato correto**
        #df_filtrado["Data"] = df_filtrado["Data"].dt.strftime("%d/%m/%Y")
        df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"], errors="coerce").dt.strftime("%d/%m/%Y")

    # **Exibir a tabela apenas se houver registros filtrados**
    if df_filtrado.empty:
        st.info("Nenhum registro encontrado.")


    #fim da parte coletad
    df_comunicacoes = pd.DataFrame(get_all_comunicacoes(), columns=[
        "ID", "Comunicado por", "Cod/Paciente", "Exame", "Valor de Pânico", "resultado_paciente", "Unidade", "Comunicado para", "Data", "Hora", "Observações"

    ])

    if not df_comunicacoes.empty:



        # **Cabeçalho da Tabela**
        st.markdown(
            """
            <div style="display: flex; font-weight: bold; padding: 10px 5px; border-bottom: 2px solid #ddd;">
                <div style="flex: 1.5;">Data</div>
                <div style="flex: 2;">Cod/Paciente</div>
                <div style="flex: 1.6;">Exame</div>
                <div style="flex: 3;">Resultado </div>
                <div style="flex: 4.1;">Unidade</div>
            
            </div>
            """,
            unsafe_allow_html=True
        )

        # **Exibir os registros**
        for index, row in df_filtrado.iterrows():
            background_color = "#f9f9f9" if index % 2 == 0 else "#ffffff"

            cols = st.columns([8, 1, 1])
            with cols[0]:
                st.markdown(
                    f"""
                    <div style="background-color: {background_color}; padding: 10px; display: flex; align-items: center; 
                                border-bottom: 1px solid #ddd; height: 50px; overflow: hidden; align-items: center;">
                        <div style="flex: 1.5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Data']}</div>
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Cod/Paciente']}</div>
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Exame']}</div>
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['resultado_paciente']}</div>
                        <div style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 50px; line-height: 50px;">{row['Unidade']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # **Botão Editar**
            with cols[1]:
                if st.button("✏️", key=f"edit_comunicacao_{index}"):
                    st.session_state.update({
                        "edit_mode": True,
                        "show_form":True,
                        "record_id_comunicacao": row["ID"],
                        "comunicado_por": row["Comunicado por"],
                        "cod_paciente": row["Cod/Paciente"],
                        "exame": row["Exame"],
                        "valor_panico": row["Valor de Pânico"],
                        "resultado_paciente": row["resultado_paciente"],
                        "unidade": row["Unidade"],
                        "comunicado_para": row["Comunicado para"],
                        "data": datetime.strptime(row["Data"], "%d/%m/%Y").date() if row["Data"] else None,
                        "hora": row["Hora"],
                        "observacoes": row["Observações"],

                    })
                    st.rerun()

            # **Botão Deletar**
            with cols[2]:
                if st.button("🗑️", key=f"delete_comunicacao_{index}"):
                    delete_comunicacao(row["ID"])
                    st.warning("Registro deletado!")
                    st.rerun()

