import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HiCode, HiLightningBolt, HiChevronDown } from 'react-icons/hi';
import axios from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const API_URL = 'http://localhost:5000/api';

const sampleCodes = {
    python: `def calculate_average(numbers):
    if not numbers:
        return 0
    total = sum(numbers)
    count = len(numbers)
    return total / count`,
    javascript: `function fetchUserData(userId) {
    return fetch(\`/api/users/\${userId}\`)
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('user', JSON.stringify(data));
            return data;
        })
        .catch(error => console.error(error));
}`,
    java: `public static List<Integer> filterEvenNumbers(List<Integer> numbers) {
    List<Integer> evenNumbers = new ArrayList<>();
    for (int num : numbers) {
        if (num % 2 == 0) {
            evenNumbers.add(num);
        }
    }
    return evenNumbers;
}`,
};

function Generate() {
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('python');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGenerate = async () => {
        if (!code.trim()) {
            setError('Please enter some code to generate comments.');
            setTimeout(() => setError(''), 3000);
            return;
        }

        setLoading(true);
        setError('');

        try {
            const response = await axios.post(`${API_URL}/generate`, {
                code: code.trim(),
                language,
            });
            setResult(response.data);
        } catch (err) {
            setError('Failed to connect to the API server. Make sure the backend is running on port 5000.');
            setTimeout(() => setError(''), 5000);
        } finally {
            setLoading(false);
        }
    };

    const loadSample = () => {
        setCode(sampleCodes[language] || sampleCodes.python);
    };

    return (
        <div>
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h2>Generate Comments</h2>
                <p>Paste your code below and let our NLP model generate intelligent comments</p>
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
                        <button className="btn btn-secondary btn-sm" onClick={loadSample}>
                            Load Sample Code
                        </button>
                    </div>
                    <button
                        className="btn btn-primary"
                        onClick={handleGenerate}
                        disabled={loading || !code.trim()}
                    >
                        {loading ? (
                            <>
                                <span className="spinner" /> Generating...
                            </>
                        ) : (
                            <>
                                <HiLightningBolt /> Generate Comments
                            </>
                        )}
                    </button>
                </div>

                <div className="code-editor-container">
                    <textarea
                        className="code-editor"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        placeholder={`// Paste your ${language} code here...\n// Example:\ndef hello_world():\n    print("Hello, World!")`}
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
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <div className="results-grid">
                            {/* NLP Model Result */}
                            <motion.div
                                className="result-panel nlp"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.2 }}
                            >
                                <div className="panel-header">
                                    <HiCode style={{ color: 'var(--accent-primary)', fontSize: '1.3rem' }} />
                                    <h3>NLP Model</h3>
                                    <span className="model-badge">Proposed</span>
                                </div>
                                <div className="comment-text" style={{ padding: '10px' }}>
                                    <SyntaxHighlighter
                                        language={language}
                                        style={vscDarkPlus}
                                        customStyle={{ background: 'transparent', margin: 0, padding: 0, fontSize: '0.85rem' }}
                                    >
                                        {result.nlp.comment}
                                    </SyntaxHighlighter>
                                </div>
                                <div className="metrics-row">
                                    <div className="metric-chip">
                                        <span className="metric-label">Confidence</span>
                                        <span className="metric-value">{(result.nlp.confidence * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="metric-chip">
                                        <span className="metric-label">BLEU</span>
                                        <span className="metric-value">{(result.nlp.metrics.bleu * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="metric-chip">
                                        <span className="metric-label">F1</span>
                                        <span className="metric-value">{(result.nlp.metrics.f1 * 100).toFixed(1)}%</span>
                                    </div>
                                </div>
                                <div className="progress-bar" style={{ marginTop: '16px' }}>
                                    <div
                                        className="progress-fill nlp"
                                        style={{ width: `${result.nlp.confidence * 100}%` }}
                                    />
                                </div>
                            </motion.div>

                            {/* ALSI Model Result */}
                            <motion.div
                                className="result-panel alsi"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.3 }}
                            >
                                <div className="panel-header">
                                    <HiCode style={{ color: 'var(--accent-warning)', fontSize: '1.3rem' }} />
                                    <h3>ALSI-Transformer</h3>
                                    <span className="model-badge">Baseline</span>
                                </div>

                                <div className="metrics-row">
                                    <div className="metric-chip">
                                        <span className="metric-label">Confidence</span>
                                        <span className="metric-value">{(result.alsi.confidence * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="metric-chip">
                                        <span className="metric-label">BLEU</span>
                                        <span className="metric-value">{(result.alsi.metrics.bleu * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="metric-chip">
                                        <span className="metric-label">F1</span>
                                        <span className="metric-value">{(result.alsi.metrics.f1 * 100).toFixed(1)}%</span>
                                    </div>
                                </div>
                                <div className="progress-bar" style={{ marginTop: '16px' }}>
                                    <div
                                        className="progress-fill alsi"
                                        style={{ width: `${result.alsi.confidence * 100}%` }}
                                    />
                                </div>
                            </motion.div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default Generate;
