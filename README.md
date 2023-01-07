# Movies API

This is a simple API for managing a list of movies. It was built using FastAPI and can be run using Docker.

## Running the API

To run the API, you will need to have Docker and Docker Compose installed on your machine.

First, clone the repository:

```bash
git clone https://github.com/example/movies-api.git
cd movies-api
```

Next, build the Docker image and start the container using Docker Compose:

```bash
docker-compose up --build
```

This will build the image using the Dockerfile and start the container. The --build flag forces Docker Compose to rebuild the image if it has changed since the last build.

Once the container is running, the API will be available at http://localhost:80.

## Endpoints

The API has the following endpoints:

- GET /v1/movies: Returns a list of movies.
- POST /v1/movies: Adds a new movie to the list.
- GET /v1/movies/{id}: Returns a specific movie.
- PUT /v1/movies/{id}: Updates a specific movie.
- DELETE /v1/movies/{id}: Deletes a specific movie.

## Shutting Down

To stop the container, use the following command:

```bash
docker-compose down
```

This will stop the container and remove it. If you want to keep the data in the container's database, you can use the --volumes flag to preserve the data volume:

```bash
docker-compose down --volumes
```
