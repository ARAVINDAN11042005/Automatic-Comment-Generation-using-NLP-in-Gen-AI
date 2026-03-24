import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Generate from './pages/Generate';
import Compare from './pages/Compare';
import Chatbot from './pages/Chatbot';
import History from './pages/History';
import About from './pages/About';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/generate" element={<Generate />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/history" element={<History />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
