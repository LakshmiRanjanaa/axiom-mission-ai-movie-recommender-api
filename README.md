# AI Movie Recommender API

A FastAPI-powered movie recommendation system that uses AI to find similar movies based on semantic similarity of plot descriptions.

## Features

- 🤖 **AI-Powered**: Uses sentence-transformers for semantic text analysis
- 🚀 **Fast API**: Built with FastAPI for high performance
- 📊 **Similarity Scoring**: Returns confidence scores for recommendations
- 📚 **Easy to Extend**: Simple CSV-based movie database
- 🔧 **Production Ready**: Includes error handling and API documentation

## Quick Start

### 1. Install Dependencies
bash
pip install -r requirements.txt


### 2. Start the Server
bash
python main.py


The API will be available at `http://localhost:8000`

### 3. View API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation

## API Endpoints

### GET `/`
Health check endpoint

### GET `/movies/count`
Returns the total number of movies in the database

### POST `/recommend`
Get movie recommendations based on description similarity

**Request Body:**

{
  "description": "A space adventure with aliens and technology",
  "top_k": 5
}


**Response:**

[
  {
    "title": "Star Wars",
    "year": 1977,
    "genre": "Sci-Fi",
    "description": "A young farm boy joins a rebellion...",
    "similarity_score": 0.85
  }
]


## Testing

Run the test script to verify everything works:
bash
python test_api.py


## Example Usage

python
import requests

response = requests.post(
    "http://localhost:8000/recommend",
    json={
        "description": "A thriller about dreams and reality",
        "top_k": 3
    }
)

recommendations = response.json()
for movie in recommendations:
    print(f"{movie['title']} - Score: {movie['similarity_score']:.3f}")


## How It Works

1. **Text Embeddings**: Uses sentence-transformers to convert movie descriptions into numerical vectors
2. **Similarity Calculation**: Computes cosine similarity between query and all movie embeddings
3. **Ranking**: Returns top-K most similar movies with confidence scores

## Next Steps

- Add more movies to the dataset
- Implement user ratings and collaborative filtering
- Add genre-based filtering
- Deploy to cloud platforms (AWS, GCP, Azure)
- Add caching for better performance

## Tech Stack

- **FastAPI**: Modern Python web framework
- **sentence-transformers**: Pre-trained NLP models
- **scikit-learn**: Machine learning utilities
- **pandas**: Data manipulation
- **uvicorn**: ASGI server