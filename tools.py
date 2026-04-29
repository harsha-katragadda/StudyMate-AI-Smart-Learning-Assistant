from memory_store import search_memory

def search_notes(query):
    results = search_memory(query)

    if not results:
        return ["No data available"]

    return results

def generate_quiz(text):
    if not text:
        return "No data available"

    return f"""
Q1: What is the system about?
Answer: It is an online platform connecting customers with restaurants.

Q2: What problem does it solve?
Answer: It reduces manual errors and improves efficiency.

Q3: Name one feature.
Answer: Real-time order tracking.

Q4: Which backend is used?
Answer: FastAPI.
"""