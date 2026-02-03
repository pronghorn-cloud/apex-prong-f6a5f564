import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useNavigate, Link } from 'react-router-dom';

function PolicyList() {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const fetchPolicies = async (query = '') => {
    setLoading(true);
    setError('');
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const url = query ? `/policies/search/?query=${encodeURIComponent(query)}` : '/policies/';
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        localStorage.removeItem('access_token');
        navigate('/login');
        return;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch policies');
      }

      const data = await response.json();
      setPolicies(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const handleSearch = (event) => {
    event.preventDefault();
    fetchPolicies(searchTerm);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  if (loading) return <div>Loading policies...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div>
      <h2>Policies</h2>
      <button onClick={handleLogout}>Logout</button>
      <form onSubmit={handleSearch} style={{ margin: '20px 0' }}>
        <input
          type="text"
          placeholder="Search policies..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      {policies.length === 0 ? (
        <p>No policies found.</p>
      ) : (
        <ul>
          {policies.map((policy) => (
            <li key={policy.id}>
              <Link to={`/policies/${policy.id}`}>
                <strong>{policy.title}</strong> - {policy.status}
              </Link>
              <p>{policy.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default PolicyList;

  useEffect(() => {
    const fetchPolicies = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        navigate('/login');
        return;
      }

      try {
        const response = await fetch('/policies/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.status === 401) {
          localStorage.removeItem('access_token');
          navigate('/login');
          return;
        }

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch policies');
        }

        const data = await response.json();
        setPolicies(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPolicies();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  if (loading) return <div>Loading policies...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div>
      <h2>Policies</h2>
      <button onClick={handleLogout}>Logout</button>
      {policies.length === 0 ? (
        <p>No policies found.</p>
      ) : (
        <ul>
          {policies.map((policy) => (
            <li key={policy.id}>
              <strong>{policy.title}</strong> - {policy.status}
              <p>{policy.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default PolicyList;
