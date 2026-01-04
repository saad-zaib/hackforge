import React, { useState, useEffect } from 'react';
import { Terminal, Play, Square, RefreshCw, Trash2, Activity, Loader, CheckCircle, AlertCircle, Server } from 'lucide-react';
import api from '../services/api';

const DockerControl = () => {
  const [containers, setContainers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [stats, setStats] = useState({ total: 0, running: 0 });

  useEffect(() => {
    fetchDockerStatus();
    // Poll status every 3 seconds
    const interval = setInterval(fetchDockerStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchDockerStatus = async () => {
    try {
      const data = await api.getDockerStatus();
      setContainers(data.containers || []);
      setStats({
        total: data.total || 0,
        running: data.running || 0
      });
      setIsLoading(false);
      setError(null);
    } catch (err) {
      console.error('Error fetching docker status:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  const handleAction = async (action, actionName) => {
    try {
      setActionLoading(actionName);
      setError(null);
      setSuccess(null);

      const result = await action();
      setSuccess(result.message || `${actionName} completed successfully`);
      
      // Wait a bit then refresh
      setTimeout(() => {
        fetchDockerStatus();
        setActionLoading(null);
      }, 1000);
    } catch (err) {
      setError(err.message);
      setActionLoading(null);
    }
  };

  const ActionButton = ({ icon: Icon, label, onClick, color, disabled }) => (
    <button
      onClick={onClick}
      disabled={disabled || actionLoading}
      className={`flex-1 p-4 rounded-xl border transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed group`}
      style={{
        backgroundColor: `${color}10`,
        borderColor: `${color}40`,
      }}
    >
      <div className="flex flex-col items-center gap-2">
        {actionLoading === label ? (
          <Loader className="w-6 h-6 animate-spin" style={{ color }} />
        ) : (
          <Icon className="w-6 h-6 group-hover:scale-110 transition-transform" style={{ color }} />
        )}
        <span className="text-sm font-semibold text-white">{label}</span>
      </div>
    </button>
  );

  const ContainerCard = ({ container }) => {
    const isRunning = container.State === 'running';
    
    return (
      <div className="p-4 rounded-xl bg-black/30 border border-gray-800 hover:border-orange-500/50 transition-all duration-300">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
            <div>
              <h4 className="text-white font-semibold">{container.Name || container.Names?.[0] || 'Unknown'}</h4>
              <p className="text-xs text-gray-500">
                {container.Image || 'No image info'}
              </p>
            </div>
          </div>
          <div className={`px-3 py-1 rounded-lg text-xs font-semibold ${
            isRunning 
              ? 'bg-green-950/30 text-green-400 border border-green-500/30' 
              : 'bg-gray-900 text-gray-500 border border-gray-700'
          }`}>
            {container.State || 'unknown'}
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading Docker status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-blue-500 to-blue-600 bg-clip-text text-transparent">
            Docker Control Panel
          </h1>
          <p className="text-gray-400">Manage your container infrastructure</p>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Status Overview</h3>
              <Activity className="w-5 h-5 text-blue-500" />
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Total Containers</span>
                <span className="text-2xl font-bold text-white">{stats.total}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Running</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-2xl font-bold text-green-500">{stats.running}</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Stopped</span>
                <span className="text-2xl font-bold text-gray-500">{stats.total - stats.running}</span>
              </div>
            </div>
          </div>

          {/* Action Controls */}
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Actions</h3>
              <Terminal className="w-5 h-5 text-blue-500" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <ActionButton
                icon={Play}
                label="Start All"
                color="#10b981"
                onClick={() => handleAction(api.startContainers, 'Start All')}
              />
              <ActionButton
                icon={Square}
                label="Stop All"
                color="#f97316"
                onClick={() => handleAction(api.stopContainers, 'Stop All')}
              />
              <ActionButton
                icon={RefreshCw}
                label="Restart All"
                color="#3b82f6"
                onClick={() => handleAction(api.restartContainers, 'Restart All')}
              />
              <ActionButton
                icon={Trash2}
                label="Destroy All"
                color="#ef4444"
                onClick={() => {
                  if (window.confirm('⚠️ This will permanently delete all containers. Are you sure?')) {
                    handleAction(api.destroyContainers, 'Destroy All');
                  }
                }}
              />
            </div>
          </div>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-950/20 border border-red-500/50 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 rounded-xl bg-green-950/20 border border-green-500/50 flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
            <p className="text-green-400">{success}</p>
          </div>
        )}

        {/* Containers List */}
        <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Server className="w-5 h-5 text-blue-500" />
              Containers
            </h3>
            <button
              onClick={fetchDockerStatus}
              disabled={actionLoading}
              className="p-2 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${actionLoading ? 'animate-spin' : ''}`} />
            </button>
          </div>

          {containers.length === 0 ? (
            <div className="text-center py-12">
              <Server className="w-16 h-16 text-gray-700 mx-auto mb-4" />
              <h4 className="text-xl font-bold text-gray-600 mb-2">No Containers Found</h4>
              <p className="text-gray-500 mb-6">Create a campaign to generate containers</p>
              <button
                onClick={() => window.location.href = '/campaigns'}
                className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
              >
                Create Campaign
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {containers.map((container, index) => (
                <ContainerCard key={index} container={container} />
              ))}
            </div>
          )}
        </div>

        {/* Info Panel */}
        <div className="mt-6 p-4 rounded-xl bg-blue-950/20 border border-blue-500/30">
          <h4 className="text-sm font-semibold text-blue-400 mb-2 flex items-center gap-2">
            <Activity className="w-4 h-4" />
            Docker Management Tips
          </h4>
          <ul className="space-y-1 text-sm text-gray-400">
            <li>• <span className="text-blue-400">Start All</span>: Builds and launches all campaign containers</li>
            <li>• <span className="text-orange-400">Stop All</span>: Stops running containers (data preserved)</li>
            <li>• <span className="text-blue-400">Restart All</span>: Restarts all containers</li>
            <li>• <span className="text-red-400">Destroy All</span>: Removes all containers and volumes (permanent)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DockerControl;
