from app.utils.googleGenai import runModel, embed
from app.db.operations import get_nearest_neighbors

def explain_search_results(query, publications):
    # Format the publications list into a string
    formatted_publications = str(publications)
    
    result = runModel("flash", 
             f"""You are AI search engine for past independent research projects at Wooster. 
             You are given a search query and you are given relevant publications found. 
             Explain the search results in a way that is easy to understand.
             ###
             Search Query: {query}
             Publications:
            {formatted_publications}
             """)
    return result
    
def create_search_query(query):
    result = runModel("flash", 
             f"""You are AI search engine for past independent research projects at Wooster. 
             You are given a search query and you need to find relevant publications. 
             I will do the semantic search so please provide the title for the search query.
             Try to make the title as abstract as possible.
             ###
             Input: I want to find the publications on pesticides in the atmosphere.
             Title: Pesticides in the Atmosphere
             ###
             Input: How do I make a good impression on my interview?
             Title: Interview Preparation
             ###
             Input: Something related to the AI
             Title: Artificial Intelligence
             ###
             Input: {query}
             """)
    return result[6:]

def search_similar_publications(query):
    embedding = embed(query)
    nearest_neighbors = get_nearest_neighbors(embedding, 3)
    return [
        {
            'title': nn[1].title,
            'url': nn[1].url,
            'downloads': nn[1].downloads,
            'abstract': nn[1].abstract,
            'advisor': nn[1].advisor,
            'department': nn[1].department,
            'disciplines': nn[1].disciplines,
            'keywords': nn[1].keywords,
            'year': nn[1].year,
            'citations': nn[1].citations
        }
        for nn in nearest_neighbors
    ]
