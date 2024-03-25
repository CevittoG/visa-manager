import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.write("# Visa Manager")

main_tab, schengen_tab, usa_tab = st.tabs(['App Desc', 'Schengen', 'USA'])

schengen_tab.write("""
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
    [*www.schengenvisainfo.com*](https://www.schengenvisainfo.com/visa-calculator/)""")

usa_tab.write("""
    ## Visa Waiver USA
    something...""")