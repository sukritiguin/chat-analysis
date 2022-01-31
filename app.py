import streamlit as st
import preprocessor
import helper
import emoji
from emoji import emojize
# from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.header("Note : Use 24 Hours Format and mm/dd/yy date format")
uploaded_file = st.sidebar.file_uploader("Choose your whatsapp chat file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocessor.preprocess(data)
    # st.text(df)
    # st.dataframe(df)

    #Find all unique users
    users_list = df['users'].unique().tolist()
    if 'Group_Notification' in users_list:
        users_list.remove('Group_Notification')
    users_list.sort()
    users_list.insert(0,"Overall")
    #create selectbox to select perticular user or all users
    selected_user = st.sidebar.selectbox("Select User",users_list)
    #show analysis button
    if st.sidebar.button("Show Analysis"):
        if(selected_user=='Overall'):
            st.title("Overall Analysis")
        else:
            st.title(selected_user + "'s Analysis")
        st.title("________________________________")
        num_messages,num_words,num_media,url_list,num_urls = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Total URL Shared")
            st.title(num_urls)
        # Per Monnth Messages
        st.title("Number of Messages per month")
        helper.perMonthMessages_Plot(selected_user, df)



        # st.header("List of URLs shared")
        # helper.df_of_URLs(selected_user,df)


        #----------------------------------#
        #Top 10 Active User
        if selected_user == 'Overall':
            st.title("Most Active User")
            helper.most_active_user(df)
            # helper.most_active_user_dataFrame(df)

        #Word Cloud
        if selected_user != 'Overall':
            st.title("Word Cloud of " + selected_user)
        else:
            st.title("Word Cloud")
        helper.create_wordCloud(selected_user, df)
        #####
        col1, col2 = st.columns(2)
        with col1:
            helper.most_active_user_dataFrame(df)
        with col2:
            if selected_user != 'Overall':
                st.header("Most Used Word Data Frame of " + selected_user)
            else:
                st.header("Most Used Word Data Frame")
            most_used_word_df = helper.most_commonly_used_word_df(selected_user, df)
            st.dataframe(most_used_word_df)
        st.title("Most Used Words Bar Plot")
        helper.barhPlotFunction(most_used_word_df['The Word'], most_used_word_df['No. of times used'], "red", "The Word", "No. of times used", 16, 400, "The Word Vs. No. of times used", 25)

        ### Emoji Analysis
        col1,col2 = st.columns(2)
        with col1:
            st.title("Used Emoji Data Frame")
            emoji_df = helper.emoji_function(selected_user,df)
            st.dataframe(emoji_df)
        with col2:
            st.title("Top 20 Emoji Pie Chart")
            top_20_emojis_df = emoji_df.head(20)
            helper.emoji_analysis_pie_chart(top_20_emojis_df,'Emoji','Count')

        helper.day_wise_messages_plot(selected_user, df)
        helper.most_Busy_Week_Days(selected_user, df)
        helper.most_busy_hours(selected_user, df)
        helper.who_deleted_the_messages_most(selected_user, df)

        ### Heat Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, axis = plt.subplots()
        axis = sns.heatmap(user_heatmap)
        st.pyplot(fig)

