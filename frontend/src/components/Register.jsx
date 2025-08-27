import React, { useState } from "react"
import { useNavigate } from "react-router-dom";
import "../../styles/Register.css"

function Register() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleRegister = async() => {
        setError(null);

        const query = `
        mutation($email: String!, $password: String!) {
            createFamily(email: $email, password: $password){
                family{
                    id
                }
                ok
            }
        }`;

        try{
            const response = await fetch("http://localhost:5000/graphql", {
                method: "POST", 
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({query, variables: {email, password}})
            });

            const json = await response.json();
            if(json.data.createFamily.ok){
                const id = json.data.createFamily.family.id
                navigate("/memberspage/${id}")
            } else {
                setError("Email already registered")
            }
        } catch (err) {
            setError("Internal error: " + err.message)
        }
    };


    return(
        <div className="container">
            <div className="topLabel">Family Register</div>
            <br/>
            <div className="inputContainer">
                <div className="label">Email: </div>
                <input
                    type="text"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <br/>
            <div className="inputContainer">
                <div className="label">Password: </div>
                <input
                    type="text"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <br/>
            <div className="inputContainer">
                <button onClick={handleRegister}>Register</button>
                <button onClick={() => navigate("/")}>Login Page</button>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}

        </div>
    )
}

export default Register