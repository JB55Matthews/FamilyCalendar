import React, { useState } from "react"
import { useNavigate } from "react-router-dom";

function Login(){
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async() => {
        setError(null);

        const query = `
        query($email: String!, $password: String!) {
            idByFamilyLogin(email: $email, password: $password){
                id
            }
        }`;

        try{
            const response = await fetch("http://localhost:5000/graphql", {
                method: "POST", 
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({query, variables: {email, password}})
            });

            const json = await response.json();
            if(json.data.idByFamilyLogin){
                const id = json.data.idByFamilyLogin.id
                navigate("/homepage/${id}")
            } else {
                setError("Invalid email or password")
            }
        } catch (err) {
            setError("Internal error: " + err.message)
        }
    };


    return(
        <div>
            <div className="topLabel">Family Login</div>
            <div className="label">Email</div>
            <input
                type="text"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <div className="label">Password</div>
            <input
                type="text"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>

            <button onClick={() => navigate("/register")}>Register</button>

            {error && <p style={{ color: "red" }}>{error}</p>}

        </div>
    )
}

export default Login