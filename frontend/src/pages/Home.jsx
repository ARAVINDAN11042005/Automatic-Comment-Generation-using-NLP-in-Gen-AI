import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { HiLightningBolt, HiChartBar, HiDatabase, HiCode, HiAcademicCap, HiSparkles } from 'react-icons/hi';

const stats = [
    { label: 'NLP Accuracy', value: '89%', icon: <HiLightningBolt />, color: 'purple' },
    { label: 'ALSI Accuracy', value: '79%', icon: <HiChartBar />, color: 'orange' },
    { label: 'Dataset Pairs', value: '57,676', icon: <HiDatabase />, color: 'green' },
    { label: 'Improvement', value: '+10%', icon: <HiSparkles />, color: 'pink' },
];

const features = [
    {
        icon: <HiCode />,
        title: 'Smart Code Analysis',
        description: 'Advanced NLP techniques analyze code structure, patterns, and semantics to generate meaningful comments.',
    },
    {
        icon: <HiChartBar />,
        title: 'Model Comparison',
        description: 'Side-by-side comparison of NLP model vs ALSI-Transformer with detailed metrics visualization.',
    },
    {
        icon: <HiDatabase />,
        title: 'Persistent Storage',
        description: 'All generated comments and metrics are stored for future reference and analysis.',
    },
    {
        icon: <HiAcademicCap />,
        title: 'Research-Backed',
        description: 'Built on extensive research comparing NLP and Transformer architectures for code documentation.',
    },
    {
        icon: <HiLightningBolt />,
        title: 'Real-Time Generation',
        description: 'Instant comment generation powered by advanced natural language processing algorithms.',
    },
    {
        icon: <HiSparkles />,
        title: 'Multi-Language Support',
        description: 'Supports Python, JavaScript, and Java code with language-aware comment generation.',
    },
];

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

function Home() {
    const [animatedStats, setAnimatedStats] = useState(stats.map(() => '0'));

    useEffect(() => {
        const timer = setTimeout(() => {
            setAnimatedStats(stats.map((s) => s.value));
        }, 300);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div>
            {/* Hero Section */}
            <motion.div
                className="hero-section"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7 }}
            >
                <h1 className="hero-title">
                    Automatic Comment
                    <br />
                    Generation using{' '}
                    <span className="gradient-text">NLP in Gen AI</span>
                </h1>
                <p className="hero-subtitle">
                    High-accuracy code comment generation system powered by advanced NLP techniques.
                    Improving code readability with intelligent, context-aware documentation.
                </p>
                <div style={{ display: 'flex', gap: '12px' }}>
                    <Link to="/generate" className="btn btn-primary">
                        <HiCode /> Start Generating
                    </Link>
                    <Link to="/compare" className="btn btn-secondary">
                        <HiChartBar /> View Comparison
                    </Link>
                </div>
            </motion.div>

            {/* Stats */}
            <motion.div
                className="stats-grid"
                variants={container}
                initial="hidden"
                animate="show"
            >
                {stats.map((stat, i) => (
                    <motion.div key={i} className="stat-card" variants={item}>
                        <div className={`stat-icon ${stat.color}`}>{stat.icon}</div>
                        <div className="stat-value">{animatedStats[i]}</div>
                        <div className="stat-label">{stat.label}</div>
                    </motion.div>
                ))}
            </motion.div>

            {/* Features */}
            <motion.div
                variants={container}
                initial="hidden"
                animate="show"
            >
                <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '8px' }}>
                    Key Features
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '24px' }}>
                    Everything you need for intelligent code documentation
                </p>
                <div className="features-grid">
                    {features.map((feature, i) => (
                        <motion.div key={i} className="feature-card" variants={item}>
                            <div className="feature-icon">{feature.icon}</div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </motion.div>
                    ))}
                </div>
            </motion.div>
        </div>
    );
}

export default Home;
