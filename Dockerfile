FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /code

# Copy the current directory contents into the container at /app
COPY . /code

# Install poetry
RUN python3 -m pip install poetry
RUN poetry config virtualenvs.create false

# Install dependencies using poetry
RUN poetry install --no-dev

# Expose the FastAPI port
EXPOSE 80

# Run the FastAPI application
CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "80"]