import { motion } from 'framer-motion';
import { HiAcademicCap, HiLightBulb, HiBeaker, HiUsers, HiCode, HiChip, HiDatabase, HiDocumentText } from 'react-icons/hi';

const container = {
    hidden: { opacity: 0 },
    show: {
        opacity: 1,
        transition: { staggerChildren: 0.1 },
    },
};

const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

function About() {
    return (
        <div>
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h2>About the Research</h2>
                <p>High-Accuracy Automatic Comment Generation using NLP in Generative AI</p>
            </motion.div>

            <motion.div
                className="about-grid"
                variants={container}
                initial="hidden"
                animate="show"
            >
                {/* Abstract */}
                <motion.div className="about-card" variants={item} style={{ gridColumn: '1 / -1' }}>
                    <h3><HiAcademicCap style={{ color: 'var(--accent-primary)' }} /> Abstract</h3>
                    <p>
                        The aim of this research is to develop an accurate Automatic Comment Generation System based on
                        NLP solutions of Generative AI and compare its efficacy with existing solutions for code comment
                        generations that enhance code readability. The proposed NLP-Based model achieved an accuracy of
                        <strong style={{ color: 'var(--accent-secondary)' }}> 89%</strong>, significantly outperforming the
                        existing ALSI-Transformer model which achieved
                        <strong style={{ color: 'var(--accent-orange)' }}> 79%</strong> accuracy.
                    </p>
                </motion.div>

                {/* Methodology */}
                <motion.div className="about-card" variants={item}>
                    <h3><HiBeaker style={{ color: 'var(--accent-secondary)' }} /> Methodology</h3>
                    <ul>
                        <li>Group 1: Existing ALSI-Transformer Model</li>
                        <li>Group 2: Proposed NLP-Based Automatic Comment Generation Model</li>
                        <li>Dataset: 57,676 method and comment pairs</li>
                        <li>Training/Test split: 80/20</li>
                        <li>Evaluation: BLEU, Precision, Recall, F1</li>
                        <li>Statistical Analysis: Mean Score and Standard Deviation</li>
                    </ul>
                </motion.div>

                {/* Key Findings */}
                <motion.div className="about-card" variants={item}>
                    <h3><HiLightBulb style={{ color: 'var(--accent-orange)' }} /> Key Findings</h3>
                    <ul>
                        <li>NLP model: 89% accuracy (mean: 0.799, std: 0.446)</li>
                        <li>ALSI model: 79% accuracy (baseline)</li>
                        <li>10% improvement in accuracy</li>
                        <li>Higher precision, recall, and F1 scores</li>
                        <li>More consistent predictions (lower std deviation)</li>
                        <li>Better generalization on unseen code patterns</li>
                    </ul>
                </motion.div>

                {/* Technology Stack */}
                <motion.div className="about-card" variants={item}>
                    <h3><HiChip style={{ color: 'var(--accent-cyan)' }} /> Technology Stack</h3>
                    <ul>
                        <li>Frontend: React + Vite with modern UI</li>
                        <li>Backend: Python Flask REST API</li>
                        <li>NLP Engine: Pattern recognition and semantic analysis</li>
                        <li>Database: SQLite for persistent storage</li>
                        <li>Visualization: Recharts for interactive charts</li>
                        <li>Animations: Framer Motion for smooth transitions</li>
                    </ul>
                </motion.div>

                {/* Architecture */}
                <motion.div className="about-card" variants={item}>
                    <h3><HiCode style={{ color: 'var(--accent-pink)' }} /> System Architecture</h3>
                    <ul>
                        <li>Code Input → NLP Preprocessing Pipeline</li>
                        <li>Pattern Recognition & Semantic Analysis</li>
                        <li>Natural Language Generation for comments</li>
                        <li>ALSI-Transformer baseline comparison</li>
                        <li>Metric calculation (BLEU, Precision, Recall, F1)</li>
                        <li>SQLite storage for submission history</li>
                    </ul>
                </motion.div>

                {/* Conclusion */}
                <motion.div className="about-card" variants={item} style={{ gridColumn: '1 / -1' }}>
                    <h3><HiDocumentText style={{ color: 'var(--accent-primary)' }} /> Conclusion</h3>
                    <p>
                        The hybrid NLP model proposed in this research performs significantly better than the existing ALSI-Transformer
                        model for the purpose of developing correct and consistent code comments. The NLP model demonstrates an
                        average accuracy of <strong style={{ color: 'var(--accent-secondary)' }}>89%</strong> compared to
                        <strong style={{ color: 'var(--accent-orange)' }}> 79%</strong> from the ALSI model, with greater measures of
                        precision, recall, and F1 score. This model is most appropriate for improving code readability
                        and software documentation, making it a valuable tool for developers and development teams seeking
                        to maintain clean, well-documented codebases.
                    </p>
                </motion.div>
            </motion.div>
        </div>
    );
}

export default About;
