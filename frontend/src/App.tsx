import { useState } from 'react';
import axios from 'axios';
import { FileText, Send, Download, Loader2, Sparkles, Scale } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

interface GenerateResponse {
  success: boolean;
  message: string;
  document_type: string;
  file_path: string;
  download_url: string;
  metadata: any;
}

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        prompt: prompt,
        include_metadata: true,
        details: {}
      };

      // const response = await axios.post('http://localhost:8000/draft-document', payload);
      const response = await axios.post('https://llm-project-backend.vercel.app/draft-document', payload);
      setResult(response.data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to generate document. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result) return;
    try {
      // const response = await axios.get(`http://localhost:8000${result.download_url}`, {
      const response = await axios.get(`https://llm-project-backend.vercel.app${result.download_url}`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', result.file_path.split(/[\\/]/).pop() || 'document.docx');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("Download failed", err);
      // Fallback: open in new tab if blob fails
      // window.open(`http://localhost:8000${result.download_url}`, '_blank');
      window.open(`https://llm-project-backend.vercel.app${result.download_url}`, '_blank');
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <motion.header
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="app-header"
      >
        <div className="logo-container">
          <Scale className="logo-icon" size={24} />
          <h1>NVN@AI</h1>
        </div>
        <div className="status-badge">
          <span className="dot"></span> System Online
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="main-content">

        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="hero-section"
        >
          <div className="hero-title">
            Draft Legal Docs at the <br />
            <span className="highlight">Speed of Thought.</span>
          </div>
          <p className="hero-subtitle">
            Powered by NVN@AI. Instant, legally sound drafts for NDAs, Agreements, and Contracts.
          </p>
        </motion.div>

        {/* Input Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="glass-card"
        >
          <div className="input-header">
            <Sparkles className="icon-accent" size={24} color="#818cf8" />
            <h2>Describe your requirements</h2>
          </div>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ex: Draft a Non-Disclosure Agreement between TechCorp (Disclosing) and John Doe (Receiving) for 24 months..."
            className="prompt-input"
          />

          <div className="input-actions">
            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={loading || !prompt.trim()}
            >
              {loading ? (
                <>
                  <Loader2 className="spin" size={20} /> Generating...
                </>
              ) : (
                <>
                  Generate Draft <Send size={18} style={{ marginLeft: 4 }} />
                </>
              )}
            </button>
          </div>

          {error && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              className="error-message"
            >
              {error}
            </motion.div>
          )}
        </motion.div>

        {/* Result Card */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 20, opacity: 0 }}
              className="glass-card result-card"
            >
              <div className="result-content">
                <div className="result-main">
                  <div className="icon-box">
                    <FileText size={32} />
                  </div>
                  <div className="result-text">
                    <h3>Document Ready</h3>
                    <div className="doc-badge">
                      {result.document_type.replace('_', ' ')}
                    </div>
                  </div>
                </div>

                <button className="download-link" onClick={handleDownload}>
                  <Download size={20} /> Download DOCX
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>© 2025 NVN@AI. Architecture by Naveen.</p>
      </footer>
    </div>
  );
}

export default App;
