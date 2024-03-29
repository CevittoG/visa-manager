from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT
from helpers.visual import highlight_invalid_trip
from helpers.map import display_map
import streamlit as st
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():

    trips_df = st.session_state['TravelHistory'].to_df()
    if not trips_df.empty:
        columns_to_show = ['type', 'country', 'entry_date', 'exit_date', 'days']
        trips_df = trips_df[columns_to_show]
        # Get map
        clicked_country = display_map(trips_df)
        st.write(clicked_country)
    else:
        st.warning('There is no data to export. Click one of the following buttons to add data.')
        st.page_link("pages/1_➕_Add_Trip.py", label="Add Trip", icon="➕")
        st.page_link("pages/3_📥_Import.py", label="Import", icon="📥")


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = ("Missing description...")
    shared_page_config(title=PAGE_KEYWORD.replace('_', ' ').title(),
                       emoji=PAGE_EMOJI,
                       page_caption=page_caption,
                       initial_sidebar_state='collapsed')

    if 'TravelHistory' not in st.session_state:
        st.session_state['TravelHistory'] = TravelHistory()

    # Page functionality
    main()

