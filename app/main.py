from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
import secrets, json, os
from .database import Base, engine, get_db, SessionLocal
from .models import User, Exam, Question, Attempt
from .security import verify_password
from .seed import seed

app=FastAPI(title="ExamFlow API", version="1.0.0", description="Online examination platform API")
Base.metadata.create_all(bind=engine)
with SessionLocal() as db: seed(db)
TOKENS={}
class LoginIn(BaseModel):
    email:str
    password:str
class ExamCreate(BaseModel):
    title:str=Field(min_length=3,max_length=180)
    subject:str=Field(min_length=2,max_length=100)
    description:str=""
    duration_minutes:int=Field(default=15,ge=1,le=240)
    questions:list[dict]=Field(min_length=5)
class ExamPatch(BaseModel):
    is_published:Optional[bool]=None
class SubmitIn(BaseModel):
    answers:dict[str,str]
def current_user(authorization:str|None=Header(default=None), db:Session=Depends(get_db)):
    token=authorization.removeprefix("Bearer ").strip() if authorization else ""
    uid=TOKENS.get(token)
    user=db.get(User,uid) if uid else None
    if not user: raise HTTPException(401,"Please log in to continue.")
    return user
def admin(user:User=Depends(current_user)):
    if user.role!="admin": raise HTTPException(403,"Admin access required.")
    return user
def exam_dict(e):
    return {"id":e.id,"title":e.title,"subject":e.subject,"description":e.description,"duration_minutes":e.duration_minutes,"question_count":len(e.questions),"is_published":e.is_published}
@app.get("/api/health")
def health(): return {"status":"ok","service":"ExamFlow"}
@app.post("/api/auth/login")
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=data.email.lower().strip()).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password.")
    token=secrets.token_urlsafe(32); TOKENS[token]=user.id
    return {"token":token,"user":{"id":user.id,"name":user.name,"email":user.email,"role":user.role}}
@app.post("/api/auth/logout")
def logout(authorization:str|None=Header(default=None)):
    token=authorization.removeprefix("Bearer ").strip() if authorization else ""; TOKENS.pop(token,None); return {"message":"Logged out"}
@app.get("/api/auth/me")
def me(user:User=Depends(current_user)): return {"id":user.id,"name":user.name,"email":user.email,"role":user.role}
@app.get("/api/exams")
def exams(user:User=Depends(current_user),db:Session=Depends(get_db)):
    q=db.query(Exam)
    if user.role!="admin": q=q.filter_by(is_published=True)
    return [exam_dict(e) for e in q.order_by(Exam.id)]
@app.get("/api/exams/{exam_id}")
def exam_detail(exam_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    e=db.get(Exam,exam_id)
    if not e or (user.role!="admin" and not e.is_published): raise HTTPException(404,"Exam not found")
    return exam_dict(e)
@app.post("/api/exams/{exam_id}/start")
def start_exam(exam_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    if user.role!="student": raise HTTPException(403,"Only students can start exams.")
    e=db.get(Exam,exam_id)
    if not e or not e.is_published: raise HTTPException(404,"Exam not available.")
    attempt=Attempt(user_id=user.id,exam_id=e.id,total_points=sum(q.points for q in e.questions))
    db.add(attempt); db.commit(); db.refresh(attempt)
    return {"attempt_id":attempt.id,"started_at":attempt.started_at.isoformat(),"duration_minutes":e.duration_minutes,"exam":exam_dict(e)}
@app.get("/api/attempts/{attempt_id}/questions")
def attempt_questions(attempt_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    a=db.get(Attempt,attempt_id)
    if not a or a.user_id!=user.id: raise HTTPException(404,"Attempt not found")
    if a.status!="in_progress": raise HTTPException(409,"This attempt has already been submitted.")
    return [{"id":q.id,"prompt":q.prompt,"options":{"A":q.option_a,"B":q.option_b,"C":q.option_c,"D":q.option_d},"points":q.points} for q in a.exam.questions]
@app.post("/api/attempts/{attempt_id}/submit")
def submit(attempt_id:int,data:SubmitIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    a=db.get(Attempt,attempt_id)
    if not a or a.user_id!=user.id: raise HTTPException(404,"Attempt not found")
    if a.status!="in_progress": raise HTTPException(409,"This attempt has already been submitted.")
    now=datetime.now(timezone.utc)
    started=a.started_at if a.started_at.tzinfo else a.started_at.replace(tzinfo=timezone.utc)
    if (now-started).total_seconds()>a.exam.duration_minutes*60+30: raise HTTPException(408,"Exam time has expired. Please submit before the timer ends.")
    qs=a.exam.questions; score=0
    clean={}
    for q in qs:
        val=data.answers.get(str(q.id),"")
        if val not in ("A","B","C","D"): val=""
        clean[str(q.id)]=val
        if val==q.correct_option: score+=q.points
    a.score=score; a.total_points=sum(q.points for q in qs); a.answers_json=json.dumps(clean); a.status="submitted"; a.submitted_at=now
    db.commit()
    return {"result_id":a.id,"exam_title":a.exam.title,"score":score,"total_points":a.total_points,"percentage":round(score/a.total_points*100,1) if a.total_points else 0,"submitted_at":now.isoformat()}
@app.get("/api/results")
def results(user:User=Depends(current_user),db:Session=Depends(get_db)):
    q=db.query(Attempt).filter_by(status="submitted")
    if user.role!="admin": q=q.filter_by(user_id=user.id)
    return [{"id":a.id,"exam_id":a.exam_id,"exam_title":a.exam.title,"student_name":a.user.name,"student_email":a.user.email,"score":a.score,"total_points":a.total_points,"percentage":round(a.score/a.total_points*100,1) if a.total_points else 0,"submitted_at":a.submitted_at.isoformat() if a.submitted_at else None} for a in q.order_by(desc(Attempt.submitted_at)).all()]
@app.get("/api/results/{result_id}")
def result_detail(result_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    a=db.get(Attempt,result_id)
    if not a or a.status!="submitted" or (user.role!="admin" and a.user_id!=user.id): raise HTTPException(404,"Result not found")
    answers=json.loads(a.answers_json or "{}")
    return {"id":a.id,"exam_title":a.exam.title,"score":a.score,"total_points":a.total_points,"percentage":round(a.score/a.total_points*100,1) if a.total_points else 0,
    "review":[{"question":q.prompt,"your_answer":answers.get(str(q.id),""),"correct_answer":q.correct_option,"options":{"A":q.option_a,"B":q.option_b,"C":q.option_c,"D":q.option_d},"is_correct":answers.get(str(q.id),"")==q.correct_option} for q in a.exam.questions]}
@app.get("/api/admin/dashboard")
def dashboard(user:User=Depends(admin),db:Session=Depends(get_db)):
    return {"students":db.query(User).filter_by(role="student").count(),"exams":db.query(Exam).count(),"published_exams":db.query(Exam).filter_by(is_published=True).count(),"submissions":db.query(Attempt).filter_by(status="submitted").count(),"recent_results":results(user,db)}
@app.post("/api/admin/exams")
def create_exam(data:ExamCreate,user:User=Depends(admin),db:Session=Depends(get_db)):
    e=Exam(title=data.title,subject=data.subject,description=data.description,duration_minutes=data.duration_minutes,is_published=True); db.add(e); db.flush()
    for item in data.questions:
        if not all(k in item for k in ("prompt","A","B","C","D","correct_option")): raise HTTPException(422,"Each question needs prompt, A, B, C, D and correct_option.")
        if item["correct_option"] not in ("A","B","C","D"): raise HTTPException(422,"correct_option must be A, B, C or D.")
        db.add(Question(exam_id=e.id,prompt=item["prompt"],option_a=item["A"],option_b=item["B"],option_c=item["C"],option_d=item["D"],correct_option=item["correct_option"],points=int(item.get("points",1))))
    db.commit(); db.refresh(e); return exam_dict(e)
@app.patch("/api/admin/exams/{exam_id}")
def patch_exam(exam_id:int,data:ExamPatch,user:User=Depends(admin),db:Session=Depends(get_db)):
    e=db.get(Exam,exam_id)
    if not e: raise HTTPException(404,"Exam not found")
    if data.is_published is not None: e.is_published=data.is_published
    db.commit(); return exam_dict(e)
@app.get("/api/admin/submissions")
def admin_submissions(user:User=Depends(admin),db:Session=Depends(get_db)):
    return results(user,db)
@app.get("/")
def index(): return FileResponse(os.path.join(os.path.dirname(__file__),"static","index.html"))
app.mount("/static",StaticFiles(directory=os.path.join(os.path.dirname(__file__),"static")),name="static")
