import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { experimentsAPI } from '../api';
import './ExperimentCompare.css';

export function ExperimentCompare() {
  const location = useLocation();
  const ids = new URLSearchParams(location.search).get('ids')?.split(',').map(Number) || [];
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [allParamKeys, setAllParamKeys] = useState(new Set());
  const [allMetricKeys, setAllMetricKeys] = useState(new Set());

  useEffect(() => {
    if (ids.length < 2) return;
    fetchComparison();
  }, [ids]);

  const fetchComparison = async () => {
    try {
      const res = await experimentsAPI.compare(ids);
      const exps = res.data.experiments;
      setExperiments(exps);

      const paramKeys = new Set();
      const metricKeys = new Set();

      exps.forEach((exp) => {
        Object.keys(exp.params).forEach(k => paramKeys.add(k));
        Object.keys(exp.metrics).forEach(k => metricKeys.add(k));
      });

      setAllParamKeys(paramKeys);
      setAllMetricKeys(metricKeys);
    } catch (err) {
      console.error('Erro ao comparar:', err);
    }
    setLoading(false);
  };

  if (ids.length < 2) return <div>Selecione pelo menos 2 experimentos para comparar</div>;
  if (loading) return <div>Carregando comparação...</div>;

  return (
    <div className="experiment-compare">
      <h2>Comparação de Experimentos</h2>

      <section className="compare-section">
        <h3>Parâmetros</h3>
        <table className="compare-table">
          <thead>
            <tr>
              <th>Parâmetro</th>
              {experiments.map((exp) => (
                <th key={exp.id}>{exp.name}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from(allParamKeys).map((key) => (
              <tr key={key}>
                <td className="compare-key">{key}</td>
                {experiments.map((exp) => (
                  <td
                    key={`${exp.id}-${key}`}
                    className={exp.params[key] !== undefined ? 'has-value' : 'no-value'}
                  >
                    {exp.params[key] !== undefined ? JSON.stringify(exp.params[key]) : '-'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="compare-section">
        <h3>Métricas</h3>
        <table className="compare-table">
          <thead>
            <tr>
              <th>Métrica</th>
              {experiments.map((exp) => (
                <th key={exp.id}>{exp.name}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from(allMetricKeys).map((key) => (
              <tr key={key}>
                <td className="compare-key">{key}</td>
                {experiments.map((exp) => {
                  const value = exp.metrics[key];
                  const isBest =
                    value !== undefined &&
                    value === Math.max(
                      ...experiments
                        .map((e) => e.metrics[key])
                        .filter((v) => v !== undefined)
                    );

                  return (
                    <td
                      key={`${exp.id}-${key}`}
                      className={isBest ? 'best-value' : value !== undefined ? 'has-value' : 'no-value'}
                    >
                      {value !== undefined ? (typeof value === 'number' ? value.toFixed(4) : JSON.stringify(value)) : '-'}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
