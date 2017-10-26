''' Holds the code for the recommendation engine. The engine is a 
user based collaborative filterting system '''
import numpy as np
import pandas as pd


def read_training_data(filepath):
    '''Reads filepath into Pandas DataFrame'''
    raw_data = pd.DataFrame()
    try:
        raw_data = pd.read_csv(
            filepath, 
            names=['attribute', 'ID', 'ignore', 'title', 'url'], 
            engine="python", 
            skiprows=7
        )
    except Exception as E:
        print(E)

    return raw_data


def create_attributes(dataframe):
    ''' takes raw_data and returns a dataframe with
    just the attributes
    [['ID', 'title', 'url'], [1001, 'help', '/help'] ... [2000, 'office', '/msoffice']]
    
    '''
    attributes = dataframe[dataframe['attribute'] == 'A']
    attributes = attributes[['ID', 'title', 'url']]

    return attributes


def create_top_visited_websites(dataframe, threashold):
    ''' takes raw_data and returns a df of the top
    websites sorted descending. Only websites with
    more than [threashold] visits are returned
    '''
    website_visits = get_websites_with_total_visits(dataframe)
    top_websites = website_visits[website_visits['count'] > threashold]
    return top_websites['url']


def get_websites_with_total_visits(data):
    ''' Takes the data DF and returns a df with 
    ['ID', 'title', 'url', 'count'] where count is the total visits to the site.
    '''
    websites = data[data['attribute'] == 'V']
    websites = websites[['ID', 'attribute']]
    website_visits = websites.groupby(by='ID').count()
    website_visits.columns=['count']

    attributes = create_attributes(data)

    website_visits = pd.merge(
        website_visits, 
        attributes, 
        left_index=True, 
        right_on="ID"
        )
    return website_visits.sort_values(by='count', ascending=False)


def get_webvisits(data):
    ''' returns DF showing one line pr website visit with
    headings ['user', 'ID'] '''
    raw_webvisits = data[data['attribute'] != 'A']
    webvisits = []
    row = []
    user = ''
    
    for line in raw_webvisits.values:
        if line[0] == 'C':
            user = line[1]
        elif line[0] == 'V':
            row = [user, line[1]]
            webvisits.append(row)
        else:
            print("ERROR")
            
    webvisits = pd.DataFrame(webvisits, columns=['user', 'ID'])

    return webvisits


def create_website_recommendation(user_id, raw_data):
    ''' takes raw data and user ID and returns 5 website recommendations
    as a list '''
    # To ensure that new users are still presented with recommendations
    users = raw_data[raw_data['attribute'] == 'C']
    userlist = list(users['ID'])

    if user_id not in userlist:
        return list(create_top_visited_websites(raw_data, 100)[0:5])

    data = raw_data[['attribute', 'ID', 'title', 'url']]
    attributes = create_attributes(data)

    top_websites = get_websites_with_total_visits(data)
    top_websites = top_websites[top_websites['count'] > 100]
            
    # Used to create user / visit matrix for user based coll. filtering
    webvisits = get_webvisits(data)
    attributes = create_attributes(data)
    webvisits_augmented = pd.merge(webvisits, attributes, on="ID")
    webvisits_augmented['count'] = 1

    uservisits = webvisits_augmented.pivot(index='url', columns='user', values='count')
    uservisits = uservisits.fillna(value=0)

    # User based coll. filtering
    # Finds similar users as the user_id
    user = uservisits[user_id]
    similarUsers = uservisits.corrwith(user, axis='index')
    similarUsers = similarUsers.dropna()
    similarUsers = similarUsers.sort_values(ascending=False)
    similarUsers.drop(user_id, inplace=True)

    # Take the most similar user (s_user_id)
    # and takes his visited websites. Then rank them according to popularity
    df = pd.DataFrame(similarUsers)
    s_user_id = df.iloc[0].name
    s_user = uservisits[s_user_id]
    s_user = pd.DataFrame(s_user)
    s_user.columns=['visited']
    s_user = s_user[s_user['visited'] == 1]
    recommended_websites = pd.merge(s_user, top_websites, left_index=True, right_on="url")
    recommended_websites = recommended_websites.sort_values(by='count', ascending=False)

    website_urls = recommended_websites['url']
    visited_sites = pd.DataFrame(user[user == 1])
    print('recommend:', list(website_urls))
    print('visited:', list(visited_sites.index.values))

    return list(website_urls)