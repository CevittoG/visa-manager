from helpers import COUNTRIES, TravelHistory, Trip, SCHENGEN_COUNTRIES
from helpers.streamlit import page_recognition, shared_page_config, TH_DF_CONFIG, DATE_FORMAT
from helpers.visual import highlight_invalid_trip
import streamlit as st
import pandas as pd
from datetime import datetime
import os


# --------------------------------------------------------------------------- PAGE FUNCTIONALITY
def main():
    travel_history_data = st.session_state['TravelHistory'].to_df()
    if travel_history_data.empty:
        st.warning('There is no data to export. Click one of the following buttons to add data.')
        st.page_link("pages/1_➕_Add_Trip.py", label="Add Trip", icon="➕")
        st.page_link("pages/3_📥_Import.py", label="Import", icon="📥")

    else:
        export_type = st.selectbox('Export type', ['File', 'Login'], placeholder='Choose and option...')
        for i in range(3):
            st.markdown('')

        if export_type == 'File':
            travel_history_data = st.session_state['TravelHistory'].to_df()
            if not travel_history_data.empty:
                # Show TravelHistory data
                with st.expander("See TravelHistory"):
                    st.dataframe(travel_history_data, column_config=TH_DF_CONFIG, use_container_width=True)
                # Prepare data
                travel_history_data = travel_history_data.rename({'type': 'Type',
                                                                  'country': 'Country',
                                                                  'entry_date': 'Entry Date',
                                                                  'exit_date': 'Exit Date',
                                                                  'days': '# Days',
                                                                  'limit_date': 'Limit Date',
                                                                  'days_left': 'Days Left',
                                                                  'entry_eval_date': 'Entry Eval Date',
                                                                  'entry_eval_days': 'Entry Eval # Days',
                                                                  'exit_eval_date': 'Exit Eval Date',
                                                                  'exit_eval_days': 'Exit Eval # Days',
                                                                  'renew_date': 'Renew Date',
                                                                  'remove': 'Remove Trip',
                                                                  'is_valid': 'Valid'
                                                                  }).to_csv(index=False, sep=';').encode('utf-8')
                today = datetime.now().strftime('%Y%m%d')
                # Download button
                st.download_button(label="Download TravelHistory", data=travel_history_data, file_name=f'TravelHistory_{today}.csv', mime='text/csv')

        elif export_type == 'Login':
            pass


if __name__ == "__main__":
    # Recognize page name
    PAGE_EMOJI, PAGE_KEYWORD = page_recognition(os.path.basename(__file__))

    # Start with page content
    page_caption = ("Ever get stuck in a charming village with questionable Wi-Fi? Don't sweat it! Download your entire travel history as a handy CSV file. Now you can access all your trip info anytime, anywhere, even if a rogue alpaca decides to munch on your phone charger (hey, it happens!).")
    shared_page_config(title=PAGE_KEYWORD.replace('_', ' ').title(),
                       emoji=PAGE_EMOJI,
                       page_caption=page_caption, )

    if 'TravelHistory' not in st.session_state:
        st.session_state['TravelHistory'] = TravelHistory()

    # Page functionality
    main()
