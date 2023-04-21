import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from tree import Node, BinarySearchTree
from spotipy.cache_handler import CacheFileHandler




# import file that has class definitions

queens_names = [["taylor swift", "taylor", "ts", "t"],
               ["selena gomez", "selena", "sg", "s"],
               ["olivia rodrigo", "olivia", "or", "o"]]

search_types = [["a song", "song", "s"],
                ["an album", "album", "a"],
                ["her entire discography", "entire discography", "discography", "all"]]

features_list = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence']


def set_up_api():
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


def get_track_features(artist, search_type, df, sp):
    """_summary_
    """
    

    
    track_features = []
    track_features_tree = BinarySearchTree()
 
    if search_type == 'entire discography':
        # use df and iterate through to create a list of track names
        # query api for feature, return average of that feature
        # plot the histogram of the features
        # print how featureable it is based on its value
        df = df.drop_duplicates(subset=['track_name'])
        tracks = df["track_name"].values.tolist()
        feature = get_feature()
        for track in tracks:
            results = sp.search(q="track:" + track + " " + "artist:" + artist, limit = 1)
            if results["tracks"]["items"]:
                track_id = results["tracks"]["items"][0]["id"]
                features = sp.audio_features(track_id)
                specific_feature = features[0][feature]
                #track_features.append(specific_feature)
                track_features_tree.put(specific_feature, track)
                

        # then create a function that takes in a list and finds average and prints how featureable it is
        # maybe create another function that takes in that list and makes a histogram? using plotly
        
    elif search_type == 'album':
        while True:
            # taylor swift brings up red instead?
            album_name = input("What album by " + artist + " would you like to know more about? ").lower()
            # use df and iterate through to create a list of track names from that album
            # query api for feature, return average of that feature
            # plot the histogram of the features
            # print how featureable it is based on its value
            # create a binary search tree that has the songs and the different values
            # then sort them? and then make a histogram or something
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
                        # return bst instead? insert the track name, feature, etc. into a tree
                        #track_features.append(specific_feature)
                        track_features_tree.put(specific_feature, track)
                break
            else:
                print("This album doesn't exist by this artist. please try again")

    elif search_type == 'song':
        while True:
            song_name = input("What song by " + artist + " would you like to know more about? ")
            # how do we validate the input of the song before asking them what feature they want
            # query api for feature and just return that feature's value
            # print how featureable it is based on its value
            results = sp.search(q="track:" + song_name + " " + "artist:" + artist, limit = 1)
            if results["tracks"]["items"]:
                feature = get_feature()
                track_id = results["tracks"]["items"][0]["id"]
                features = sp.audio_features(track_id)
                specific_feature = features[0][feature]
                #track_features.append(specific_feature)
                track_features_tree.put(specific_feature, song_name)
                break
            else:
                print("This song doesn't exist by this artist. please try again")
            
    return track_features_tree
    return track_features    

def get_artist():
    while True:
        artist = input("Would you like to learn about Taylor Swift, Olivia Rodrigo, or Selena Gomez's discography? ").lower()
        if artist in queens_names[0] or artist in queens_names[1] or artist in queens_names[2]:
            return artist
        else:
            print("Please enter one of the three names: 'Taylor Swift', 'Selena Gomez', or 'Olivia Rodrigo'. If you're feeling lazy, shorthands like 'Taylor', 'TS', or 'T' are okay as well")
    return

def get_search_type():
    while True:
        search_type = input("Do you want to know about a song, an album, or her entire discography? ").lower()
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
    while True:
        feature = input("Would you like to know about the acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, or valence? ").lower()
        if feature in features_list:
            return feature
        else:
            print("Please indicate one of the following: 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence")
    
def inorder(Node):
    if Node:
        inorder(Node.leftChild)
        print(Node.feature, Node.track)
        inorder(Node.rightChild)
    
def main():
    # import the csv files
    olivia_rodrigo = pd.read_csv("olivia.csv")

    selena_gomez = pd.read_csv("selena.csv")

    # taylor swift has many albums like folklore or folklore: long pond studios, so we need just a list
    # same as selena gomez
    taylor_swift = pd.read_csv("taylor.csv")  
    
   
    # think of better name
    print("Welcome to my project!")
    # validate that the answer is one of the three?
    
    sp = set_up_api
    artist = get_artist()
    search_type = get_search_type()
    
    # cache somewhere?
    
    tree = BinarySearchTree()
    if artist in queens_names[0]:
        tree = get_track_features("Taylor Swift", search_type, taylor_swift, sp)
    elif artist in queens_names[1]:
        tree = get_track_features("Selena Gomez", search_type, selena_gomez, sp)
    elif artist in queens_names[2]:
        tree = get_track_features("Olivia Rodrigo", search_type, olivia_rodrigo, sp)
    
    inorder(tree.root)
    

if __name__ == '__main__':
    main()

