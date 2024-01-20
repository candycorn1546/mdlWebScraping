import logging
import os
import time
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import concurrent.futures
import threading

# Use a global lock to synchronize DataFrame access
df_lock = threading.Lock()

# Define a global variable to signal when to stop saving updates
save_updates = True

def load_existing_data(csv_file, excel_file):
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    elif os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:
        return pd.DataFrame(columns=['Title', 'Country', 'Synopsis', 'Director', 'Actors', 'Genres', 'Rating', 'Number of Raters', 'URL'])

def save_dataframe_periodically(df, csv_file, excel_file, interval_seconds=30):
    global save_updates
    while save_updates:
        # Save the DataFrame to CSV and Excel files
        with df_lock:
            df.to_csv(csv_file, index=False)
            df.to_excel(excel_file, index=False)

        # Sleep for the specified interval
        time.sleep(interval_seconds)

def scraping(url, df, processed_urls):
    try:
        #print(f"Processing URL: {url}")
        result = requests.get(url, timeout=10)
        content = result.text
        only_a_tags = SoupStrainer("a")
        soup = BeautifulSoup(content, "html.parser", parse_only=only_a_tags)
        anchor_tags = soup.find_all('a')
        href_links = [a.get('href') for a in anchor_tags if a.get('href') and a.get('href').startswith('/')]
        href_pattern = re.compile(r'/[0-9].*')
        matches = href_pattern.findall('\n'.join(href_links))
        for match in set(matches):
            website = "https://mydramalist.com/" + match

            # Check if the URL is already processed or in the DataFrame
            with df_lock:
                if website in processed_urls or website in df['URL'].values:
                    print(f"URL {website} already processed, skipping.")
                    continue

            result = requests.get(website)
            content = result.text
            soup = BeautifulSoup(content, "html.parser")
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

                    with df_lock:
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
                        processed_urls.add(website)
                        print(f"Added entry for URL: {website}")

    except Exception as e:
        logging.error(f"Error while scraping {url}: {e}")
        print(f"Error while scraping {url}: {e}")

# Rest of your code...

def scrape_with_threadpool(section, df):
    processed_urls = set()  # Set to store processed URLs for each section
    urls = [f"https://mydramalist.com/{section}?page={page}" for page in range(1, 251)]
    batch_size = 10

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            executor.map(scraping, batch_urls, [df] * len(batch_urls), [processed_urls] * len(batch_urls))


if __name__ == "__main__":
    start_time = time.time()
    total_shows_added = 0
    total_movies_added = 0
    section_counts = {}
    csv_directory = '/Users/vy/PycharmProjects/mdlWebScraping/'
    csv_drama_file = os.path.join(csv_directory, 'Data_Drama.csv')
    excel_drama_file = os.path.join(csv_directory, 'Data_Drama.xlsx')
    csv_movie_file = os.path.join(csv_directory, 'Data_Movie.csv')
    excel_movie_file = os.path.join(csv_directory, 'Data_Movie.xlsx')

    # Load existing data
    df_drama = load_existing_data(csv_drama_file, excel_drama_file)
    df_movie = load_existing_data(csv_movie_file, excel_movie_file)

    try:
        # Start the thread to save updates periodically
        save_thread_drama = threading.Thread(target=save_dataframe_periodically, args=(df_drama, csv_drama_file, excel_drama_file))
        save_thread_drama.start()

        for section in ['shows/popular', 'shows/top', 'movies/popular', 'movies/top', 'shows/variety', 'shows/newest']:
        #for section in ['shows/top', 'movies/top', 'shows/variety']:
            # Pass the correct DataFrame to the function
            df = df_drama if 'shows' in section else df_movie

            # Get the initial count before scraping
            initial_count = df.shape[0]

            scrape_with_threadpool(section, df)
            items_added = df.shape[0] - initial_count
            if 'shows' in section:
                total_shows_added += items_added
                section_counts[section] = items_added
            else:
                total_movies_added += items_added
                section_counts[section] = items_added

    except Exception as e:
        print(e)

    finally:
        # Stop the thread when the main scraping is finished
        save_updates = False
        save_thread_drama.join()

    end_time = time.time()
    total_runtime = round((end_time - start_time) / 60, 2)
    print(f'Total runtime: {total_runtime} minutes\n')

    # Print the total shows and movies added
    print(f'Total shows added: {total_shows_added}')
    print(f'Total movies added: {total_movies_added}')

    # Print the counts for each section
    for section, count in section_counts.items():
        print(f'Total added for {section}: {count}')

    # Save the DataFrames after the loop
    df_drama.to_csv(csv_drama_file, index=False)
    df_drama.to_excel(excel_drama_file, index=False)
    df_movie.to_excel(excel_movie_file, index=False)
    df_movie.to_csv(csv_movie_file, index=False)
