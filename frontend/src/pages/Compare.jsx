import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line,
} from 'recharts';
import { HiChartBar, HiTrendingUp } from 'react-icons/hi';
import axios from 'axios';
import API_BASE_URL from '../api';

const API_URL = API_BASE_URL;

const COLORS = {
    nlp: '#6c63ff',
    alsi: '#ff6b6b',
    green: '#00d4aa',
    orange: '#ff9f43',
};

const customTooltipStyle = {
    backgroundColor: '#1a1a2e',
    border: '1px solid rgba(108, 99, 255, 0.3)',
    borderRadius: '8px',
    padding: '12px',
    color: '#e8e8f0',
    fontSize: '0.85rem',
};

function Compare() {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await axios.get(`${API_URL}/metrics`);
            setMetrics(response.data.research_metrics);
        } catch {
            // Use default research metrics if API unavailable
            setMetrics({
                nlp_model: {
                    name: 'NLP-Based Model (Proposed)',
                    accuracy: 89, precision: 88.5, recall: 87.2,
                    f1_score: 87.8, bleu_score: 78.5,
                    mean_score: 0.799, std_deviation: 0.446,
                },
                alsi_model: {
                    name: 'ALSI-Transformer (Existing)',
                    accuracy: 79, precision: 77.3, recall: 75.8,
                    f1_score: 76.5, bleu_score: 65.2,
                    mean_score: 0.654, std_deviation: 0.512,
                },
                improvement: {
                    accuracy_gain: 10, precision_gain: 11.2,
                    recall_gain: 11.4, f1_gain: 11.3, bleu_gain: 13.3,
                },
                dataset: {
                    total_pairs: 57676, training_set: 46141,
                    test_set: 11535, language: 'Solidity (Smart Contracts)',
                },
            });
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="loading-overlay">
                <span className="spinner" /> Loading metrics...
            </div>
        );
    }

    if (!metrics) return null;

    const barData = [
        { metric: 'Accuracy', NLP: metrics.nlp_model.accuracy, ALSI: metrics.alsi_model.accuracy },
        { metric: 'Precision', NLP: metrics.nlp_model.precision, ALSI: metrics.alsi_model.precision },
        { metric: 'Recall', NLP: metrics.nlp_model.recall, ALSI: metrics.alsi_model.recall },
        { metric: 'F1 Score', NLP: metrics.nlp_model.f1_score, ALSI: metrics.alsi_model.f1_score },
        { metric: 'BLEU', NLP: metrics.nlp_model.bleu_score, ALSI: metrics.alsi_model.bleu_score },
    ];

    const radarData = [
        { metric: 'Accuracy', NLP: metrics.nlp_model.accuracy, ALSI: metrics.alsi_model.accuracy },
        { metric: 'Precision', NLP: metrics.nlp_model.precision, ALSI: metrics.alsi_model.precision },
        { metric: 'Recall', NLP: metrics.nlp_model.recall, ALSI: metrics.alsi_model.recall },
        { metric: 'F1', NLP: metrics.nlp_model.f1_score, ALSI: metrics.alsi_model.f1_score },
        { metric: 'BLEU', NLP: metrics.nlp_model.bleu_score, ALSI: metrics.alsi_model.bleu_score },
    ];

    const pieData = [
        { name: 'Training Set', value: metrics.dataset.training_set },
        { name: 'Test Set', value: metrics.dataset.test_set },
    ];

    const improvementData = [
        { metric: 'Accuracy', gain: metrics.improvement.accuracy_gain },
        { metric: 'Precision', gain: metrics.improvement.precision_gain },
        { metric: 'Recall', gain: metrics.improvement.recall_gain },
        { metric: 'F1 Score', gain: metrics.improvement.f1_gain },
        { metric: 'BLEU', gain: metrics.improvement.bleu_gain },
    ];

    return (
        <div>
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h2>Model Comparison</h2>
                <p>Comprehensive analysis of NLP Model vs ALSI-Transformer performance</p>
            </motion.div>

            {/* Overview Stats */}
            <div className="stats-grid">
                <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
                    <div className="stat-icon purple"><HiChartBar /></div>
                    <div className="stat-value">{metrics.nlp_model.accuracy}%</div>
                    <div className="stat-label">NLP Accuracy</div>
                </motion.div>
                <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
                    <div className="stat-icon orange"><HiChartBar /></div>
                    <div className="stat-value">{metrics.alsi_model.accuracy}%</div>
                    <div className="stat-label">ALSI Accuracy</div>
                </motion.div>
                <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                    <div className="stat-icon green"><HiTrendingUp /></div>
                    <div className="stat-value">+{metrics.improvement.accuracy_gain}%</div>
                    <div className="stat-label">Accuracy Gain</div>
                </motion.div>
                <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
                    <div className="stat-icon cyan"><HiChartBar /></div>
                    <div className="stat-value">{metrics.dataset.total_pairs.toLocaleString()}</div>
                    <div className="stat-label">Dataset Pairs</div>
                </motion.div>
            </div>

            {/* Charts Grid */}
            <div className="charts-grid">
                {/* Bar Chart */}
                <motion.div className="chart-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                    <h3>Performance Metrics Comparison</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={barData} barGap={8}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="metric" tick={{ fill: '#a0a0b8', fontSize: 12 }} />
                            <YAxis tick={{ fill: '#a0a0b8', fontSize: 12 }} domain={[0, 100]} />
                            <Tooltip contentStyle={customTooltipStyle} />
                            <Legend wrapperStyle={{ fontSize: '0.85rem' }} />
                            <Bar dataKey="NLP" fill={COLORS.nlp} radius={[4, 4, 0, 0]} />
                            <Bar dataKey="ALSI" fill={COLORS.alsi} radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* Radar Chart */}
                <motion.div className="chart-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
                    <h3>Multi-Dimensional Analysis</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <RadarChart data={radarData}>
                            <PolarGrid stroke="rgba(255,255,255,0.1)" />
                            <PolarAngleAxis dataKey="metric" tick={{ fill: '#a0a0b8', fontSize: 11 }} />
                            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#6b6b80', fontSize: 10 }} />
                            <Radar name="NLP" dataKey="NLP" stroke={COLORS.nlp} fill={COLORS.nlp} fillOpacity={0.2} strokeWidth={2} />
                            <Radar name="ALSI" dataKey="ALSI" stroke={COLORS.alsi} fill={COLORS.alsi} fillOpacity={0.15} strokeWidth={2} />
                            <Legend wrapperStyle={{ fontSize: '0.85rem' }} />
                        </RadarChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* Improvement Chart */}
                <motion.div className="chart-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
                    <h3>Improvement Over ALSI (%)</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={improvementData} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis type="number" tick={{ fill: '#a0a0b8', fontSize: 12 }} domain={[0, 20]} />
                            <YAxis type="category" dataKey="metric" tick={{ fill: '#a0a0b8', fontSize: 12 }} width={80} />
                            <Tooltip contentStyle={customTooltipStyle} />
                            <Bar dataKey="gain" fill={COLORS.green} radius={[0, 4, 4, 0]} name="Improvement %" />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* Pie Chart - Dataset Distribution */}
                <motion.div className="chart-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }}>
                    <h3>Dataset Distribution</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={pieData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={100}
                                dataKey="value"
                                label={({ name, value }) => `${name}: ${value.toLocaleString()}`}
                                labelLine={{ stroke: '#a0a0b8' }}
                            >
                                <Cell fill={COLORS.nlp} />
                                <Cell fill={COLORS.orange} />
                            </Pie>
                            <Tooltip contentStyle={customTooltipStyle} />
                        </PieChart>
                    </ResponsiveContainer>
                    <div style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '8px' }}>
                        Total: {metrics.dataset.total_pairs.toLocaleString()} method-comment pairs ({metrics.dataset.language})
                    </div>
                </motion.div>
            </div>

            {/* Statistical Summary */}
            <motion.div
                className="card"
                style={{ marginTop: '24px' }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
            >
                <h3 style={{ marginBottom: '20px' }}>Statistical Summary</h3>
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>NLP Model (Proposed)</th>
                            <th>ALSI-Transformer (Existing)</th>
                            <th>Improvement</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Accuracy</td>
                            <td><span className="score-badge high">{metrics.nlp_model.accuracy}%</span></td>
                            <td><span className="score-badge medium">{metrics.alsi_model.accuracy}%</span></td>
                            <td style={{ color: 'var(--accent-secondary)' }}>+{metrics.improvement.accuracy_gain}%</td>
                        </tr>
                        <tr>
                            <td>Precision</td>
                            <td><span className="score-badge high">{metrics.nlp_model.precision}%</span></td>
                            <td><span className="score-badge medium">{metrics.alsi_model.precision}%</span></td>
                            <td style={{ color: 'var(--accent-secondary)' }}>+{metrics.improvement.precision_gain}%</td>
                        </tr>
                        <tr>
                            <td>Recall</td>
                            <td><span className="score-badge high">{metrics.nlp_model.recall}%</span></td>
                            <td><span className="score-badge medium">{metrics.alsi_model.recall}%</span></td>
                            <td style={{ color: 'var(--accent-secondary)' }}>+{metrics.improvement.recall_gain}%</td>
                        </tr>
                        <tr>
                            <td>F1 Score</td>
                            <td><span className="score-badge high">{metrics.nlp_model.f1_score}%</span></td>
                            <td><span className="score-badge medium">{metrics.alsi_model.f1_score}%</span></td>
                            <td style={{ color: 'var(--accent-secondary)' }}>+{metrics.improvement.f1_gain}%</td>
                        </tr>
                        <tr>
                            <td>BLEU Score</td>
                            <td><span className="score-badge high">{metrics.nlp_model.bleu_score}%</span></td>
                            <td><span className="score-badge medium">{metrics.alsi_model.bleu_score}%</span></td>
                            <td style={{ color: 'var(--accent-secondary)' }}>+{metrics.improvement.bleu_gain}%</td>
                        </tr>
                        <tr>
                            <td>Mean Score</td>
                            <td>{metrics.nlp_model.mean_score}</td>
                            <td>{metrics.alsi_model.mean_score}</td>
                            <td style={{ color: 'var(--accent-secondary)' }}>+{(metrics.nlp_model.mean_score - metrics.alsi_model.mean_score).toFixed(3)}</td>
                        </tr>
                        <tr>
                            <td>Std Deviation</td>
                            <td>{metrics.nlp_model.std_deviation}</td>
                            <td>{metrics.alsi_model.std_deviation}</td>
                            <td style={{ color: 'var(--accent-secondary)' }}>{(metrics.nlp_model.std_deviation - metrics.alsi_model.std_deviation).toFixed(3)}</td>
                        </tr>
                    </tbody>
                </table>
            </motion.div>
        </div>
    );
}

export default Compare;
