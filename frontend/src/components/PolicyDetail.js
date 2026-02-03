import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function PolicyDetail() {
  const { policyId } = useParams();
  const [policy, setPolicy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPolicy = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        navigate('/login');
        return;
      }

      try {
        const response = await fetch(`/policies/${policyId}`, {
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
          throw new Error(errorData.detail || 'Failed to fetch policy');
        }

        const data = await response.json();
        setPolicy(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPolicy();
  }, [policyId, navigate]);

  if (loading) return <div>Loading policy details...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!policy) return <div>Policy not found.</div>;

  return (
    <div>
      <h2>{policy.title}</h2>
      <p><strong>Status:</strong> {policy.status}</p>
      <p><strong>Description:</strong> {policy.description}</p>
      <p><strong>Document Type:</strong> {policy.document_type ? policy.document_type.name : 'N/A'}</p>
      <p><strong>Created By:</strong> {policy.created_by}</p>
      <p><strong>Created At:</strong> {new Date(policy.created_at).toLocaleDateString()}</p>
      <p><strong>Last Updated:</strong> {new Date(policy.updated_at).toLocaleDateString()}</p>

      <h3>Current Version</h3>
      {policy.current_version ? (
        <div>
          <p><strong>Version Number:</strong> {policy.current_version.version_number}</p>
          <p><strong>Effective Date:</strong> {policy.current_version.effective_date ? new Date(policy.current_version.effective_date).toLocaleDateString() : 'N/A'}</p>
          <p><strong>Summary of Changes:</strong> {policy.current_version.summary_of_changes || 'N/A'}</p>
          {/* Link to content blob/display content would go here */}
        </div>
      ) : (
        <p>No current version available.</p>
      )}

      {/* TODO: Add a list of all versions and allow comparison/viewing old content */}
    </div>
  );
}

export default PolicyDetail;
