import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import pandas as pd
import numpy as np

loc_button = Button(label="Get Location")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=True,
    override_height=75,
    debounce_time=0)

from urllib.request import urlopen
import json
import requests
def get_loc(lat,lon):
    url=f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(url)
    data = json.loads(response.content)
    return data['address']

if result:
    if "GET_LOCATION" in result:
        location = result.get("GET_LOCATION")
        # st.write(location)
        df = pd.DataFrame(
                list(zip([location['lat']],[location['lon']])),
                columns=['lat', 'lon'])

        st.map(df)
        loc = get_loc(location['lat'],location['lon'])
        st.table(pd.DataFrame(loc.items(), columns=['Attribute', 'Value']))
