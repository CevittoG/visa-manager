import streamlit as st
from helpers.streamlit import shared_page_config, sidebar_user_info, user_login
from helpers.database import db_init_conn, user_sing_up
from helpers import TravelHistory
import os


SCHENGEN_DESC = """
## Schengen Tourist Visa
[The Schengen area](https://www.schengenvisainfo.com/schengen-visa-countries-list/) represents a border-free zone 
between several European countries. In addition, these countries issue a uniform Schengen visa for foreign 
nationals. To control the comings and goings of millions of people who enter the Schengen area, the 90/180-day rule 
was established.

What does it mean?

The 90/180-day rule states that any foreign national who enters the 
Schengen zone (any country within the area) can stay for up to 90 days within **any 180 days**. At first glance, it 
seems a very simple rule, but it’s often misunderstood, and many people overstay it, resulting in them facing 
penalties. This is why it’s important to know how exactly the 90/180-day rule works. 
[*www.schengenvisainfo.com*](https://www.schengenvisainfo.com/visa-calculator/)"""
USA_DESC = """
## Visa Waiver USA
something..."""


def main():
    main_tab, schengen_tab, usa_tab = st.tabs(['App Desc', 'Schengen', 'USA'])

    schengen_tab.write(SCHENGEN_DESC)
    usa_tab.write(USA_DESC)

    with main_tab:
        st.markdown("## Sing-up")
        user_agree = st.checkbox("By checking this box, you agree to assume all responsibility for the content you create and share within the app.")
        c1, c2, c3 = st.columns([2, 2, 1])

        user = c1.text_input(label='Username', placeholder="Username", key="user_signup", autocomplete="email", label_visibility='collapsed', disabled=not user_agree)
        pswd = c2.text_input(label='Password', placeholder="Password", key="password_signup", type="password", autocomplete="on", label_visibility='collapsed', disabled=not user_agree)
        if c3.button('Sing-up', type='primary', disabled=not user_agree):
            insert_response = db_insert(db_conn, 'users', {'username': user, 'password': pswd})
            if isinstance(insert_response, str) and insert_response == 'duplicate key value violates unique constraint "users_username_key"':
                st.error('Username already exist, please select another username.')
            elif isinstance(insert_response, str):
                st.error('Unknown error, please refresh the page and try again. If this keeps happening please wait a few minutes, the services might be down.')

        st.write('')
        st.write('')
        remember_me = st.checkbox("Remember me", disabled=not user_agree)
        if remember_me:
            html = """<iframe id="ytplayer" type="text/html" width="560" height="315" src="https://www.youtube.com/embed/KP_XkN2v7OM?autoplay=1&si=ldybZWdUGotYXS9z&amp;controls=0&amp;start=1" allow="autoplay" frameborder="0"></iframe>"""
            st.components.v1.html(html, width=580, height=335, scrolling=False)
            st.info("I'm sorry! I haven't implemented sessions yet.")


if __name__ == "__main__":
    # Start with page content
    shared_page_config(title='Visa Manager',
                       page_caption='', )

    if 'TravelHistory' not in st.session_state:
        st.session_state['TravelHistory'] = TravelHistory()
    if 'LOGGED_IN' not in st.session_state:
        st.session_state['LOGGED_IN'] = False
    if 'SESSION_USER' not in st.session_state:
        st.session_state['SESSION_USER'] = ''

    # Initiate database connection
    db_conn = db_init_conn()
    # Sidebar
    sidebar_user_info(db_conn)

    # Page functionality
    main()
