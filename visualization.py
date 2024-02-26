import os
import webbrowser
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html


def create_charts(df_drama, df_movie):  # create all the graphs
    df_drama['Type'] = 'Drama'
    df_movie['Type'] = 'Movie'
    df_combined = pd.concat([df_drama, df_movie], ignore_index=True)

    app = dash.Dash(__name__)  # framework for graph

    app.layout = (html.Div
        ([
        html.H1("Drama and Movie Data Analysis"),  # title

        html.Div([  # pie chart
            dcc.Graph(id='genre-pie-chart'),  # genre pie chart
            dcc.Graph(id='movie-genre-pie-chart'),  # movie genre pie chart
        ], style={'display': 'flex'}),  # display the pie chart in a row

        dcc.Graph(id='country-bar-chart'),  # bar chart for country
        dcc.Graph(id='top-actors-chart'),  # bar chart for top actors
        dcc.Graph(id='scatter-plot-drama'),  # scatter plot for drama
        dcc.Graph(id='scatter-plot-combined'),  # scatter plot for combined
        dcc.Graph(id='scatter-plot-movie'),  # scatter plot for movie
        dcc.Location(id='redirect-url'),  # redirect url
        dcc.Graph(id='scatter-plot-drama-year'),  # scatter plot for drama year
        dcc.Graph(id='scatter-plot-movie-year'),  # scatter plot for movie year
    ]))

    def create_scatter_plot_drama(df, title):  # scatter drama plot
        fig = px.scatter(df[df['Type'] == 'Drama'],
                         x='Rating',  # x-axis  rating
                         y='Number of Raters',  # y-axis number of raters
                         title=title,  # title of the plot
                         labels={'Rating': 'Rating', 'Number of Raters': 'Number of Raters'},
                         hover_name='Title', color='Country', custom_data=['URL'])
        fig.update_traces(mode='markers', marker=dict(size=8), selector=dict(mode='markers'),
                          customdata=df[df['Type'] == 'Drama']['URL'])  # update the traces
        fig.update_traces(  # update the traces
            customdata=df[df['Type'] == 'Drama']['URL'],
            selector=dict(mode='markers'),
            hovertemplate="<br>".join([
                "Title: %{hovertext}",
                "Rating: %{x}",
                "Number of Raters: %{y}"
            ])
        )
        return fig  # return the figure

    def create_scatter_plot_combined(df, title, color_column):  # scatter plot for drama and movie combined
        fig = px.scatter(df, x='Rating', y='Number of Raters', title=title,
                         labels={'Rating': 'Rating', 'Number of Raters': 'Number of Raters'},
                         hover_name='Title', color=color_column, custom_data=['URL'],
                         color_discrete_map={'Drama': 'red', 'Movie': 'yellow'})
        fig.update_traces(mode='markers', marker=dict(size=8), selector=dict(mode='markers'), customdata=df['URL'])
        fig.update_traces(
            customdata=df['URL'],
            selector=dict(mode='markers'),
            hovertemplate="<br>".join([
                "Title: %{hovertext}",
                "Rating: %{x}",
                "Number of Raters: %{y}"
            ])
        )
        return fig

    def create_scatter_plot_movie(df, title):  # create scatter plot for movie only
        fig = px.scatter(df[df['Type'] == 'Movie'], x='Rating', y='Number of Raters', title=title,
                         labels={'Rating': 'Rating', 'Number of Raters': 'Number of Raters'},
                         hover_name='Title', color='Country', custom_data=['URL'])
        fig.update_traces(mode='markers', marker=dict(size=8), selector=dict(mode='markers'),
                          customdata=df[df['Type'] == 'Movie']['URL'])
        fig.update_traces(
            customdata=df[df['Type'] == 'Movie']['URL'],
            selector=dict(mode='markers'),
            hovertemplate="<br>".join([
                "Title: %{hovertext}",
                "Rating: %{x}",
                "Number of Raters: %{y}"
            ])
        )
        return fig

    @app.callback(  # callback for genre pie chart
        dash.dependencies.Output('genre-pie-chart', 'figure'),
        [dash.dependencies.Input('genre-pie-chart', 'clickData')]
    )
    def update_genre_pie_chart(clickData):  # update the genre pie chart
        try:
            genres_series = df_combined['Genres'].dropna()  # drop the na values
            flat_genres = [genre.strip() for genres_str in genres_series for genre in
                           genres_str.split('\n')]  # split the genres
            genre_counts = pd.Series(flat_genres).value_counts(normalize=True) * 100  # count the genres
            threshold = 2  # threshold for the genres
            small_sections = genre_counts[genre_counts < threshold]  # small sections
            genre_counts = genre_counts[genre_counts >= threshold]  # genre counts
            if not small_sections.empty:  # if small sections are not empty
                genre_counts['Other'] = small_sections.sum()

            fig = px.pie(
                names=genre_counts.index,
                values=genre_counts.values,
                title='Distribution of Drama Genres',
                labels={'Genre': 'Percentage'},
                template='seaborn',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                title=dict(text='Distribution of Drama Genres', font=dict(color='black', size=20)),
                legend=dict(font=dict(color='black')),
                height=600,
                width=800
            )

            return fig
        except Exception as e:
            print(f"Error in update_genre_pie_chart: {str(e)}")
            return dash.no_update

    @app.callback(  # callback for movie genre pie chart
        dash.dependencies.Output('movie-genre-pie-chart', 'figure'),
        [dash.dependencies.Input('movie-genre-pie-chart', 'clickData')]
    )
    def update_movie_genre_pie_chart(clickData):  # update the movie genre pie chart
        try:
            movie_genres_series = df_combined[df_combined['Type'] == 'Movie']['Genres'].dropna()
            flat_movie_genres = [genre.strip() for genres_str in movie_genres_series for genre in
                                 # split the movie genres
                                 genres_str.split('\n')]
            movie_genre_counts = pd.Series(flat_movie_genres).value_counts(normalize=True) * 100
            threshold = 2
            small_sections = movie_genre_counts[movie_genre_counts < threshold]
            movie_genre_counts = movie_genre_counts[movie_genre_counts >= threshold]
            if not small_sections.empty:
                movie_genre_counts['Other'] = small_sections.sum()

            fig = px.pie(
                names=movie_genre_counts.index,
                values=movie_genre_counts.values,
                title='Distribution of Movie Genres',
                labels={'Genre': 'Percentage'},
                template='seaborn',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                title=dict(text='Distribution of Movie Genres', font=dict(color='black', size=20)),
                legend=dict(font=dict(color='black')),
                height=600,
                width=800
            )

            return fig
        except Exception as e:
            print(f"Error in update_movie_genre_pie_chart: {str(e)}")
            return dash.no_update

    @app.callback(
        dash.dependencies.Output('country-bar-chart', 'figure'),
        [dash.dependencies.Input('country-bar-chart', 'clickData')]
    )
    def update_country_bar_chart(clickData):
        country_counts = df_combined['Country'].value_counts()

        fig = px.bar(country_counts, x=country_counts.index, y=country_counts.values,
                     title='Distribution of Dramas and Movies by Country',
                     labels={'y': 'Number of Dramas/Movies', 'x': 'Country'},
                     template='plotly_dark', color=country_counts.values,
                     color_continuous_scale='Viridis')

        fig.update_layout(
            template='plotly_white',
            title=dict(text='Distribution of Dramas and Movies by Country', font=dict(color='black')),
            xaxis=dict(title=dict(font=dict(color='black')), tickfont=dict(color='black')),
            yaxis=dict(title=dict(font=dict(color='black')), tickfont=dict(color='black')),
            coloraxis=dict(colorbar=dict(title=dict(font=dict(color='black'))))
        )

        return fig

    @app.callback(
        dash.dependencies.Output('top-actors-chart', 'figure'),
        [dash.dependencies.Input('top-actors-chart', 'clickData')]
    )
    def update_top_actors_chart(clickData):
        top_n = 15
        min_raters = 5000
        min_rating = 8.5  # Minimum movie rating

        # Filter the DataFrame based on both minimum raters and minimum rating
        filtered_df = df_combined[
            (df_combined['Number of Raters'] >= min_raters) & (df_combined['Rating'] >= min_rating)]

        actors_series = filtered_df['Actors'].dropna()
        flat_actors = [actor.strip().split(',')[0] for actors_str in actors_series for actor in actors_str.split('\n')]
        actors_df = pd.DataFrame({'Actor': flat_actors})
        actor_counts = actors_df['Actor'].value_counts()
        top_actors = actor_counts.head(top_n)

        fig = px.bar(top_actors, x=top_actors.index, y=top_actors.values,
                     title=f'Top {top_n} Actors by Number of Dramas and Movies (5000+ Raters)',
                     labels={'y': 'Number of Dramas/Movies', 'x': 'Actor'},
                     template='plotly_dark', color=top_actors.values,
                     color_continuous_scale='Viridis')

        fig.update_layout(
            template='plotly_white',
            title=dict(text=f'Top {top_n} Actors by Number of Dramas and Movies (5000+ Raters)',
                       font=dict(color='black')),
            xaxis=dict(title=dict(font=dict(color='black')), tickfont=dict(color='black')),
            yaxis=dict(title=dict(font=dict(color='black')), tickfont=dict(color='black')),
            coloraxis=dict(colorbar=dict(title=dict(font=dict(color='black'))))
        )

        return fig

    @app.callback(
        dash.dependencies.Output('scatter-plot-drama', 'figure'),
        [dash.dependencies.Input('scatter-plot-drama', 'clickData')]
    )
    def update_scatter_plot_drama(clickData):
        return create_scatter_plot_drama(df_combined, 'Drama Scatter Plot')

    @app.callback(
        dash.dependencies.Output('scatter-plot-combined', 'figure'),
        [dash.dependencies.Input('scatter-plot-combined', 'clickData')]
    )
    def update_scatter_plot_combined(clickData):
        excluded_genre = 'Variety'
        filtered_df = df_combined.copy()
        if excluded_genre:
            filtered_df = filtered_df[~filtered_df['Genres'].str.contains(excluded_genre, case=False, na=False)]

        return create_scatter_plot_combined(filtered_df, 'Combined Scatter Plot', 'Type')

    @app.callback(
        dash.dependencies.Output('scatter-plot-movie', 'figure'),
        [dash.dependencies.Input('scatter-plot-movie', 'clickData')]
    )
    def update_scatter_plot_movie(clickData):
        return create_scatter_plot_movie(df_combined, 'Movie Scatter Plot')

    @app.callback(
        dash.dependencies.Output('redirect-url', 'pathname'),
        [dash.dependencies.Input('scatter-plot-drama', 'clickData'),
         dash.dependencies.Input('scatter-plot-combined', 'clickData'),
         dash.dependencies.Input('scatter-plot-movie', 'clickData'),
         dash.dependencies.Input('scatter-plot-drama-year', 'clickData'),
         dash.dependencies.Input('scatter-plot-movie-year', 'clickData')]
    )
    def update_redirect_url(clickData_drama, clickData_combined, clickData_movie, clickData_drama_year,
                            clickData_movie_year):  # Redirect to the URL of the clicked title
        clickData = clickData_drama or clickData_combined or clickData_movie or clickData_drama_year or clickData_movie_year
        if clickData and 'points' in clickData and clickData['points']:  # If a point is clicked
            title = clickData['points'][0]['hovertext']  # Get the title
            print("Clicked Title:", title)  # print the title
            url = df_combined[df_combined['Title'] == title]['URL'].iloc[0] if title in df_combined[
                'Title'].values else None  # get the url
            if url:
                webbrowser.open_new_tab(url)  # open the url in a new tab
                return '/'  # Use the URL for redirection

    @app.callback(
        dash.dependencies.Output('scatter-plot-drama-year', 'figure'),
        [dash.dependencies.Input('scatter-plot-drama-year', 'clickData')]
    )
    def update_scatter_plot_drama_year(clickData):
        return create_scatter_plot_drama_year(df_combined, 'Drama Scatter Plot (Colored by Year)')

    def create_scatter_plot_drama_year(df, title):
        fig = px.scatter(df[df['Type'] == 'Drama'], x='Rating', y='Number of Raters', title=title,
                         labels={'Rating': 'Rating', 'Number of Raters': 'Number of Raters'},
                         hover_name='Title', color='Year', custom_data=['URL'],
                         color_continuous_scale='Rainbow')  # Choose your desired color scale
        fig.update_traces(mode='markers', marker=dict(size=8), selector=dict(mode='markers'),
                          customdata=df[df['Type'] == 'Drama']['URL'])
        fig.update_traces(
            customdata=df[df['Type'] == 'Drama']['URL'],
            selector=dict(mode='markers'),
            hovertemplate="<br>".join([
                "Title: %{hovertext}",
                "Rating: %{x}",
                "Number of Raters: %{y}"
            ])
        )
        return fig

    @app.callback(
        dash.dependencies.Output('scatter-plot-movie-year', 'figure'),  # scatter plot for movie year
        [dash.dependencies.Input('scatter-plot-movie-year', 'clickData')]
    )
    def update_scatter_plot_movie_year(clickData):
        return create_scatter_plot_movie_year(df_combined, 'Movie Scatter Plot (Colored by Year)')

    def create_scatter_plot_movie_year(df, title):
        fig = px.scatter(df[df['Type'] == 'Movie'], x='Rating', y='Number of Raters', title=title,
                         labels={'Rating': 'Rating', 'Number of Raters': 'Number of Raters'},
                         hover_name='Title', color='Year', custom_data=['URL'],
                         color_continuous_scale='Rainbow')  # Choose your desired color scale
        fig.update_traces(mode='markers', marker=dict(size=8), selector=dict(mode='markers'),
                          customdata=df[df['Type'] == 'Movie']['URL'])
        fig.update_traces(
            customdata=df[df['Type'] == 'Movie']['URL'],
            selector=dict(mode='markers'),
            hovertemplate="<br>".join([
                "Title: %{hovertext}",
                "Rating: %{x}",
                "Number of Raters: %{y}"
            ])
        )
        return fig

    app.run_server(use_reloader=False, port=4874)  # run the server


if __name__ == "__main__":
    df_drama = pd.read_csv('Data_Drama.csv')
    df_movie = pd.read_csv('Data_Movie.csv')
    df_combined = pd.concat([df_drama, df_movie], ignore_index=True)
    create_charts(df_drama, df_movie)
