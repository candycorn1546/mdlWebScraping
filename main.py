import os
import time
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

start_time = time.time()
df_drama = pd.DataFrame(columns=['Title', 'Synopsis', 'Director', 'Actors', 'Genres', 'Rating', 'Number of Raters', 'URL'])
df_movie = pd.DataFrame(columns=['Title', 'Synopsis', 'Director', 'Actors', 'Genres', 'Rating', 'Number of Raters', 'URL'])

try:
    for section, df in zip(['shows', 'movies'], [df_drama, df_movie]):
        for page in range(1, 2):
            website = f"https://mydramalist.com/{section}/top?page={page}"
            result = requests.get(website)
            content = result.text
            only_a_tags = SoupStrainer("a")
            soup = BeautifulSoup(content, "lxml", parse_only=only_a_tags)
            anchor_tags = soup.find_all('a')
            href_links = [a.get('href') for a in anchor_tags if a.get('href') and a.get('href').startswith('/')]
            href_pattern = re.compile(r'/[0-9].*')
            matches = href_pattern.findall('\n'.join(href_links))
            for match in set(matches):
                website = "https://mydramalist.com/" + match

                result = requests.get(website)
                content = result.text
                soup = BeautifulSoup(content, "lxml")

                box = soup.find("h1", class_="film-title")
                if box is not None:
                    title = box.get_text()
                    watchers_info = soup.find('div', class_='hfs').text
                    watchers_count = watchers_info.split(': ')[1]
                    watchers_count2 = int(watchers_info.split('from ')[1].split(' users')[0].replace(',', ''))
                    rating = float(watchers_count.split('/')[0])
                    if watchers_count2 >= 500:
                        director_name = soup.select_one(
                            '#show-detailsxx > div.show-detailsxss > ul:nth-child(1) > li:nth-child(4)').find('a', class_='text-primary')
                        director_name_text = director_name.get_text(strip=True)
                        synopsis_box = soup.find("div", class_="show-synopsis")
                        synopsis = synopsis_box.get_text(strip=True, separator=' ')
                        modified_text = synopsis.split("(Source")[0]
                        actors = soup.select('li.list-item')
                        genres = soup.find('li', class_='list-item p-a-0 show-genres')
                        genres_text = genres.get_text(strip=True).split('Genres:')[1].strip()
                        genresList = [genre.strip() for genre in genres_text.split(',')]
                        genres_string = '\n '.join(genresList)
                        actors_info = []
                        actor_items = soup.find_all('li', class_='list-item col-sm-4')[:6]
                        for actor_item in actor_items:
                            actor_name = actor_item.select_one('b[itempropx="name"]').text
                            role_name = actor_item.select_one('small').text
                            actors_info.append({
                                'actor_name': actor_name,
                                'role_name': role_name,
                            })
                        actors_info_str = '\n'.join([f"{info['actor_name']}, Role: {info['role_name']}" for info in actors_info])

                        df.loc[df.shape[0]] = [title, modified_text, director_name_text, actors_info_str, genres_string,
                                               rating, watchers_count2, website]

except Exception as e:
    print(e)

end_time = time.time()
total_runtime = end_time - start_time
print(f'Total runtime: {total_runtime} seconds')

csv_directory = '/Users/vy/PycharmProjects/mdlWebScraping/'
csv_drama_file = os.path.join(csv_directory, 'Data_Drama.csv')
csv_movie_file = os.path.join(csv_directory, 'Data_Movie.csv')

