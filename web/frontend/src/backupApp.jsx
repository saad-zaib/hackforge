import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import { 
  Target, Shield, Cpu, TrendingUp, Play, Square, 
  RefreshCw, Trash2, Flag, Award, BarChart3 
} from 'lucide-react';
import './App.css';

const API_BASE = 'http://localhost:8000';

// ============================================================================
// Dashboard Component
// ============================================================================
function Dashboard() {
  const [stats, setStats] = useState(null);
  const [dockerStatus, setDockerStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // Refresh every 5s
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      // First check if API is reachable
      const healthCheck = await axios.get(`${API_BASE}/health`).catch(() => null);
      
      if (!healthCheck) {
        console.error('API not reachable at', API_BASE);
        setLoading(false);
        return;
      }

      // Load stats and docker status
      const statsPromise = axios.get(`${API_BASE}/api/stats`).catch(() => ({ data: {
        total_blueprints: 0,
        total_machines: 0,
        total_campaigns: 0
      }}));
      
      const dockerPromise = axios.get(`${API_BASE}/api/docker/status`).catch(() => ({ data: {
        running: 0,
        total: 0
      }}));
      
      const machinesPromise = axios.get(`${API_BASE}/api/machines`).catch(() => ({ data: [] }));

      const [statsRes, dockerRes, machinesRes] = await Promise.all([
        statsPromise,
        dockerPromise,
        machinesPromise
      ]);
      
      // Override stats with actual data
      const actualStats = {
        total_blueprints: statsRes.data.total_blueprints || 2,
        total_machines: machinesRes.data.length || 0,
        total_campaigns: statsRes.data.total_campaigns || 0
      };
      
      setStats(actualStats);
      setDockerStatus(dockerRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      // Set default values on error
      setStats({
        total_blueprints: 2,
        total_machines: 0,
        total_campaigns: 0
      });
      setDockerStatus({
        running: 0,
        total: 0
      });
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>🎯 Hackforge Dashboard</h1>
      
      <div className="stats-grid">
        <StatCard 
          icon={<Shield />}
          title="Blueprints"
          value={stats?.total_blueprints || 0}
          color="#00ff88"
        />
        <StatCard 
          icon={<Target />}
          title="Machines"
          value={stats?.total_machines || 0}
          color="#667eea"
        />
        <StatCard 
          icon={<Cpu />}
          title="Campaigns"
          value={stats?.total_campaigns || 0}
          color="#f093fb"
        />
        <StatCard 
          icon={<Play />}
          title="Running"
          value={dockerStatus?.running || 0}
          color="#4facfe"
        />
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <Link to="/campaigns/create" className="btn btn-primary">
            <Target size={20} />
            Create Campaign
          </Link>
          <Link to="/machines" className="btn btn-secondary">
            <Shield size={20} />
            View Machines
          </Link>
          <Link to="/docker" className="btn btn-accent">
            <Cpu size={20} />
            Docker Control
          </Link>
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// Stat Card Component
// ============================================================================
function StatCard({ icon, title, value, color }) {
  return (
    <div className="stat-card" style={{ borderColor: color }}>
      <div className="stat-icon" style={{ color }}>
        {icon}
      </div>
      <div className="stat-content">
        <div className="stat-value">{value}</div>
        <div className="stat-title">{title}</div>
      </div>
    </div>
  );
}

// ============================================================================
// Create Campaign Component
// ============================================================================
function CreateCampaign() {
  const [userId, setUserId] = useState('user_' + Math.random().toString(36).substr(2, 9));
  const [difficulty, setDifficulty] = useState(2);
  const [count, setCount] = useState(2);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleCreate = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE}/api/campaigns`, {
        user_id: userId,
        difficulty: parseInt(difficulty),
        count: parseInt(count)
      });

      setResult(response.data);
    } catch (error) {
      alert('Error creating campaign: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-campaign">
      <h1>🎯 Create New Campaign</h1>

      <div className="form-container">
        <div className="form-group">
          <label>User ID</label>
          <input 
            type="text" 
            value={userId} 
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter your user ID"
          />
        </div>

        <div className="form-group">
          <label>Difficulty Level: {difficulty}/5</label>
          <input 
            type="range" 
            min="1" 
            max="5" 
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          />
          <div className="difficulty-labels">
            <span>Easy</span>
            <span>Medium</span>
            <span>Hard</span>
          </div>
        </div>

        <div className="form-group">
          <label>Number of Machines</label>
          <select value={count} onChange={(e) => setCount(e.target.value)}>
            <option value="2">2 Machines</option>
            <option value="3">3 Machines</option>
            <option value="5">5 Machines (All)</option>
          </select>
        </div>

        <button 
          className="btn btn-primary btn-large" 
          onClick={handleCreate}
          disabled={loading}
        >
          {loading ? 'Creating Campaign...' : 'Create Campaign'}
        </button>
      </div>

      {result && (
        <div className="campaign-result">
          <h2>✅ Campaign Created!</h2>
          <div className="result-info">
            <p><strong>Campaign ID:</strong> {result.campaign_id}</p>
            <p><strong>Machines:</strong> {result.machines.length}</p>
          </div>

          <div className="machines-list">
            <h3>Your Machines:</h3>
            {result.machines.map((machine, idx) => (
              <div key={idx} className="machine-card">
                <div className="machine-header">
                  <h4>Machine {idx + 1}: {machine.variant}</h4>
                  <span className="difficulty-badge">Level {machine.difficulty}</span>
                </div>
                <div className="machine-details">
                  <p><strong>URL:</strong> <a href={machine.url} target="_blank" rel="noopener noreferrer">{machine.url}</a></p>
                  <p><strong>Flag:</strong> <code>{machine.flag}</code></p>
                </div>
              </div>
            ))}
          </div>

          <div className="next-steps">
            <h3>Next Steps:</h3>
            <ol>
              <li>Go to <Link to="/docker">Docker Control</Link> and start containers</li>
              <li>Click on machine URLs above to access them</li>
              <li>Find vulnerabilities and capture flags!</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Machines List Component
// ============================================================================
function MachinesList() {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMachines();
  }, []);

  const loadMachines = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/machines`);
      setMachines(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading machines:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading machines...</div>;
  }

  return (
    <div className="machines-page">
      <h1>🎯 Available Machines</h1>

      {machines.length === 0 ? (
        <div className="empty-state">
          <p>No machines available yet.</p>
          <Link to="/campaigns/create" className="btn btn-primary">
            Create Campaign
          </Link>
        </div>
      ) : (
        <div className="machines-grid">
          {machines.map((machine) => (
            <div key={machine.machine_id} className="machine-item">
              <div className="machine-item-header">
                <h3>{machine.variant}</h3>
                <span className="difficulty-badge">Level {machine.difficulty}</span>
              </div>
              <div className="machine-item-body">
                <p><strong>ID:</strong> <code>{machine.machine_id.slice(0, 12)}...</code></p>
                <p><strong>Category:</strong> {machine.blueprint_id}</p>
              </div>
              <div className="machine-item-actions">
                <button className="btn btn-small btn-primary">
                  <Flag size={16} />
                  Submit Flag
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Docker Control Component
// ============================================================================
function DockerControl() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const loadStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/docker/status`);
      setStatus(response.data);
    } catch (error) {
      console.error('Error loading status:', error);
    }
  };

  const handleStart = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/docker/start`);
      alert('Containers are starting... This may take a few minutes.');
      setTimeout(loadStatus, 5000);
    } catch (error) {
      alert('Error starting containers: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/docker/stop`);
      alert('Containers stopped successfully');
      loadStatus();
    } catch (error) {
      alert('Error stopping containers: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRestart = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/docker/restart`);
      alert('Containers restarted successfully');
      loadStatus();
    } catch (error) {
      alert('Error restarting containers: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDestroy = async () => {
    if (!window.confirm('Are you sure? This will remove all containers.')) {
      return;
    }

    setLoading(true);
    try {
      await axios.delete(`${API_BASE}/api/docker/destroy`);
      alert('Containers destroyed successfully');
      loadStatus();
    } catch (error) {
      alert('Error destroying containers: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="docker-control">
      <h1>🐳 Docker Control Panel</h1>

      <div className="docker-status">
        <h2>Status</h2>
        <div className="status-info">
          <div className="status-item">
            <span>Total Containers:</span>
            <strong>{status?.total || 0}</strong>
          </div>
          <div className="status-item">
            <span>Running:</span>
            <strong className="status-running">{status?.running || 0}</strong>
          </div>
        </div>
      </div>

      <div className="docker-actions">
        <h2>Actions</h2>
        <div className="action-grid">
          <button 
            className="btn btn-success" 
            onClick={handleStart}
            disabled={loading}
          >
            <Play size={20} />
            Start All
          </button>

          <button 
            className="btn btn-warning" 
            onClick={handleStop}
            disabled={loading}
          >
            <Square size={20} />
            Stop All
          </button>

          <button 
            className="btn btn-info" 
            onClick={handleRestart}
            disabled={loading}
          >
            <RefreshCw size={20} />
            Restart All
          </button>

          <button 
            className="btn btn-danger" 
            onClick={handleDestroy}
            disabled={loading}
          >
            <Trash2 size={20} />
            Destroy All
          </button>
        </div>
      </div>

      {status && status.containers && status.containers.length > 0 && (
        <div className="containers-list">
          <h2>Containers</h2>
          {status.containers.map((container, idx) => (
            <div key={idx} className="container-item">
              <div className="container-info">
                <span className={`status-dot ${container.State}`}></span>
                <strong>{container.Name}</strong>
                <span className="container-state">{container.State}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Main App Component
// ============================================================================
function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-brand">
            <Shield className="brand-icon" />
            <span>Hackforge</span>
          </div>
          <div className="nav-links">
            <Link to="/">Dashboard</Link>
            <Link to="/campaigns/create">Create Campaign</Link>
            <Link to="/machines">Machines</Link>
            <Link to="/docker">Docker</Link>
          </div>
        </nav>

        <div className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/campaigns/create" element={<CreateCampaign />} />
            <Route path="/machines" element={<MachinesList />} />
            <Route path="/docker" element={<DockerControl />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
