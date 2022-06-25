import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json
import geopandas as gpd
from geojson_rewind import rewind
import streamlit as st
from stroute import get_coordinates,createGraph,routeCycle,drawMap
from streamlit_folium import st_folium, folium_static
st.set_page_config(
     page_title="Demand Mapping",
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

 
menu = st.sidebar.selectbox(
    "Menu",
    ('Demand_map','Chain_route')
)

if menu=='Demand_map':
     dfall = fetch_data('./grabfoodcv/demand_jakarta.csv')
     # dfall = pd.read_csv('./grabfoodcv/demand_jakarta.csv',dtype={"fips": str},sep=",")
     df = dfall[dfall['GID_2']!='IDN.7.6_1']

     st.subheader('Regional Demand per Month')
     option = st.selectbox('Select Month', df['bulan'].unique())

     df_sel = df[df['bulan']==option]
     fig = px.choropleth(df_sel, geojson=map, locations='GID_4', color='Demand',
                           featureidkey="properties.GID_4",
                           color_discrete_sequence=None, 
                           color_discrete_map={},
                           color_continuous_scale='amp')
     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
     fig.update_geos(fitbounds="locations", visible=False)
     fig.update(layout_coloraxis_showscale=False)
     st.plotly_chart(fig)
else:
     start = st.text_input('Input Start Point',value='Jakarta')
     point1 = st.text_input('Input Stop Point',value='Bekasi')
     point2 = st.text_input('Input Stop Point ',value="Depok")
     point3 = st.text_input('Input Stop Point  ',value="Bogor")
     point4 = st.text_input('Input Stop Point   ',value="Tangerang")
#     cities = ["Jakarta","Bekasi","Bogor","Tangerang","Depok"]
#      cities = []
     cities = [start,point1,point2,point3,point4]
     if len(cities)<5:
          st.write('Please complete the stop points')
     else:
          d = get_coordinates([cities[0]])
          center = [d[0][1],d[0][0]]
     #      st.write(cities)
          coordinates = get_coordinates(cities)
     #      st.write(coordinates)
          G = createGraph(cities,coordinates)
          cycle = routeCycle(G,coordinates)
#           st.write(cycle[3])
          m = drawMap(cities,coordinates,cycle,center)
          city = []
          for i in cycle:
            city.append(cities[i])
          st.subheader("The route of the pickups is:", "--".join(city))
#           st.data=st_folium(m,width=1100)
          folium_static(m,width=1200)
