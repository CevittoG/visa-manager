import streamlit as st
from helpers.streamlit import shared_page_config, sidebar_setup, user_login
from helpers.database import db_init_conn, user_sing_up
from helpers import TravelHistory
import os

MAIN_DESC = """
## App Features
Dreaming of exotic adventures but worried about visa restrictions? This app is your all-in-one travel companion, designed to make exploring the world smoother than ever.  Here's how it helps:

* **Plan and Conquer**: Planning your next adventure? Add your destination and activities – our visa validation tool will check if your tourist visa allows them, avoiding any unwanted surprises at immigration!

* **Stay Flexible**: Travel plans change! Edit your trip details with ease, whether it's a last-minute location switch, extending your stay, or following a spontaneous detour.

* **Become a Power Traveler**: Got a long travel itinerary? Ditch the manual entry! Upload a file with all your adventures, and our app will validate your visas for each stop in a flash.

* **Offline Access, No Worries**: Don't let unreliable Wi-Fi hold you back! Download your entire travel history as a file for offline access. Now you can see all your trip info anytime, anywhere.

* **Explore Visually**: Feeling like a seasoned explorer? See all your past and upcoming trips pinned on a beautiful world map, transforming your wanderlust into a visual masterpiece. It's your brag board of amazing destinations, ready to inspire wanderlust in everyone!"""
SCHENGEN_DESC = """
## Schengen Tourist Visa
[The Schengen area](https://www.schengenvisainfo.com/schengen-visa-countries-list/) represents a border-free zone 
between several European countries. In addition, these countries issue a uniform Schengen visa for foreign 
nationals. To control the comings and goings of millions of people who enter the Schengen area, the 90/180-day rule 
was established.

What does it mean?

The 90/180-day rule states that any foreign national who enters the 
Schengen zone (any country within the area) can stay for up to 90 days within **any 180 days**. At first glance, it 
seems a very simple rule, but it’s often misunderstood, and many people overstay it, resulting in them facing 
penalties. This is why it’s important to know how exactly the 90/180-day rule works. 
[*www.schengenvisainfo.com*](https://www.schengenvisainfo.com/visa-calculator/)"""
USA_DESC = """
## ESTA Visa Waiver USA
The [Visa Waiver Program (VWP)](https://www.usa.gov/visa-waiver-esta) allows citizens of participating countries to travel to the U.S. for business or pleasure for stays of up to 90 days per visit. This flexibility lets you plan your dream itinerary!

Here's an example: Imagine you're participating on the VWP planning a trip to the U.S. The 90-day limit per visit gives you the option to:

* Double the Adventure: Take two separate 90-day trips across the year, exploring different regions or coasts.
* Multiple Mini-Escapes: Plan shorter, more frequent trips – maybe 9 visits of 20 days each, spread throughout the year.
**Remember, these are just examples!** The VWP allows for a maximum total stay of 180 days within a one-year period.

**Important Note**: While our app can help you explore potential itineraries, it's crucial to  verify your specific eligibility and any limitations with the official  U.S. Department of State website or your local U.S. Embassy/Consulate.

[Complete your ESTA application online](https://esta.cbp.dhs.gov/)"""


def main():
    main_tab, schengen_tab, usa_tab = st.tabs(['App Desc', 'Schengen', 'USA'])

    schengen_tab.write(SCHENGEN_DESC)
    usa_tab.write(USA_DESC)

    with main_tab:

        if not st.session_state['LOGGED_IN']:
            st.markdown("## Sing-up")
            st.markdown("Creating an account is optional, but it lets you save your meticulously planned itineraries. That means next time you're ready to conquer the world, you can pick up right where you left off, skipping the hassle of re-entering all those details. More time exploring, less time planning")
            user_agree = st.checkbox("By checking this box, you agree to assume all responsibility for the content you create and share within the app.")
            c1, c2, c3 = st.columns([2, 2, 1])

            user = c1.text_input(label='Username', placeholder="Username", key="user_signup", autocomplete="email", label_visibility='collapsed', disabled=not user_agree)
            pswd = c2.text_input(label='Password', placeholder="Password", key="password_signup", type="password", autocomplete="on", label_visibility='collapsed', disabled=not user_agree)
            if c3.button('Sing-up', type='primary', disabled=not user_agree):
                new_user = user_sing_up(db_conn, user, pswd)
                if isinstance(new_user, str):
                    st.error(new_user)
                else:
                    user_login(db_conn, *new_user)
            st.write('')
            st.write('')
            remember_me = st.checkbox("Remember me", disabled=not user_agree)
            if remember_me:
                html = """<iframe id="ytplayer" type="text/html" width="560" height="315" src="https://www.youtube.com/embed/KP_XkN2v7OM?autoplay=1&si=ldybZWdUGotYXS9z&amp;controls=0&amp;start=1" allow="autoplay" frameborder="0"></iframe>"""
                st.components.v1.html(html, width=580, height=335, scrolling=False)
                st.info("I'm sorry! I haven't implemented sessions yet.")
        else:
            st.markdown(f"## Welcome {st.session_state.SESSION_USER['username']}!")

        st.write(MAIN_DESC)


if __name__ == "__main__":
    # Start with page content
    shared_page_config(title='Visa Manager',
                       page_caption='', )

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
