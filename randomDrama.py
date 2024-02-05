from flask import Flask, render_template
import random
import pandas as pd

app = Flask(__name__)

# Load drama data
drama_data = pd.read_csv('Data_Drama.csv')  # Assuming you have a CSV file named Data_Drama.csv

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_synopsis')
def get_synopsis():
    random_row = drama_data.sample()
    title = random_row['Title'].values[0]
    country = random_row['Country'].values[0]
    synopsis = random_row['Synopsis'].values[0]
    director = random_row['Director'].values[0]
    actors = random_row['Actors'].values[0]
    actors_list = actors.split("\n")
    actors = "<br>".join(actors_list)

    genres = random_row['Genres'].values[0]
    rating = int(random_row['Rating'].values[0])  # Convert to regular integer
    num_raters = int(random_row['Number of Raters'].values[0])  # Convert to regular integer
    url = random_row['URL'].values[0]

    # Construct the response dictionary
    response = {
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

    return response


@app.route('/get_full_info')
def get_full_info():
    random_row = drama_data.sample()
    title = random_row['Title'].values[0]
    country = random_row['Country'].values[0]
    synopsis = random_row['Synopsis'].values[0]
    director = random_row['Director'].values[0]
    actors = random_row['Actors'].values[0]
    genres = random_row['Genres'].values[0]
    rating = int(random_row['Rating'].values[0])  # Convert to regular integer
    num_raters = int(random_row['Number of Raters'].values[0])  # Convert to regular integer
    url = random_row['URL'].values[0]

    # Construct the response dictionary
    response = {
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

    return response


if __name__ == '__main__':
    app.run(debug=True,port=2748)
