# Starter - Casting Agency API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `casting_agency` database:
```bash
createdb casting_agency
```
Populate the database using the `casting_agency.psql` file provided. From the `starter` folder in terminal run:

```bash
psql casting_agency < casting_agency.psql
```

### Run the Server

From within the `./starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.



### Expected endpoints and behaviors

`GET '/actors'`
- Retrieve the list of actors from the database.
- Request Arguments: None
- Returns: An object with a list of actors and the total number of actors.

```json
{
    "actors": [
        {
            "bio": "Japanese actor and filmmaker known for action films.",
            "gender": "Male",
            "id": 1,
            "name": "Takeshi Kitano",
            "nationality": "Japanese",
            "year_of_birth": 1947
        },
        {
            "bio": "Known internationally for her role in Babel.",
            "gender": "Female",
            "id": 2,
            "name": "Rinko Kikuchi",
            "nationality": "Japanese",
            "year_of_birth": 1981
        }
    ],
    "success": true,
    "total_actors": 2
}
```

`POST '/actors'`
- Add information of a new actor to the database.
- Request Arguments: name - string, year_of_birth - integer, gender: string, nationality: string, bio: string

```json
{
    "name": "Tadanobu Asano",
    "year_of_birth": 1973,
    "gender": "Male",
    "nationality": "Japanese",
    "bio": "Tadanobu Asano is a Japanese actor known for his roles in arthouse and international films.'"
}
```
- Returns: An object actor with bio, gender, id, name, nationality, year_of_birth

```json
{
    "actor": {
        "bio": "Tadanobu Asano is a Japanese actor known for his roles in arthouse and international films.'",
        "gender": "Male",
        "id": 14,
        "name": "Tadanobu Asano",
        "nationality": "Japanese",
        "year_of_birth": 1973
    },
    "success": true
}
```

`PATCH '/actors/<int:actor_id>'`
- Edit the information of the actor with the corresponding ID in the database.
- Request Arguments: name - string, year_of_birth - integer, gender: string, nationality: string, bio: string
```json
{
    "name": "Tadanobu Asano",
    "year_of_birth": 1973
}
```
- Returns: An object with the modified information (bio, gender, id, name, nationality, year_of_birth)

```json
{
    "actor": {
        "bio": "Popular actress and singer in Japan.",
        "gender": "Female",
        "id": 10,
        "name": "Tadanobu Asano",
        "nationality": "Japanese",
        "year_of_birth": 1973
    },
    "success": true
}
```

`DELETE '/actors/<int:actor_id>'`
- Delete the record of the actor corresponding to the ID in the database.
- Request Arguments: None
- Returns: An object with 'deleted' as the ID of the deleted actor.

```json
{
    "deleted": 13,
    "success": true
}
```

`GET '/movies`
- Retrieve the list of movies from the database.
- Request Arguments: None
- Returns: An object with a list of movies and the total number of movies.

```json
{
    "movies": [
        {
            "description": "Samurai defend a village from bandits.",
            "genre": "Action, Drama",
            "id": 2,
            "rating": 8.7,
            "title": "Seven Samurai"
        },
        {
            "description": "Two teens switch bodies and lives.",
            "genre": "Animation, Romance",
            "id": 3,
            "rating": 8.4,
            "title": "Your Name"
        }
    ],
    "success": true,
    "total_movies": 2
}
`POST '/movies'`
- Add information of a new movie to the database.
- Request Arguments: title - string, genre - string, gender: string, rating: float, description: string


```json
{
    "title": "Norwegian Wood",
    "genre": "Drama, Romance",
    "rating": 7.4,
    "description": "A beautifully crafted film that follows a young man's emotional struggles following the death of his friend. Based on the novel by Haruki Murakami."
}
```

- Returns: An object movie with description, genre, id, rating, title.
```json
{
    "movie": {
        "description": "A beautifully crafted film that follows a young man's emotional struggles following the death of his friend. Based on the novel by Haruki Murakami.",
        "genre": "Drama, Romance",
        "id": 14,
        "rating": 7.4,
        "title": "Norwegian Wood"
    },
    "success": true
}
```


`PATCH '/movies/<int:movie_id>'`
- Edit the information of the movie with the corresponding ID in the database.
- Request Arguments:(optional) description - string, genre - string, gender: string, rating: float, title: string

```json
{
    "title": "Norwegian Wood",
    "genre": "Drama, Romance",
    "rating": 7.4
}

- Returns: An object with the modified information (description, genre, id, rating, title)

```json
{
    "movie": {
        "description": "A magical adventure in a spirit world.",
        "genre": "Drama, Romance",
        "id": 1,
        "rating": 7.4,
        "title": "Norwegian Wood"
    },
    "success": true
}
```

`DELETE '/movies/<int:movie_id>'`

- Delete the record of the movie corresponding to the ID in the database.
- Request Arguments: None
- Returns: An object with 'deleted' as the ID of the deleted movie.
```json
{
    "deleted": 9,
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb castinig_agency_test
createdb castinig_agency_test
psql castinig_agency_test < trivia.psql
python test_app.py