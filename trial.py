import googleapiclient.discovery
import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector
import re
import iso8601


api_service_name = "youtube"
api_version = "v3"

#it will be keep it as a public variable
api_key="AIzaSyAUpi9XT15zWAd0hU-atPeK9wEyk-AWBaw"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


#channel details
def channel_data(channel_id):
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
            )
        response = request.execute()
        ch_data={"channel_id":channel_id,
            "channel_name":response['items'][0]['snippet'].get('title',''),
            "channel_description":response['items'][0]['snippet']['description'],
            "channel_Playlists_id":response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
            "channel_viewCount":response['items'][0]['statistics']['viewCount'],
            "channel_subscriberCount":response['items'][0]['statistics']['subscriberCount'],
            "channel_videoCount":response['items'][0]['statistics']['videoCount']
            }
        return ch_data 

#Playlist details
def video_details(channel_id):
    video_ids=[]
    request= youtube.channels().list(
        part="contentDetails",
        id=channel_id
        )
    response=request.execute()
    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token=None

    while True:
        request1= youtube.playlistItems().list(
            part='snippet',
            maxResults=50,
            playlistId=playlist_id,
            pageToken=next_page_token 
            )
        response1= request1.execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
            next_page_token=response1.get('nextPageToken')
        if  next_page_token is None:
            break
    return video_ids

#duration convertion part
def iso8601_to_seconds(new_duration):
    pattern = re.compile( r'^P(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$')
    match = pattern.match(new_duration)
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = float(match.group(3)) if match.group(3) else 0
        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        return total_seconds
    else:
        return None

#video details
def video_info(video_Ids):     
    video_data=[]
    for vc_id in video_Ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=vc_id,
            )
        response = request.execute()
        new_duration =iso8601_to_seconds(response['items'][0]['contentDetails'].get('duration',0))
        vi_data={"channel_id":channel_id,
            "video_id":response['items'][0]['id'],
            "video_name":response['items'][0]['snippet']['title'],         
            "video_description":response['items'][0]['snippet']['description'],
            "publishedAt":response['items'][0]['snippet']['publishedAt'],
            "view_count":response['items'][0]['statistics'].get('viewCount',0),
            "like_count":response['items'][0]['statistics'].get('likeCount',0),
            "dislike_count":response['items'][0]['statistics'].get('dislikeCount',0),
            "favourite_count":response['items'][0]['statistics'].get('favouriteCount',0),
            "duration":new_duration,
            "comment_count":response['items'][0]['statistics'].get('commentCount',0),
            "caption_status":response['items'][0]['contentDetails'].get('caption',0)
            }
        video_data.append(vi_data)
    return video_data

#comment details
def comment_info(video_Ids):
    comment_data=[]
    try:
        for video_id in video_Ids:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                )
            response = request.execute()
            cmt_data={"channel_id":channel_id,
            "video_id":response['items'][0]['id'],
            "comment_id":response['items'][0]['snippet']['topLevelComment']['id'],
            "comment_text":response['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay'],
            "comment_author":response['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            "comment_published_date":response['items'][0]['snippet']['topLevelComment']['snippet']['publishedAt']
            }
            comment_data.append(cmt_data)
    except:
        pass    
    return comment_data

def youtuberesult(channel_id):
    channel_details=channel_data(channel_id)
    video_Ids=video_details(channel_id)
    vid_details=video_info(video_Ids)
    cmt_deatils=comment_info(video_Ids)
    result={"channel":channel_details,
            "playlist":video_Ids,
            "video":vid_details,
            "comment":cmt_deatils
            }
    return result
st.set_page_config(layout="wide")

st.title(":blue[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
channel_id=st.text_input('Enter Channel id')

info=st.button("Get Info") 
if channel_id: 
    final_result = youtuberesult(channel_id)
    st.success("Your info ready")
    ch_df = pd.DataFrame([final_result["channel"]])
    vc_df = pd.DataFrame(final_result["video"])
    cmt_df = pd.DataFrame(final_result["comment"])
    migrate_data=st.button("Migrate to MYSQL")    
    if migrate_data:
#MYSQL connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=""
            )
        mycursor = mydb.cursor(buffered=True)

#Create a SQLAlchemy engine to connect to the MySQL database
        engine = create_engine("mysql+mysqlconnector://root:@localhost/youtube_final")
#channel dataframe push to SQLAlchemy it will create and insert table
        ch_df.to_sql('channel', con=engine, if_exists='append', index=False)
#video ataframe push to SQLAlchemy it will create and insert table
        vc_df.to_sql('video', con=engine, if_exists='append', index=False)
#comment dataframe push to SQLAlchemy it will create and insert table
        cmt_df.to_sql('comment', con=engine, if_exists='append', index=False)

        mydb.commit()
        st.success("Data migration successful!")
    data_migrate=st.radio("Select for Table Views",("channel","video","comment"))
    if data_migrate =="channel":
        st.write(ch_df)
    elif data_migrate =="video":
        st.write(vc_df)   
    elif data_migrate =="comment":
        st.write(cmt_df)


#MYSQL connector
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
        )
    mycursor = mydb.cursor(buffered=True)

    question= st.selectbox("Select all questions",("1.What are the names of all the videos and their corresponding channels?",
                                                "2.Which channels have the most number of videos, and how many videos do they have?",
                                                "3.What are the top 10 most viewed videos and their respective channels?",
                                                "4.How many comments were made on each video and what are their corresponding video names?",
                                                "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                                                "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                                "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                                                "8.What are the names of all the channels that have published videos in the year 2022?",
                                                "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                                "10.Which videos have the highest number of comments, and what are their corresponding channel names?"))

    if question == "1.What are the names of all the videos and their corresponding channels?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name,video.video_name \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id")
        df1=pd.DataFrame(mycursor.fetchall(),columns=["video_name", "channel_name"])
        st.write(df1)

    elif question == "2.Which channels have the most number of videos, and how many videos do they have?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name,channel_videoCount \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id \
        GROUP BY channel.channel_name \
        ORDER BY channel_videoCount DESC")
        df2=pd.DataFrame(mycursor.fetchall(),columns=["channel_name ", "channel_videoCount"])
        st.write(df2)

    elif question == "3.What are the top 10 most viewed videos and their respective channels?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name,video.video_name,video.view_count \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id \
        GROUP BY video.view_count \
        ORDER BY video.view_count DESC \
        limit 10")
        df3=pd.DataFrame(mycursor.fetchall(),columns=["channel_name ","video_name","view_count"])
        st.write(df3)

    elif question == "4.How many comments were made on each video and what are their corresponding video names?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT video.video_name, SUM(video.comment_count) AS total_comments \
        FROM video \
        GROUP BY video_name \
        ORDER BY total_comments DESC")
        df4=pd.DataFrame(mycursor.fetchall(),columns=["video_name","total_comments"])
        st.write(df4)

    elif question == "5.Which videos have the highest number of likes, and what are their corresponding channel names?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name,video.video_name,video.like_count \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id \
        ORDER BY video.like_count DESC")
        df5=pd.DataFrame(mycursor.fetchall(),columns=["channel_name","video_name"," like_count"])
        st.write(df5)

    elif question == "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT video.video_name,SUM(video.like_count) AS total_likes,SUM(video.dislike_count) AS total_dislikes \
        FROM video \
        GROUP BY video.video_name \
        ORDER BY total_likes DESC, total_dislikes DESC")
        df6=pd.DataFrame(mycursor.fetchall(),columns=["video_name","total_likes","total_dislikes"])
        st.write(df6)

    elif question == "7.What is the total number of views for each channel, and what are their corresponding channel names?":
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name,channel.channel_viewCount \
        FROM channel \
        ORDER BY channel_viewCount DESC")
        df7=pd.DataFrame(mycursor.fetchall(),columns=["channel_name","channel_viewCount"])
        st.write(df7)

    elif question == "8.What are the names of all the channels that have published videos in the year 2022?":   
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT DISTINCT channel.channel_name,video.video_name,video.publishedAt \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id \
        WHERE YEAR(video.publishedAt) = 2022 \
        GROUP BY channel.channel_name")
        df8=pd.DataFrame(mycursor.fetchall(),columns=["channel_name","video_name","publishedAt"])
        st.write(df8)

    elif question == "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?": 
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name, AVG(video.duration) AS average_duration \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id \
        GROUP BY channel.channel_name")
        df9=pd.DataFrame(mycursor.fetchall(),columns=["channel_name","average_duration"])
        st.write(df9)

    elif question == "10.Which videos have the highest number of comments, and what are their corresponding channel names?":   
        mycursor.execute('USE youtube_final')
        mycursor.execute("SELECT channel.channel_name,video.video_name,video.comment_count \
        FROM channel \
        JOIN video ON channel.channel_id = video.channel_id \
        ORDER BY video.comment_count DESC")
        df10=pd.DataFrame(mycursor.fetchall(),columns=["channel_name","video_name","comment_count"])
        st.write(df10)