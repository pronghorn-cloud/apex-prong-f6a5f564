import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './components/Login';
import PolicyList from './components/PolicyList';
import PolicyDetail from './components/PolicyDetail';
import Notifications from './components/Notifications';
import Reports from './components/Reports';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/policies">Policies</Link> | <Link to="/notifications">Notifications</Link> | <Link to="/reports">Reports</Link>
      </nav>
      <Routes>
        <Route path="/" element={<div><h1>Welcome to Power Policy!</h1><p>Please log in to continue.</p></div>} />
        <Route path="/login" element={<Login />} />
        <Route path="/policies" element={<PolicyList />} />
        <Route path="/policies/:policyId" element={<PolicyDetail />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Router>
  );
}

export default App;
