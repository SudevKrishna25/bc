from fastapi import FastAPI, HTTPException
import logging

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Sample mock test data
mock_tests = [
    {"id": 1, "title": "Physics: Mechanics & Waves", "level": "Intermediate", "questions": 30, "time": "45 Minutes"},
    {"id": 2, "title": "Chemistry: Organic Compounds", "level": "Advanced", "questions": 35, "time": "50 Minutes"},
    {"id": 3, "title": "Biology: Cell Structure & Function", "level": "Beginner", "questions": 25, "time": "40 Minutes"},
    {"id": 4, "title": "Mathematics: Calculus Fundamentals", "level": "Intermediate", "questions": 20, "time": "45 Minutes"},
]

# Root endpoint
@app.get("/")
def home():
    return {"message": "FastAPI Mock Test Backend Running!"}

# Get all mock tests
@app.get("/tests")
def get_tests():
    return {"tests": mock_tests}

# Get a specific test by ID
@app.get("/tests/{test_id}")
def get_test(test_id: int):
    test = next((t for t in mock_tests if t["id"] == test_id), None)
    if test is None:
        logging.error(f"404 Error: Test with ID {test_id} not found")
        raise HTTPException(status_code=404, detail="Test not found")
    return test

# 404 Error handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    logging.error(f"404 Error: User attempted to access {request.url}")
    return {"error": "Page not found", "path": str(request.url)}

# Run the server using:
# uvicorn main:app --reload
