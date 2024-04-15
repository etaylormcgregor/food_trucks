# San Francisco Food Trucks

A web app that displays a searchable list of SF food truck permits.

### Implementation

The app is implemented using Flask with a SQLite database. Flask is a simple, light-weight web framework perfect for getting small projects off the ground quickly, which is why I chose it for this project. Similarly, SQLite is a simple, light-weight database that works well for simple apps. The frontend is HTML, and I used SQLAlchemy as an ORM.

To calculate the nearest 5 food trucks to a set of coordinates, I ordered the trucks by their [Haversine distance](https://en.wikipedia.org/wiki/Haversine_formula) from the user-inputed coordinates and chose the top 5.

### Critique

#### If I had more time
1) Add automated tests
2) Refactor the backend to make the API RESTful and therefore useful outside the context of this web app
3) Refactor to make the app more easily extendable (for example: adding the functionality to finnd the 5 closest food trucks to a given address vs. coordinates)
4) Improve the styling of the UI / use React

#### Trade-offs
The main trade-off I made was simplicity for the sake of speed. Flask, SQLite, and HTML would not be my choice for a production application, but they're great tools for simple apps or personal projects.

#### What I left out
I didn't implement automated testing.

#### What are the problems with the implementation
If the app were to all of a sudden receive a lot of traffic my main concern would be how many database calls the app is making. The required functionality could all be implemented on the frontend much more efficiently, especially given the size of the data. Querying the database for every search is not an efficient design.

### How to run the app

```
docker build -t app .
docker run -p 5000:5000 app
```
