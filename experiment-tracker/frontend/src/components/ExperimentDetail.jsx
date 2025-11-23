import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { experimentsAPI } from '../api';
import { format } from 'date-fns';
import './ExperimentDetail.css';

export function ExperimentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [experiment, setExperiment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExperiment();
  }, [id]);

  const fetchExperiment = async () => {
    try {
      const res = await experimentsAPI.get(id);
      setExperiment(res.data);
    } catch (err) {
      console.error('Erro ao carregar experimento:', err);
    }
    setLoading(false);
  };

  if (loading) return <div>Carregando...</div>;
  if (!experiment) return <div>Experimento não encontrado</div>;

  return (
    <div className="experiment-detail">
      <div className="detail-header">
        <button onClick={() => navigate('/')} className="back-btn">
          ← Voltar
        </button>
        <h1>{experiment.name}</h1>
        <span className="status-badge" style={{
          backgroundColor: experiment.status === 'completed' ? '#28a745' : 
                          experiment.status === 'failed' ? '#dc3545' : '#ffc107'
        }}>
          {experiment.status}
        </span>
      </div>

      {experiment.description && (
        <p className="description">{experiment.description}</p>
      )}

      <div className="detail-grid">
        <section className="detail-section">
          <h3>Informações</h3>
          <div className="info-grid">
            <div className="info-item">
              <label>ID:</label>
              <span>{experiment.id}</span>
            </div>
            <div className="info-item">
              <label>Usuário:</label>
              <span>{experiment.user || '-'}</span>
            </div>
            <div className="info-item">
              <label>Criado em:</label>
              <span>{format(new Date(experiment.created_at), 'dd/MM/yyyy HH:mm:ss')}</span>
            </div>
            <div className="info-item">
              <label>Git Branch:</label>
              <span className="code">{experiment.git_branch || '-'}</span>
            </div>
            <div className="info-item">
              <label>Git Commit:</label>
              <span className="code">{experiment.git_commit?.slice(0, 7) || '-'}</span>
            </div>
            <div className="info-item">
              <label>Dataset:</label>
              <span>{experiment.dataset_version || '-'}</span>
            </div>
          </div>
        </section>

        <section className="detail-section">
          <h3>Parâmetros ({Object.keys(experiment.params).length})</h3>
          {Object.keys(experiment.params).length > 0 ? (
            <table className="param-table">
              <tbody>
                {Object.entries(experiment.params).map(([key, value]) => (
                  <tr key={key}>
                    <td className="param-key">{key}</td>
                    <td className="param-value">{JSON.stringify(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum parâmetro registrado</p>
          )}
        </section>

        <section className="detail-section">
          <h3>Métricas ({Object.keys(experiment.metrics).length})</h3>
          {Object.keys(experiment.metrics).length > 0 ? (
            <table className="metric-table">
              <tbody>
                {Object.entries(experiment.metrics).map(([key, value]) => (
                  <tr key={key}>
                    <td className="metric-key">{key}</td>
                    <td className="metric-value">
                      {typeof value === 'number' ? value.toFixed(4) : JSON.stringify(value)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhuma métrica registrada</p>
          )}
        </section>

        {Object.keys(experiment.artifacts).length > 0 && (
          <section className="detail-section">
            <h3>Artefatos ({Object.keys(experiment.artifacts).length})</h3>
            <ul className="artifacts-list">
              {Object.entries(experiment.artifacts).map(([name, path]) => (
                <li key={name}>
                  <span className="artifact-name">{name}</span>
                  <span className="artifact-path">{path}</span>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
}
