import streamlit as st
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import emoji
from emoji import emojize
from collections import Counter

#Bar Plot Funcction
def barPlotFunction(x, y, color_name, x_label, y_label, font_size, font_weight, chart_title, chart_font_size):
    fig, axis = plt.subplots()
    # fig = plt.figure(figsize=(10, 5), dpi=300)
    axis.bar(x, y, color=color_name)
    plt.xticks(rotation='vertical');
    plt.xlabel(x_label, size=font_size, fontweight=font_weight)
    plt.ylabel(y_label, size=font_size, fontweight=font_weight)
    plt.title(chart_title, size=chart_font_size, fontweight="bold")
    st.pyplot(fig)
def barhPlotFunction(x, y, color_name, x_label, y_label, font_size, font_weight, chart_title, chart_font_size):
    fig, axis = plt.subplots()
    # fig = plt.figure(figsize=(10, 5), dpi=300)
    axis.barh(x, y, color=color_name)
    plt.xticks(rotation='vertical');
    plt.xlabel(x_label, size=font_size, fontweight=font_weight)
    plt.ylabel(y_label, size=font_size, fontweight=font_weight)
    plt.title(chart_title, size=chart_font_size, fontweight="bold")
    st.pyplot(fig)

def countNumberOfWords(df):
    total_words = 0
    for every_message in df['messages']:
        total_words = total_words + len(every_message.split())
    return total_words
def countNumberOfMedia(df):
    media_ommited_df = df[df['messages'] == '<Media omitted>\n']
    return media_ommited_df.shape[0]

def countURLs(df):
    from urlextract import URLExtract
    extractor = URLExtract()
    url_list = []
    for it in df['messages']:
        for url in extractor.gen_urls(it):
            url_list.append(url)
    return url_list,len(url_list)

def printList(demo_list):
    counter = 1
    for it in demo_list:
        st.write(str(counter) + ". " + it)
        counter=counter+1



def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    num_messages = df.shape[0]
    num_words = countNumberOfWords(df)
    url_list, num_url = countURLs(df)
    return num_messages, num_words, countNumberOfMedia(df), url_list, num_url



#-----------------------------------------------------------------#

def df_of_URLs(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    from urlextract import URLExtract
    extractor = URLExtract()
    url_list = []
    for it in df['messages']:
        for url in extractor.gen_urls(it):
            url_list.append(url)
    url_df = pd.DataFrame(url_list)
    url_df.rename(columns={0: "URL"}, inplace=True)
    st.dataframe(url_df)


def most_active_user(df):
    top_ten_active_users = df['users'].value_counts().head(10)
    st.header("Most Active User Bar Graph")
    fig = plt.figure(figsize = (10, 5),dpi=300)
    plt.bar(top_ten_active_users.index, top_ten_active_users.values,color='yellowgreen')
    plt.xticks(rotation='vertical')
    plt.xlabel("User Name/Mobile Number", size=16, fontweight="300")
    plt.ylabel("Number of Messages", size=16, fontweight="300")
    plt.title("User vs. Total Number of Messages", size=20, fontweight="bold")
    st.pyplot(fig)

def most_active_user_dataFrame(df):
    top_ten_active_users = df['users'].value_counts().head(10)
    temp_df = round(((top_ten_active_users / df.shape[0]) * 100),2).reset_index();
    user_and_persentages_of_message_df = temp_df.rename(columns={'index': 'Name', 'users': 'Percentage'})
    st.header("User and Percentage of Messages")
    st.dataframe(user_and_persentages_of_message_df)



#----------------------------------------
#Return Fresh Data
def fresh_data(df):
    df_without_Group_Notification = df[df['users'] != 'Group_Notification']
    df_without_others_data = df_without_Group_Notification[
        df_without_Group_Notification['messages'] != '<Media omitted>\n']
    df_without_others_data = df_without_others_data[df_without_others_data['messages'] != 'This message was deleted\n']
    df_without_others_data = df_without_others_data.reset_index()
    return df_without_others_data


# WordCloud

def create_wordCloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    wc = WordCloud(width=800, height=800, min_font_size=10, background_color='white')
    df_without_others_data = fresh_data(df)
    word = df_without_others_data['messages'].str.cat(sep=" ")
    words = wc.generate(word)
    fig, axis = plt.subplots()
    plt.figure(figsize=(8, 4), dpi=300)
    axis.imshow(words)
    st.pyplot(fig)



#Most Commonly used word DF
def most_commonly_used_word_df(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    #DF -: List of most commonly used words
    list_of_words = []
    df_without_others_data = fresh_data(df)
    for message in df_without_others_data['messages']:
        list_of_words.extend(message.split())
    most_used_word_df = pd.DataFrame(Counter(list_of_words).most_common(20))
    most_used_word_df.rename(columns={0: 'The Word', 1: "No. of times used"}, inplace=True)
    return most_used_word_df


# Emoji Function
def emoji_function(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojis = []
    for message in df['messages']:
        for letter in message:
            if letter in emoji.UNICODE_EMOJI['en']:
                emojis.append(letter)
    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emojis_df.rename(columns={0: "Emoji", 1: "Count"}, inplace=True)
    return emojis_df

def emoji_analysis_pie_chart(df,col1,col2):
    fig = plt.figure(figsize=(10, 5), dpi=300)
    plt.pie(df[col2], labels=df[col1],autopct="%0.2f")
    plt.xticks(rotation='vertical')
    plt.xlabel("Emoji", size=16, fontweight="300")
    plt.ylabel("Number of Emoji", size=16, fontweight="300")
    plt.title("User vs. Total Number of Emoji", size=20, fontweight="bold")
    st.pyplot(fig)


def perMonthMessages_Plot(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]


    per_month_message_df = df.groupby(['year', 'month', 'month_num']).count()['messages'].reset_index()
    yearMonth = []
    for i in range(per_month_message_df.shape[0]):
        yearMonth.append(per_month_message_df['month'][i] + '-' + str(per_month_message_df['year'][i]))
    per_month_message_df['year_month'] = yearMonth
    per_month_message_df.rename(columns={'messages': "num_messages"}, inplace=True)
    fig, axis = plt.subplots()
    axis.plot(per_month_message_df['year_month'], per_month_message_df['num_messages'], color='red')
    plt.xticks(rotation='vertical')
    plt.xlabel("Month-Year", size=16, fontweight="300")
    plt.ylabel("Number of messages", size=16, fontweight="300")
    plt.title("Month-Year Vs. Number of messages Plot", size=20, fontweight="bold")
    st.pyplot(fig)

def dailyMessagesBarPlot(df):
    fig, axis = plt.subplots()
    axis.bar(df['yyyy_mm_dd'], df['messages'], color='red')
    plt.xticks(rotation='vertical')
    plt.xlabel("Date", size=16, fontweight="300")
    plt.ylabel("Number of messages", size=16, fontweight="300")
    plt.title("Date Vs. Number of messages Plot", size=20, fontweight="bold")
    st.pyplot(fig)

def top_20_busy_day_scatter_plot(df):
    # Top 20 Busy Day Scattered Plot
    fig, axis = plt.subplots()
    axis.scatter(df['yyyy_mm_dd'], df['messages'], color='red')
    plt.xticks(rotation='vertical')
    plt.xlabel("Date", size=16, fontweight="300")
    plt.ylabel("Number of messages", size=16, fontweight="300")
    plt.title("Date Vs. Number of messages Plot", size=20, fontweight="bold")
    plt.grid()
    st.pyplot(fig)

def day_wise_messages_plot(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    df['yyyy_mm_dd'] = df['date'].dt.date
    messages_by_day_df = df.groupby('yyyy_mm_dd').count()['messages'].reset_index()
    temp_df = messages_by_day_df.sort_values('messages', ascending=False)
    top_20_busy_day = temp_df.reset_index()
    top_20_busy_day = temp_df.head(20)
    top_20_busy_day = top_20_busy_day.reset_index()
    top_20_busy_day.drop(['index'], axis=1, inplace=True)
    for i in range(top_20_busy_day.shape[0]):
        top_20_busy_day['yyyy_mm_dd'][i] = str(top_20_busy_day['yyyy_mm_dd'][i])


    # Daily Message Bar Plot Function
    st.title("Daily Messages Bar Plot")
    dailyMessagesBarPlot(messages_by_day_df)
    # top 20 busy day scttered plot
    st.title("Top 20 busy day - Scatter Plot")
    top_20_busy_day_scatter_plot(top_20_busy_day)



### Most Busy Week Days
def most_Busy_Week_Days(selected_user,df):
    st.title("Most Busy Week Days")
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    busy_day_in_week_df = df.groupby('day_name').count()['messages'].reset_index()


    weekDayDict = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7
    }
    busy_day_in_week_df = busy_day_in_week_df.reset_index()
    busy_day_in_week_df.rename(columns={'index': 'day_id'}, inplace=True)
    for i in range(7):
        busy_day_in_week_df['day_id'][i] = weekDayDict[busy_day_in_week_df['day_name'][i]]
    busy_day_in_week_df = busy_day_in_week_df.sort_values('day_id')
    busy_day_in_week_df = busy_day_in_week_df.drop(['day_id'], axis=1)
    # st.dataframe(busy_day_in_week_df)

    fig, axis = plt.subplots()
    axis.bar(busy_day_in_week_df['day_name'], busy_day_in_week_df['messages'], color='magenta')
    plt.xticks(rotation='vertical')
    plt.xlabel("Week Days", size=16, fontweight="300")
    plt.ylabel("Number of messages", size=16, fontweight="300")
    plt.title("Week Days Vs. Number of messages Plot", size=20, fontweight="bold")
    plt.grid()
    st.pyplot(fig)


### Most busy hours
def most_busy_hours(selected_user,df):
    st.title("Most Busy Hours")
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    most_busy_hour_df = df.groupby('hour').count()['messages'].reset_index()
    fig, axis = plt.subplots()
    axis.bar(most_busy_hour_df['hour'], most_busy_hour_df['messages'], color='lightseagreen')
    plt.xticks(rotation='vertical')
    plt.xlabel("Hours", size=16, fontweight="300")
    plt.ylabel("Number of messages", size=16, fontweight="300")
    plt.title("Hours Vs. Number of messages Plot", size=20, fontweight="bold")
    plt.grid()
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    plt.xticks(x)
    st.pyplot(fig)



def who_deleted_the_messages_most(selected_user,df):
    st.title("Who deleted the messages most ?")
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    deleted_message_df = df[df['messages'] == 'This message was deleted\n']
    deleted_message_df = deleted_message_df.groupby('users').count()['messages'].reset_index()
    deleted_message_df = deleted_message_df.sort_values('messages', ascending=False).reset_index()
    deleted_message_df = deleted_message_df.drop(['index'], axis=1)
    deleted_message_df = deleted_message_df.head(10)
    fig, axis = plt.subplots()
    axis.barh(deleted_message_df['users'], deleted_message_df['messages'], color='tomato')
    plt.xticks(rotation='vertical')
    plt.xlabel("No. of messages deleted", size=16, fontweight="300")
    plt.ylabel("Person", size=16, fontweight="300")
    plt.title("Person Vs. No. of messages deleted", size=20, fontweight="bold")
    plt.grid()
    st.pyplot(fig)





#### Heatmap
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap
