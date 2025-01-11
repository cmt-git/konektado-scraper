import requests
from fastapi import FastAPI
from mongodb import GetFromMongoDB
import uvicorn


app = FastAPI()


@app.get("/scrape")
async def scrape_get():
    try:
        current_items = GetFromMongoDB()  # Call your MongoDB function
        filtered_items = [
            {
                **i,  # Unpack existing dictionary
                "_id": str(i["_id"]),  # Convert '_id' to string
            }
            for i in current_items
        ]
        # print(current_items)  # Debugging output
        return {"data": filtered_items}  # Return data as a JSON response
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": "An error occurred while fetching data from MongoDB"}
