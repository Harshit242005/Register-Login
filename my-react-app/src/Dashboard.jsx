import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function Dashboard() {
  // Access the query parameter from the URL
  const searchParams = new URLSearchParams(useLocation().search);
  const username = searchParams.get('username');
  const navigate = useNavigate();

  const Logout = () => {
    // Clear all user-related data from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    localStorage.removeItem('password');

    // Navigate back to the home page
    navigate('/');

  }

  return (
    <div>
      <h1>Welcome to the Dashboard, {username}!</h1>
      <button onClick={Logout}>Logout</button>
      {/* Other content of your Dashboard */}
    </div>
  );
}

export default Dashboard;
