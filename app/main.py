import sys
import os

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from app.utils.search_functions import explain_search_results, create_search_query, search_similar_publications

app = FastAPI()

def search(query):
    title = create_search_query(query)
    similar_publications = search_similar_publications(title)
    explanation = explain_search_results(query, similar_publications)
    return {"similar_publications": similar_publications, "explanation": explanation, "search_title": title}

@app.get("/search")
async def search_endpoint(query: str):
    try:
        result = search(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
