import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json
import geopandas as gpd
from geojson_rewind import rewind
import streamlit as st

# f = gpd.read_file('./grabfoodcv/jakarta.shp')
f = gpd.read_file('./grabfoodcv/jakarta.geojson')
geo_ur = json.loads(f.to_json())
map = rewind(geo_ur,rfc7946=False)

# map = gpd.read_file('/content/drive/MyDrive/Hackathon/jakarta.geojson')
# map = json.load('/content/drive/MyDrive/Hackathon/jakarta.geojson')
# map = json.load(response)
# dfall = pd.read_csv('/content/drive/MyDrive/Hackathon/jakarta.csv',dtype={"fips": str},sep=",")
dfall = pd.read_csv('./grabfoodcv/demand_jakarta.csv',dtype={"fips": str},sep=",")
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
c1,c2 = st.columns((1,1))
# with c1:
st.plotly_chart(fig)
# with c2:
# import plotly.graph_objects as go
# line=df['tanggal'].tolist()

# fig = go.Figure(data=[
#     go.Bar(name=line, x=line, y=df['Demand']),
#     go.Bar(name=line, x=line, y=df['Local_stock'])
# ])
# # Change the bar mode
# fig.update_layout(barmode='group')

# df['tanggal'] = df['tanggal'].astype('date')
fig = px.line(df,x= 'tanggal', y='Wasted')
st.plotly_chart(fig)
