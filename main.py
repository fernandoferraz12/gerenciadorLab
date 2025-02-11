import streamlit as st
from crud_ocorrencias import crud_ocorrencias
from crud_questionamento import crud_questionamento
from crud_valores_panico import crud_valores_panico
from crud_equipamentos import crud_equipamentos
from registro_manutencao import registro_manutencao
from config_links import config_links
from menu_links import menu_links

# Configuração inicial
st.set_page_config(page_title="App com Múltiplos CRUDs", layout="wide")
st.title("🏥 Gestão Laboratorial")

# Menu lateral com ícones para cada módulo
menu = st.sidebar.selectbox(
    "📌 **Selecione o módulo:**",
    [
        "Selecione...",
        "📝 Ocorrências",
        "❓ Questionamento de Exames",
        "⚠️ Valores de Pânico",
        "🛠️ Equipamentos",
        "🔧 Registro de Manutenção",
        "🔗 Menu de Links",
        "⚙️ Configuração de Links"
    ]
)

# Navegação entre as telas
if menu == "📝 Ocorrências":
    crud_ocorrencias()
elif menu == "❓ Questionamento de Exames":
    crud_questionamento()
elif menu == "⚠️ Valores de Pânico":
    crud_valores_panico()
elif menu == "🛠️ Equipamentos":
    crud_equipamentos()
elif menu == "🔧 Registro de Manutenção":
    registro_manutencao()
elif menu == "🔗 Menu de Links":
    menu_links()
elif menu == "⚙️ Configuração de Links":
    config_links()
