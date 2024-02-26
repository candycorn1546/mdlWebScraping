from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load drama data
drama_data = pd.read_csv('Data_Drama.csv')  # load csv file


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_synopsis') # route to get the synopsis
def get_synopsis():
    random_row = drama_data.sample() # get a random row
    title = random_row['Title'].values[0] # get the title
    country = random_row['Country'].values[0] # get the country
    synopsis = random_row['Synopsis'].values[0]     # get the synopsis
    director = random_row['Director'].values[0] # get the director
    actors = random_row['Actors'].values[0] # get the actors
    actors_list = actors.split("\n") # split the actors
    actors = "<br>".join(actors_list) # join the actors

    genres = random_row['Genres'].values[0] # get the genres
    rating = float(random_row['Rating'].values[0]) # get the rating
    num_raters = int(random_row['Number of Raters'].values[0]) # get the number of raters
    url = random_row['URL'].values[0]   # get the url

    response = { # create a response
        'title': title,
        'country': country,
        'synopsis': synopsis,
        'director': director,
        'actors': actors,
        'genres': genres,
        'rating': rating,
        'num_raters': num_raters,
        'url': url
    }

    return response     # return the response


if __name__ == '__main__':
    app.run(port=2748)
