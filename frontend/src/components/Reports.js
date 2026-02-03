import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Reports() {
  const [policySummary, setPolicySummary] = useState(null);
  const [attestationStatus, setAttestationStatus] = useState(null);
  const [policyVersionId, setPolicyVersionId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return null;
    }
    return { 'Authorization': `Bearer ${token}` };
  };

  const fetchData = async () => {
    setLoading(true);
    setError('');
    const headers = getAuthHeaders();
    if (!headers) return;

    try {
      // Fetch Policy Status Summary
      const policySummaryResponse = await fetch('/reports/policy-status-summary', { headers });
      if (policySummaryResponse.status === 401) { navigate('/login'); return; }
      if (!policySummaryResponse.ok) { throw new Error('Failed to fetch policy summary'); }
      const summaryData = await policySummaryResponse.json();
      setPolicySummary(summaryData);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAttestationStatus = async (versionId) => {
    if (!versionId) return;
    setLoading(true);
    setError('');
    const headers = getAuthHeaders();
    if (!headers) return;

    try {
      const attestationResponse = await fetch(`/reports/attestation-status/${versionId}`, { headers });
      if (attestationResponse.status === 401) { navigate('/login'); return; }
      if (!attestationResponse.ok) { throw new Error('Failed to fetch attestation status'); }
      const attestationData = await attestationResponse.json();
      setAttestationStatus(attestationData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAttestationSearch = (e) => {
    e.preventDefault();
    fetchAttestationStatus(policyVersionId);
  };

  if (loading) return <div>Loading reports...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div>
      <h2>Reports & Dashboards</h2>

      <h3>Policy Status Summary</h3>
      {policySummary ? (
        <ul>
          {Object.entries(policySummary).map(([status, count]) => (
            <li key={status}>{status}: {count} policies</li>
          ))}
        </ul>
      ) : (
        <p>No policy status summary available.</p>
      )}

      <h3>Attestation Status by Policy Version</h3>
      <form onSubmit={handleAttestationSearch}>
        <input
          type="number"
          placeholder="Enter Policy Version ID"
          value={policyVersionId}
          onChange={(e) => setPolicyVersionId(e.target.value)}
          required
        />
        <button type="submit">Get Attestation Status</button>
      </form>
      {attestationStatus && (
        <div>
          <h4>Policy: {attestationStatus.policy_title} (Version {attestationStatus.version_number})</h4>
          <p>Total Users: {attestationStatus.total_users}</p>
          <p>Attested: {attestationStatus.attested_count}</p>
          <p>Non-Attested: {attestationStatus.non_attested_count}</p>
          
          <h5>Attested Users:</h5>
          {attestationStatus.attested_users.length > 0 ? (
            <ul>
              {attestationStatus.attested_users.map((user, index) => (
                <li key={index}>{user.username} ({user.email}) - Attested at: {new Date(user.attested_at).toLocaleString()}</li>
              ))}
            </ul>
          ) : (<p>No users have attested yet.</p>)}

          <h5>Non-Attested Users:</h5>
          {attestationStatus.non_attested_users.length > 0 ? (
            <ul>
              {attestationStatus.non_attested_users.map((user, index) => (
                <li key={index}>{user.username} ({user.email})</li>
              ))}
            </ul>
          ) : (<p>All users have attested.</p>)}
        </div>
      )}
    </div>
  );
}

export default Reports;
