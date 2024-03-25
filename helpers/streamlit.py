import streamlit as st
import re
from helpers import COUNTRIES

DATE_FORMAT = "MM-DD-YY"
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
    'remove': st.column_config.CheckboxColumn('Remove Trip', required=True)
}


def page_recognition(file_path: str, regex=r'^\d+_([^\w\s,]+)_(.+?)\.py$'):
    regex_search = re.search(regex, file_path)
    PAGE_EMOJI = regex_search.group(1)
    PAGE_KEYWORD = regex_search.group(2).lower()

    return PAGE_EMOJI, PAGE_KEYWORD


def add_logo(logo_url: str, height: int = 120):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6
    The url can either be a url to the image, or a local path to the image.
    Args:
        logo_url (str): URL/local path of the logo
    """

    logo = f"url({logo_url})"
    # else:
    #     logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"

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