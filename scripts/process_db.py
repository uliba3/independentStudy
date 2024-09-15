import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.operations import add_independent_study, add_vector_embedding, is_exists, get_all
from app.db.schema import IndependentStudy, VectorEmbedding
from app.category import all_categories
from scripts.webscrape import scrape_openworks_page
from app.utils.googleGenai import embed

def add_all_publications():
    for i in range(1, 10):
        url = f"https://openworks.wooster.edu/independentstudy/{i}/"
        if is_exists(IndependentStudy, {'url': url}):
            print(f"Independent study already exists: {url}")
        else:
            print(f"Independent study does not exist: {url}")
            data = scrape_openworks_page(url)
            print(data)
            if data['status'] == '404':
                continue
            add_independent_study(data)

def add_vector_embedding_title():
    independent_studies = get_all(IndependentStudy)
    for independent_study in independent_studies:
        if independent_study.title is None:
            continue
        print(independent_study.id, independent_study.title)
        if is_exists(VectorEmbedding, {'independent_study_id': independent_study.id, 'original_text': independent_study.title}):
            print(f"Vector embedding already exists: {independent_study.id}, {independent_study.title}")
        else:
            print(f"Vector embedding does not exist: {independent_study.id}, {independent_study.title}")
            embedding = embed(independent_study.title)
            add_vector_embedding(independent_study.id, 'title', embedding, independent_study.title)

def add_vector_embedding_abstract():
    independent_studies = get_all(IndependentStudy)
    for independent_study in independent_studies:
        if independent_study.abstract is None:
            continue
        print(independent_study.id, independent_study.title)
        if is_exists(VectorEmbedding, {'independent_study_id': independent_study.id, 'original_text': independent_study.abstract}):
            print(f"Vector embedding already exists: {independent_study.id}, {independent_study.abstract}")
        else:
            print(f"Vector embedding does not exist: {independent_study.id}, {independent_study.abstract}")
            embedding = embed(independent_study.abstract)
            add_vector_embedding(independent_study.id, 'abstract', embedding, independent_study.abstract)

def add_vector_embedding_keywords():
    independent_studies = get_all(IndependentStudy)
    for independent_study in independent_studies:
        if len(independent_study.keywords) == 0:
            continue
        keywords = ' '.join(independent_study.keywords)
        print(independent_study.id, keywords)
        if is_exists(VectorEmbedding, {'independent_study_id': independent_study.id, 'original_text': keywords}):
            print(f"Vector embedding already exists: {independent_study.id}, {keywords}")
        else:
            print(f"Vector embedding does not exist: {independent_study.id}, {keywords}")
            embedding = embed(keywords)
            add_vector_embedding(independent_study.id, 'keywords', embedding, keywords)

if __name__ == "__main__":
    add_all_publications()
    add_vector_embedding_title()
    add_vector_embedding_abstract()
    add_vector_embedding_keywords()
