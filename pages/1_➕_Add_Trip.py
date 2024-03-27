from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT
from helpers.visual import highlight_invalid_trip
import streamlit as st
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])

    country = c1.selectbox('Country', SCHENGEN_COUNTRIES)
    entry_date = c2.date_input('Entry date', format=DATE_FORMAT)
    exit_date = c3.date_input('Exit date', format=DATE_FORMAT)
    c4.text("")
    c4.text("")
    if c4.button('Add trip', type='primary'):
        new_trip = Trip(country, entry_date, exit_date)
        st.session_state['TravelHistory'].add_trip(new_trip)
        st.toast(f":{'green' if new_trip.valid else 'red'}[{new_trip}]", icon='✅' if new_trip.valid else '⛔')

    # Show TravelHistory data
    trips_df = st.session_state['TravelHistory'].to_df()
    if not trips_df.empty:
        # Mark with red all invalid trips
        trips_df = trips_df.style.apply(highlight_invalid_trip, axis=1)
        columns_to_show = ['type', 'country', 'entry_date', 'exit_date', 'days', 'limit_date', 'days_left', 'entry_eval_date', 'entry_eval_days', 'exit_eval_date', 'exit_eval_days', 'renew_date']
        st.dataframe(trips_df, column_config=TH_DF_CONFIG, column_order=columns_to_show)


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = ("On this page you can add trips to your travel history. It will only be necessary to select country and dates, the app will do the rest...")
    shared_page_config(title=PAGE_KEYWORD.replace('_', ' ').title(),
                       emoji=PAGE_EMOJI,
                       page_caption=page_caption, )

    if 'TravelHistory' not in st.session_state:
        st.session_state['TravelHistory'] = TravelHistory()

    # Page functionality
    main()
