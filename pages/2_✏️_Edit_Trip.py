from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT, sidebar_setup
from helpers.visual import highlight_invalid_trip
from helpers.database import db_init_conn
import streamlit as st
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():
    # Show TravelHistory data
    trips_df = st.session_state['TravelHistory'].to_df()
    if not trips_df.empty:
        trips_df = st.session_state['TravelHistory'].to_df()
        trips_df['remove'] = False
        # Mark with red all invalid trips
        trips_df = trips_df.style.apply(highlight_invalid_trip, axis=1)
        columns_to_show = ['type', 'country', 'entry_date', 'exit_date', 'days', 'limit_date', 'days_left', 'remove']
        edited_trips_df = st.data_editor(trips_df, column_config=TH_DF_CONFIG, column_order=columns_to_show)

        if st.button('Save changes', type='primary'):
            messages = st.session_state['TravelHistory'].update_trips(edited_trips_df)
            for msg in messages:
                st.toast(msg[0], icon=msg[1])


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = ("Travel plans are rarely set in stone, especially for the adventurous soul! Did you discover a hidden gem that deserves an extra day of exploration? No worries! Edit your trip details here with ease, whether it's a last-minute location change, extended stay, or a spontaneous detour to chase a local festival.")
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
