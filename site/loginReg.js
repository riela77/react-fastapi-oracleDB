import React, { useEffect, useRef, useState } from "react";
import axios from "axios";

const LoginReg = () => {
  const [userList, setUserList] = useState([]);
  const profileInput = useRef();

  const [user, setUser] = useState({
    userid: "",
    userpw: "",
    profile: null,
  });

  const [regResult, setRegResult] = useState({});

  const changeUser = (e) => {
    const { name, value, files } = e.target;
    if (name === "profile") {
      setUser({ ...user, profile: files[0] }); 
    } else {
      setUser({ ...user, [name]: value });
    }
  };

  // DB에서 사용자 정보 불러오기 
  useEffect(
    () => {
      axios.get(`http://localhost:5678/user.get`)
      // res: 서버로부터 받은 응답 객체 그 자체 
      .then((res) => {
        // res.data는 객체안에 있는 데이터이고
        // res.data.users 는 서버에서 불러온 dict형태의 데이터 중에 키값이 users인 데이터를 이르는 말
      const fixedUsers = res.data.users.map(user => ({
        id: user.user_id,
        pw: user.user_pw,
        profile: user.user_pf, // 이미 완성된 URL 형태로 되어 있음
      }));
      setUserList(fixedUsers);
    });
}, []);      


  const regUser = () => {
    const formData = new FormData();
    formData.append("userid", user.userid);
    formData.append("userpw", user.userpw);
    formData.append("profile", user.profile); 

    axios
      .post("http://localhost:5678/user.reg", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true,
      })
      .then((res) => {
        setRegResult(res.data);
        setUser({ userid: "", userpw: "", profile: null });
        profileInput.current.value = ""; // 파일 input 초기화

        // 성공시 userList에 새 id 추가
        if (res.data.result === "성공") {
  setUserList((prev) => [
    ...prev,
    {
      id: res.data.id,
      pw: res.data.pw,
      profile: `http://localhost:5678/user.profile.get?filename=${res.data.profile}`,
    },
  ]);
}

      })
      .catch((err) => {
        console.error("등록 실패:", err);
      });
  };

  return (
    <>
      <h3>회원 등록</h3>
      <label>
        아이디: <input name="userid" value={user.userid} onChange={changeUser} />
      </label>
      <br />
      <label>
        비밀번호: <input name="userpw" value={user.userpw} onChange={changeUser} />
      </label>
      <br />
      <label>
        프로필 사진:{" "}
        <input
          ref={profileInput}
          type="file"
          name="profile"
          onChange={changeUser}
          accept="image/*"
        />
      </label>
      <br />
      <button onClick={regUser}>등록</button>
      <hr />
      <h4>결과</h4>
  
    <p>등록 결과: {regResult.result}</p>
    <p>아이디: {regResult.userid}</p>

    {regResult.profile && (
      <>
        <img
          src={`http://localhost:5678/user.profile.get?filename=${regResult.profile}`}
          alt="등록된 프로필"
          style={{ width: "200px", marginTop: "10px", borderRadius: "10px" }}
        />
        <br />
        <a
          href={`http://localhost:5678/user.profile.get?filename=${regResult.profile}`}
          download
        >
          이미지 다운로드
        </a>
    
      </>
    )}
     <hr />
      <h4>사용자 목록</h4>
      <table border="1" cellPadding="8" cellSpacing="0" style={{ width: "100%", textAlign: "center" }}>
        <thead>
          <tr>
            <th>프로필 사진</th>
            <th>아이디</th>
            <th>비밀번호</th>
          </tr>
        </thead>
        <tbody>
  {userList.map((user, i) => (
  <tr key={i}>
    <td>
      <img
        src={user.profile}
        alt="프로필"
        style={{ width: "80px", borderRadius: "8px" }}
      />
    </td>
    <td>{user.id}</td>
    <td>{user.pw}</td>
  </tr>
))}

</tbody>

      </table>
    </>
  );
};

export default LoginReg;
