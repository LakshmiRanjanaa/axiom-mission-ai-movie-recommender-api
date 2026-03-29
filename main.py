from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Movie Recommender API",
    description="Get movie recommendations based on semantic similarity using AI",
    version="1.0.0"
)

# Load pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Global variables for movie data and embeddings
movies_df = None
movie_embeddings = None

class MovieQuery(BaseModel):
    description: str
    top_k: int = 5

class MovieRecommendation(BaseModel):
    title: str
    year: int
    genre: str
    description: str
    similarity_score: float

@app.on_event("startup")
async def load_data():
    """Load movie data and compute embeddings on startup"""
    global movies_df, movie_embeddings
    
    # Load sample movie dataset
    movies_df = pd.read_csv('movies_dataset.csv')
    
    # Generate embeddings for all movie descriptions
    descriptions = movies_df['description'].tolist()
    movie_embeddings = model.encode(descriptions)
    
    print(f"Loaded {len(movies_df)} movies and computed embeddings")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Movie Recommender API is running!"}

@app.get("/movies/count")
async def get_movie_count():
    """Get total number of movies in database"""
    return {"total_movies": len(movies_df)}

@app.post("/recommend", response_model=List[MovieRecommendation])
async def recommend_movies(query: MovieQuery):
    """Get movie recommendations based on description similarity"""
    try:
        # Encode the input description
        query_embedding = model.encode([query.description])
        
        # Calculate cosine similarity with all movies
        similarities = cosine_similarity(query_embedding, movie_embeddings)[0]
        
        # Get top-k most similar movies
        top_indices = np.argsort(similarities)[::-1][:query.top_k]
        
        recommendations = []
        for idx in top_indices:
            movie = movies_df.iloc[idx]
            recommendations.append(MovieRecommendation(
                title=movie['title'],
                year=int(movie['year']),
                genre=movie['genre'],
                description=movie['description'],
                similarity_score=float(similarities[idx])
            ))
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)