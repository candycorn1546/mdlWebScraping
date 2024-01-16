import logging
import os
import time
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import concurrent.futures

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')

def scraping(url, df):
    result = requests.get(url)
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
            if 'users' not in watchers_info:
                continue
            watchers_count = watchers_info.split(': ')[1]
            watchers_count2 = int(watchers_info.split('from ')[1].split(' users')[0].replace(',', ''))
            rating = float(watchers_count.split('/')[0])
            if watchers_count2 >= 500:
                director_name = soup.select_one(
                    '#show-detailsxx > div.show-detailsxss > ul:nth-child(1) > li:nth-child(4) a.text-primary')
                director_name_text = director_name.get_text(strip=True) if director_name else None
                synopsis_box = soup.find("div", class_="show-synopsis")
                synopsis = synopsis_box.get_text(strip=True, separator=' ') if synopsis_box else None
                modified_text = synopsis.split("(Source")[0] if synopsis else None
                actors_info = []
                actor_items = soup.find_all('li', class_='list-item col-sm-4')[:6]
                for actor_item in actor_items:
                    actor_name = actor_item.select_one('b[itempropx="name"]').text if actor_item.select_one(
                        'b[itempropx="name"]') else None
                    role_name = actor_item.select_one('small').text if actor_item.select_one('small') else None
                    actors_info.append({
                        'actor_name': actor_name,
                        'role_name': role_name,
                    })
                actors_info_str = '\n'.join(
                    [f"{info['actor_name']}, Role: {info['role_name']}" for info in actors_info])

                country = None
                country_element = soup.find('b', class_='inline')
                if country_element:
                    country = country_element.find_next('i', class_='flag').previous_sibling.strip()
                else:
                    li_element = soup.find('li', class_='list-item p-a-0')
                    if li_element:
                        li_text = li_element.get_text(strip=True)
                        if 'Country:' in li_text:
                            country = li_text.replace('Country:', '').strip()

                genres = soup.find('li', class_='list-item p-a-0 show-genres')
                genres_text = genres.get_text(strip=True).split('Genres:')[1].strip() if genres else None
                genresList = [genre.strip() for genre in genres_text.split(',')] if genres_text else None
                genres_string = '\n '.join(genresList) if genresList else None

                df.loc[df.shape[0]] = {
                    'Title': title,
                    'Country': country,
                    'Synopsis': modified_text,
                    'Director': director_name_text,
                    'Actors': actors_info_str,
                    'Genres': genres_string,
                    'Rating': rating,
                    'Number of Raters': watchers_count2,
                    'URL': website
                }

def scrape_with_threadpool(section, df):
    urls = [f"https://mydramalist.com/{section}?page={page}" for page in range(1, 3)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        executor.map(scraping, urls, [df]*len(urls))

if __name__ == "__main__":
    start_time = time.time()
    total_shows_added = 0
    total_movies_added = 0
    section_counts = {}
    df_drama = pd.DataFrame(
        columns=['Title', 'Country', 'Synopsis', 'Director', 'Actors', 'Genres', 'Rating', 'Number of Raters', 'URL'])
    df_movie = pd.DataFrame(
        columns=['Title', 'Country', 'Synopsis', 'Director', 'Actors', 'Genres', 'Rating', 'Number of Raters', 'URL'])

    try:
        for section in ['shows/popular', 'shows/top', 'movies/popular', 'movies/top', 'shows/variety', 'shows/newest']:
            # Pass the correct DataFrame to the function
            df = df_drama if 'shows' in section else df_movie

            # Get the initial count before scraping
            initial_count = df.shape[0]

            scrape_with_threadpool(section, df)
            items_added = df.shape[0] - initial_count
            if 'shows' in section:
                total_shows_added += items_added
                section_counts[section] = items_added
                #print(f'{section}: {items_added} shows added')
            else:
                total_movies_added += items_added
                section_counts[section] = items_added
                #print(f'{section}: {items_added} movies added')

    except Exception as e:
        print(e)

    end_time = time.time()
    total_runtime = round((end_time - start_time)/60,2)
    print(f'Total runtime: {total_runtime} minutes\n')

    # Print the total shows and movies added
    print(f'Total shows added: {total_shows_added}')
    print(f'Total movies added: {total_movies_added}')

    # Print the counts for each section
    for section, count in section_counts.items():
        print(f'Total added for {section}: {count}')

    csv_directory = '/Users/vy/PycharmProjects/mdlWebScraping/'
    csv_drama_file = os.path.join(csv_directory, 'Data_Drama.csv')
    csv_movie_file = os.path.join(csv_directory, 'Data_Movie.csv')
    excel_drama_file = os.path.join(csv_directory, 'Data_Drama.xlsx')
    excel_movie_file = os.path.join(csv_directory, 'Data_Movie.xlsx')

    # Save the DataFrames after the loop
    df_drama.to_csv(csv_drama_file, index=False)
    df_drama.to_excel(excel_drama_file, index=False)
    df_movie.to_excel(excel_movie_file, index=False)
    df_movie.to_csv(csv_movie_file, index=False)
