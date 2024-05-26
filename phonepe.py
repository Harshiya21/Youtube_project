import streamlit as st
import pandas as pd 
import mysql.connector
import matplotlib.pyplot as plt 
import plotly.express as px 
import requests 
import json 


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="phonepae")
print(mydb)
mycursor = mydb.cursor(buffered=True)

#Data retrieval from MYSQL DATABASE TO DATAFRAME to update the streamllit dashboard
mycursor.execute('select *from phonepae.Agg_Trans')
Agg_Trans_df=pd.DataFrame(mycursor.fetchall(),columns=["State","Year","Quarter",
                                                        "Transaction_type","Transaction_count","Transaction_amount"])


#AGG USERS 
mycursor.execute('select *from phonepae.Agg_Users')
Agg_Users_df=pd.DataFrame(mycursor.fetchall(),columns=["State","Year","Quarter",
                                                        "Brand","Count","Percentage"])

#MAP TRANS
mycursor.execute('select *from phonepae.Map_Trans')
Map_Trans_df=pd.DataFrame(mycursor.fetchall(),columns=["State","Year","Quarter",
                                                        "District","Metric_count","Metric_amount"])

#MAP USERS
mycursor.execute('select *from phonepae.Map_Users')
Map_Users_df=pd.DataFrame(mycursor.fetchall(),columns=["State","Year","Quarter",
                                                        "Districts","RegisteredUsers", "AppOpens"])

#TOP TRANS
mycursor.execute('select *from phonepae.Top_Trans')
Top_Trans_df=pd.DataFrame(mycursor.fetchall(),columns=["State","Year","Quarter",
                                                        "Pincodes","Metric_count","Metric_amount"])

#TOP USERS 
mycursor.execute('select *from phonepae.Top_Users')
Top_Users_df=pd.DataFrame(mycursor.fetchall(),columns=["State","Year","Quarter",
                                                        "Pincodes","RegisteredUsers"])
#AGG TRANSACTION
def Transaction_amount_count_Y(df, year):
    tacy = df[df['Year'] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="State", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="State", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=600, width=600)
        st.plotly_chart(fig_count)
    
    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="State",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

        return tacy

def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df['Quarter'] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="State", y="Transaction_amount", title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset)

        st.plotly_chart(fig_amount)
    
    with col2:

        fig_count=px.bar(tacyg, x="State", y="Transaction_count", title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Emrld)
                        
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="State",title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

        return tacy

def Agg_tran_Transaction_type(df,state):
    Atcy=df[df["State"]== state]
    Atcy.reset_index(drop=True, inplace=True)

    Atcyg=Atcy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    Atcyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_line_1=px.line(Atcyg, x="Transaction_type", y="Transaction_count", title=f"{state.upper()} TRANSACTION COUNT",
                width=1000,markers =True,color_discrete_sequence=px.colors.sequential.Magma)
                        
        st.plotly_chart(fig_line_1)
    
    with col2:
        fig_line_2=px.line(Atcyg, x="Transaction_type", y="Transaction_amount", title=f"{state.upper()} TRANSACTION AMOUNT",
                width=1000,markers =True,color_discrete_sequence=px.colors.sequential.Plasma)
                        
        st.plotly_chart(fig_line_2)

#MAP TRANSACTION

def Map_trans_amount_Y(df,year):
    macy=df[df['Year'] == year]
    macy.reset_index(drop=True, inplace=True)

    macyg=macy.groupby("State")[["Metric_count","Metric_amount"]].sum()
    macyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(macyg, x="State", y="Metric_amount", title=f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Reds_r)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(macyg, x="State", y="Metric_count", title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Purples_r)
                        
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(macyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_amount",color_continuous_scale="Rainbow",
                                range_color=(macyg["Metric_amount"].min(), macyg["Metric_amount"].max()),
                                hover_name="State",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(macyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_count",color_continuous_scale="Rainbow",
                                range_color=(macyg["Metric_count"].min(), macyg["Metric_count"].max()),
                                hover_name="State",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        return macy

def Map_trans_amount_Y_Q(df,quarter):
    macy=df[df['Quarter'] == quarter]
    macy.reset_index(drop=True, inplace=True)

    macyg=macy.groupby("State")[["Metric_count","Metric_amount"]].sum()
    macyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(macyg, x="State", y="Metric_amount", title=f"{macy['Year'].min()} Year {quarter} Quarter TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Sunset)

        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count=px.bar(macyg, x="State", y="Metric_count", title=f"{macy['Year'].min()} Year {quarter} Quarter TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
                        
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(macyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_amount",color_continuous_scale="Rainbow",
                                range_color=(macyg["Metric_amount"].min(), macyg["Metric_amount"].max()),
                                hover_name="State",title=f"{macy['Year'].min()} Year {quarter} Quarter TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(macyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_count",color_continuous_scale="Rainbow",
                                range_color=(macyg["Metric_count"].min(), macyg["Metric_count"].max()),
                                hover_name="State",title=f"{macy['Year'].min()} Year {quarter} Quarter TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
            
        return macy
    
def Map_trans_district(df,state):
    mtcy=df[df["State"]== state]
    mtcy.reset_index(drop=True, inplace=True)

    mtcyg=mtcy.groupby("District")[["Metric_count","Metric_amount"]].sum()
    mtcyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1=px.bar(mtcyg, x="Metric_count", y="District", title=f"{state.upper()} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis_r)
        
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(mtcyg, x="Metric_amount", y="District", title=f"{state.upper()} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.dense_r)
        
        st.plotly_chart(fig_bar_2)

#TOP TRANSACTION
def Top_trans_amt_count_Y(df,year):
    tacy=df[df['Year'] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("State")[["Metric_count","Metric_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg, x="State", y="Metric_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Reds_r)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg, x="State", y="Metric_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Purples_r)
                        
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Metric_amount"].min(), tacyg["Metric_amount"].max()),
                                hover_name="State",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:   
        fig_india_2=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Metric_count"].min(), tacyg["Metric_count"].max()),
                                hover_name="State",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        return tacy
    
def Top_trans_amt_count_Y_Q(df,quarter):
    tacy=df[df['Quarter'] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("State")[["Metric_count","Metric_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg, x="State", y="Metric_amount", title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Rainbow)

        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count=px.bar(tacyg, x="State", y="Metric_count", title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r)
                        
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:   
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for features in data1["features"]:
            state_name.append(features["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Metric_amount"].min(), tacyg["Metric_amount"].max()),
                                hover_name="State",title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2: 
        fig_india_2=px.choropleth(tacyg,geojson= data1,locations= "State", featureidkey= "properties.ST_NM",
                                color="Metric_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Metric_count"].min(), tacyg["Metric_count"].max()),
                                hover_name="State",title=f"{tacy['Year'].min()} Year {quarter} Quarter TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
            
        return tacy

def Top_trans_district(df,state):
    tts=Top_trans_Y[Top_trans_Y["State"]== "West Bengal"]
    tts.reset_index(drop=True, inplace=True)

    ttsg=tts.groupby("Pincodes")[["Metric_count","Metric_amount"]].sum()
    ttsg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1: 
        fig_bar_1=px.bar(tts,x="Quarter", y="Metric_count", title="TRANSACTION COUNT",
                            hover_data="Pincodes", color_discrete_sequence=px.colors.sequential.Cividis_r)
            
        st.plotly_chart(fig_bar_1)

    with col2: 
        fig_bar_2=px.bar(tts, x="Quarter", y="Metric_amount", title="TRANSACTION AMOUNT",
                            hover_data="Pincodes", color_discrete_sequence=px.colors.sequential.dense_r)
            
        st.plotly_chart(fig_bar_2)    

#AGG USERS
def Agg_users_count_Y(df,year):
    aucy=df[df['Year'] == year]
    aucy.reset_index(drop=True, inplace=True)

    aucyg=pd.DataFrame(aucy.groupby("Brand")["Count"].sum())
    aucyg.reset_index(inplace=True)

    fig_bar=px.bar(aucyg, x="Brand", y="Count", title=f"{year} BRAND and COUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_bar)
    return aucy

def Agg_users_count_Y_Q(df,quarter):
    aucy=df[df['Quarter'] == quarter]
    aucy.reset_index(drop=True, inplace=True)

    aucyg=pd.DataFrame(aucy.groupby("Brand")["Count"].sum())
    aucyg.reset_index(inplace=True)

    fig_bar=px.bar(aucyg, x="Brand", y="Count", title=f"{aucy['Year'].min()} Year {quarter} Quarter BRAND AND COUNT",
                    color_discrete_sequence=px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_bar)
    return aucy

def Agg_user_count_s(df,state):
    Aucs=df[df["State"]== state]
    Aucs.reset_index(drop=True, inplace=True)

    Aucsg=Aucs.groupby("Brand")[["Count","Percentage"]].sum()
    Aucsg.reset_index(inplace=True)

    fig_pie=px.pie(Aucsg, names="Brand", values="Count", title=f"{state.upper()} BRAND, COUNT,PERCENTAGE",
                width=600,hover_data="Percentage",hole=0.5)
    
    st.plotly_chart(fig_pie)

#MAP Users
def Map_users_Y(df,year):
    muy=df[df['Year'] == year]
    muy.reset_index(drop=True, inplace=True)

    muyg=muy.groupby("State")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1=px.bar(muyg, x="State", y="RegisteredUsers", title=f"{year} RegisteredUsers",
                        color_discrete_sequence=px.colors.sequential.Jet)

        st.plotly_chart(fig_bar_1)
    
    with col2:
        fig_bar_2=px.bar(muyg, x="State", y="AppOpens", title=f"{year} AppOpens",
                    color_discrete_sequence=px.colors.sequential.Greens_r)

        st.plotly_chart(fig_bar_2)

        return muy
    
def Map_users_Q(df,quarter):
    muyq=df[df['Quarter'] == quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg= muyq.groupby("State")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line=px.line(muyqg, x="State", y=["RegisteredUsers","AppOpens"], title=f"{quarter} REGISTEREDUSERS AND APPOPENS",
                    width=1000,height= 800,markers= True, color_discrete_sequence=px.colors.sequential.Magenta_r )

    st.plotly_chart(fig_line)

    return muyq

def Map_user_s(df,state):
    mus=df[df["State"]== state]
    mus.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1=px.bar(mus,x="RegisteredUsers", y="Districts", title=f"{state.upper()} RegisteredUsers",
                    width=600,color_discrete_sequence=px.colors.sequential.Redor )
        
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(mus,x="AppOpens", y="Districts", title=f"{state.upper()} AppOpens",
                    width=600,color_discrete_sequence=px.colors.sequential.RdBu)
        
        st.plotly_chart(fig_bar_2)

#TOP USERs
def Top_users_Y(df,year):
    tuy=df[df['Year'] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["State","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_bar_1=px.bar(tuyg, x="State", y="RegisteredUsers",color="Quarter",title=f"{year} RegisteredUsers",
                    color_discrete_sequence=px.colors.sequential.OrRd)

    st.plotly_chart(fig_bar_1)

    return tuy

def Top_users_state(df,state):
    tuy=df[df['State'] == state]
    tuy.reset_index(drop=True, inplace=True)

    fig_bar=px.bar(tuy, x="Quarter", y="RegisteredUsers",title="RegisteredUsers,Pincodes,Quarter",
                    color="RegisteredUsers",hover_data="Pincodes", color_discrete_sequence=px.colors.sequential.Rainbow)

    st.plotly_chart(fig_bar)

#streamlit part 

st.set_page_config(
    page_title="Phonep Pulse",
    page_icon="c:/Users/nawas/Downloads/phonepe image.png",
    layout="wide")

st.title(':violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]')

with st.sidebar:
    select= st.sidebar.selectbox("Select the Menu",["HOME", "GEO VISUALIZATION", "INSIGHTS"])

if select == "HOME":

    col1,col2 = st.columns(2)

    with col1:
        st.header(":violet[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.write("****FEATURES****")
        st.write("****✳Credit & Debit card linking****")
        st.write("****✳Bank Balance check****")
        st.write("****✳Money Storage****")
        st.write("****✳PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/about-us/")

    with col2:
        video_file1 = open(r"c:\Users\nawas\Downloads\pulse-video.mp4",'rb')
        video_bytes = video_file1.read()

        st.video(video_bytes)

elif select == "GEO VISUALIZATION":
    
    tab1,tab2=st.tabs(["Transactions","Users"])
    
    with tab1:
        
        method1 = st.radio("Selct an option",["Agg Transactions","Map Transactions","Top Transactions"])
            
        if method1 == "Agg Transactions":
            years=st.slider("Select the Year_Tr",Agg_Trans_df["Year"].min(),Agg_Trans_df["Year"].max(),Agg_Trans_df["Year"].min())
            Agg_Trans_tac_Y=Transaction_amount_count_Y(Agg_Trans_df,years)
            quarters = st.selectbox("Select the Quarter", Agg_Trans_tac_Y["Quarter"].unique())
            Agg_Trans_tac_Y_Q=Transaction_amount_count_Y_Q(Agg_Trans_tac_Y,quarters)
            states = st.selectbox("Select the State", Agg_Trans_tac_Y["State"].unique())
            Agg_tran_Transaction_type(Agg_Trans_tac_Y_Q, states)

        elif method1 =="Map Transactions":  
            years=st.slider("Select the Year_Tr",Map_Trans_df["Year"].min(),Map_Trans_df["Year"].max(),Map_Trans_df["Year"].min())     
            Map_trans_Y=Map_trans_amount_Y(Map_Trans_df,years)
            quarters = st.selectbox("Select the Quarter", Map_trans_Y["Quarter"].unique())
            Map_trans_Y_Q = Map_trans_amount_Y_Q(Map_trans_Y,quarters)
            states = st.selectbox("Select the State", Map_trans_Y["State"].unique())           
            Map_trans_district(Map_trans_Y_Q, states)

        elif method1 =="Top Transactions":   
            years=st.slider("Select the Year_Tr",Top_Trans_df["Year"].min(),Top_Trans_df["Year"].max(),Top_Trans_df["Year"].min())     
            Top_trans_Y=Top_trans_amt_count_Y(Top_Trans_df,years)
            quarters = st.selectbox("Select the Quarter", Top_trans_Y["Quarter"].unique())
            Top_trans_Y_Q = Top_trans_amt_count_Y_Q(Top_trans_Y,quarters)
            states = st.selectbox("Select the State", Top_trans_Y["State"].unique()) 
            Top_trans_district(Top_trans_Y_Q ,states)
    
    with tab2:
        
        method2 = st.radio("Selct an option",["Agg Users","Map Users","Top Users"])  

        if method2 =="Agg Users":
            years=st.slider("Select the Year_Us",Agg_Users_df["Year"].min(),Agg_Users_df["Year"].max(),Agg_Users_df["Year"].min())     
            Agg_user_Y = Agg_users_count_Y(Agg_Users_df,years)
            quarters = st.selectbox("Select the Quarter_Us", Agg_user_Y["Quarter"].unique())
            Agg_user_Y_Q = Agg_users_count_Y_Q(Agg_user_Y,quarters)
            states = st.selectbox("Select the State_Us",Agg_user_Y_Q["State"].unique())
            Agg_user_count_s(Agg_user_Y_Q,states)

        elif method2 =="Map Users":  
            years=st.slider("Select the Year_Us",Map_Users_df["Year"].min(),Map_Users_df["Year"].max(),Map_Users_df["Year"].min())
            Map_User_Y = Map_users_Y(Map_Users_df,years)
            quarters = st.selectbox("Select the Quarter_Us", Map_User_Y["Quarter"].unique())
            Map_User_Y_Q = Map_users_Q(Map_User_Y,quarters)
            states = st.selectbox("Select the State_Us",Map_User_Y_Q ["State"].unique())
            Map_user_s(Map_User_Y_Q,states)

        elif method2 =="Top Users":   
            years=st.slider("Select the Year_Us",Top_Users_df["Year"].min(),Top_Users_df["Year"].max(),Top_Users_df["Year"].min())
            Top_User_Y = Top_users_Y(Top_Users_df,years)
            states = st.selectbox("Select the State_Us",Top_User_Y["State"].unique())
            Top_users_state(Top_User_Y,states)

elif select == "INSIGHTS":
    questions= st.selectbox("Select all questions",("1.Top 10 Transaction Amount by State",
                                                "2.Least 10 Transaction Amount by State",
                                                "3.Top 10 Districts based on the Metric Amount",
                                                "4.Least 10 Districts based on the Metric Amount",
                                                "5.State based on Metric Count",
                                                "6.States based on Metric Amount",
                                                "7.Mobile Brand based on Count",
                                                "8.Least 10 AppOpens by Districts",
                                                "9.Top 10 RegisteredUsers by Districts",
                                                "10.RegisteredUsers by States"))
    
    if questions == "1.Top 10 Transaction Amount by State":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT State,SUM(Transaction_amount) AS Transaction_Amount \
        FROM Agg_Trans \
        GROUP BY State \
        ORDER BY Transaction_amount DESC \
        LIMIT 10''')
        df1=pd.DataFrame(mycursor.fetchall(),columns=["State","Transaction_Amount"])
        fig_bar_1=px.bar(df1,x="State",y="Transaction_Amount",title="Top 10 Transaction Amount by State",
                        width=600,color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig_bar_1)

    elif questions == "2.Least 10 Transaction Amount by State":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT State,SUM(Transaction_amount) AS Transaction_Amount \
        FROM Agg_Trans \
        GROUP BY State \
        ORDER BY Transaction_amount ASC \
        LIMIT 10''')
        df2=pd.DataFrame(mycursor.fetchall(),columns=["State","Transaction_Amount"])
        fig_bar_2 =px.bar(df2,x="State",y="Transaction_Amount",title="Least 10 Transaction Amount by State",
                        width=600,color_discrete_sequence=px.colors.sequential.Jet)
        st.plotly_chart(fig_bar_2)

    elif questions == "3.Top 10 Districts based on the Metric Amount":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT District,SUM(Metric_amount) AS Metric_Amount \
        FROM Map_Trans \
        GROUP BY District \
        ORDER BY Metric_Amount DESC \
        LIMIT 10''')
        df3=pd.DataFrame(mycursor.fetchall(),columns=["District","Metric_Amount"])
        fig_line_3 = px.line(df3, x="District", y="Metric_Amount",title ="Top 10 Districts by Metric Amount", width=1000, height=800,
                        markers=True, color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_line_3)    

    elif questions == "4.Least 10 Districts based on the Metric Amount":    
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT District,SUM(Metric_amount) AS Metric_Amount \
        FROM Map_Trans \
        GROUP BY District \
        ORDER BY Metric_Amount ASC \
        LIMIT 10''')
        df4=pd.DataFrame(mycursor.fetchall(),columns=["District","Metric_Amount"])
        fig_line_4 = px.line(df4, x="District", y="Metric_Amount",title ="Least 10 Districts by Metric Amount", width=1000, height=800,
                        markers=True, color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_line_4)

    elif questions == "5.State based on Metric Count":    
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT State,AVG(Metric_count) AS Metric_Count \
        FROM Top_Trans \
        GROUP BY State \
        ORDER BY Metric_Count DESC''')
        df5=pd.DataFrame(mycursor.fetchall(),columns=["State","Metric_Count"])
        fig_bar_5 = px.bar(df5, x="State", y="Metric_Count",title="State by Metric Count",
                        width=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_5)

    elif questions == "6.States based on Metric Amount":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT State,SUM(Metric_amount) AS Metric_Amount
        FROM Top_Trans \
        GROUP BY State \
        ORDER BY Metric_Amount DESC''')
        df6=pd.DataFrame(mycursor.fetchall(),columns=["State","Metric_Amount"])
        fig_bar_6 = px.bar(df6, x="State", y="Metric_Amount",title="State by Metric_Amount",
                        width=600,color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_bar_6)  

    elif questions == "7.Mobile Brand based on Count":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT State,Brand,SUM(Count) AS Count \
        FROM Agg_Users \
        GROUP BY State,Brand \
        ORDER BY Count DESC ''')
        df7=pd.DataFrame(mycursor.fetchall(),columns=["State","Brand","Count"])
        fig_sunburst_7 = px.sunburst(df7, path=["State","Brand"], values="Count")
        st.plotly_chart(fig_sunburst_7)

    elif questions == "8.Least 10 AppOpens by Districts":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT Districts,SUM(AppOpens) AS AppOpens \
        FROM Map_Users \
        GROUP BY Districts \
        ORDER BY AppOpens ASC \
        LIMIT 10''')
        df8=pd.DataFrame(mycursor.fetchall(),columns=["Districts","AppOpens"])
        fig_pie_8=px.pie(df8, names="Districts", values="AppOpens", title="Least 10 AppOpens by Districts",
                        width=600,hole=0.5)
        st.plotly_chart(fig_pie_8)    

    elif questions == "9.Top 10 RegisteredUsers by Districts": 
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT Districts,AVG(RegisteredUsers) AS RegisteredUsers \
        FROM Map_Users \
        GROUP BY Districts \
        ORDER BY RegisteredUsers DESC \
        LIMIT 10''')
        df9=pd.DataFrame(mycursor.fetchall(),columns=["Districts","RegisteredUsers"])
        fig_scatter_9=px.scatter(df9, x="Districts", y="RegisteredUsers", title="Top 10 RegisteredUsers by Districts",
                        width=600,color_discrete_sequence=px.colors.sequential.PuBuGn_r)
        st.plotly_chart(fig_scatter_9)

    elif questions == "10.RegisteredUsers by States":
        mycursor.execute('USE phonepae')
        mycursor.execute('''SELECT State,SUM(RegisteredUsers) AS RegisteredUsers \
        FROM Top_Users \
        GROUP BY State \
        ORDER BY RegisteredUsers DESC''')
        df10=pd.DataFrame(mycursor.fetchall(),columns=["State","RegisteredUsers"])
        fig_bar_10 = px.bar(df10, x="RegisteredUsers", y="State",title="RegisteredUsers by States",orientation="h",
                        width=1000,color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar_10)        