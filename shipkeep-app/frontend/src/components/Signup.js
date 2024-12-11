import React, { useState } from "react";

function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState(""); // To display success/error messages

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage(""); // Clear any previous messages

    try {
      const response = await fetch("/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();
      setMessage(data.message); // Set the message from the response

      if (response.ok) {
        // Optionally, you can redirect to the login page or clear the form
        setUsername("");
        setEmail("");
        setPassword("");
      }
    } catch (error) {
      console.error("Signup error:", error);
      setMessage("An error occurred during signup.");
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      {message && <p>{message}</p>} {/* Display the message */}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;
