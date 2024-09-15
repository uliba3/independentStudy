from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python, JavaScript
from diagrams.programming.framework import FastAPI, React
from diagrams.onprem.database import PostgreSQL
from diagrams.custom import Custom

with Diagram("Wooster Research Search Engine Architecture", show=False, filename="docs/architecture.png"):

    frontend = React("Frontend")

    with Cluster("Backend"):
        main = FastAPI("Program")
        with Cluster("Database"):
            db = PostgreSQL("Database")
            vector_db = PostgreSQL("Vector Database")
        gemini1 = Custom("Gemini API", "resources/gemini.png")
        gemini2 = Custom("Gemini API", "resources/gemini.png")
        
    with Cluster("Web Scraping"):
        internet = Custom("openworks.wooster.edu", "resources/internet.jpg")
    
    internet >> Edge(label="0. Web Scrape and save to database") << db
    frontend >> Edge(label="1. User Query") >> main >> Edge(label="5. Return Results") >> frontend
    gemini1 >> Edge(label="2. Generate IS title based on user query") << main
    main >> Edge(label="3. Vector Search using the generated IS title") << vector_db
    gemini2 >> Edge(label="4. Generate IS description based on results") << main
    db >> Edge(style="dotted") << vector_db