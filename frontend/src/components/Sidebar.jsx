import { NavLink } from 'react-router-dom';
import { HiHome, HiCode, HiChartBar, HiClock, HiInformationCircle } from 'react-icons/hi';

const navItems = [
    { path: '/', label: 'Dashboard', icon: <HiHome /> },
    { path: '/generate', label: 'Generate Comments', icon: <HiCode /> },
    { path: '/compare', label: 'Model Comparison', icon: <HiChartBar /> },
    { path: '/history', label: 'History', icon: <HiClock /> },
    { path: '/about', label: 'About Research', icon: <HiInformationCircle /> },
];

function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">
                <h1>CodeComment AI</h1>
                <p>NLP-Based Comment Generator</p>
            </div>

            <nav className="sidebar-nav">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        end={item.path === '/'}
                        className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                    >
                        <span className="nav-icon">{item.icon}</span>
                        {item.label}
                    </NavLink>
                ))}
            </nav>

            <div className="sidebar-footer">
                <p>Final Year Project © 2026</p>
            </div>
        </aside>
    );
}

export default Sidebar;
