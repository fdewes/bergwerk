import pandas as pd
from sqlalchemy import create_engine
import requests
import os


print("Running tracker cron!")

BOT_USERNAME = os.getenv('BOT_USERNAME')
BOT_PASSWORD = os.getenv('BOT_PASSWORD')
SQL_USER = os.getenv('SQL_USER')
SQL_PASS = os.getenv('SQL_PASS')

HOST = "http://bergwerk-wiki/w"

PREAMBLE = "[[Category:Tracker]]\n"

def sql2pd(host, database, user, password, table):
    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)
    df = pd.read_sql_table(table, con=engine)
    return df



def login(host: str):
    url = host + "/api.php"
    session = requests.Session()

    # Get login token
    response = session.get(url, params={
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json'
    })
    login_token = response.json()['query']['tokens']['logintoken']

    # Log in
    response = session.post(url, data={
        'action': 'login',
        'lgname': BOT_USERNAME,
        'lgpassword': BOT_PASSWORD,
        'lgtoken': login_token,
        'format': 'json'
    })

    if response.json()['login']['result'] != 'Success':
        raise Exception('Failed to log in')

    return session


def get_entire_page(host: str, page: str):
    url = host + "/api.php"

    page_params = {
        'action': 'parse',
        'format': 'json',
        'prop': 'wikitext',
        'page': page
    }
    response = session.get(url, params=page_params)
    response.raise_for_status()

    data = response.json()
    try:
        page_text = data['parse']['wikitext']['*']
    except KeyError:
        page_text = None

    return page_text

def get_csrf_token(host, session):

    URL = host + "/api.php"
    response = session.get(URL, params={
        'action': 'query',
        'meta': 'tokens',
        'format': 'json'
    })
    return response.json()['query']['tokens']['csrftoken']

def create_or_update_page(host, title, content):
    session = login(host)
    csrf_token = get_csrf_token(host, session)
    URL = host + "/api.php"
    response = session.post(URL, data={
        'action': 'edit',
        'title': title,
        'text': content,
        'token': csrf_token,
        'format': 'json'
    })
    if 'error' in response.json():
        raise Exception(response.json()['error'])
    return response.json()

def gen_overview_page(df):
        
    page_content = """[[Category:Tracker]]\n= Conversation Tracker ="""

    overview = f"\n\nThere are {len(df.id.unique())} conversations stored in the conversation tracker.\n"
    page_content += overview

    dft = df.groupby(by="id").ts.min().reset_index()
    dft['datetime'] = pd.to_datetime(dft['ts'], unit = "s")
    dft['year'] = dft.datetime.dt.year
    dft['month'] = dft.datetime.dt.month
    dft['month_name'] = dft.datetime.dt.month_name()
    dft['day'] = dft.datetime.dt.day
    dft['ymd'] = dft['datetime'].dt.strftime('%Y%m%d')
    dft['ymdhm'] = dft['datetime'].dt.strftime('%Y%m%d%H%M')
    dft['human_date'] = dft['datetime'].dt.strftime('%d. %B %Y')
    dft = dft.sort_values("ts", ascending=False)

    all_conversations = ""
    months_with_data = dft.human_date.unique().astype(list)

    for m in months_with_data:
        all_conversations += f"= {m} =\n"
        dfm = dft[(dft["human_date"] == m)]
        ids_of_day = dfm.id.unique().astype(list)
        for id in ids_of_day:
                ymd = dfm[dfm.id == id].ymd.values[0]
                all_conversations += f"* [[{ymd}:{id}|{id}]]\n"

    page_content += all_conversations

    return dft, page_content


session = login(HOST)

df = sql2pd("bergwerk-db", "tracker_db", SQL_USER, SQL_PASS, "tracker")
dft, ovp = gen_overview_page(df)
create_or_update_page(HOST, "Tracker", ovp)

for id in dft.id.values.astype(list):
    wt = PREAMBLE
    df_c = df[(df.id == id)].copy()
    df_c['datetime'] = pd.to_datetime(df_c['ts'], unit = "s")
    df_c['time'] = df_c['datetime'].dt.strftime('%H:%M')


    conv_date_m  = dft[dft.id == id].ymd.values[0]
    conv_date_h  = dft[dft.id == id].human_date.values[0]

    title = conv_date_m + ":" + id
    wt += f"= {conv_date_h} =\n"

    for i in df_c.index:
        line = ( 
            "<strong>" + df_c.loc[i, "role"] + "</strong>"
            " <small>(" +  df_c.loc[i, "time"] + "):</small> " +  
            "<markdown>" + df_c.loc[i, "text"] + "</markdown>" +
            df_c.loc[i, "buttons"] + "\n\n\n" )
        
        wt += line

    create_or_update_page(HOST, title, wt)
