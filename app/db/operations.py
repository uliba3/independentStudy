from app.db.schema import IndependentStudy, VectorEmbedding
from app.db.session import session
from sqlalchemy import func, or_
from app.utils.googleGenai import embed

def add_independent_study(data):
    if not is_exists(IndependentStudy, {'url': data['url']}):
        new_publication = IndependentStudy(
            title=data.pop('title', None),
            url=data.pop('url', None),
            downloads=data.pop('downloads', None),
            abstract=data.pop('abstract', None),
            advisor=data.pop('advisor1', None),
            department=data.pop('subject_area', []),
            disciplines=data.pop('bp_categories', []),
            keywords=data.pop('keywords', []),
            year=data.pop('year', None),
            downloadLink=data.pop('downloadLink', None),
            citations=data.pop('citations', None)
        )
        session.add(new_publication)
        session.commit()
        print(f"Added new independent study: {new_publication.title}")
    else:
        print(f"Independent study already exists: {data.get('title')}")

def add_vector_embedding(independent_study_id, text_type, embedding, original_text):
    if not is_exists(VectorEmbedding, {'independent_study_id': independent_study_id, 'original_text': original_text}):
        new_embedding = VectorEmbedding(
            independent_study_id=independent_study_id,
            text_type=text_type,
            embedding=embedding,
            original_text=original_text
        )
        session.add(new_embedding)
        session.commit()
        print(f"Added new vector embedding: {independent_study_id}, {original_text}")
    else:
        print(f"Vector embedding already exists: {independent_study_id}, {original_text}")

def get_all(name):
    return session.query(name).all()

def get_by_id(name, id):
    return session.query(name).get(id)

def get_all_by_field(name, field_value_map):
    query = session.query(name)
    for field, value in field_value_map.items():
        query = query.filter(getattr(name, field) == value)
    return query.all()

def is_exists(name, field_value_map):
    return len(get_all_by_field(name, field_value_map)) > 0

def get_nearest_neighbors(embedding, k, publication_type_id=None):
    subquery = (
        session.query(
            VectorEmbedding.independent_study_id,
            func.min(VectorEmbedding.embedding.cosine_distance(embedding)).label('min_distance')
        )
        .group_by(VectorEmbedding.independent_study_id)
        .subquery()
    )

    query = (
        session.query(VectorEmbedding, IndependentStudy)
        .join(IndependentStudy)
        .join(subquery, VectorEmbedding.independent_study_id == subquery.c.independent_study_id)
        .filter(VectorEmbedding.embedding.cosine_distance(embedding) == subquery.c.min_distance)
        .order_by(subquery.c.min_distance)
    )

    if publication_type_id is not None:
        query = query.filter(IndependentStudy.publication_type_id == publication_type_id)

    return query.limit(k).all()

if __name__ == "__main__":
    print(get_nearest_neighbors(embed("African Art"), 3)[0][1].title)
    session.commit()
    session.close()
