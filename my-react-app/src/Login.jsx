import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'
function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/login', {
        username,
        password,
      });

      if (response.status === 200 && response.data.status === 'success') {
        // Login successful, handle tokens as needed
        console.log('Access Token:', response.data.access_token);
        console.log('Refresh Token:', response.data.refresh_token);

        // Login successful, handle tokens as needed
        const accessToken = response.data.access_token;
        const refreshToken = response.data.refresh_token;

        // Save tokens and user credentials to localStorage or cookies
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('username', username);
        localStorage.setItem('password', password);

          // Send the username as a query parameter
      navigate(`/Dashboard?username=${username}`);
      } else {
        // Handle login failure, show error message
        setError(response.data.message || 'Login failed');
      }
    } catch (error) {
      // Handle network errors or other issues
      console.error('Login error:', error.message);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        {/* Your form fields go here */}
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <Link to="/GenerateOTP">forgot the password</Link>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Login;