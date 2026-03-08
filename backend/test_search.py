from app.core.vector_store import vector_store

def test_search():
    query = "头疼"
    print(f"Searching for: {query}")
    results = vector_store.search(query)
    
    docs = results['documents'][0]
    metas = results['metadatas'][0]
    
    if not docs:
        print("No results found.")
    else:
        for i, (doc, meta) in enumerate(zip(docs, metas)):
            print(f"Result {i+1}:")
            print(f"  Title: {meta.get('title')}")
            print(f"  Text: {doc[:50]}...")

if __name__ == "__main__":
    test_search()
