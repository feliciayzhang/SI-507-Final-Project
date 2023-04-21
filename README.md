# SI-507-Final-Project: Learning the moods of Taylor Swift, Selena Gomez, and Olivia Rodrigo discography
Github repo for SI 507 final project

## Project Description
This project is meant to be an interactive program for users to interact with and learn more about the music of the three artists Taylor Swift, Selena Gomez, and Olivia Rodrigo. Specifically, this program looks at the danceability, energy, and valence of the discography. Interaction is done through the command line, where the user can enter input and the program will run. Graphs (histograms and boxplots) are also displayed for better visualization of these metrics.

## Install Project
To use this project, the user needs to have python installed on their computer. Furthermore, there are a few libraries that are required to be downloaded as well. These include pandas, numpy,spotipy (which is a package to use the Spotify API), and plotly. These can be installed with `pip install pandas` (replacing the respective library name). 
This project also uses the Spotify API, so the user will need to make an account at https://developer.spotify.com/. The user will need to. reate a new project, and replace the `client_id` and `client_secret` fields with the tokens provided on their own Spotify account. This project also utilizes caching with spotipy.cache_handler and use Oauth with spotipy.oauth2. 
Datasets that are used in this project are taken from kaggle.com, and contain information on the track names and album names of the songs of Taylor Swift, Selena Gomez, and Olivia Rodrigo. These are stored in `taylor.csv`, `selena.csv`, and `olivia.csv` respectively.

## Using This Project
To use this project, run the file called final_project.py in the command line. This will start the program and prompt the user to choose between one of the three artists: Taylor Swift, Selena Gomez, or Olivia Rodrigo. Once the user selects an artist, they are able to choose from the artist's entire discography, a specific album, or a specific song. After that, they can choose between learning about the danceability, energy, or valence of what they have selected. The program will then output those metrics and provide some descriptions. The user also has the option of viewing histograms or boxplots of the data in their web browser. The user is able to do this for as long as they want until they enter 'exit' to any of the questions.

## Data Organization
Querying the Spotify API is done by matching what the user enters with its corresponding field in the data returned by the API. If the user chooses an album, the program looks through the dataframe that stores that artist and finds the track names that are in that album. Then those tracks are queried through using the API, and the feature that the user selected (danceability, energy, or valence) are returned and inserted into a binary search tree. See `tree.py` for class definitions of the trees and nodes. For example, if the user chooses danceability and the album Lover by Taylor Swift, the program will insert 'danceability', the actual value of danceability, Lover, and the track nams of each song on the album into the tree. Inorder traversal of the tree is employed to take the values and make a new data frame that cane be used to create histograms and boxplots later on.


# Credits
Felicia Zhang

# License
N/A
