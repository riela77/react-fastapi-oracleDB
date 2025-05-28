from fastapi import FastAPI, Form, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from usersDB.userDAO import userDAO
from fastapi import Query
from fastapi.responses import FileResponse
from usersDB.userManager import userManager
import os

userM=userManager()
app = FastAPI()
userD=userDAO()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB연결 확인용
@app.get("/te.st")
def test():
    h={"Access-Control-Allow-Origin":"*"}
    return userD.test_connection()

# DB에서 등록된 사람 불러오기 
@app.get("/user.get")
def userGet():
    return userD.get()

# 사용자 등록 아직 DB연결하기 전
@app.post("/user.regfirst")
async def user_register(
    userid: str = Form(...),
    userpw: str = Form(...),
    profile: UploadFile = File(...),
):
    return await userM.profileUpload(profile, userid, userpw)

@app.post("/user.reg")
async def user_register(
    userid: str = Form(...),
    userpw: str = Form(...),
    profile: UploadFile = File(...)
):
    return await userD.reg(userid, userpw, profile)

IMAGE_FOLDER = os.path.join("usersDB", "image")

# 프로필 이미지 조회 API
@app.get("/user.profile.get")
async def get_profile_image(filename: str = Query(..., description="프로필 이미지 파일명")):
    file_path = os.path.join(IMAGE_FOLDER, filename)

    # 파일이 존재하는지 확인
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="image/png")
