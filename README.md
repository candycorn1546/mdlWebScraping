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

## Pictures of Data
1. Pie chart that shows the most popular genres between movies and dramas 
<img width="1450" alt="Screenshot 2024-02-24 at 10 41 33 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/3df05993-0bc6-4c0c-bc2f-5f4b73b872a2">
<br><br>

2. Bar graph showing the most popular countries
<img width="1498" alt="Screenshot 2024-02-24 at 10 56 36 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/9ef16757-0889-4938-aba1-19a45cda4403">
<br><br>

3. Top 15 actors/actresses who are most well-received on the website
<img width="1482" alt="Screenshot 2024-02-24 at 10 59 54 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/a38f2dbe-fb2d-4387-bb58-08ab4d58b1e1">
<br><br>

4. A scatter plot with all dramas identified by country
<img width="1500" alt="Screenshot 2024-02-24 at 11 01 20 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/e5392b72-fd4b-4fb4-afb1-63d15c798a1f">
<br><br>

5. A scatter plot with all movies identified by country
<img width="1499" alt="Screenshot 2024-02-24 at 11 01 52 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/038fc137-e52b-4948-80d2-4b01fe32f2fb">
<br><br>

6. Combinated scatter plot between movies and dramas
<img width="1479" alt="Screenshot 2024-02-24 at 11 01 29 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/c383d66e-f9b0-4b88-9285-704e62c4c4a0">
<br><br>
7. A scatter plot with all dramas identified by year
<img width="1493" alt="Screenshot 2024-02-24 at 11 02 00 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/fa68d2a9-ae23-44b6-a0db-e89028d0c00d">
<br><br>
8. A scatter plot with all movies identified by country
<img width="1491" alt="Screenshot 2024-02-24 at 11 02 15 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/c1b0923e-6a08-4bed-b608-b154a800f553">
<br><br>

## Random Drama Generator Website
- #### A minimalist-looking website that generates a random drama synopsis, based on the synopsis the user can then learn more information about the dramas or fetch a new synopsis.
<img width="1512" alt="Screenshot 2024-02-24 at 11 15 30 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/c71d13c9-96a9-4075-a6f8-770a1e7fc52d">
<br><br>
<img width="1512" alt="Screenshot 2024-02-24 at 11 15 57 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/60a484b7-62b4-4f54-bddf-c6d281219e58">
<br><br>
<img width="1508" alt="Screenshot 2024-02-24 at 11 16 03 PM" src="https://github.com/candycorn1546/mdlWebScraping/assets/157404986/b94b5f7c-e28c-44fa-8fe6-c700b706c9c2">

### Disclaimer
- This project is for education purposes only. Do not use this application maliciously and be well aware of what you are doing before executing or modifying the program.





