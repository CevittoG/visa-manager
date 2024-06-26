from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT, sidebar_setup
from helpers.database import db_init_conn
from helpers.map import display_map
from helpers.visual import ordinal, highlight_invalid_trip
import streamlit as st
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():

    trips_df = st.session_state['TravelHistory'].to_df()
    if not trips_df.empty:
        columns_to_show = ['country', 'entry_date', 'exit_date', 'days']
        # Get map
        clicked_country = display_map(trips_df[columns_to_show])
        c1, _, c2 = st.columns([3, 1, 3])
        if clicked_country != '':
            c1.markdown(f'## {clicked_country}')
            for idx, row in trips_df.loc[trips_df['country'] == clicked_country].iterrows():
                if not row.empty:
                    c1.markdown(f"* #### {idx}{ordinal(idx)} Trip", unsafe_allow_html=True)
                    c1.text(f"\t{'From:':10s}{row['entry_date']}")
                    c1.text(f"\t{'To:':10s}{row['exit_date']}")
                    c1.text(f"\t{'Days:':10s}{row['days']}")
        # Mark with red all invalid trips
        trips_df = trips_df.style.apply(highlight_invalid_trip, axis=1)
        c2.dataframe(trips_df, column_config=TH_DF_CONFIG, column_order=columns_to_show)
    else:
        st.warning('There is no data to export. Click one of the following buttons to add data.')
        st.page_link("pages/1_➕_Add_Trip.py", label="Add Trip", icon="➕")
        st.page_link("pages/3_📥_Import.py", label="Import", icon="📥")


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = (" Feeling like a seasoned explorer? Unleash your inner Marco Polo and visualize your travel conquests on a dazzling world map! See all your past and upcoming trips neatly pinned, transforming your wanderlust into a visual masterpiece.  This isn't just a map – it's your travel brag board, ready to inspire wanderlust in everyone who sees it.")
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

