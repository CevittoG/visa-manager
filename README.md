# VisaManager

This Python-based web application, built with Streamlit, simplifies travel planning by automating visa validation for your itineraries. No more scrambling through regulations or worrying about visa surprises at immigration!

### Effortless Planning & Peace of Mind
1. **Get Started**: Head over to the deployed app https://visa-manager-cevittog.streamlit.app and create a free account (optional).
2. **Plan Your Adventures**: Add your trips, specifying destinations and dates. Our visa validation tool checks current regulations to ensure your tourist visa covers your planned stay.
3. **Stay Flexible**: Travel plans can be fluid! Edit your trip details with ease, whether it's adjusting dates, adding a new stop, or extending your stay.
4. **Bulk Up Your Bucket List**: Got a long travel list? Bulk upload your travel data using a CSV file, and the app will validate visas for each stop in a flash.
5. **Offline Access**: Don't let unreliable Wi-Fi hold you back! Download your travel history as a CSV file for offline access.
6. **Explore Visually**: Visualize your travel adventures with an interactive world map! See past and upcoming trips come to life, fueling your wanderlust and inspiring future explorations.

### Example
Planning a multi-country adventure in Europe?
Simply add your destinations (France, Italy, Spain) and planned travel dates.
The app will check visa validity for each country based on current tourist visa regulations.
This ensures you have the appropriate visa for a smooth travel experience.

### Technical Details
* Developed with [Python 3.10](https://www.python.org/downloads/release/python-3100/)
* Database storage with [Supabase](https://supabase.com/) (PostgresSQL)
* Deployment with [Streamlit Cloud](https://streamlit.io/cloud)
* Map visualization with [Folium](https://pypi.org/project/folium/)
* Countries boundaries [geojson file](https://github.com/datasets/geo-countries/blob/master/data/countries.geojson)
