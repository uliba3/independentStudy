from sqlalchemy import MetaData, Table, Column, Integer, Float, String, ARRAY, Date, ForeignKey, create_engine, Enum
from sqlalchemy.dialects.postgresql import JSONB, ARRAY as PG_ARRAY
from sqlalchemy_schemadisplay import create_schema_graph

metadata = MetaData()

publication_type = Table('publication_type', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('schema_name', String),
    Column('url', String)
)

publication = Table('publication', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('publication_type_id', Integer, ForeignKey('publication_type.id'), nullable=False),
    Column('url', String),
    Column('downloads', Integer),
    Column('details', JSONB)
)

vector_embedding = Table('vector_embedding', metadata,
    Column('id', Integer, primary_key=True),
    Column('publication_id', Integer, ForeignKey('publication.id')),
    Column('text_type', String, nullable=False),
    Column('embedding', PG_ARRAY(Float, dimensions=1), nullable=False),
    Column('original_text', String, nullable=False)
)

# Create an engine (replace with your actual database URL)
engine = create_engine('sqlite://')

# Create the graph
graph = create_schema_graph(metadata=metadata,
    show_datatypes=True,
    show_indexes=False,
    rankdir='LR',
    concentrate=False,
    engine=engine
)

# Output the graph
graph.write_png('database_diagram.png')