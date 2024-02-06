import './App.css';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './Home';
// import Navigation from './Navigation';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import RegisterStageSecond from './RegisterStageSecond';
import VerifyOTP from './VerifyOTP';
import Verify from './Verify';
import NewPassword from './NewPassword';

function App() {
  return (
    <div>
     
      <Router>
      {/* <Navigation /> */}
        <Routes>
          <Route path='/' element={<Home />}/>
          <Route path='/RegisterStageOne' element={<Register />}/>
          <Route path='/RegisterStageSecond' element={<RegisterStageSecond />}/>

          <Route path='/Login' element={<Login />}/>
          <Route path='/NewPassword/:email' element={<NewPassword />}/>
          <Route path='/Dashboard' element={<Dashboard />}/>
          <Route path='/GenerateOTP' element={<VerifyOTP />}/>\
         <Route path='/VerifyOTP/:email' element={<Verify />}/> 
        </Routes>
      </Router>
    </div>
  );
}

export default App;