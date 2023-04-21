import sys
import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as subp

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from tree import Node, BinarySearchTree
from spotipy.cache_handler import CacheFileHandler


# global variables
queens_names = [["taylor swift", "taylor", "ts", "t"],
               ["selena gomez", "selena", "sg", "s"],
               ["olivia rodrigo", "olivia", "or", "o"]]

search_types = [["a song", "song", "s"],
                ["an album", "album", "a"],
                ["her entire discography", "entire discography", "discography", "all"]]

features_list = ['danceability', 'energy', 'valence']


def set_up_api():
    """sets up using the Spotify API as well as caching

    Returns:
        sp, which allows the program to search through the api
    """
    client_id = "5ed3386dbfdb4cc082e0f281f615cfbe"
    client_secret = "02540fa6e3a743bb815f204aa4329551"

    cache_handler = CacheFileHandler(cache_path='.spotifycache')

    
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri = 'http://localhost/',
                                                cache_handler=cache_handler))
    return sp

def is_exit(input):
    """determines whether the user entered 'exit' or not

    Args:
        input (string): a value that the user entered

    Returns:
        True if the user entered 'exit', false if not
    """
    if input == 'exit':
        print("Thanks for playing! Bye!")
        return True
    else:
        return False

def get_track_features(artist, search_type, df, sp):
    """retrieves the features of what the user requested and returns them in a binary search tree

    Args:
        artist (string): artist's name
        search_type (string): search type (song, album, discography)
        df (pd.DataFrame): the dataframe that corresponds with the artist selected
        sp (spotify object): allows usage of the API

    Returns:
        _type_: _description_
    """
    track_features_tree = BinarySearchTree()
 
    if search_type == 'entire discography':
        df = df.drop_duplicates(subset=['track_name'])
        tracks = df["track_name"].values.tolist()
        feature = get_feature()
        for track in tracks:
            results = sp.search(q="track:" + track + " " + "artist:" + artist, limit = 1)
            if results["tracks"]["items"]:
                track_id = results["tracks"]["items"][0]["id"]
                features = sp.audio_features(track_id)
                specific_feature = features[0][feature]
                track_features_tree.put(feature, specific_feature, results['tracks']['items'][0]['album']['name'], track)
                        
    elif search_type == 'album':
        while True:
            album_name = input("What album by " + artist + " would you like to know more about? Enter 'exit' at anytime to quit. ").lower()
            if is_exit(album_name):
                sys.exit()
            album = sp.search(q="album:" + album_name + " " + "artist:" + artist, limit = 1)
            if album['tracks']['items']:
                album_name = album['tracks']['items'][0]['album']['name']
                album_tracks = df.loc[df['album_name'] == album_name]
                tracks = album_tracks['track_name'].values.tolist()
                feature = get_feature()
                for track in tracks:
                    results = sp.search(q="track:" + track + " " + "artist:" + artist, limit = 1)
                    if results["tracks"]["items"]:
                        track_id = results["tracks"]["items"][0]["id"]
                        features = sp.audio_features(track_id)
                        specific_feature = features[0][feature]
                        track_features_tree.put(feature, specific_feature, album_name, track)
                break
            else:
                print("This album doesn't exist by this artist. please try again")
    

    elif search_type == 'song':
        while True:
            song_name = input("What song by " + artist + " would you like to know more about? Enter 'exit' at anytime to quit. ")
            if is_exit(song_name):
                sys.exit()
            results = sp.search(q="track:" + song_name + " " + "artist:" + artist, limit = 1)
            if results["tracks"]["items"]:
                feature = get_feature()
                track_id = results["tracks"]["items"][0]["id"]
                features = sp.audio_features(track_id)
                specific_feature = features[0][feature]
                song_name = results['tracks']['items'][0]['name']
                track_features_tree.put(feature, specific_feature, results['tracks']['items'][0]['album']['name'], song_name)
                break
            else:
                print("This song doesn't exist by this artist. please try again")
    return track_features_tree

def get_artist():
    """retrieves the artist that the user wants to see and validates input

    Returns:
        string of the user's name
    """
    while True:
        artist = input("Would you like to learn about Taylor Swift, Olivia Rodrigo, or Selena Gomez's discography? Enter 'exit' at anytime to quit. ").lower()
        if is_exit(artist):
                sys.exit()
        if artist in queens_names[0]:
            return "Taylor Swift"
        elif artist in queens_names[1]:
            return "Selena Gomez"
        elif artist in queens_names[2]:
            return "Olivia Rodrigo"
        else:
            print("Please enter one of the three names: 'Taylor Swift', 'Selena Gomez', or 'Olivia Rodrigo'. If you're feeling lazy, shorthands like 'Taylor', 'TS', or 'T' are okay as well")
    return

def get_search_type():
    """retrieves the search type that the user wants to see, validates input

    Returns:
        string of the search type selected
    """
    while True:
        search_type = input("Do you want to know about a song, an album, or her entire discography? Enter 'exit' at anytime to quit. ").lower()
        if is_exit(search_type):
                sys.exit()
        if search_type in search_types[0]:
            return search_types[0][1]
        elif search_type in search_types[1]:
            return search_types[1][1]
        elif search_type in search_types[2]:
            return search_types[2][1]
        else:
            print("Please indicate one of the three options: 'song', 'album', or 'entire discography'. If you're feeling lazy, shorthands like 's', 'a', or 'all' are okay as well")
    return
        
def get_feature():
    """retrieves the feature that the user wants to see, validates input

    Returns:
        string of the feature selected
    """
    while True:
        feature = input("Would you like to know about the danceability, energy, or valence? Enter 'exit' at anytime to quit. ").lower()
        if is_exit(feature):
                sys.exit()
        if feature in features_list:
            return feature
        else:
            print("Please indicate one of the following: 'danceability', 'energy', 'valence")

def show_graph(graph_type, df, search_type, feature, artist):
    """displays the graph that the user selected

    Args:
        graph_type (string): specifies if user wants histogram or boxplot
        df (pd.DataFrame): the new dataframe that the inorder traversal created
        search_type (string): search type specified by user
        feature (string): feature specified by user
        artist (string): artist specified by user
    """
    if graph_type == 'histogram' or graph_type == 'h':
        q3, q1 = np.percentile(df['feature_value'], [75 ,25])
        optimal_bin_size = 2 * (q3-q1) * (len(df)**(-1/3))
        nbins = math.ceil((df['feature_value'].max() - df['feature_value'].min()) / optimal_bin_size) + 1
        mean_value = np.mean(df['feature_value'])
        
        if search_type == search_types[2][1]:
            histogram = px.histogram(df, x = 'feature_value',
                                    nbins = nbins,
                                    title = "Histogram of the " + feature + " of " + artist + "'s entire discography",
                                    labels = {'feature_value': feature})
        if search_type == search_types[1][1]:
            histogram = px.histogram(df, x = 'feature_value',
                                    nbins = nbins,
                                    title = "Histogram of the " + feature + " of " + artist +"'s album " + df['album_name'][0],
                                    labels = {'feature_value': feature})
        histogram.add_vline(x = mean_value, line_color = 'limegreen')
        histogram.add_annotation(x=mean_value, y = np.max(histogram.data[0].y), text= round(mean_value,2), showarrow=False, font=dict(color="black"))
        histogram.show()      
    elif graph_type == 'boxplot' or graph_type == 'b':
        if search_type == search_types[2][1]:
            if artist.lower() == queens_names[0][0]:
                albums_list = ['Taylor Swift', "Fearless (Taylor's Version)", 'Speak Now', "Red (Taylor's Version)", 
                               "1989", "reputation", "Lover", "folklore", "evermore (deluxe edition)", 'Midnights (3am Edition)']
            else:
                songs_by_album = df.groupby('album_name').agg('count')
                more_than_5 = songs_by_album.loc[songs_by_album['track_name'] >= 5]
                albums_list = more_than_5.index.tolist()
            new_df = df.loc[df['album_name'].isin(albums_list)]
            boxplot1 = go.Box(y = df['feature_value'], name = feature + ' overall')
            boxplot2 = go.Box(x = new_df['album_name'], y = new_df['feature_value'], name = feature + ' by album')
            fig = subp.make_subplots(rows=1, cols=2, column_widths = [1, 3])
            fig.append_trace(boxplot1, row=1, col=1)
            fig.append_trace(boxplot2, row=1, col=2)
            fig.update_layout(title = 'Boxplots of the ' + feature + " of " + artist + "'s entire discography overall and by album",
                              height = 700, width = 1300)
            fig.show()
        elif search_type == search_types[1][1]:
            boxplot = px.box(df, x = 'album_name', y = 'feature_value', points = 'all', title = "Boxplot of the " + feature + " of " + artist +"'s album " + df['album_name'][0],
                                    labels = {'feature_value': feature})
            boxplot.show()


def get_graph_type(search_type, artist_name, feature, album_name=None):
    """retrieves the type of graph that the user wants to see, validates input

    Args:
        search_type (string): the search type the user wanted to see
        artist_name (string): the artist name that the user wanted to see
        feature (string): feature that the user wanted to see
        album_name (string, optional): name of album that the user wanted to see, if it exists. Defaults to None.

    Returns:
        _type_: _description_
    """
    while True:
        if search_type == search_types[1][1]:
            graph_type = input("Would you like to see a histogram (h) or boxplot (b) of the " + feature + " of " + album_name + "? Enter 'exit' at anytime to quit. ")
        elif search_type == search_types[2][1]:
            graph_type = input("Would you like to see a histogram (h) or boxplot (b) of the " + feature + " of " + artist_name + "'s entire discography? Enter 'exit' at anytime to quit. ")
        if is_exit(graph_type):
                sys.exit()
        if graph_type.lower() == 'histogram' or graph_type.lower() == 'h' or graph_type.lower() == 'boxplot' or graph_type.lower() == 'b':
            return graph_type
        elif graph_type.lower() == 'no' or graph_type.lower() == 'n' or graph_type == 'nope' or graph_type == 'nah':
            break
        else:
            print("Please indicate one of the following: 'histgram', 'h', 'boxplot', or 'b', or no if you would not like to see a graph")

def prepare_df(Node, df):
    """takes the binary search tree created from get_track_features and uses inorder traversal to create a dataframe with the 
    values from least to highest

    Args:
        Node (Node): root node of the binary search tree
        df (pd.DataFrame): the empty dataframe that is waiting to be populated

    Returns:
        data frame with the values from the binary search tree in order
    """
    if Node:
        prepare_df(Node.leftChild, df)
        #print(Node.feature_name, Node.feature_value, Node.album_name, Node.track)
        df.loc[len(df)] = [Node.feature_name, Node.feature_value, Node.album_name, Node.track]
        prepare_df(Node.rightChild, df)
    return df
    
def print_feature_description(track_name, feature_name, feature_value):
    """prints some information about the input based on its values of the feature

    Args:
        track_name (string): could be track name, or album name, or artist's name
        feature_name (string): feature that the user wants to know
        feature_value (string): value of the feature
    """
    if feature_name == features_list[0]:
        if feature_value > 0.75:
            print("You could have a whole dance party to " + track_name + "!")
        elif feature_value > 0.5:
            print(track_name + " is pretty danceable! Go have some fun")
        elif feature_value > 0.25:
            print("You can move a little bit to " + track_name)
        else:
            print("You should probably just stay sitting when listening to " + track_name)
    elif feature_name == features_list[1]:
        if feature_value > 0.75:
            print(track_name + " will make you feel like you drank a few Celsius's!")
        elif feature_value > 0.5:
            print(track_name + " will give you the energy to get through your day")
        elif feature_value > 0.25:
            print("The energy of " + track_name + " is alright")
        else:
            print("You probably don't want to listen to " + track_name + " if you're searching for some energy. Just go to sleep")
    elif feature_name == features_list[2]:
        if feature_value > 0.75:
            print(track_name + " is a happy cheerful time! let's be happy! :D")
        elif feature_value > 0.5:
            print("If you need some cheering up, " + track_name + " is a good one to listen to")
        elif feature_value > 0.25:
            print(track_name + " is somewhat postiive-sounding :o")
        else:
            print("If you feel like crying, you should listen to " + track_name)
    
def main():
    """the main function that will run the program
    """
    olivia_rodrigo = pd.read_csv("olivia.csv")
    selena_gomez = pd.read_csv("selena.csv")
    taylor_swift = pd.read_csv("taylor.csv")  
    
    print("Welcome to my project, learning the moods of Taylor Swift, Selena Gomez, and Olivia Rodrigo’s discography!")
    
    sp = set_up_api()
    
    while True:
        artist = get_artist()
        search_type = get_search_type()
        tree = BinarySearchTree()
        
        if artist.lower() == queens_names[0][0]:
            tree = get_track_features(artist, search_type, taylor_swift, sp)
        elif artist.lower() == queens_names[1][0]:
            tree = get_track_features(artist, search_type, selena_gomez, sp)
        elif artist.lower() == queens_names[2][0]:
            tree = get_track_features(artist, search_type, olivia_rodrigo, sp)
        
        new_df = pd.DataFrame(columns = ['feature_name', 'feature_value', 'album_name', 'track_name'])
        new_df = prepare_df(tree.root, new_df)  
        feature = new_df["feature_name"][0]
        average_feature = new_df['feature_value'].mean()
        
        if search_type == search_types[1][1]:
            album_name = new_df['album_name'][0]
            print(new_df)
            print("The average " + feature + " of " + artist + "'s album " + album_name + " is " + str(round(average_feature, 3)))
            print_feature_description(album_name, feature, average_feature)
            graph_type = get_graph_type(search_type, artist, feature, album_name)
            show_graph(graph_type, new_df, search_type, feature, artist)
                
        elif search_type == search_types[2][1]:
            print("The average " + feature + " of " + artist + "'s entire discography is " + str(round(average_feature, 3)))
            print_feature_description(artist, feature, average_feature)
            graph_type = get_graph_type(search_type, artist, feature, artist)
            show_graph(graph_type, new_df, search_type, feature, artist)
        else:
            track_name = new_df['track_name'][0]
            print("The " + feature + " of " + artist + "'s " + track_name + " is " + str(average_feature))
            print_feature_description(track_name, feature, average_feature)
        
                

if __name__ == '__main__':
    main()

