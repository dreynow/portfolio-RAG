from scripts.database import collection

def test_query(question):
    print(f"\n--- Testing Query: {question} ---")
    
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    
    if not results['documents'][0]:
        print("The librarian found NOTHING. Check your ingestion.")
        return

    for i, doc in enumerate(results['documents'][0]):
        distance = results['distances'][0][i]
        print(f"\n[Chunk {i+1}] (Distance: {distance:.4f})")
        print(f"Content: {doc[:300]}...") 

if __name__ == "__main__":
    test_query("What is Mother's recent job title?")
    test_query("What technical skills are listed?")