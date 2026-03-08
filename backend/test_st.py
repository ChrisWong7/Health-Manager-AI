
try:
    print("Importing sentence_transformers...")
    from sentence_transformers import SentenceTransformer
    print("sentence_transformers imported.")
    
    print("Loading model (this might take a while)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded.")
    
    sentences = ["This is an example sentence", "Each sentence is converted"]
    embeddings = model.encode(sentences)
    print(f"Embeddings shape: {embeddings.shape}")
except ImportError:
    print("sentence_transformers not installed.")
except Exception as e:
    print(f"Error: {e}")
