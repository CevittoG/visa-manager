from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT, sidebar_setup
from helpers.database import db_init_conn
from helpers.map import display_map
import streamlit as st
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():

    trips_df = st.session_state['TravelHistory'].to_df()
    if not trips_df.empty:
        columns_to_show = ['country', 'entry_date', 'exit_date', 'days']
        # Get map
        clicked_country = display_map(trips_df[columns_to_show])
        if clicked_country != '':
            st.markdown(f'## {clicked_country}')
            # ToDo: Show trips data
            for idx, row in trips_df.loc[trips_df['country'] == clicked_country].iterrows():
                if not row.empty:
                    st.markdown(f"### #{idx}\n\n{row['entry_date']} to {row['exit_date']} - {row['days']} days")
    else:
        st.warning('There is no data to export. Click one of the following buttons to add data.')
        st.page_link("pages/1_➕_Add_Trip.py", label="Add Trip", icon="➕")
        st.page_link("pages/3_📥_Import.py", label="Import", icon="📥")


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = ("Missing description...")  # ToDo: Missing description
    shared_page_config(title=PAGE_KEYWORD.replace('_', ' ').title(),
                       emoji=PAGE_EMOJI,
                       page_caption=page_caption,
                       initial_sidebar_state='collapsed')

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

