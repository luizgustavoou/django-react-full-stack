import React from "react";
import Form from "../components/Form";

function Login() {
    return <Form route="/api/token/" method="login"></Form>;
}

export default Login;
