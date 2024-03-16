import datetime
import secrets
from typing import Union, Annotated, List
import uuid

import repository.db as db
import model.saved_file as SF
from model.user import User
from schema.user_schema import UserCreate, UserLogin, Token

from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session


db.Base.metadata.create_all(bind=db.engine)
app = FastAPI()


security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/ping")
def get_ping():
    return {"ping": datetime.datetime.now()}


class UploadFilesModel(BaseModel):
    year: str
    documentNames: list[UploadFile]
    documentUrls: list[str]

    def download_files(self):
        for x in zip(self.documentNames, self.documentUrls):
            pass


@app.post("/esgreports/upload")
def upload_files(
    documentName: Annotated[list[UploadFile], File()],
    DocumentURL: Annotated[list[str], Form()],
    year: Annotated[str, Form()],
    db: Session = Depends(db.get_db),
    user: str = Depends(get_current_username),
):
    print(documentName)
    DocumentURL = DocumentURL[0].split(",")
    print(DocumentURL)

    trackerid = str(uuid.uuid4())
    for file, url in zip(documentName, DocumentURL):
        with open(file.filename, "wb") as out_file:
            content = file.file.read()
            out_file.write(content)
            SF.create_savedfile(
                db, year, file.filename, url, "training", user, trackerid
            )

    return {"status": "success", "message": "uploaded files", "trackerid": trackerid}


class ReportYear(BaseModel):
    year: str


@app.post("/esgreports/retrieve")
def retrieve_files(
    report_year: ReportYear,
    db: Session = Depends(db.get_db),
    user: str = Depends(get_current_username),
):
    files = SF.get_savedfile(db, report_year.year, user)
    return {"files": files}


class Metadata(BaseModel):
    generateReportForYear: str
    userId: str


@app.post("/questionnaire/generatefirstdraft/pdf")
def generate_first_draft(
    SurveyQuestionnaireDocument: Annotated[UploadFile, File()],
    documentType: str,
    metadata: Metadata,
):
    with open(SurveyQuestionnaireDocument.filename, "wb") as out_file:
        content = SurveyQuestionnaireDocument.file.read()
        out_file.write(content)

    return {"taskid": "x", "status": "success", "createdAt": datetime.datetime.now()}


@app.get("/questionnaire/generatefirstdraft/pdf/{reportYear}/{TaskId}/status")
def get_draft_status():
    return {"taskid": "taskid", "status": "success", "created": datetime.datetime.now()}


@app.get("/firstdraftreport/download/result/{reportYear}")
def get_draft_report():
    return {"file": "ok"}


class QuestionAnswer(BaseModel):
    reportYear: str
    inputQuestion: str


class QuestionAnswerResult(BaseModel):
    reportYear: str


@app.post("/questionnaire/generatefirstdraft/generateAnswer")
def question_answer(question: QuestionAnswer):
    return {
        "reportYear": question.reportYear,
        "questionnaireSummary": {
            "response": "hahah",
            "status": "success",
            "citation": "this page",
            "documentRef": "page 1",
            "accuracy": "0.8",
            "confidence": "0.8",
        },
    }


@app.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(db.get_db)):
    user = User(username=user_data.username)
    user.hash_password(user_data.password)
    db.add(user)
    db.commit()
    return {"message": "User has been created"}


@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(db.get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, default="Invalid Credentials")
    token = user.generate_token()
    return Token(access_token=token, token_type="bearer")
