from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config
import streamlit as st
import os

########################################################################################################################
# INITIAL PAGE SETTING
########################################################################################################################
# Recognize page name
PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

# Start with page content
page_caption = (" On this page you can edit records from your travel history. It will only be necessary to select the cell you want to edit in the following table, and then complete a new value. If you wish to remove"
                "a trip, just select the last column ('Remove') and then save your changes.")
shared_page_config(title=PAGE_KEYWORD.replace('_', ' ').title(),
                   emoji=PAGE_EMOJI,
                   page_caption=page_caption,)

if 'TravelHistory' not in st.session_state:
    st.session_state['TravelHistory'] = TravelHistory()


########################################################################################################################
# PAGE FUNCTIONALITY
########################################################################################################################
if not st.session_state['TravelHistory'].to_df().empty:
    trips_df = st.session_state['TravelHistory'].to_df()
    trips_df = trips_df[['type', 'country', 'entry_date', 'exit_date', 'days', 'limit_date', 'days_left']]
    trips_df['remove'] = False
    edited_trips_df = st.data_editor(trips_df, column_config=TH_DF_CONFIG)

    if st.button('Save changes', type='primary'):
        st.session_state['TravelHistory'].update_trips(edited_trips_df)
