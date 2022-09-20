import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json
import geopandas as gpd
from geojson_rewind import rewind
import streamlit as st
from stroute import get_coordinates,createGraph,routeCycle,drawMap
from streamlit_folium import st_folium, folium_static
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import json
import requests
def get_loc(lat,lon):
    url=f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(url)
    data = json.loads(response.content)
    return data['address']
st.set_page_config(
     page_title="AQI",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded"
 )

f = gpd.read_file('./grabfoodcv/jakarta.geojson')
geo_ur = json.loads(f.to_json())
map = rewind(geo_ur,rfc7946=False)

@st.cache
def fetch_data(url):
     data = pd.read_csv(url,dtype={"fips": str},sep=",")
     return data
# menu = st.sidebar.selectbox(
#     "Menu",
#     ('Demand_map','Chain_route')
# )
st.subheader('AQI per State')
# if menu=='Demand_map':
c1,c2,c3 = st.columns((5,1,5))
with c1:
     df = fetch_data('./grabfoodcv/aqi_jakarta.csv')
     st.dataframe(df)
#      dfall = fetch_data('./grabfoodcv/demand_jakarta.csv')
     # dfall = pd.read_csv('./grabfoodcv/demand_jakarta.csv',dtype={"fips": str},sep=",")
#      df = dfall[dfall['GID_2']!='IDN.7.6_1']
     df = df[df['State']!='KAB.ADM.KEP.SERIBU']
#      option = st.selectbox('Select Month', df['bulan'].unique())
     option = st.selectbox('Select State', ['All']+df['State'].unique().tolist())
    
     if option=='All':
        df = df
     else:
        df = df[df['State']==option]
     fig = px.choropleth(df, geojson=map, locations='GID_4', 
                           color='Level',
                           featureidkey="properties.GID_4",
#                            color_discrete_sequence=None, 
                           color_discrete_map={'Good':'green','Fair':'yellow','Poor':'orange','Very Poor':'red','Hazardous':'darkred'},
#                            color_continuous_scale='Portland'
                        )
     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
     fig.update_geos(fitbounds="locations", visible=False)
     fig.update(layout_coloraxis_showscale=False)
     st.plotly_chart(fig)
with c2:
    st.empty()
with c3:
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
     
# else:
# c1,c2 = st.columns((1,2))
# with c1:
#      start = st.text_input('Input Start Point',value='Jakarta')
#      point1 = st.text_input('Input Stop Point',value='Depok')
#      point2 = st.text_input('Input Stop Point ',value="Bekasi")
#      point3 = st.text_input('Input Stop Point  ',value="Bogor")
# #      point4 = st.text_input('Input Stop Point   ',value="Tangerang")
#      #     cities = ["Jakarta","Bekasi","Bogor","Tangerang","Depok"]
#      #      cities = []
# #      cities = [start,point1,point2,point3,point4]
#      cities = [start,point1,point2,point3]
# with c2:
#      if len(cities)<4:
#           st.write('Please complete the stop points')
#      else:
#           d = get_coordinates([cities[0]])
#           center = [d[0][1],d[0][0]]
#      #      st.write(cities)
#           coordinates = get_coordinates(cities)
#      #      st.write(coordinates)
#           G = createGraph(cities,coordinates)
#           cycle = routeCycle(G,coordinates)
#      #           st.write(cycle[3])
#           m = drawMap(cities,coordinates,cycle,center)
#           city = []
#           for i in cycle:
#             city.append(cities[i])
#           st.subheader("The route of the pickups is:", "--".join(city))
#      #           st.data=st_folium(m,width=1100)
#           folium_static(m,width=715)
