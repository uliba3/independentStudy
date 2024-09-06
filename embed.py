import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

revision = None  # Replace with the specific revision to ensure reproducibility if the model is updated.

model = SentenceTransformer("avsolatorio/GIST-small-Embedding-v0", revision=revision)

def embed(text):
    return model.encode(text, convert_to_tensor=True).tolist()

