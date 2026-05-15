import { useState } from "react";
import { loginUser } from "./authService";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

const handleLogin = async (e) => {
  e.preventDefault();

  console.log("LOGIN BUTTON CLICKED");

  try {
    console.log("Sending request...");

    const data = await loginUser(email, password);

    console.log("BACKEND RESPONSE:", data);

    localStorage.setItem(
      "access_token",
      data.access_token
    );

    localStorage.setItem(
      "refresh_token",
      data.refresh_token
    );

    alert("Login successful!");

    navigate("/dashboard");

  } catch (error) {
    console.log("FULL ERROR:", error);

    if (error.response) {
      console.log("ERROR DATA:", error.response.data);
      console.log("STATUS:", error.response.status);
    }

    alert("Login failed");
  }
};

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Kairova</h1>

        <p style={styles.subtitle}>
          Sign in to your dashboard
        </p>

        <form onSubmit={handleLogin} style={styles.form}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            style={styles.input}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            style={styles.input}
          />

          <button type="submit" style={styles.button}>
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f4f7fb",
  },

  card: {
    width: "350px",
    padding: "40px",
    borderRadius: "12px",
    backgroundColor: "white",
    boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
  },

  title: {
    marginBottom: "10px",
    textAlign: "center",
  },

  subtitle: {
    marginBottom: "25px",
    textAlign: "center",
    color: "#666",
  },

  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },

  input: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "16px",
  },

  button: {
    padding: "12px",
    border: "none",
    borderRadius: "8px",
    backgroundColor: "#111827",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
  },
};