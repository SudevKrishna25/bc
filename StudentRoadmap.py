from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date
import uuid

app = FastAPI()

# Data Models
class RoadmapRequest(BaseModel):
    exam_type: str
    subjects: List[str]
    start_date: date
    end_date: date
    study_pace: str

    @validator("subjects")
    def validate_subjects(cls, v):
        if not v:
            raise ValueError("At least one subject must be selected.")
        return v

    @validator("study_pace")
    def validate_study_pace(cls, v):
        if v not in ["intensive", "balanced", "relaxed"]:
            raise ValueError("Invalid study pace.")
        return v

class Task(BaseModel):
    id: str
    title: str
    completed: bool
    duration: str
    type: str

class Week(BaseModel):
    week: int
    focus: str
    tasks: List[Task]

class RoadmapResponse(BaseModel):
    roadmap_id: str
    exam_type: str
    subjects: List[str]
    start_date: date
    end_date: date
    study_pace: str
    weeks: List[Week]

# Mock Data
AVAILABLE_SUBJECTS = ["Physics", "Chemistry", "Biology", "Mathematics", "English"]
STUDY_PACE_OPTIONS = [
    {"value": "intensive", "label": "Intensive"},
    {"value": "balanced", "label": "Balanced"},
    {"value": "relaxed", "label": "Relaxed"},
]

# Helper Functions
def generate_tasks(subject: str, week: int) -> List[Task]:
    """Generate tasks for a given subject and week."""
    tasks = []
    if subject == "Physics":
        tasks = [
            {"id": str(uuid.uuid4()), "title": f"Study Newton's Laws of Motion (Week {week})", "completed": False, "duration": "3 hours", "type": "study"},
            {"id": str(uuid.uuid4()), "title": f"Practice problems on Force and Motion (Week {week})", "completed": False, "duration": "2 hours", "type": "practice"},
        ]
    elif subject == "Chemistry":
        tasks = [
            {"id": str(uuid.uuid4()), "title": f"Study Atomic Models and Theories (Week {week})", "completed": False, "duration": "3 hours", "type": "study"},
            {"id": str(uuid.uuid4()), "title": f"Practice Electronic Configuration Problems (Week {week})", "completed": False, "duration": "2 hours", "type": "practice"},
        ]
    elif subject == "Biology":
        tasks = [
            {"id": str(uuid.uuid4()), "title": f"Study Cell Structure and Organelles (Week {week})", "completed": False, "duration": "4 hours", "type": "study"},
            {"id": str(uuid.uuid4()), "title": f"Review Cell Division Process (Week {week})", "completed": False, "duration": "2 hours", "type": "review"},
        ]
    return tasks

def generate_roadmap(request: RoadmapRequest) -> RoadmapResponse:
    """Generate a study roadmap based on the request."""
    roadmap_id = str(uuid.uuid4())
    weeks = []

    for week in range(1, 5):  # 4-week roadmap
        focus = f"Week {week}: Revision and Practice"
        tasks = []
        for subject in request.subjects:
            tasks.extend(generate_tasks(subject, week))
        weeks.append({"week": week, "focus": focus, "tasks": tasks})

    return RoadmapResponse(
        roadmap_id=roadmap_id,
        exam_type=request.exam_type,
        subjects=request.subjects,
        start_date=request.start_date,
        end_date=request.end_date,
        study_pace=request.study_pace,
        weeks=weeks,
    )

# API Endpoints
@app.get("/subjects", response_model=List[str])
def get_subjects():
    """Return a list of available subjects."""
    return AVAILABLE_SUBJECTS

@app.get("/study-pace-options", response_model=List[dict])
def get_study_pace_options():
    """Return a list of study pace options."""
    return STUDY_PACE_OPTIONS

@app.post("/roadmap", response_model=RoadmapResponse)
def create_roadmap(request: RoadmapRequest):
    """Generate a study roadmap based on the provided data."""
    try:
        roadmap = generate_roadmap(request)
        return roadmap
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)