import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './components/Login';
import PolicyList from './components/PolicyList';
import PolicyDetail from './components/PolicyDetail';
import Notifications from './components/Notifications';
import Reports from './components/Reports';
import Notifications from './components/Notifications';

function App() {
  return (
        <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/policies">Policies</Link> | <Link to="/notifications">Notifications</Link> | <Link to="/reports">Reports</Link>
        <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/policies">Policies</Link> | <Link to="/notifications">Notifications</Link>
      </nav>
        <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/policies">Policies</Link>
      </nav>
      <Routes>
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/" element={<div><h1>Welcome to Power Policy!</h1><p>Please log in to continue.</p></div>} />
        <Route path="/policies/:policyId" element={<PolicyDetail />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/" element={<div><h1>Welcome to Power Policy!</h1><p>Please log in to continue.</p></div>} />
        <Route path="/policies/:policyId" element={<PolicyDetail />} />
        <Route path="/" element={<div><h1>Welcome to Power Policy!</h1><p>Please log in to continue.</p></div>} />
      </Routes>
    </Router>
  );
}

export default App;

  );
}

export default App;
