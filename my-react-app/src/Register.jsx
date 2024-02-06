// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom'
// function Register() {
//   const [username, setUsername] = useState('');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [phonenumber, setPhonenumber] = useState('');
//   const navigate = useNavigate();

//   const sendInitialDetails = async (e) => {
//     e.preventDefault(); // Prevents the default form submission behavior

//     try {

//       // Make an Axios POST request to your endpoint
//       // defining the stage 1 registeration
//       const response = await axios.post('http://localhost:8000/RegisterStageOne', {
//         username,
//         email,
//         password,
//         phone: phonenumber,
//       });

//       // Handle the response as needed
//       console.log(response.data);
//       if (response.data.success) {
//         navigate('/RegisterStageSecond')
//       }
//       else {
//         console.log(`invalid data for making register one stage complete: ${response.data.message}`)
//       }

//       // Optionally, you can redirect the user or perform other actions based on the response
//     } catch (error) {
//       // Handle errors, e.g., show an error message to the user
//       console.error('Error sending initial details:', error.message);
//     }
//   };

//   return (
//     <div>
//       {/* Form for user registration */}
//       <form onSubmit={sendInitialDetails}>
//         <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
//         <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
//         <input type="number" minLength={10} maxLength={10} value={phonenumber} onChange={(e) => setPhonenumber(e.target.value)} placeholder="Phone Number" />
//         <input type="password" maxLength={6} minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
//         <button type="submit">Register</button>
//       </form>
//     </div>
//   );
// }
// export default Register;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phonenumber, setPhonenumber] = useState('');
  const navigate = useNavigate();

  const sendInitialDetails = (e) => {
    e.preventDefault();

    // Pass the user details to the next page using the navigate function
    navigate('/RegisterStageSecond', {
      state: {
        username,
        email,
        password,
        phone: phonenumber,
      },
    });
  };

  return (
    <div>
      {/* Form for user registration */}
      <form onSubmit={sendInitialDetails}>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input type="number" minLength={10} maxLength={10} value={phonenumber} onChange={(e) => setPhonenumber(e.target.value)} placeholder="Phone Number" />
        <input type="password" maxLength={6} minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
