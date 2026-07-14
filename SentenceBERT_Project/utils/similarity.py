from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similarity(student_answer, reference_answer):
    # Generate embeddings
    student_embedding = model.encode([student_answer])
    reference_embedding = model.encode([reference_answer])

    # Compute cosine similarity
    similarity = cosine_similarity(
        student_embedding,
        reference_embedding
    )[0][0]

    # Normalize score to 0–100
    normalized_score = ((similarity + 1) / 2) * 100

    return round(similarity, 4), round(normalized_score, 2)