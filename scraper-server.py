import requests
from fastapi import FastAPI

app = FastAPI()


def call_api():
    url = ""

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


@app.get("/scrape")
def read_item(location: str, complaint_type: str, timestamp: str):
    call_api()
    return {"location": location, "complaint": complaint_type, "timestamp": timestamp}
