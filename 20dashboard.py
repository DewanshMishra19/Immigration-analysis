import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px 


#global variable
years = list(map(str, range(1980, 2014)))

#loading data
@st.cache_data
def load_data():
    df1=pd.read_excel('8Canada.xlsx', sheet_name=1,skiprows=20, skipfooter=2)
    cols_to_rename = {
    'OdName':'Country',
    'AreaName':'Continent',
    'RegName':'Region',
    'DevName':'Status'
    }
    df1=df1.rename(columns=cols_to_rename)
    cols_to_drop=["AREA","REG","DEV","Type","Coverage"]
    df1=df1.drop(columns=cols_to_drop)
    df1= df1.set_index('Country')
    df1.columns=[str(name).lower()for name in df1.columns.tolist()]
    df1['total']=df1[years].sum(axis=1)
    df1=df1.sort_values(by='total',ascending=False)
    return df1

#comfiguration the layout
st.set_page_config(
    layout='wide',
    page_title="Immigration Data Analysis",
    page_icon="😑",
)

#loading data
with st.spinner("Loading Data..."):
   df1=load_data()
   st.sidebar.success("Data laoded successfully! 🎉")

#creating the ui interface
c1,c2,c3=st.columns([2,1,1])
c1.title("Immigration Analysis")
c2.header("Summary of data")
total_rows=df1.shape[0]
total_immig=df1.total.sum()
max_immig = df1.total.max()
max_immig_country=df1.total.idxmax()
c2.metric("Total countries", total_rows)
c2.metric("Total Years",len(years))
c2.metric("Total Immigration",f"{total_immig/1000000:.2f}M")
c2.metric("Maximum immigration",f"{max_immig/1000000:.2f}M",
          f"{max_immig_country}")
c3.header("Top 10 Cpuntries")
top_10=df1.head(10)['total']
c3.dataframe(top_10,use_container_width=True)
fig=px.bar(top_10, x=top_10.index, y='total')
c3.plotly_chart(fig,use_container_width=True)

#countries wise visualization
countries=df1.index.tolist()
country=c1.selectbox("Select a country",countries)
immig = df1.loc[country, years]
fig=px.area(immig, x=immig.index, y=immig.values,title="Immigration trend")
c1.plotly_chart(fig,use_container_width=True)
fig2=px.histogram(immig, x=immig.values, nbins=10, marginal="box")
c1.plotly_chart(fig2,use_container_width=True)

max_immig_for_country=immig.max()
max_year= immig.idxmax()
c2.metric(f"Max immigration for {country}",
          f"{max_immig_for_country/1000:.2f}K",
          f"{max_year}")

st.header("continent wise analysis")
c1,c2,c3=st.columns(3)
continents=df1['continent'].unique().tolist()
cdf=df1.groupby('continent')[years].sum()  #groupby continent and sum
cdf['total']=cdf.sum(axis=1)
c1.dataframe(cdf,use_container_width=True)
figcontinent=px.bar(cdf, x=cdf.index, y='total', title='continent wise immigration')
c2.plotly_chart(figcontinent, use_container_width=True)
#mapContinent=px.scatter_geo(df1,locations='continent',
                           # color='total',hover_name='Country',color)
                           
figMap=px.choropleth(df1, locations=df1.index,locationmode='country names',
                     color='total',title="world map",
                     projection="natural earth",
                     width=1000, height=700,
                     template='plotly_dark')
st.plotly_chart(figMap, use_container_width=True)
