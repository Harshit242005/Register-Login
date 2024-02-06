import React, { useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom'
function RegisterStageSecond() {
  const location = useLocation();
  const { state } = location;

  // Access the user details from the state object
  const { username, email, password, phone } = state;
  // State to manage form data
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username,
    email,
    password,
    phone,
    course_interest: '',
    highest_education: '12th pass',
    percentage: '',
    start_study: '',
    receive_newsletter: false,
    receive_promo_offers: false,
    have_passport: false,
  });
  
  console.log(`the form data that we are sending is: ${formData}`);
  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(`Important data: ${formData.course_interest}, ${formData.percentage}, ${formData.start_study}`)
    try {
      // Make API request to the backend endpoint
      const response = await axios.post('http://localhost:8000/Register', formData);

      // Handle the response, e.g., show a success message
      console.log(response.data);
      if (response.data.success) {
        const username = response.data.username;
        navigate(`/Dashboard?username=${username}`)
      }
    } catch (error) {
      // Handle errors, e.g., show an error message
      console.error('Error submitting registration:', error);
    }
  };

  // Function to handle changes in form fields
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    // Update form data based on the type of input field
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="bg-white shadow-lg rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-6 text-center">Register Now To Apply</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <input
              type="text"
              name="course_interest"
              placeholder="Course Interest"
              className="form-input"
              value={formData.course_interest}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="highest_education" className="block text-sm font-medium text-gray-700">
              Highest Education
            </label>
            <select
              id="highest_education"
              name="highest_education"
              className="form-input"
              value={formData.highest_education}
              onChange={handleChange}
              required
            >
              <option value="12th pass">12th Pass</option>
              {/* Add other options here */}
            </select>
          </div>

          <div className="mb-4">
            <input
              type="number"
              name="percentage"
              placeholder="Percentage"
              className="form-input"
              value={formData.percentage}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-4">
            <input
              type="date"
              name="start_study"
              className="form-input"
              placeholder="When did you start your studies?"
              value={formData.start_study}
              onChange={handleChange}
              required
            />
          </div>
          <div className="flex items-center mb-4">
            <input
              type="checkbox"
              name="receive_newsletter"
              className="form-checkbox"
              checked={formData.receive_newsletter}
              onChange={handleChange}
            />
            <span className="ml-2">I wish to receive the newsletter.</span>
          </div>
          <div className="flex items-center mb-4">
            <input
              type="checkbox"
              name="receive_promo_offers"
              className="form-checkbox"
              checked={formData.receive_promo_offers}
              onChange={handleChange}
            />
            <span className="ml-2">I wish to receive promotional offers.</span>
          </div>
          <div className="flex items-center mb-4">
            <input
              type="checkbox"
              name="have_passport"
              className="form-checkbox"
              checked={formData.have_passport}
              onChange={handleChange}
            />
            <span className="ml-2">I have a passport</span>
          </div>
          <div className="text-center mt-6">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Submit Registration
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default RegisterStageSecond;
