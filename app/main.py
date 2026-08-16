from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="PlaceMux Applications & Shortlisting - Task 4")

jobs = {
    1: {
        "id": 1,
        "title": "Python Backend Intern",
        "company": "Demo Company",
        "required_skills": ["python", "fastapi", "sql"],
    },
    2: {
        "id": 2,
        "title": "Data Analyst Intern",
        "company": "Demo Company",
        "required_skills": ["python", "sql", "excel"],
    },
}

students = {
    101: {"id": 101, "name": "Asha", "skills": ["python", "fastapi", "sql", "git"]},
    102: {"id": 102, "name": "Rahul", "skills": ["python", "excel"]},
}

applications = []
shortlisted = []


class Application(BaseModel):
    student_id: int
    job_id: int


class ShortlistRequest(BaseModel):
    application_id: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "applications-shortlisting"}


@app.get("/jobs")
def list_jobs():
    return list(jobs.values())


@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


@app.post("/applications", status_code=201)
def apply(application: Application):
    if application.student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if application.job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[application.job_id]
    student = students[application.student_id]
    required = set(job["required_skills"])
    available = set(student["skills"])
    meets_threshold = required.issubset(available)

    record = {
        "id": len(applications) + 1,
        "student_id": application.student_id,
        "job_id": application.job_id,
        "status": "eligible" if meets_threshold else "below_skill_threshold",
        "meets_skill_threshold": meets_threshold,
    }
    applications.append(record)
    return record


@app.get("/companies/applications")
def company_applications():
    return applications


@app.post("/companies/shortlist")
def shortlist(request: ShortlistRequest):
    matching = [item for item in applications if item["id"] == request.application_id]
    if not matching:
        raise HTTPException(status_code=404, detail="Application not found")

    application = matching[0]
    if not application["meets_skill_threshold"]:
        raise HTTPException(
            status_code=400,
            detail="Candidate is below the required skill threshold",
        )

    if application["id"] not in shortlisted:
        shortlisted.append(application["id"])

    return {"application_id": application["id"], "status": "shortlisted"}
