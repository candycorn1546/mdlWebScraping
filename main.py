import logging
import os
import time
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import concurrent.futures
import threading

df_lock = threading.Lock()
save_updates = True


def load_existing_data(csv_file, excel_file):  # function for loading existing df
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    elif os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:  # if df doesn't exist
        return pd.DataFrame(columns=['Title', 'Year', 'Country', 'Synopsis', 'Director', 'Actors', 'Genres', 'Rating',
                                     'Number of Raters', 'URL'])


def save_dataframe_periodically(df, csv_file, excel_file, interval_seconds=30):  # save df occasionally in case of crash
    global save_updates
    while save_updates:
        with df_lock:
            df.to_csv(csv_file, index=False)
            df.to_excel(excel_file, index=False)
        time.sleep(interval_seconds)


def scraping(url, df, processed_urls):  # scraper
    try:
        result = requests.get(url, timeout=10)  # get request to url
        content = result.text  # extract content
        only_a_tags = SoupStrainer("a")  # a filter to only get hyperlink
        soup = BeautifulSoup(content, "html.parser", parse_only=only_a_tags)  # parse only hyperlink due to a tag
        anchor_tags = soup.find_all('a')  # find all a tag in HTML
        href_links = [a.get('href') for a in anchor_tags if a.get('href') and a.get('href').startswith('/')]
        # extract all valid href with '/'
        href_pattern = re.compile(r'/[0-9].*')  # get all href that start with '/' and a number from 0-9
        matches = href_pattern.findall('\n'.join(href_links))  # join the href to the link
        for match in set(matches):  # for a match (set to avoid dups)
            website = "https://mydramalist.com" + match  # join website with href
            with df_lock:  # lock to ensure thread safety while accessing
                if website in processed_urls or website in df['URL'].values:
                    # if website is already in URL then go to next
                    continue
            result = requests.get(website)
            content = result.text  # extract content
            soup = BeautifulSoup(content, "html.parser")  # BeautifulSoup to parse the HTML
            box = soup.find("h1", class_="film-title")  # find the class film title
            if box is not None:  # if the box is not None
                title = box.get_text()  # get title
                title_tag = soup.find('h1', class_='film-title')
                title_text = title_tag.text
                year_match = re.search(r'\((\d{4})\)', title_text)
                year = year_match.group(1) if year_match else None  # get year
                watchers_info = soup.find('div', class_='hfs').text  # find div with clas 'hfs' and get watcher info
                if 'users' not in watchers_info:  # if substring user is not in watcher info
                    continue
                watchers_count = watchers_info.split(': ')[1]
                watchers_count2 = int(watchers_info.split('from ')[1].split(' users')[0].replace(',', ''))
                rating = float(watchers_count.split('/')[0])  # get rating number
                if watchers_count2 >= 500:  # if less than 500 raters then move on
                    director_name = soup.select_one(
                        '#show-detailsxx > div.show-detailsxss > ul:nth-child(1) > li:nth-child(4)').find('a',
                                                                                                          class_='text-primary')
                    director_name_text = director_name.get_text(strip=True)  # get director name
                    synopsis_box = soup.find("div", class_="show-synopsis")  # get the synopsis box
                    synopsis = synopsis_box.get_text(strip=True, separator=' ') if synopsis_box else None
                    modified_text = synopsis.split("(Source")[0].split("Edit")[
                        0] if synopsis else None  # get the synopsis without extra info
                    actors_info = []
                    actor_items = soup.find_all('li', class_='list-item col-sm-4')[:6]  # find all the elements
                    for actor_item in actor_items:  # Extract the actor's name
                        actor_name = actor_item.select_one('b[itempropx="name"]').text if actor_item.select_one(
                            'b[itempropx="name"]') else None
                        role_name = actor_item.select_one('small').text if actor_item.select_one(
                            'small') else None  # Extract the role name
                        actors_info.append({  # Append actor and role
                            'actor_name': actor_name,
                            'role_name': role_name,
                        })
                    actors_info_str = '\n'.join(
                        [f"{info['actor_name']}, Role: {info['role_name']}" for info in actors_info])  # toString

                    country = None
                    country_element = soup.find('b', class_='inline')  # Find b element with the class "inline"
                    if country_element:  # if the  element is found, extract the name
                        country = country_element.find_next('i', class_='flag').previous_sibling.strip()
                    else:  # If not found, find a li element with class "list-item p-a-0"
                        li_element = soup.find('li', class_='list-item p-a-0')
                        if li_element:  # If the li element is found, extract
                            li_text = li_element.get_text(strip=True)
                            if 'Country:' in li_text:
                                country = li_text.replace('Country:', '').strip()
                                # strip country and extract the country name

                    genres = soup.find('li', class_='list-item p-a-0 show-genres')  # find class 'show-genres'
                    genres_text = genres.get_text(strip=True).split('Genres:')[1].strip() if genres else None
                    # Extracting genre information from the text content
                    genresList = [genre.strip() for genre in genres_text.split(',')] if genres_text else None
                    # split the string on commas and strip whitespace from each genre
                    genres_string = '\n '.join(genresList) if genresList else None  # toString

                    with df_lock:  # ensure thread safety
                        df.loc[df.shape[0]] = {  # new row to the df with extracted information
                            'Title': title,
                            'Year': int(year),
                            'Country': country,
                            'Synopsis': modified_text,
                            'Director': director_name_text,
                            'Actors': actors_info_str,
                            'Genres': genres_string,
                            'Rating': rating,
                            'Number of Raters': watchers_count2,
                            'URL': website
                        }
                        processed_urls.add(website)  # add processed URL to the set of processed URLs

    except Exception as e:
        logging.error(f"Error while scraping {url}: {e}")  # exception occurs, log the error message with URL
        print(f"Error while scraping {url}: {e}")


def scrape_with_threadpool(section, df):
    processed_urls = set()  # keep track of processed urls
    urls = [f"https://mydramalist.com/{section}?page={page}" for page in range(1, 251)]  # list of URLs to scrape
    batch_size = 10  # batch size for concurrent

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # ThreadPoolExecutor with a maximum of 50 worker
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            executor.map(scraping, batch_urls, [df] * len(batch_urls), [processed_urls] * len(batch_urls))
            # map the scraping into batch of urls, passing the df and processed urls set


if __name__ == "__main__":
    start_time = time.time()  # timer
    total_shows_added = 0  # count
    total_movies_added = 0  # count
    section_counts = {}  # dictionary
    csv_directory = '/Users/vy/PycharmProjects/mdlWebScraping/'  # Directory path
    csv_drama_file = os.path.join(csv_directory, 'Data_Drama.csv')  # file path
    excel_drama_file = os.path.join(csv_directory, 'Data_Drama.xlsx')  # file path
    csv_movie_file = os.path.join(csv_directory, 'Data_Movie.csv')  # file path
    excel_movie_file = os.path.join(csv_directory, 'Data_Movie.xlsx')  # file path

    df_drama = load_existing_data(csv_drama_file, excel_drama_file)  # Load existing data
    df_movie = load_existing_data(csv_movie_file, excel_movie_file)  # Load existing data

    try:
        save_thread_drama = threading.Thread(target=save_dataframe_periodically,
                                             args=(df_drama, csv_drama_file, excel_drama_file))
        save_thread_drama.start()

        for section in ['shows/popular', 'shows/top', 'movies/popular', 'movies/top', 'shows/newest']:
            # sections to scrape data
            df = df_drama if 'shows' in section else df_movie  # if show then in show else in movie
            initial_count = df.shape[0]  # initial count of rows in df

            scrape_with_threadpool(section, df)
            items_added = df.shape[0] - initial_count  # calculator num of item added to df
            if 'shows' in section:
                total_shows_added += items_added
                section_counts[section] = items_added
            else:
                total_movies_added += items_added
                section_counts[section] = items_added

    except Exception as e:  # Handle any exceptions
        print(e)

    finally:
        save_updates = False
        save_thread_drama.join()

    end_time = time.time()
    total_runtime = round((end_time - start_time) / 60, 2)
    print(f'Total runtime: {total_runtime} minutes\n')  # calculate run time and turn it into mins

    print(f'Total shows added: {total_shows_added}')  # total show added
    print(f'Total movies added: {total_movies_added}')  # total movies added

    for section, count in section_counts.items():
        print(f'Total added for {section}: {count}')

    # Save drama and movie df to CSV and excel
    df_drama.to_csv(csv_drama_file, index=False)
    df_drama.to_excel(excel_drama_file, index=False)
    df_movie.to_excel(excel_movie_file, index=False)
    df_movie.to_csv(csv_movie_file, index=False)
