# run_query.py

from app.search_engine import search_query

query = input("Ask something about the PDF: ")
result = search_query(query)

print("\n🔍 Top Match:")
print("Page:", result.get("page"))
print("Text:", result.get("text"))

if result.get("images"):
    print("Linked images:", result["images"])
