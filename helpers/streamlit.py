import streamlit as st
import re
import supabase
from helpers import COUNTRIES
from helpers.database import db_select, db_update, get_user_trips
from helpers.database import db_select, get_user_trips, db_upsert

DATE_FORMAT = "MM-DD-YYYY"
TH_DF_CONFIG = {
    'type': st.column_config.TextColumn('Type', disabled=True),
    'country': st.column_config.SelectboxColumn('Country', options=COUNTRIES, required=True),
    'entry_date': st.column_config.DateColumn('Entry Date', format=DATE_FORMAT, required=True),
    'exit_date': st.column_config.DateColumn('Exit Date', format=DATE_FORMAT, required=True),
    'days': st.column_config.NumberColumn('# Days', disabled=True),
    'limit_date': st.column_config.DateColumn('Limit Date', format=DATE_FORMAT, disabled=True),
    'days_left': st.column_config.NumberColumn('Days Left', disabled=True),
    'entry_eval_date': st.column_config.DateColumn('Entry Eval Date', format=DATE_FORMAT, disabled=True),
    'entry_eval_days': st.column_config.NumberColumn('Entry Eval # Days', disabled=True),
    'exit_eval_date': st.column_config.DateColumn('Exit Eval Date', format=DATE_FORMAT, disabled=True),
    'exit_eval_days': st.column_config.NumberColumn('Exit Eval # Days', disabled=True),
    'renew_date': st.column_config.DateColumn('Renew Date', format=DATE_FORMAT, disabled=True),
    'remove': st.column_config.CheckboxColumn('Remove Trip', required=True),
    'is_valid': st.column_config.CheckboxColumn('Valid', disabled=True)
}


def page_recognition(file_path: str, regex=r'^\d+_([^\w\s,]+)_(.+?)\.py$'):
    regex_search = re.search(regex, file_path)
    PAGE_EMOJI = regex_search.group(1)
    PAGE_KEYWORD = regex_search.group(2).lower()

    return PAGE_EMOJI, PAGE_KEYWORD


def add_logo(logo_url: str, height: int = 120):
    logo = f"url({logo_url})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def shared_page_config(title="", image="", initial_sidebar_state="expanded", emoji="", page_caption=None):  # ("auto" or "expanded" or "collapsed")
    # Set up the pages
    st.set_page_config(layout="wide", page_title='VISA Manager - ' + title, page_icon="🗺️", initial_sidebar_state=initial_sidebar_state)
    # Show if debug mode
    if st.secrets['DEBUG']:
        st.warning("DEBUG IS ACTIVATED")

    # Hide the menu and footer
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # Display the title, if any
    if title:
        st.title(emoji + " "*bool(emoji) + title)
    # Add the logo, if anys
    if image:
        add_logo(image, height=20)
    # Add page caption, if exists
    if page_caption is not None:
        st.caption(page_caption)

    return


def sidebar_user_info(db_conn: supabase.Client):
    # Check if users as logged in
    if not st.session_state['LOGGED_IN']:
        if st.secrets['DEBUG']:
            user_login(db_conn, 30, 'TestUser', 3)
        st.sidebar.markdown('## Login')
        user = st.sidebar.text_input(label='Username', placeholder="Username", key="username", autocomplete='on', label_visibility='collapsed')
        pswd = st.sidebar.text_input(label='PIN', placeholder="PIN", key="pin", type="password", autocomplete="on", label_visibility='collapsed', help='Personal Identification Number (numeric)')

        if st.sidebar.button('Login', type='primary', disabled=user is None and pswd is None):
            select_response = db_select(db_conn, 'users', ['id', 'username', 'password'], ('username', 'eq', str(user)))
            # Check for query error
            if isinstance(select_response, str):
                st.error('Unknown error, please refresh the page and try again. If this keeps happening please wait a few minutes, the services might be down.')
            # Check if user exists
            elif len(select_response) == 0:
                st.sidebar.warning("Username doesn't exist, please create an user on main page")
            # Check password
            elif pswd == str(select_response[0]['password']):
                th_id = db_select(db_conn, 'travel_history', 'id', ('user_id', 'eq', select_response[0]['id']))[0]['id']
                user_login(db_conn, select_response[0]['id'], select_response[0]['username'], th_id)

    else:
        st.sidebar.markdown(f"## {st.session_state.SESSION_USER['username']}")
        if st.session_state.SESSION_USER['last_login'] is not None:
            st.sidebar.markdown(f"Last seen on {st.session_state.SESSION_USER['last_login']}")

        # Export streamlit's TravelHistory session_state variable into db
        if st.sidebar.button('Save changes', type='primary', key='save'):
            # Current trips as a list of tuples
            trips_list = st.session_state['TravelHistory'].to_records()
            if trips_list:
                # Trip_id related to user
                trips_ids = db_select(db_conn, 'travel_history_trips', 'trip_id', ('travel_history_id', 'eq', st.session_state.SESSION_USER['th_id']))

                # Create json_data for upsert
                if trips_ids:
                    upsert_trips_data = []
                    for trip_id_dict, trip_info in zip(trips_ids, trips_list):
                        # Combine dictionary and tuple elements into a new dictionary
                        trip_info_dict = {**trip_id_dict, **dict(zip(['country', 'entry_date', 'exit_date'], trip_info))}
                        upsert_trips_data.append(trip_info_dict)
                else:
                    upsert_trips_data = [{'country': t[0], 'entry_date': t[1], 'exit_date': t[2]} for t in trips_list]

                upsert_trips = db_upsert(db_conn, 'trips', upsert_trips_data)

                # Check for query error
                if isinstance(upsert_trips, str):
                    st.sidebar.error('Unknown error, please refresh the page and try again. If this keeps happening please wait a few minutes, the services might be down.')
                elif len(upsert_trips) > 0:
                    upsert_travel_history_trips_data = [{'travel_history_id': st.session_state.SESSION_USER['th_id'], 'trip_id': t['id']} for t in upsert_trips]
                    upsert_travel_history_trips = db_upsert(db_conn, 'travel_history_trips', upsert_travel_history_trips_data)
                    # Check for query error
                    if isinstance(upsert_travel_history_trips, str):
                        st.sidebar.error('Unknown error, please refresh the page and try again. If this keeps happening please wait a few minutes, the services might be down.')
                    elif len(upsert_travel_history_trips) > 0:
                        st.sidebar.success("Data saved")
            else:
                st.sidebar.warning('There is no new data to save')


def user_login(db_conn, user_id, username, th_id):
    # Update streamlit variables
    st.session_state['LOGGED_IN'] = True
    st.session_state['SESSION_USER'] = {'user_id': user_id,
                                        'username': username,
                                        'last_login': db_select(db_conn, 'users', 'last_login', ('id', 'eq', str(user_id)))[0]['last_login'],
                                        'th_id': th_id}
    # st.session_state['TravelHistory'] =
    print(get_user_trips(db_conn, th_id))
    # Refresh page
    st.rerun()
