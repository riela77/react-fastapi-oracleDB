from typing import final
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
from DBconnectLibrary.kimDBmanager import kimDBmanager
import json

# . :같은 파일 안에 있는 다른 파일 import하기
from .userManager import userManager

userM=userManager()

class userDAO:
    def test_connection(self):
        con, cur = None, None
        try:
            con, cur = kimDBmanager.makeConCur("KIMCR/1@195.168.9.126:1521/xe")
            print("✅ 오라클 DB 연결 성공!")
            return {"result": "연결 성공"}
        except Exception as e:
            print("❌ DB 연결 실패:", e)
            return {"result": f"연결 실패: {e}"}
        finally:
            if con and cur:
                kimDBmanager.closeConCur(con, cur)

    def get(self):
        base_url = "http://localhost:5678/user.profile.get?filename="

        con, cur = None, None  # 초기화
        h = {"Access-Control-Allow-Origin": "*"}
        try:
            con, cur = kimDBmanager.makeConCur("KIMCR/1@195.168.9.126:1521/xe")
            sql = "SELECT * FROM may27_siteUsers"
            cur.execute(sql)
            users=[]
            for user_pf,user_id,user_pw in cur:
                users.append(
                    { "user_pf":  base_url + user_pf,"user_id": user_id,"user_pw": user_pw}
                )
            r={"result": "조회 성공","users":users}

            return JSONResponse(r, headers=h)
        except :
            return JSONResponse({"result":"조회 실패"},headers=h)
        
        finally:
            kimDBmanager.closeConCur(con, cur)


    async def reg(self, userid: str = Form(...), userpw: str = Form(...), profile: UploadFile = File(...)):
        try:
            # 1. 프로필 파일 저장
            profile_filename = await userM.profileUploadSecond(profile)

            # 2. DB 연결 및 저장
            con, cur = kimDBmanager.makeConCur("KIMCR/1@195.168.9.126:1521/xe")
            sql = "INSERT INTO may27_siteUsers (user_id, user_pw, user_pf) VALUES (:2, :3, :1)"
            cur.execute(sql, (userid, userpw, profile_filename))
            con.commit()
            cur.close()

            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
            }
            return JSONResponse({
                "result": "성공",
                "id": userid,
                "pw": userpw,
                "profile": profile_filename
            }, headers=headers)

        except Exception as e:
            print("DB 저장 실패:", e)
            return JSONResponse({
                "result": "실패",
                "reason": str(e)
            }, status_code=500)