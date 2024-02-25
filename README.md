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
  6. After scraping, save the updated DataFrames to CSV and Excel files.

- ### Data Analysis
  Upon successful data collection, PyShowHarvest proceeds to the analysis phase. Utilizing Pandas for data manipulation and Plotly for visualization, the project generates various charts and graphs. These visualizations provide insights into crucial aspects, including genre distribution, country representation, top actors, and the correlation between viewer ratings and the number of raters.

### Key Features
- **Genre Distribution:** Explore the distribution of genres in both dramas and movies through interactive pie charts.
- **Country Representation:** Visualize the geographical distribution of dramas and movies to understand their global representation.
- **Top Actors Analysis:** Explore insights into the most prolific actors, based on the number of dramas and movies they have been part of. This feature allows users to:
  - Identify actors who have contributed significantly to the Asian drama and movie landscape.
  - Click on an actor's name in the visualization to open the corresponding actor page on MyDramaList in a new browser tab.
  - Gain comprehensive information about the actor's career, filmography, and contributions to the industry.- **Rating Correlation:** Analyze the relationship between viewer ratings and the number of raters through insightful charts.
- **Scatterplot Interaction:** Explore a dynamic scatterplot that visualizes the relationship between ratings and the number of raters for both dramas and movies. This interactive chart allows users to:
  - Hover over data points to view detailed information about each title.
  - Click on a data point to open the corresponding MyDramaList page for the selected title in a new browser tab.
  - Gain deeper insights into viewer ratings and popularity trends.  

