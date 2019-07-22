import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import json


def process_song_file(cur, filepath):
    """
Takes a single song file and inserts it into the DB.

Args:
    cur: Connection cursor.
    filepath: filepath to current song file.
    """
    
    with open(filepath) as f:
        data = json.load(f)
    
    # open song file
    df = pd.DataFrame([data]) 

    # insert song record
    song_data = [df['song_id'][0], 
                 df['title'][0], 
                 df['artist_id'][0], 
                 int(df['year'][0]), 
                 float(df['duration'][0])]
    
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    df['artist_longitude'] = df['artist_longitude'].astype(float)
    df['artist_latitude'] = df['artist_latitude'].astype(float)

    artist_data = [
        df['artist_id'][0],
        df['artist_name'][0],
        df['artist_location'][0],
        df['artist_longitude'][0],
        df['artist_latitude'][0]]
    
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
Takes a single log file and inserts it into the DB.

Args:
    cur: Connection cursor.
    filepath: filepath to current song file.
    """
    
    # open log file
    json_log_data = []
    for line in open(filepath):
        json_log_data.append(json.loads(line))

    df = pd.DataFrame(json_log_data)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong'] 

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
    
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels,time_data)))
    
    time_df = time_df.drop_duplicates(['timestamp','hour','day','week','month','year','weekday'])
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]
    user_df = user_df.drop_duplicates(['userId','firstName','lastName','gender','level'])

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row['ts'], row['userId'],row['level'], songid, artistid, row['sessionId'], row['location'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Used to process multiple song or log files in a specified directory.

Args:
    cur: Connection cursor.
    conn: Postgres DB connection object.
    filepath: filepath to the directory containing data.
    func: Function used to process data. Either "process_song_file" or "process_log_file"
    """
        
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()