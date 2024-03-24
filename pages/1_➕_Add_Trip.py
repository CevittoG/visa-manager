from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
import streamlit as st

# --------------------------------------------------------------------------------------------- PLATFORM INIT
st.set_page_config(
    page_title="VISA",
    page_icon="🗺️",
    layout="wide"
)

st.title('Visa Manager')
if 'TravelHistory' not in st.session_state:
    st.session_state['TravelHistory'] = TravelHistory()


c1, c2, c3, c4 = st.columns([2, 1, 1, 1])

country = c1.selectbox('Country', SCHENGEN_COUNTRIES)
entry_date = c2.date_input('Entry date')
exit_date = c3.date_input('Exit date')
c4.text("")
c4.text("")
if c4.button('Add trip'):
    new_trip = Trip(country, entry_date, exit_date)
    st.session_state['TravelHistory'].add_trip(new_trip)
    st.write(new_trip)

if not st.session_state['TravelHistory'].to_df().empty:
    st.write(st.session_state['TravelHistory'].to_df())
