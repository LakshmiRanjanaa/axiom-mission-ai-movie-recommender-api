import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Health Check: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_movie_count():
    """Test getting total movie count"""
    response = requests.get(f"{BASE_URL}/movies/count")
    print(f"Movie Count: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_recommendations():
    """Test movie recommendations"""
    # Test data - different movie descriptions
    test_queries = [
        {
            "description": "A space adventure with aliens and advanced technology",
            "top_k": 3
        },
        {
            "description": "A romantic story about love and loss on a ship",
            "top_k": 3
        },
        {
            "description": "A crime story with mobsters and violence",
            "top_k": 3
        }
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query['description']}")
        response = requests.post(
            f"{BASE_URL}/recommend",
            json=query,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"Found {len(recommendations)} recommendations:")
            for rec in recommendations:
                print(f"  - {rec['title']} ({rec['year']}) - Score: {rec['similarity_score']:.3f}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        print()

if __name__ == "__main__":
    print("Testing AI Movie Recommender API\n")
    print("Make sure the API is running with: python main.py\n")
    
    try:
        test_health_check()
        test_movie_count()
        test_recommendations()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure it's running on localhost:8000")