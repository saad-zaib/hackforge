import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Target, Shield, Play, Square, RefreshCw, Trash2, Loader, 
  AlertCircle, CheckCircle, ArrowLeft, Send, FileText, Activity,
  TrendingUp, Trophy, ChevronRight
} from 'lucide-react';
import api from '../services/api';

const CampaignDetail = () => {
  const { campaignId } = useParams();
  const navigate = useNavigate();
  const [userId] = useState('user_default');
  
  const [campaign, setCampaign] = useState(null);
  const [containers, setContainers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState({});
  const [success, setSuccess] = useState(null);
  
  // Flag submission
  const [selectedMachine, setSelectedMachine] = useState(null);
  const [flagInput, setFlagInput] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);
  
  // Container logs
  const [containerLogs, setContainerLogs] = useState(null);

  useEffect(() => {
    fetchCampaignData();
    const interval = setInterval(fetchContainers, 3000);
    return () => clearInterval(interval);
  }, [campaignId]);

  const fetchCampaignData = async () => {
    try {
      setIsLoading(true);
      const data = await api.getCampaign(campaignId);
      setCampaign(data);
      await fetchContainers();
      setIsLoading(false);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  const fetchContainers = async () => {
    try {
      const data = await api.getCampaignContainers(campaignId);
      setContainers(data.containers || []);
    } catch (err) {
      console.error('Error fetching containers:', err);
    }
  };

  const handleContainerAction = async (containerId, actionFunc, actionName) => {
    const key = `${actionName}-${containerId}`;
    try {
      setActionLoading(prev => ({ ...prev, [key]: true }));
      setError(null);
      setSuccess(null);

      await actionFunc(containerId);
      setSuccess(`${actionName} completed successfully`);
      
      setTimeout(() => {
        fetchContainers();
        setActionLoading(prev => ({ ...prev, [key]: false }));
        setSuccess(null);
      }, 1500);
    } catch (err) {
      setError(`Failed to ${actionName.toLowerCase()}: ${err.message}`);
      setActionLoading(prev => ({ ...prev, [key]: false }));
    }
  };

  const handleViewLogs = async (containerId, containerName) => {
    try {
      setError(null);
      const logs = await api.getContainerLogs(containerId);
      setContainerLogs({ 
        containerId, 
        containerName,
        logs: logs.logs || 'No logs available' 
      });
    } catch (err) {
      setError(`Failed to fetch logs: ${err.message}`);
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
        setTimeout(() => {
          fetchCampaignData();
        }, 2000);
      }
      
      setSubmitting(false);
    } catch (err) {
      setSubmitResult({
        correct: false,
        message: err.message,
        points: 0
      });
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

  const getContainerForMachine = (machineId) => {
    return containers.find(c => c.machine_id === machineId);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading campaign...</p>
        </div>
      </div>
    );
  }

  if (error && !campaign) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-red-950/20 border border-red-500/50 rounded-2xl p-8 text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Error Loading Campaign</h2>
          <p className="text-gray-400 mb-6">{error}</p>
          <button
            onClick={() => navigate('/campaigns')}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
          >
            Back to Campaigns
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate('/campaigns')}
          className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Campaigns
        </button>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
            {campaign?.campaign_name || 'Campaign Details'}
          </h1>
          <p className="text-gray-400">
            Difficulty Level {campaign?.difficulty} • {campaign?.machine_count} Machines
          </p>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-950/20 border border-red-500/50 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <p className="text-red-400 flex-1">{error}</p>
            <button onClick={() => setError(null)} className="text-red-400 hover:text-red-300 text-xl font-bold">
              ×
            </button>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 rounded-xl bg-green-950/20 border border-green-500/50 flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
            <p className="text-green-400">{success}</p>
          </div>
        )}

        {/* Progress Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center gap-3 mb-3">
              <Target className="w-6 h-6 text-orange-500" />
              <h3 className="text-lg font-bold">Progress</h3>
            </div>
            <div className="text-3xl font-bold text-white mb-2">
              {campaign?.progress?.solved || 0}/{campaign?.progress?.total || 0}
            </div>
            <div className="h-2 bg-gray-900 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-orange-500 to-orange-600"
                style={{ width: `${campaign?.progress?.percentage || 0}%` }}
              />
            </div>
          </div>

          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center gap-3 mb-3">
              <Trophy className="w-6 h-6 text-yellow-500" />
              <h3 className="text-lg font-bold">Points</h3>
            </div>
            <div className="text-3xl font-bold text-yellow-500">
              {campaign?.progress?.total_points || 0}
            </div>
            <p className="text-sm text-gray-400 mt-2">Total earned</p>
          </div>

          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center gap-3 mb-3">
              <Activity className="w-6 h-6 text-green-500" />
              <h3 className="text-lg font-bold">Running</h3>
            </div>
            <div className="text-3xl font-bold text-green-500">
              {containers.filter(c => c.State === 'running').length}
            </div>
            <p className="text-sm text-gray-400 mt-2">Active containers</p>
          </div>
        </div>

        {/* Machines List */}
        <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <Shield className="w-6 h-6 text-orange-500" />
            Machines
          </h2>

          <div className="space-y-4">
            {campaign?.machines?.map((machine, index) => {
              const container = getContainerForMachine(machine.machine_id);
              const isRunning = container?.State === 'running';
              const containerId = container?.Id || '';
              
              const startKey = `Start-${containerId}`;
              const stopKey = `Stop-${containerId}`;
              const restartKey = `Restart-${containerId}`;

              return (
                <div
                  key={machine.machine_id}
                  className="p-6 rounded-xl bg-black/30 border border-gray-800 hover:border-orange-500/50 transition-all duration-300"
                >
                  {/* Machine Header */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-4">
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-lg"
                        style={{ backgroundColor: getDifficultyColor(machine.difficulty) }}
                      >
                        {index + 1}
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-white">{machine.variant}</h3>
                        <p className="text-sm text-gray-500">
                          {machine.blueprint_id} • Level {machine.difficulty}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      {machine.solved && (
                        <div className="px-3 py-1 rounded-lg bg-green-950/30 text-green-400 border border-green-500/30 text-sm font-semibold flex items-center gap-2">
                          <CheckCircle className="w-4 h-4" />
                          Solved
                        </div>
                      )}
                      {container && (
                        <div className={`px-3 py-1 rounded-lg text-sm font-semibold flex items-center gap-2 ${
                          isRunning 
                            ? 'bg-green-950/30 text-green-400 border border-green-500/30' 
                            : 'bg-gray-900 text-gray-500 border border-gray-700'
                        }`}>
                          <div className={`w-2 h-2 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
                          {container.State}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Machine Info */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="p-3 rounded-lg bg-gray-900/50">
                      <p className="text-xs text-gray-500 mb-1">Machine ID</p>
                      <code className="text-orange-500 text-sm font-mono">{machine.machine_id.substring(0, 16)}...</code>
                    </div>
                    {machine.port && (
                      <div className="p-3 rounded-lg bg-gray-900/50">
                        <p className="text-xs text-gray-500 mb-1">Access URL</p>
                        <code className="text-blue-500 text-sm">http://localhost:{machine.port}</code>
                      </div>
                    )}
                  </div>

                  {/* Docker Controls */}
                  {container && (
                    <div className="mb-4">
                      <div className="grid grid-cols-4 gap-2">
                        <button
                          onClick={() => handleContainerAction(containerId, api.startContainer, 'Start')}
                          disabled={isRunning || actionLoading[startKey]}
                          className="p-3 rounded-lg bg-green-500/20 hover:bg-green-500/30 disabled:opacity-50 border border-green-500/40 transition-all group"
                        >
                          <div className="flex flex-col items-center gap-1">
                            {actionLoading[startKey] ? (
                              <Loader className="w-4 h-4 text-green-500 animate-spin" />
                            ) : (
                              <Play className="w-4 h-4 text-green-500" />
                            )}
                            <span className="text-xs font-semibold text-green-500">Start</span>
                          </div>
                        </button>

                        <button
                          onClick={() => handleContainerAction(containerId, api.stopContainer, 'Stop')}
                          disabled={!isRunning || actionLoading[stopKey]}
                          className="p-3 rounded-lg bg-orange-500/20 hover:bg-orange-500/30 disabled:opacity-50 border border-orange-500/40 transition-all"
                        >
                          <div className="flex flex-col items-center gap-1">
                            {actionLoading[stopKey] ? (
                              <Loader className="w-4 h-4 text-orange-500 animate-spin" />
                            ) : (
                              <Square className="w-4 h-4 text-orange-500" />
                            )}
                            <span className="text-xs font-semibold text-orange-500">Stop</span>
                          </div>
                        </button>

                        <button
                          onClick={() => handleContainerAction(containerId, api.restartContainer, 'Restart')}
                          disabled={!isRunning || actionLoading[restartKey]}
                          className="p-3 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 disabled:opacity-50 border border-blue-500/40 transition-all"
                        >
                          <div className="flex flex-col items-center gap-1">
                            {actionLoading[restartKey] ? (
                              <Loader className="w-4 h-4 text-blue-500 animate-spin" />
                            ) : (
                              <RefreshCw className="w-4 h-4 text-blue-500" />
                            )}
                            <span className="text-xs font-semibold text-blue-500">Restart</span>
                          </div>
                        </button>

                        <button
                          onClick={() => handleViewLogs(containerId, container.Name)}
                          className="p-3 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 transition-all"
                        >
                          <div className="flex flex-col items-center gap-1">
                            <FileText className="w-4 h-4 text-purple-500" />
                            <span className="text-xs font-semibold text-purple-500">Logs</span>
                          </div>
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Flag Submission */}
                  {!machine.solved && (
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
                          className="flex-1 px-4 py-2 bg-black/50 border border-gray-800 rounded-lg text-white focus:outline-none focus:border-orange-500 transition-colors text-sm"
                        />
                        <button
                          onClick={() => handleSubmitFlag(machine.machine_id)}
                          disabled={submitting || !flagInput.trim()}
                          className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-700 text-white rounded-lg transition-colors flex items-center gap-2"
                        >
                          {submitting && selectedMachine === machine.machine_id ? (
                            <Loader className="w-4 h-4 animate-spin" />
                          ) : (
                            <Send className="w-4 h-4" />
                          )}
                        </button>
                      </div>

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
                  )}

                  {/* Stats */}
                  {machine.attempts > 0 && (
                    <div className="mt-4 pt-4 border-t border-gray-800 flex items-center gap-4 text-sm text-gray-400">
                      <span>Attempts: {machine.attempts}</span>
                      {machine.points_earned > 0 && (
                        <span>Points: <span className="text-orange-500 font-semibold">+{machine.points_earned}</span></span>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Container Logs Modal */}
        {containerLogs && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6">
            <div className="bg-gray-900 rounded-2xl border border-gray-800 max-w-4xl w-full max-h-[80vh] overflow-hidden">
              <div className="p-6 border-b border-gray-800 flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Container Logs</h3>
                  <p className="text-sm text-gray-400">{containerLogs.containerName}</p>
                </div>
                <button 
                  onClick={() => setContainerLogs(null)}
                  className="text-gray-400 hover:text-white text-2xl font-bold"
                >
                  ×
                </button>
              </div>
              <div className="p-6 overflow-auto max-h-[calc(80vh-100px)]">
                <pre className="text-xs text-green-400 font-mono bg-black/50 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
                  {containerLogs.logs}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CampaignDetail;
