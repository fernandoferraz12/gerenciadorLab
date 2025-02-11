import sqlite3
import streamlit as st


def get_all_links():
    conn = sqlite3.connect("crud_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM links_menu ORDER BY id ASC")
    links = cursor.fetchall()
    conn.close()
    return links


def menu_links():
    st.title("📌 Menu de Links")

    links = get_all_links()

    if not links:
        st.warning("⚠️ Nenhum link configurado. Vá até a configuração para adicionar novos botões.")
    else:
        for link in links:
            st.markdown(
                f'''
                <a href="{link[2]}" target="_blank" style="text-decoration: none;">
                    <button style="
                        width: 70%;
                        height: 40px;
                        font-size: 16px;
                        margin-bottom: 10px;
                        border-radius: 10px;
                        background-color: #7EC9C7; 
                        color: white; 
                        border: none;
                        cursor: pointer;
                        transition: 0.3s;
                    "
                    onmouseover="this.style.backgroundColor='#005a9e'"
                    onmouseout="this.style.backgroundColor='#0078D7'">
                        🔗 {link[1]}
                    </button>
                </a>
                ''',
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    menu_links()
