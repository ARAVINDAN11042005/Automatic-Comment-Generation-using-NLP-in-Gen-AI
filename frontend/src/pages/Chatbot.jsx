import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HiSparkles, HiCode, HiCheckCircle } from 'react-icons/hi';
import axios from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const API_URL = 'http://localhost:5000/api';

function Chatbot() {
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('python');
    const [result, setResult] = useState(null);
    const [commentsResult, setCommentsResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingComments, setLoadingComments] = useState(false);
    const [error, setError] = useState('');

    const handleFixCode = async () => {
        if (!code.trim()) {
            setError('Please enter some code to fix.');
            setTimeout(() => setError(''), 3000);
            return;
        }

        setLoading(true);
        setError('');
        setCommentsResult(null); // Reset comments

        try {
            const response = await axios.post(`${API_URL}/fix-code`, {
                code: code.trim(),
                language,
            });
            setResult(response.data);
        } catch (err) {
            setError('Failed to reach the chatbot AI. Make sure the backend is running.');
            setTimeout(() => setError(''), 5000);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateComments = async () => {
        if (!result || !result.fixed_code) return;

        setLoadingComments(true);
        setError('');

        try {
            const response = await axios.post(`${API_URL}/generate`, {
                code: result.fixed_code,
                language,
            });
            setCommentsResult(response.data);
        } catch (err) {
            setError('Failed to generate comments.');
            setTimeout(() => setError(''), 5000);
        } finally {
            setLoadingComments(false);
        }
    };

    return (
        <div>
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h2>Code Fixer Chatbot</h2>
                <p>Paste your buggy code below. Our AI will fix syntax mistakes before you generate comments.</p>
            </motion.div>

            <motion.div
                className="card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
            >
                <div className="editor-toolbar">
                    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                        <div style={{ position: 'relative' }}>
                            <select
                                className="language-select"
                                value={language}
                                onChange={(e) => setLanguage(e.target.value)}
                            >
                                <option value="python">Python</option>
                                <option value="javascript">JavaScript</option>
                                <option value="java">Java</option>
                            </select>
                        </div>
                    </div>
                    <button
                        className="btn btn-primary"
                        onClick={handleFixCode}
                        disabled={loading || !code.trim()}
                        style={{ background: 'linear-gradient(135deg, #00d4aa, #6c63ff)' }}
                    >
                        {loading ? (
                            <>
                                <span className="spinner" /> Analyzing code...
                            </>
                        ) : (
                            <>
                                <HiSparkles /> Fix My Code
                            </>
                        )}
                    </button>
                </div>

                <div className="code-editor-container">
                    <textarea
                        className="code-editor"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        placeholder={`// Paste your buggy ${language} code here...\n// Example (Python missing colon):\ndef hello_world()\n    print "Hello!"`}
                        spellCheck={false}
                    />
                </div>
            </motion.div>

            {/* Error Toast */}
            <AnimatePresence>
                {error && (
                    <motion.div
                        className="toast error"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 20 }}
                    >
                        ⚠️ {error}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Results */}
            <AnimatePresence>
                {result && (
                    <motion.div
                        className="card"
                        style={{ marginTop: '24px', border: '1px solid var(--accent-secondary)' }}
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <div className="panel-header" style={{ marginBottom: '20px' }}>
                            <HiCheckCircle style={{ color: 'var(--accent-secondary)', fontSize: '1.5rem' }} />
                            <h3>Fixed Code Results</h3>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <h4 style={{ color: 'var(--text-secondary)', marginBottom: '8px', fontSize: '0.9rem' }}>Changes Applied:</h4>
                            <ul style={{ paddingLeft: '20px', color: 'var(--text-primary)', fontSize: '0.85rem' }}>
                                {result.fixes_applied.map((fix, idx) => (
                                    <li key={idx} style={{ marginBottom: '4px' }}>{fix}</li>
                                ))}
                            </ul>
                        </div>

                        <div className="comment-text" style={{ padding: '0', background: 'transparent' }}>
                            <SyntaxHighlighter
                                language={language}
                                style={vscDarkPlus}
                                customStyle={{ borderRadius: '8px', margin: 0, padding: '16px', fontSize: '0.85rem' }}
                            >
                                {result.fixed_code}
                            </SyntaxHighlighter>
                        </div>

                        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end' }}>
                            <button
                                className="btn btn-primary"
                                onClick={handleGenerateComments}
                                disabled={loadingComments}
                            >
                                {loadingComments ? 'Generating...' : 'Get Comments for Fixed Code'}
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Comments Result */}
            <AnimatePresence>
                {commentsResult && (
                    <motion.div
                        className="results-stacked"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{ marginTop: '24px' }}
                    >
                        {/* NLP Model Result Output */}
                        <div className="result-panel nlp">
                            <div className="panel-header">
                                <HiCode style={{ color: 'var(--accent-primary)', fontSize: '1.3rem' }} />
                                <h3>NLP Model Comments</h3>
                                <span className="model-badge">Generated</span>
                            </div>
                            <div className="comment-text" style={{ padding: '10px' }}>
                                <SyntaxHighlighter
                                    language={language}
                                    style={vscDarkPlus}
                                    customStyle={{ background: 'transparent', margin: 0, padding: 0, fontSize: '0.85rem' }}
                                >
                                    {commentsResult.nlp.comment}
                                </SyntaxHighlighter>
                            </div>
                            <div className="metrics-row">
                                <div className="metric-chip">
                                    <span className="metric-label">Confidence</span>
                                    <span className="metric-value">{(commentsResult.nlp.confidence * 100).toFixed(1)}%</span>
                                </div>
                                <div className="metric-chip">
                                    <span className="metric-label">BLEU</span>
                                    <span className="metric-value">{(commentsResult.nlp.metrics.bleu * 100).toFixed(1)}%</span>
                                </div>
                                <div className="metric-chip">
                                    <span className="metric-label">F1</span>
                                    <span className="metric-value">{(commentsResult.nlp.metrics.f1 * 100).toFixed(1)}%</span>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default Chatbot;
