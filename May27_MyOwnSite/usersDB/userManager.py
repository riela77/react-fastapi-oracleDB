import os
from fastapi import UploadFile
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime

class userManager:
    def __init__(self):
        self.imageFolder = "./usersDB/image/"
        if not os.path.exists(self.imageFolder):
            os.makedirs(self.imageFolder)  # 폴더 없으면 자동 생성

    def getIcon(self, profile):
        return FileResponse(self.imageFolder + profile, filename=profile)
        
	# profile 파일 업로드로 받음 (UploadFile 타입).
    async def profileUpload(self, profile: UploadFile, userid: str, userpw: str):
    	# 현재 시간을 문자열로 변환해서 파일이름에 추가 (파일 중복 방지파일 중복 방지)
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        # 파일의 바이너리 내용을 비동기로 읽음 
        content = await profile.read()

        ext = os.path.splitext(profile.filename)[1]  # 확장자 추출
        fileName = f"{os.path.splitext(profile.filename)[0]}_{now}{ext}"

        with open(self.imageFolder + fileName, "wb") as f:
            f.write(content)

        result = {
            "result": "성공",
            "userid": userid,
            "userpw": userpw,
            "profile": fileName,
        }
        headers = {
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true",
        }
        return JSONResponse(result, headers=headers)
    
    async def profileUploadSecond(self, profile):
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        content = await profile.read()

        ext = os.path.splitext(profile.filename)[1]
        fileName = f"{os.path.splitext(profile.filename)[0]}_{now}{ext}"

        full_path = os.path.join(self.imageFolder, fileName)
        with open(full_path, "wb") as f:
            f.write(content)

        return fileName