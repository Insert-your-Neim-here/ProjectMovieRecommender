from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = None

def _get_model():
    global _model
    if _model is None:
        # Model loads ONLY when first needed
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_text(text: str) -> list[float]:
    model = _get_model()
    vec = model.encode([text], normalize_embeddings=True)[0]
    return vec.tolist()
# def embed_text(text: str) -> list[float]:
#     return [0.0] * 384

