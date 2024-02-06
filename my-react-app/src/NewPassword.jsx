import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
function NewPassword() {
  const { email } = useParams();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const handleFormSubmit = async (e) => {
    e.preventDefault();

    // Add a condition to check if both passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      // Make an Axios POST request to the endpoint with email and password
      const response = await axios.post('http://localhost:8000/NewPassword', {
        email,
        password,
      });

      // Handle the response as needed
      console.log(response.data);
      if (response.data.success) {
        navigate('/Login')
      } else {
        setError('Error changing the password rfor the gamil user');
      }

      // Optionally, you can redirect the user or perform other actions based on the response

    } catch (error) {
      // Handle errors, e.g., show an error message to the user
      console.error('Error updating password:', error.message);
      setError('Error updating password. Please try again.'); // Set an error state for display
    }
  };

  return (
    <div>
      <h1>New Password</h1>
      <p>Email: {email}</p>
      <form onSubmit={handleFormSubmit} className="space-y-4">
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Update Password</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default NewPassword;
