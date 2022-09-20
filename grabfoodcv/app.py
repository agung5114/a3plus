import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import pandas as pd
st.set_page_config(
     page_title="Loc",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded"
 )

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
          df = pd.DataFrame(list(zip([location['lat']],[location['lon']])),columns=['lat', 'lon'])
        # st.write(location)
# location = result.get("GET_LOCATION")
          c1,c2 = st.columns((3,2))
          with c1:
              st.map(df)
          with c2:
              df = pd.read_csv('./grabfoodcv/aqi_jakarta.csv',sep=",")
              loc = get_loc(location['lat'],location['lon'])
              st.table(pd.DataFrame(loc.items(), columns=['Attribute', 'Value']))
              dfsample = df.sample(1)
              st.subheader('AQI value: '+str(dfsample['AQI'].tolist()[0])+'  |  '\
                          +'Quality Level: '+dfsample['Level'].tolist()[0])
              sb = st.button('Submit Air Quality Report')
              if sb:
                  st.write("Submission Successful, coin achieved: 0.002DOT")
