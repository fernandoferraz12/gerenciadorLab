import sqlite3
import streamlit as st
import pandas as pd

def crud_equipamentos():
    st.subheader("Cadastro de Equipamentos")

    # **Criar banco de dados e tabela**
    def create_database():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ativo TEXT NOT NULL,
                cod_interno TEXT NOT NULL,
                equipamento TEXT NOT NULL,
                marca TEXT NOT NULL,
                numero_serie TEXT NOT NULL,
                empresa_responsavel TEXT NOT NULL,
                preventiva TEXT NOT NULL,
                tipo TEXT NOT NULL,
                local TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    # **CRUD - Equipamentos**
    def add_equipamento(ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO equipamentos (ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local))
        conn.commit()
        conn.close()

    def get_all_equipamentos():
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM equipamentos ORDER BY id DESC')
        records = cursor.fetchall()
        conn.close()
        return records

    def update_equipamento(record_id, ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE equipamentos
            SET ativo = ?, cod_interno = ?, equipamento = ?, marca = ?, numero_serie = ?, empresa_responsavel = ?, preventiva = ?, tipo = ?, local = ?
            WHERE id = ?
        ''', (ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local, record_id))
        conn.commit()
        conn.close()

    def delete_equipamento(record_id):
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM equipamentos WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    def get_all_records():
        """Busca todos os registros da tabela equipamentos"""
        conn = sqlite3.connect("crud_app.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM equipamentos ORDER BY id DESC')

        records = cursor.fetchall()
        conn.close()
        return records

    # **Criar tabelas**
    create_database()

    # **Gerenciar estado**
    if "show_form_equipamento" not in st.session_state:
        st.session_state.show_form_equipamento = False
    if "edit_mode_equipamento" not in st.session_state:
        st.session_state.edit_mode_equipamento = False
    if "record_id_equipamento" not in st.session_state:
        st.session_state.record_id_equipamento = None

    # **Botão para abrir o formulário**
    if st.button("NOVO EQUIPAMENTO", key="new_equipamento"):
        st.session_state.show_form_equipamento = True
        st.session_state.edit_mode_equipamento = False
        st.session_state.record_id_equipamento = None

        # Resetando os campos do formulário
        st.session_state.ativo = ""
        st.session_state.cod_interno = ""
        st.session_state.equipamento = ""
        st.session_state.marca = ""
        st.session_state.numero_serie = ""
        st.session_state.empresa_responsavel = ""
        st.session_state.preventiva = ""
        st.session_state.tipo = ""
        st.session_state.local = ""

    # **Exibir Formulário**
    if st.session_state.show_form_equipamento or st.session_state.edit_mode_equipamento:
        st.subheader("Cadastro de Equipamento" if not st.session_state.edit_mode_equipamento else "Editar Equipamento")

        with st.form(key="form_equipamento", clear_on_submit=False):

            # Criando o selectbox corretamente
            status_options = ["", "Ativo", "Inativo"]
            ativo = st.selectbox("Status", status_options,
                                 index=status_options.index(
                                     st.session_state.ativo) if "ativo" in st.session_state and st.session_state.ativo in status_options else 0)

            cod_interno = st.text_input("Código Interno", value=st.session_state.get("cod_interno", ""))
            equipamento = st.text_input("Equipamento", value=st.session_state.get("equipamento", ""))
            marca = st.text_input("Marca", value=st.session_state.get("marca", ""))
            numero_serie = st.text_input("Número de Série", value=st.session_state.get("numero_serie", ""))
            empresa_responsavel = st.text_input("Empresa Responsável", value=st.session_state.get("empresa_responsavel", ""))
            preventiva = st.selectbox("Preventiva", ["", "ANUAL", "SEMESTRAL"], index=["", "ANUAL", "SEMESTRAL"].index(st.session_state.get("preventiva", "")) if st.session_state.edit_mode_equipamento else 0)
            tipo = st.selectbox("Tipo", ["", "EQUIPAMENTOS. LAB", "GELADEIRA", "CENTRIFUGA"], index=["", "EQUIPAMENTOS. LAB", "GELADEIRA", "CENTRIFUGA"].index(st.session_state.get("tipo", "")) if st.session_state.edit_mode_equipamento else 0)
            local = st.text_input("Local", value=st.session_state.get("local", ""))

            col1, col2 = st.columns([1, 1])
            with col1:
                salvar_button = st.form_submit_button("Salvar", type="primary")
            with col2:
                fechar_button = None
                if not st.session_state.edit_mode_equipamento:
                    fechar_button = st.form_submit_button("Fechar")

            if salvar_button:
                if st.session_state.edit_mode_equipamento:
                    update_equipamento(st.session_state.record_id_equipamento, ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local)
                    st.success("Registro atualizado com sucesso!")
                else:
                    add_equipamento(ativo, cod_interno, equipamento, marca, numero_serie, empresa_responsavel, preventiva, tipo, local)
                    st.success("Equipamento cadastrado com sucesso!")

                st.session_state.show_form_equipamento = False
                st.session_state.edit_mode_equipamento = False
                st.rerun()

            if fechar_button:
                st.session_state.show_form_equipamento = False
                st.session_state.edit_mode_equipamento = False
                st.rerun()

    # **Filtros**
    st.subheader("Filtros")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        filtro_cod_interno = st.text_input("Filtrar por Código Interno:")
    with col2:
        filtro_equipamento = st.text_input("Filtrar por Equipamento:")
    with col3:
        filtro_marca = st.text_input("Filtrar por Marca:")
    with col4:
        filtro_tipo = st.selectbox("Filtrar por Tipo:", ["", "EQUIPAMENTOS LAB", "GELADEIRA", "CENTRÍFUGA"], index=0)
    with col5:
        filtro_local = st.text_input("Filtrar por Local:")

    # **Aplicar filtros**
    # **Carregar todos os registros antes de aplicar filtros**
    df_filtrado = pd.DataFrame(get_all_records(), columns=[
        "ID", "ativo", "cod_interno", "equipamento", "marca", "numero_serie",
        "empresa_responsavel", "preventiva", "tipo", "local"  # ✅ Certifique-se de incluir "local"
    ])

    # **Substituir valores None por strings vazias**
    df_filtrado.fillna("", inplace=True)

    # **Aplicar filtros**
    if not df_filtrado.empty:  # ✅ Certificando que há registros antes dos filtros
        if filtro_cod_interno:
            df_filtrado = df_filtrado[df_filtrado["cod_interno"].str.contains(filtro_cod_interno, case=False, na=False)]
        if filtro_equipamento:
            df_filtrado = df_filtrado[df_filtrado["equipamento"].str.contains(filtro_equipamento, case=False, na=False)]
        if filtro_marca:
            df_filtrado = df_filtrado[df_filtrado["marca"].str.contains(filtro_marca, case=False, na=False)]
        if filtro_tipo:
            df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]
        if filtro_local:
            df_filtrado = df_filtrado[df_filtrado["local"].str.contains(filtro_local, case=False, na=False)]

    # **Verificar se há registros após aplicar filtros**
    if df_filtrado.empty:
        st.info("Nenhum registro encontrado.")
    else:
        st.subheader("Registros de Equipamentos")


        # ✅ **Adicionando o campo "Local" na exibição da tabela**
        st.markdown("""
        <div style="display: flex; font-weight: bold; padding: 10px 5px; border-bottom: 2px solid #ddd;">
            <div style="flex: 2;">Código Interno</div>
            <div style="flex: 2;">Equipamento</div>
            <div style="flex: 2;">Marca</div>
            <div style="flex: 2;">Tipo</div>
            <div style="flex: 2;">Local</div>  <!-- ✅ Novo campo "Local" adicionado -->
            <div style="flex: 1.5; text-align: center;">Ações</div>
        </div>
        """, unsafe_allow_html=True)

        # **Exibir registros**
        for index, row in df_filtrado.iterrows():
            background_color = "#f9f9f9" if index % 2 == 0 else "#ffffff"

            cols = st.columns([8, 1, 1])
            with cols[0]:
                st.markdown(f"""
                    <div style="background-color: {background_color}; padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #ddd;">
                        <div style="flex: 2;">{row['cod_interno']}</div>
                        <div style="flex: 2;">{row['equipamento']}</div>
                        <div style="flex: 2;">{row['marca']}</div>
                        <div style="flex: 2;">{row['tipo']}</div>
                        <div style="flex: 2;">{row['local']}</div>  <!-- ✅ Exibindo o campo "Local" -->
                    </div>
                """, unsafe_allow_html=True)

            with cols[1]:
                if st.button("✏️", key=f"edit_equipamento_{index}"):
                    st.session_state.update({
                        "ativo": row["ativo"],
                        "cod_interno": row["cod_interno"],
                        "equipamento": row["equipamento"],
                        "marca": row["marca"],
                        "numero_serie": row["numero_serie"],
                        "empresa_responsavel": row["empresa_responsavel"],
                        "preventiva": row["preventiva"],
                        "tipo": row["tipo"],
                        "local": row["local"],  # ✅ Certificando que o Local será carregado ao editar
                        "show_form_equipamento": True,
                        "edit_mode_equipamento": True
                    })
                    st.rerun()

            with cols[2]:
                if st.button("🗑️", key=f"delete_equip_{index}"):
                    delete_equipamento(row["ID"])
                    st.warning("Registro deletado!")
                    st.rerun()
