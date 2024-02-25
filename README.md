# PyShowHarvest Web Scraping and Data Analysis

- ### Overview
  This project, named PyShowHarvest, focuses on web scraping data from a popular website providing comprehensive information about Asian dramas and movies. The primary objective is to collect valuable insights and statistics from the scraped data, enabling a detailed analysis of trends related to dramas and movies.

- ### Introduction
  MyDramaList provides a rich source of information, including titles, directors, actors, genres, ratings, and more. PyShowHarvest leverages Python and libraries like requests and BeautifulSoup to extract this information through web scraping. Subsequently, the project employs data analysis tools like Pandas and Plotly to derive meaningful patterns and trends.

- ### Process
  1. Import all the dependencies, and load the existing CSV and Excel files. If the file doesn't exist, it will create new CSV and Excel files.
  2. The main function called 'scrapping' handles the scraping of all the information from the website including synopsis, URL, actors, country, genre, etc.
  3. Iterates through different sections (e.g., popular shows, top movies) to scrape data.
  4. The function extracts relevant information from the parsed HTML using various techniques such as finding specific HTML elements by class name (find, find_all) or using regular expressions (re).
  5. Uses 'scrape_with_threadpool' function to scrape multiple URLs concurrently using ThreadPoolExecutor.
  6. After scraping, it saves the updated DataFrames to CSV and Excel files.
     

