
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
function Verify() {
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [countdown, setCountdown] = useState(30);
  const { email } = useParams();
  const [isResendDisabled, setIsResendDisabled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    let timer;
    if (countdown > 0) {
      timer = setInterval(() => {
        setCountdown((prevCountdown) => prevCountdown - 1);
      }, 1000);
    }

    return () => clearInterval(timer);
  }, [countdown]);

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make an Axios POST request to the "VerifyOTP" endpoint
      const response = await axios.post('http://localhost:8000/VerifyOTP', { email, otp });
      console.log(response);
      if (response.data.success) {
        navigate(`/NewPassword/${email}`);
      }
      else {
        setError('Error verifying OTP. Please try again.');
      }

    } catch (error) {
      // Handle errors, e.g., show an error message to the user
      console.error('Error verifying OTP:', error.message);
      setError('Error verifying OTP. Please try again.'); // Set an error state for display
    }
  };

  const handleResendClick = async () => {
    // Add logic to resend OTP
    try {
        // Make an Axios POST request to the "VerifyOTP" endpoint
        const response = await axios.post('http://localhost:8000/ResendOTP', { email });
        console.log(response);
  
      } catch (error) {
        // Handle errors, e.g., show an error message to the user
        console.error('Error verifying OTP:', error.message);
        setError('Error verifying OTP. Please try again.'); // Set an error state for display
      }
    // For demonstration purposes, we'll reset the countdown to 30 seconds
    setCountdown(30);
    setIsResendDisabled(true);

    // Simulate an API call for OTP resend
    setTimeout(() => {
      setIsResendDisabled(false);
    }, 30000);
  };

  return (
    <div className="bg-gray-100 flex items-center justify-center h-screen">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Verify phone number</h2>
        <form onSubmit={handleFormSubmit} className="space-y-6">
          {/* No need for {% csrf_token %} in React */}
          <div className="text-sm text-gray-700 mb-4">
            A 6 digit One-Time Password has been sent to {email}
          </div>
          <div className="mb-4">
            <input
              type="text"
              maxLength="6"
              pattern="[0-9]*"
              inputMode="numeric"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="w-full p-4 text-center form-control form-control-lg border-orange-600"
              required
            />
          </div>
          <div className="flex justify-between items-center mb-6">
            <div className="text-sm text-gray-600">
              Didn't receive the code?{' '}
              <button
                type="button"
                onClick={handleResendClick}
                disabled={isResendDisabled}
                className={`font-medium text-orange-600 ${
                  isResendDisabled ? 'cursor-not-allowed' : 'hover:text-orange-500'
                }`}
              >
                Resend OTP
              </button>
            </div>
            <div className="text-sm text-gray-600">{`${Math.floor(countdown / 60)
              .toString()
              .padStart(2, '0')}:${(countdown % 60).toString().padStart(2, '0')}`}</div>
          </div>
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
          >
            Submit OTP
          </button>
        </form>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </div>
  );
}

export default Verify;
