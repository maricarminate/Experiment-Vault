import React, { useState, useEffect } from 'react';
import { experimentsAPI } from '../api';
import { format } from 'date-fns';
import './ExperimentList.css';

export function ExperimentList() {
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [filters, setFilters] = useState({ status: '', user: '' });

  useEffect(() => {
    fetchExperiments();
  }, [filters]);

  const fetchExperiments = async () => {
    setLoading(true);
    try {
      const res = await experimentsAPI.list(0, 50, filters);
      setExperiments(res.data);
    } catch (err) {
      console.error('Erro ao carregar experimentos:', err);
    }
    setLoading(false);
  };

  const toggleSelect = (id) => {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Deletar este experimento?')) return;
    try {
      await experimentsAPI.delete(id);
      fetchExperiments();
    } catch (err) {
      console.error('Erro ao deletar:', err);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      running: '#ffc107',
      completed: '#28a745',
      failed: '#dc3545',
    };
    return colors[status] || '#6c757d';
  };

  return (
    <div className="experiment-list">
      <div className="filters">
        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
        >
          <option value="">Todos os status</option>
          <option value="running">Em execução</option>
          <option value="completed">Concluído</option>
          <option value="failed">Falhou</option>
        </select>

        <input
          type="text"
          placeholder="Filtrar por usuário..."
          value={filters.user}
          onChange={(e) => setFilters({ ...filters, user: e.target.value })}
        />

        {selectedIds.size > 1 && (
          <button className="compare-btn">
            Comparar {selectedIds.size} experimentos
          </button>
        )}
      </div>

      {loading ? (
        <p>Carregando...</p>
      ) : experiments.length === 0 ? (
        <p>Nenhum experimento encontrado</p>
      ) : (
        <table className="experiments-table">
          <thead>
            <tr>
              <th style={{ width: '40px' }}>
                <input
                  type="checkbox"
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedIds(new Set(experiments.map(e => e.id)));
                    } else {
                      setSelectedIds(new Set());
                    }
                  }}
                  checked={selectedIds.size === experiments.length && experiments.length > 0}
                />
              </th>
              <th>Nome</th>
              <th>Status</th>
              <th>Usuário</th>
              <th>Métricas</th>
              <th>Data</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {experiments.map((exp) => (
              <tr key={exp.id}>
                <td>
                  <input
                    type="checkbox"
                    checked={selectedIds.has(exp.id)}
                    onChange={() => toggleSelect(exp.id)}
                  />
                </td>
                <td className="exp-name">{exp.name}</td>
                <td>
                  <span
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(exp.status) }}
                  >
                    {exp.status}
                  </span>
                </td>
                <td>{exp.user || '-'}</td>
                <td>
                  <small>
                    {Object.keys(exp.metrics).length > 0
                      ? Object.keys(exp.metrics).join(', ')
                      : '-'}
                  </small>
                </td>
                <td className="date">
                  {format(new Date(exp.created_at), 'dd/MM HH:mm')}
                </td>
                <td>
                  <a href={`/experiments/${exp.id}`} className="link">Ver</a>
                  <button
                    onClick={() => handleDelete(exp.id)}
                    className="delete-btn"
                  >
                    ✕
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}