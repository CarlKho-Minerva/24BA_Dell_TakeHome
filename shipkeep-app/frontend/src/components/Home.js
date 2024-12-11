import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate

function Home() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch("/api/logout");
      if (response.ok) {
        navigate("/login"); // Redirect to login page
      } else {
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <div>
      <h2>Welcome to the Home Page!</h2>
      <p>You are now logged in.</p>
      <button onClick={handleLogout}>Logout</button> {/* Add logout button */}
    </div>
  );
}

export default Home;
