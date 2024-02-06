import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
function LoginForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();


  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make an Axios POST request to the "VerifyOTP" endpoint
      const response = await axios.post('http://localhost:8000/GenerateOTP', { email });
      // Check if the response indicates success
      if (response.data.success) {
        // Navigate to the "/Verify" endpoint with the email as a parameter
        navigate(`/VerifyOTP/${email}`);
      } else {
        setError('Error generating OTP. Please try again.');
      }
    } catch (error) {
      // Handle errors, e.g., show an error message to the user
      console.error('Error sending email:', error.message);
      setError('Error sending email. Please try again.'); // Set an error state for display
    }
  };

  return (
    <div className="bg-gray-100 flex items-center justify-center h-screen">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h2 className="text-3xl font-bold mb-4 text-gray-800">Generate OTP</h2>
        <form onSubmit={handleFormSubmit} className="space-y-4">
          {/* No need for {% csrf_token %} in React */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="focus:ring-orange-500 focus:border-blue-500 flex-1 block w-full rounded-md sm:text-sm border-gray-300"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
          >
            Request OTP
          </button>
        </form>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </div>
  );
}

export default LoginForm;
