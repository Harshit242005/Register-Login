import React from 'react';
import { Link, useNavigate } from 'react-router-dom'
import styles from './styles/Home.module.css'
import axios from 'axios';
function Home() {



  const navigate = useNavigate();

  const handleLoginClick = async () => {
    // Check if username and password exist in localStorage
    const storedUsername = localStorage.getItem('username');
    const storedPassword = localStorage.getItem('password');

    if (storedUsername && storedPassword) {
      try {
        const response = await axios.post('http://localhost:8000/login', {
          username: storedUsername,
          password: storedPassword,
        });

        if (response.status === 200 && response.data.status === 'success') {
          // Login successful, handle tokens as needed
          const accessToken = response.data.access_token;
          const refreshToken = response.data.refresh_token;

          // Save tokens and user credentials to localStorage or cookies
          localStorage.setItem('access_token', accessToken);
          localStorage.setItem('refresh_token', refreshToken);

          // Send the username as a query parameter
          navigate(`/Dashboard?username=${storedUsername}`);
        } else {
          // Handle login failure, show error message
          console.error('Login failed:', response.data.message || 'Unknown error');
        }
      } catch (error) {
        // Handle network errors or other issues
        console.error('Login error:', error.message);
      }
    } else {
      // Redirect to the Login page if username and password do not exist in localStorage
      navigate('/Login');
    }
  };

  return (
    <div className={styles.btns}>
      <Link to="/RegisterStageOne"><button className={styles.btn}>New User</button></Link>
      <button
        className={styles.btn}
        onClick={handleLoginClick}>
        Already a user
      </button>
      
    </div>
  );
}

export default Home;
