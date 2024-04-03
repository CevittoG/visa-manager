from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT, sidebar_setup
from helpers.database import db_init_conn
from helpers.files import csv_to_list
import streamlit as st
import pandas as pd
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():
    import_type = st.selectbox('Import type', ['File', 'Login'], placeholder='Choose and option...')
    for i in range(3):
        st.markdown('')

    if import_type == 'File':
        uploaded_file = st.file_uploader("Choose a file", label_visibility='collapsed', type=['csv'])

        if uploaded_file is not None:
            imported_data = pd.read_csv(uploaded_file, sep=';')
            validated_data = csv_to_list(imported_data)
            # Check if data is valid
            if isinstance(validated_data, str):
                st.error(validated_data)
            else:
                st.success(f"{uploaded_file.name} is valid")
                if st.button('Load file'):
                    st.session_state['TravelHistory'] = TravelHistory()
                    for t in validated_data:
                        st.session_state['TravelHistory'].add_trip(Trip(*t))
                    st.dataframe(st.session_state['TravelHistory'].to_df(), column_config=TH_DF_CONFIG)

    elif import_type == 'Login':
        st.info("I'm sorry! I haven't implemented this yet.")
        c1, c2, c3 = st.columns([2, 2, 1])

        user = c1.text_input(label='Email', placeholder="Email", key="user", autocomplete="email", label_visibility='collapsed', disabled=True)
        pswd = c2.text_input(label='Password', placeholder="Password", key="password", type="password", autocomplete="on", label_visibility='collapsed', disabled=True)
        if c3.button('Login', type='primary', disabled=True):
            pass

        st.write('')
        st.write('')
        st.write('')
        remember_me = st.checkbox("Remember me")
        if remember_me:
            html = """<iframe id="ytplayer" type="text/html" width="560" height="315" src="https://www.youtube.com/embed/KP_XkN2v7OM?autoplay=1&si=ldybZWdUGotYXS9z&amp;controls=0&amp;start=1" allow="autoplay" frameborder="0"></iframe>"""
            st.components.v1.html(html, width=580, height=335, scrolling=False)
            st.info("I'm sorry! I haven't implemented sessions yet.")


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = ("Description missing...")
    shared_page_config(title=PAGE_KEYWORD.replace('_', ' ').title(),
                       emoji=PAGE_EMOJI,
                       page_caption=page_caption, )

    if 'TravelHistory' not in st.session_state:
        st.session_state['TravelHistory'] = TravelHistory()
    if 'LOGGED_IN' not in st.session_state:
        st.session_state['LOGGED_IN'] = False
    if 'SESSION_USER' not in st.session_state:
        st.session_state['SESSION_USER'] = ''

    # Initiate database connection
    db_conn = db_init_conn()
    # Sidebar
    sidebar_setup(db_conn)

    # Page functionality
    main()
