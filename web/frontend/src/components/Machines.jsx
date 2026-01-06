import React, { useState, useEffect } from 'react';
import { Server, Target, Flag, Loader, AlertCircle, CheckCircle, Send, ExternalLink, Play, Square, RotateCw, Trash2 } from 'lucide-react';
import api from '../services/api';

const Machines = () => {
  const [userId] = useState('user_default');
  const [machines, setMachines] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMachine, setSelectedMachine] = useState(null);
  const [flagInput, setFlagInput] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);
  const [containerAction, setContainerAction] = useState({});

  useEffect(() => {
    fetchMachines();
    // Refresh every 10 seconds
    const interval = setInterval(fetchMachines, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchMachines = async () => {
    try {
      setIsLoading(true);
      const data = await api.getMachines();
      console.log('Fetched machines:', data);
      setMachines(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching machines:', err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleContainerAction = async (containerId, action) => {
    if (!containerId) return;

    setContainerAction(prev => ({ ...prev, [containerId]: action }));

    try {
      let result;
      switch (action) {
        case 'start':
          result = await api.startContainer(containerId);
          break;
        case 'stop':
          result = await api.stopContainer(containerId);
          break;
        case 'restart':
          result = await api.restartContainer(containerId);
          break;
        default:
          return;
      }

      console.log(`Container ${action} result:`, result);
      
      // Refresh machines after action
      setTimeout(fetchMachines, 2000);
    } catch (err) {
      console.error(`Error ${action} container:`, err);
      alert(`Failed to ${action} container: ${err.message}`);
    } finally {
      setContainerAction(prev => ({ ...prev, [containerId]: null }));
    }
  };

  const handleSubmitFlag = async (machineId) => {
    if (!flagInput.trim()) return;

    try {
      setSubmitting(true);
      setSubmitResult(null);

      const result = await api.validateFlag(machineId, flagInput, userId);
      setSubmitResult(result);

      if (result.correct) {
        setFlagInput('');
        setTimeout(fetchMachines, 2000);
      }
    } catch (err) {
      setSubmitResult({
        correct: false,
        message: err.message,
        points: 0
      });
    } finally {
      setSubmitting(false);
    }
  };

  const getDifficultyColor = (level) => {
    const colors = {
      1: '#10b981',
      2: '#3b82f6',
      3: '#f59e0b',
      4: '#f97316',
      5: '#ef4444'
    };
    return colors[level] || '#ff7300';
  };

  const getDifficultyLabel = (level) => {
    const labels = {
      1: 'Beginner',
      2: 'Easy',
      3: 'Medium',
      4: 'Hard',
      5: 'Expert'
    };
    return labels[level] || 'Unknown';
  };

  const getContainerStatusColor = (status) => {
    switch (status) {
      case 'running':
        return '#10b981';
      case 'exited':
        return '#ef4444';
      case 'paused':
        return '#f59e0b';
      default:
        return '#6b7280';
    }
  };

  if (isLoading && machines.length === 0) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading machines...</p>
        </div>
      </div>
    );
  }

  if (error && machines.length === 0) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-red-950/20 border border-red-500/50 rounded-2xl p-8 text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Error Loading Machines</h2>
          <p className="text-gray-400 mb-6">{error}</p>
          <button
            onClick={fetchMachines}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
              Available Machines
            </h1>
            <p className="text-gray-400">
              {machines.length} machine{machines.length !== 1 ? 's' : ''} ready for exploitation
            </p>
          </div>
          <button
            onClick={fetchMachines}
            disabled={isLoading}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <RotateCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {machines.length === 0 ? (
          <div className="text-center py-16">
            <Server className="w-24 h-24 text-gray-700 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-gray-600 mb-2">No Machines Available</h3>
            <p className="text-gray-500 mb-6">Create a campaign to generate machines</p>
            <button
              onClick={() => window.location.href = '/campaigns'}
              className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
            >
              Create Campaign
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {machines.map((machine, index) => (
              <div
                key={machine.machine_id}
                className="group relative rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6 hover:border-orange-500/50 transition-all duration-300"
                style={{
                  animation: `slideUp 0.4s ease-out ${index * 0.1}s both`
                }}
              >
                {/* Machine Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div
                      className="p-3 rounded-xl"
                      style={{ backgroundColor: `${getDifficultyColor(machine.difficulty)}20` }}
                    >
                      <Target className="w-6 h-6" style={{ color: getDifficultyColor(machine.difficulty) }} />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white">{machine.variant}</h3>
                      <p className="text-sm text-gray-500">{machine.blueprint_id}</p>
                      {machine.campaign_name && (
                        <p className="text-xs text-orange-500 mt-1">Campaign: {machine.campaign_name}</p>
                      )}
                    </div>
                  </div>

                  <div
                    className="px-3 py-1 rounded-lg text-xs font-semibold"
                    style={{
                      backgroundColor: `${getDifficultyColor(machine.difficulty)}20`,
                      color: getDifficultyColor(machine.difficulty)
                    }}
                  >
                    Level {machine.difficulty}
                  </div>
                </div>

                {/* Container Status & Controls */}
                {machine.container && (
                  <div className="mb-4 p-3 rounded-lg bg-black/30 border border-gray-800">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: getContainerStatusColor(machine.container.status) }}
                        />
                        <span className="text-xs text-gray-400">
                          Container: {machine.container.status}
                        </span>
                      </div>

                      {/* Container Controls */}
                      <div className="flex gap-1">
                        {machine.container.status !== 'running' ? (
                          <button
                            onClick={() => handleContainerAction(machine.container.container_id, 'start')}
                            disabled={containerAction[machine.container.container_id] === 'start'}
                            className="p-1.5 bg-green-500/20 hover:bg-green-500/30 rounded text-green-500 transition-colors"
                            title="Start Container"
                          >
                            {containerAction[machine.container.container_id] === 'start' ? (
                              <Loader className="w-3 h-3 animate-spin" />
                            ) : (
                              <Play className="w-3 h-3" />
                            )}
                          </button>
                        ) : (
                          <button
                            onClick={() => handleContainerAction(machine.container.container_id, 'stop')}
                            disabled={containerAction[machine.container.container_id] === 'stop'}
                            className="p-1.5 bg-red-500/20 hover:bg-red-500/30 rounded text-red-500 transition-colors"
                            title="Stop Container"
                          >
                            {containerAction[machine.container.container_id] === 'stop' ? (
                              <Loader className="w-3 h-3 animate-spin" />
                            ) : (
                              <Square className="w-3 h-3" />
                            )}
                          </button>
                        )}

                        <button
                          onClick={() => handleContainerAction(machine.container.container_id, 'restart')}
                          disabled={containerAction[machine.container.container_id] === 'restart'}
                          className="p-1.5 bg-blue-500/20 hover:bg-blue-500/30 rounded text-blue-500 transition-colors"
                          title="Restart Container"
                        >
                          {containerAction[machine.container.container_id] === 'restart' ? (
                            <Loader className="w-3 h-3 animate-spin" />
                          ) : (
                            <RotateCw className="w-3 h-3" />
                          )}
                        </button>
                      </div>
                    </div>

                    {machine.url && machine.is_running && (
                      <a
                        href={machine.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 text-sm text-orange-500 hover:text-orange-400 transition-colors"
                      >
                        <ExternalLink className="w-4 h-4" />
                        {machine.url}
                      </a>
                    )}
                  </div>
                )}

                {/* Machine Info */}
                <div className="space-y-3 mb-4">
                  <div className="p-3 rounded-lg bg-black/30 border border-gray-800">
                    <p className="text-xs text-gray-500 mb-1">Machine ID</p>
                    <code className="text-orange-500 text-sm font-mono">{machine.machine_id}</code>
                  </div>

                  {/* Progress Indicator */}
                  {machine.solved && (
                    <div className="p-3 rounded-lg bg-green-950/20 border border-green-500/50 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-500" />
                      <span className="text-sm text-green-400">
                        Solved! +{machine.points_earned} points
                      </span>
                    </div>
                  )}

                  {machine.attempts > 0 && !machine.solved && (
                    <div className="p-3 rounded-lg bg-orange-950/20 border border-orange-500/50">
                      <span className="text-xs text-orange-400">
                        {machine.attempts} attempt{machine.attempts !== 1 ? 's' : ''} made
                      </span>
                    </div>
                  )}
                </div>

                {/* Flag Submission */}
                <div className="space-y-3">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Enter flag here..."
                      value={selectedMachine === machine.machine_id ? flagInput : ''}
                      onFocus={() => setSelectedMachine(machine.machine_id)}
                      onChange={(e) => {
                        setSelectedMachine(machine.machine_id);
                        setFlagInput(e.target.value);
                        setSubmitResult(null);
                      }}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          handleSubmitFlag(machine.machine_id);
                        }
                      }}
                      disabled={machine.solved}
                      className="flex-1 px-4 py-2 bg-black/50 border border-gray-800 rounded-lg text-white focus:outline-none focus:border-orange-500 transition-colors text-sm disabled:opacity-50"
                    />
                    <button
                      onClick={() => handleSubmitFlag(machine.machine_id)}
                      disabled={submitting || !flagInput.trim() || machine.solved}
                      className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-700 text-white rounded-lg transition-colors flex items-center gap-2"
                    >
                      {submitting && selectedMachine === machine.machine_id ? (
                        <Loader className="w-4 h-4 animate-spin" />
                      ) : (
                        <Send className="w-4 h-4" />
                      )}
                    </button>
                  </div>

                  {/* Submission Result */}
                  {submitResult && selectedMachine === machine.machine_id && (
                    <div
                      className={`p-3 rounded-lg border flex items-center gap-2 ${
                        submitResult.correct
                          ? 'bg-green-950/20 border-green-500/50'
                          : 'bg-red-950/20 border-red-500/50'
                      }`}
                    >
                      {submitResult.correct ? (
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                      ) : (
                        <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                      )}
                      <div className="flex-1">
                        <p className={`text-sm font-medium ${submitResult.correct ? 'text-green-400' : 'text-red-400'}`}>
                          {submitResult.message}
                        </p>
                        {submitResult.points > 0 && (
                          <p className="text-xs text-gray-400 mt-1">
                            +{submitResult.points} points earned!
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* Bottom Border Animation */}
                <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 to-orange-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500" />
              </div>
            ))}
          </div>
        )}
      </div>

      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default Machines;
