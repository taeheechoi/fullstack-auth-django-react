import { Route, Routes } from 'react-router-dom';
import './App.css';
import Profile from './components/Profile';
import SignIn from './components/SignIn';


function App() {
  return (
    <div className="App">
      <h1>Fullstack Auth Django React</h1>
      <Routes>
        <Route path='/' element={<SignIn/>} />
        <Route path='profile' element={<Profile/>}/>
      </Routes>
    </div>
  );
}

export default App;
