# Fampay Backend Assignment

### Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

### Tech Stack Used

* Python 3.8
* FastAPI
* SQLite

### Instructions

Clone the repository to your local machine and then navigate inside the repository.
Once inside the repository, create a Python virtual environment using the terminal

```
python -m venv <virtual-environment-name>
```

Then, activate the virtual environment using

```
source <virtual-environment-name>/bin/activate
```

Install the required dependencies for the project using the included `requirements.txt` file

```
pip install -r requirements.txt
```

Specify the YouTube API keys as well as the search query in the `settings.py` file 

Once all required libraries are installed with valid API keys and search query in the `settings.py` file, the FastAPI server can be run using the command

```
uvicorn main:app --reload
```

Navigate over to `http://127.0.0.1:8000/docs` to view the Swagger UI for the API and to test out the API routes. 

Alternatively, visit `http://127.0.0.1:8000/videos` to fetch all video information from the database or `http://127.0.0.1:8000/search_videos` to search through the database using **title** and **description**

