# -*- coding: utf-8 -*-
"""
Created on Fri May  1 15:06:27 2020

@author: Michael.Battye
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML

font = {'fontname':'Helvetica',
        'color':  'black',
        'weight': 'normal',
        'size': 24
        }

filepath1 = r"C:\Users\Michael.Battye\Desktop\Python Scripts\Spotify\MyData\StreamingHistory0.json"
filepath2 = r"C:\Users\Michael.Battye\Desktop\Python Scripts\Spotify\MyData\StreamingHistory1.json"

df1 = pd.read_json(filepath1)
df2 = pd.read_json(filepath2)

df = df1.append(df2)

df['endTime'] = pd.to_datetime(df['endTime'])
df['month'] = df.apply(lambda row: row.endTime.strftime("%B"), axis=1)
df['year'] = df.apply(lambda row: row.endTime.strftime("%Y"),axis=1)

#remove first unfilled month
n = df.index[df['month'] == 'May'].tolist()[0]
df = df.iloc[n:,:]
print(df.head())

colors = ["#fff75e","#fff056","#ffe94e","#ffe246","#ffda3d","#ffd53e","#fecf3e","#fdc43f","#fdbe39","#fdb833"]
#colors = ['#FFBA08','#d22730']

fig, ax = plt.subplots(figsize=(20,8))

months = df['month'].unique()
print(months)

# init function
def init():
    return fig, ax

def draw_barchart(current_month):
    dff = (df[df['month'].eq(current_month)])
    current_year = dff['year'].iloc[0]
    dff = dff.groupby('artistName').endTime.nunique().reset_index()
    dff.rename(columns={"endTime":"count"},inplace=True)
    dff.sort_values(by=['count'],ascending=False,inplace=True)
    dff = dff.iloc[:10,:]
    ax.clear()
    ax.barh(dff['artistName'],dff['count'],color=colors)
    ax.invert_yaxis()
    dx = dff['count'].max() / 200
    for i, (value, name) in enumerate(zip(dff['count'], dff['artistName'])):
        ax.text(value-dx, i,     name,           fontdict=font,size=12, weight=520, ha='right', va='center')
        ax.text(value+dx, i,     f'{value:,.0f}',  fontdict=font,size=14, ha='left',  va='center')
    ax.text(1, 0.4, current_month, transform=ax.transAxes, fontdict=font, size=46, ha='right', weight=800)
    ax.text(1, 0.28, current_year, transform=ax.transAxes, fontdict=font, size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Plays', transform=ax.transAxes, fontdict=font, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.box(False)

animator = animation.FuncAnimation(fig,draw_barchart,init_func=init,frames=months,interval=1500,repeat_delay=2000)
HTML(animator.to_jshtml())
# or use animator.to_html5_video() or animator.save()
animator.save(r"C:\Users\Michael.Battye\Desktop\Python Scripts\Spotify\spotify_animation.gif")

"""
months_keys = []
months_values = []

for year in range(19,21):
    for i in range(1,13):
        if i+1 == 13:
            A = df[(df['endTime'] >= '20'+str(year)+'-'+str(i).zfill(2)+'-01 00:00') & (df['endTime'] <'20'+str(year+1)+'-01-01 00:00')]
        else:
            A = df[(df['endTime'] >= '20'+str(year)+'-'+str(i).zfill(2)+'-01 00:00') & (df['endTime'] <'20'+str(year)+'-'+str(i+1).zfill(2)+'-01 00:00')]
        if A.empty == False:
            months_keys.append(str(i).zfill(2)+'-20'+str(year))
            months_values.append(A)

#months = dict(zip(months_keys,months_values))
#top_artists = []


#month = '08-2019'
#dff=(df[df[]])


#Define Barchart Function
fig, ax = plt.subplots(figsize=(15, 8)) 
def barchart(month,month_df):           
    ax.barh(month_df['artistName'],month_df['playCount'])
    ax.text(1, 0.4, month, transform=ax.transAxes, size=46, ha='right')


num_artists = 5
#print('Most played artists per month')
def animate(months,top_artists):
    for month, month_df in months.items():
        #print(month)
        month_df.rename({'endTime': 'playCount'}, axis=1, inplace=True)
        month_df = (month_df.groupby(['artistName']).count().reset_index().sort_values(by='playCount',ascending=False))[['artistName', 'playCount']].head(num_artists).reset_index()
        #print(month_df.head(num_artists))
        month_df = month_df[::-1]   # flip values from top to bottom
        top_artists.append(month_df)
        barchart(month,month_df)

top_artists_dict = dict(zip(months_keys,top_artists))


animator = animation.FuncAnimation(fig, animate, frames=range(len(top_artists_dict)))
HTML(animator.to_jshtml())
#animator.save('r"U:\Python Scripts\Spotify\animation.gif', fps=30, extra_args=['-vcodec', 'libx264'])


artists = ["The 1975", "Kanye West", "Bon Iver", "James Blake", "Enter Shikari"]

for month, month_df in months.items():
    print(month)
    for artist in artists:
        artist_per_month = month_df[(month_df['artistName'] == artist)]
        print(str(len(artist_per_month.index))+" plays of "+artist)
"""