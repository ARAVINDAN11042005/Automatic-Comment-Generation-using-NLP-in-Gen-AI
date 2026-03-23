import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HiClock, HiTrash, HiEye, HiX, HiRefresh } from 'react-icons/hi';
import axios from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const API_URL = 'http://localhost:5000/api';

function History() {
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedItem, setSelectedItem] = useState(null);
    const [toast, setToast] = useState('');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${API_URL}/history`);
            setSubmissions(response.data.submissions);
        } catch {
            setSubmissions([]);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`${API_URL}/history/${id}`);
            setSubmissions(submissions.filter((s) => s.id !== id));
            setToast('Submission deleted successfully');
            setTimeout(() => setToast(''), 3000);
            if (selectedItem?.id === id) setSelectedItem(null);
        } catch {
            setToast('Failed to delete');
            setTimeout(() => setToast(''), 3000);
        }
    };

    const getScoreClass = (score) => {
        if (score >= 0.85) return 'high';
        if (score >= 0.7) return 'medium';
        return 'low';
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return 'N/A';
        // The timestamp is already in IST from the backend
        // Parse it as local time by replacing space with T
        const parts = dateStr.replace(' ', 'T');
        const date = new Date(parts);
        if (isNaN(date.getTime())) return dateStr;
        return date.toLocaleString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
        });
    };

    return (
        <div>
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                        <h2>Submission History</h2>
                        <p>View all past code submissions and generated comments</p>
                    </div>
                    <button className="btn btn-secondary btn-sm" onClick={fetchHistory}>
                        <HiRefresh /> Refresh
                    </button>
                </div>
            </motion.div>

            {loading ? (
                <div className="loading-overlay">
                    <span className="spinner" /> Loading history...
                </div>
            ) : submissions.length === 0 ? (
                <motion.div
                    className="empty-state"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                >
                    <div className="empty-icon">📝</div>
                    <h3>No submissions yet</h3>
                    <p>Generate some comments to see your history here</p>
                </motion.div>
            ) : (
                <motion.div
                    className="card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Code Preview</th>
                                <th>Language</th>
                                <th>NLP Score</th>
                                <th>ALSI Score</th>
                                <th>Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {submissions.map((sub, i) => (
                                <motion.tr
                                    key={sub.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.05 }}
                                >
                                    <td>{sub.id}</td>
                                    <td>
                                        <div className="code-preview">{sub.code_input}</div>
                                    </td>
                                    <td>
                                        <span style={{
                                            padding: '3px 10px',
                                            background: 'var(--bg-tertiary)',
                                            borderRadius: '12px',
                                            fontSize: '0.75rem',
                                            fontWeight: 600,
                                        }}>
                                            {sub.language}
                                        </span>
                                    </td>
                                    <td>
                                        <span className={`score-badge ${getScoreClass(sub.nlp_score)}`}>
                                            {(sub.nlp_score * 100).toFixed(1)}%
                                        </span>
                                    </td>
                                    <td>
                                        <span className={`score-badge ${getScoreClass(sub.alsi_score)}`}>
                                            {(sub.alsi_score * 100).toFixed(1)}%
                                        </span>
                                    </td>
                                    <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                        {formatDate(sub.created_at)}
                                    </td>
                                    <td>
                                        <div style={{ display: 'flex', gap: '6px' }}>
                                            <button
                                                className="btn btn-secondary btn-icon"
                                                style={{ width: '32px', height: '32px' }}
                                                onClick={() => setSelectedItem(sub)}
                                                title="View details"
                                            >
                                                <HiEye />
                                            </button>
                                            <button
                                                className="btn btn-danger btn-icon"
                                                style={{ width: '32px', height: '32px' }}
                                                onClick={() => handleDelete(sub.id)}
                                                title="Delete"
                                            >
                                                <HiTrash />
                                            </button>
                                        </div>
                                    </td>
                                </motion.tr>
                            ))}
                        </tbody>
                    </table>
                </motion.div>
            )}

            {/* Detail Modal */}
            <AnimatePresence>
                {selectedItem && (
                    <motion.div
                        style={{
                            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            zIndex: 1000, padding: '20px',
                        }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setSelectedItem(null)}
                    >
                        <motion.div
                            className="card"
                            style={{
                                maxWidth: '800px', width: '100%', maxHeight: '80vh',
                                overflow: 'auto', position: 'relative',
                            }}
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="card-header">
                                <h3>Submission #{selectedItem.id}</h3>
                                <button
                                    className="btn btn-secondary btn-icon"
                                    onClick={() => setSelectedItem(null)}
                                >
                                    <HiX />
                                </button>
                            </div>

                            <div style={{ marginBottom: '20px' }}>
                                <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                                    Code Input ({selectedItem.language})
                                </h4>
                                <div className="comment-text" style={{ padding: '8px' }}>
                                    <SyntaxHighlighter
                                        language={selectedItem.language}
                                        style={vscDarkPlus}
                                        customStyle={{ background: 'transparent', margin: 0, padding: 0, fontSize: '0.82rem' }}
                                    >
                                        {selectedItem.code_input}
                                    </SyntaxHighlighter>
                                </div>
                            </div>

                            <div className="results-grid" style={{ marginTop: '0' }}>
                                <div className="result-panel nlp">
                                    <div className="panel-header">
                                        <h4 style={{ fontSize: '0.95rem' }}>NLP Model</h4>
                                        <span className="model-badge">Proposed</span>
                                    </div>
                                    <div className="comment-text" style={{ padding: '10px' }}>
                                        <SyntaxHighlighter
                                            language={selectedItem.language}
                                            style={vscDarkPlus}
                                            customStyle={{ background: 'transparent', margin: 0, padding: 0, fontSize: '0.85rem' }}
                                        >
                                            {selectedItem.nlp_comment}
                                        </SyntaxHighlighter>
                                    </div>
                                    <div className="metrics-row">
                                        <div className="metric-chip">
                                            <span className="metric-label">Score</span>
                                            <span className="metric-value">{(selectedItem.nlp_score * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="metric-chip">
                                            <span className="metric-label">BLEU</span>
                                            <span className="metric-value">{(selectedItem.nlp_bleu * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="metric-chip">
                                            <span className="metric-label">F1</span>
                                            <span className="metric-value">{(selectedItem.nlp_f1 * 100).toFixed(1)}%</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="result-panel alsi">
                                    <div className="panel-header">
                                        <h4 style={{ fontSize: '0.95rem' }}>ALSI-Transformer</h4>
                                        <span className="model-badge">Baseline</span>
                                    </div>
                                    <div className="comment-text" style={{ padding: '10px' }}>
                                        <SyntaxHighlighter
                                            language={selectedItem.language}
                                            style={vscDarkPlus}
                                            customStyle={{ background: 'transparent', margin: 0, padding: 0, fontSize: '0.85rem' }}
                                        >
                                            {selectedItem.alsi_comment}
                                        </SyntaxHighlighter>
                                    </div>
                                    <div className="metrics-row">
                                        <div className="metric-chip">
                                            <span className="metric-label">Score</span>
                                            <span className="metric-value">{(selectedItem.alsi_score * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="metric-chip">
                                            <span className="metric-label">BLEU</span>
                                            <span className="metric-value">{(selectedItem.alsi_bleu * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="metric-chip">
                                            <span className="metric-label">F1</span>
                                            <span className="metric-value">{(selectedItem.alsi_f1 * 100).toFixed(1)}%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Toast */}
            <AnimatePresence>
                {toast && (
                    <motion.div
                        className="toast success"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 20 }}
                    >
                        ✅ {toast}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default History;
