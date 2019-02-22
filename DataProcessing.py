# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def missingValuesCount(key, list):
    num = 0
    for row in list[key]:
        if pd.isna(row):
            num += 1
    return num

def main():
    movies = pd.read_csv("source/Movie_Movies.csv")
    genre = pd.read_csv("source/Movie_Genres.csv")
    actors = pd.read_csv("source/Movie_Actors.csv")
    writer = pd.read_csv("source/Movie_Writer.csv")
    additionalRatings = pd.read_csv("source/Movie_AdditionalRating.csv")
    # print(Genre['Genre'].nunique())

    #print(Movies.info())
    # print(Genre['Genre'].nunique())

    movies.drop(['Awards', 'DVD', 'Plot', 'Poster', 'Production', 'Website', 'Type', 'Rated'],
                axis=1, inplace=True)
    # print(movies.info())
    actors.drop(['Unnamed: 0'], axis=1, inplace=True)
    writer.drop(['Unnamed: 0'], axis=1, inplace=True)
    additionalRatings.drop(['Unnamed: 0'], axis=1, inplace=True)
    genre.drop(['Unnamed: 0'], axis=1, inplace=True)

    # movies = pd.merge(movies, additionalRatings, on='imdbID')
    # Country,Director,Language,Released,Runtime,Title,Year,imdbID,imdbRating,imdbVotes
    print("Broj nedostajucih vrednosti ")
    print("Country: ")
    print(missingValuesCount('Country', movies))
    print("Director: ")
    print(missingValuesCount('Director', movies))
    print("Language: ")
    print(missingValuesCount('Language', movies))
    print("Released: ")
    print(missingValuesCount('Released', movies))
    print("Runtime: ")
    print(missingValuesCount('Runtime', movies))
    print("Title: ")
    print(missingValuesCount('Title', movies))
    print("Year: ")
    print(missingValuesCount('Year', movies))
    print("imdbID: ")
    print(missingValuesCount('imdbID', movies))
    print("imdbRating: ")
    print(missingValuesCount('imdbRating', movies))
    print("imdbVotes: ")
    print(missingValuesCount('imdbVotes', movies))

    # Actors,imdbID
    print("Actors")
    print("Actors: ")
    print(missingValuesCount('Actors', actors))
    print("Director: ")
    print(missingValuesCount('imdbID', actors))


    # Genre,imdbID
    print("Genre: ")
    print(missingValuesCount('Genre', genre))
    print("imdbID: ")
    print(missingValuesCount('imdbID', genre))


    # Person,Responsibility,imdbID
    print("Person: ")
    print(missingValuesCount('Person', writer))
    print("Responsibility: ")
    print(missingValuesCount('Responsibility', writer))
    print("imdbID: ")
    print(missingValuesCount('imdbID', writer))


    movies = movies[movies['Year'].notnull()].reset_index()

    genre['Genre'] = genre['Genre'].apply(lambda x: x.strip())

    # clean Year column
    variable_types = {}
    for year in movies['Year']:
        if type(year) != int:
            invalid_type = type(year).__name__
            if invalid_type in variable_types.keys():
                if year not in variable_types[invalid_type]:
                    variable_types[invalid_type].append(year)
            else:
                variable_types[invalid_type] = []
                variable_types[invalid_type].append(year)

    movies['Year'] = movies['Year'].apply(
        lambda x: int(str(x).split(".")[0]) if type(x) == float else x)
    movies['Year'] = movies['Year'].apply(
        lambda x: x.split("–")[0] if type(x) is str else x)
    movies['Year'] = movies['Year'].apply(lambda x: int(x) if type(x) != int else x)

    # Movies_Genre = pd.merge(Movies, Genre, on='imdbID')

    movies = movies[(movies['Year'] >= 1990) & (movies['Year'] <= 2016)]

    #movies = movies[movies['Runtime'].notnull()]
    movies = movies[movies['imdbRating'].notnull()]

    print("Runtime")
    runtime = []
    for row in movies['Runtime']:
        movie_runtime = 0
        if pd.isna(row):
            runtime.append(np.nan)
            continue
        elif 'h' in row:
            hours, minutes = row.split("h")
            if "min" in minutes.strip():
                minutes, seconds = minutes.strip().split("min")
                movie_runtime = movie_runtime + int(hours) * 60 + int(minutes)
        elif "min" in row.strip():
            minutes, seconds = row.strip().split("min")
            if "," in minutes:
                minutes = minutes.replace(",", "")
            movie_runtime = int(float(minutes))
        runtime.append(movie_runtime)

    movies['Runtime'] = runtime

    rating = []
    for row in additionalRatings['Rating']:
        if "%" in row:
            rating.append(float(row.replace('%', '')) / 100)
        if "/" in row:
            x,y = row.split("/")
            rating.append(float(x) / float(y))


    ratingSourceClass=[]
    for row in additionalRatings['RatingSource']:
        if "Internet" in row:
            ratingSourceClass.append(2)
        elif "Rotten" in row:
            ratingSourceClass.append(0)
        elif "Metacritic" in row:
            ratingSourceClass.append(1)



    additionalRatings['RatingSourceClass'] = ratingSourceClass
    additionalRatings['Parsed_rating'] = rating
    # Dump modified csv files
    print("Writing data")
    movies.to_csv("data/movies.csv", index=False)
    genre.to_csv("data/genres.csv", index=False)
    actors.to_csv("data/actors.csv", index=False)
    writer.to_csv("data/writers.csv", index=False)
    additionalRatings.to_csv("data/additional_ratings.csv")


if __name__ == '__main__':
    main()
