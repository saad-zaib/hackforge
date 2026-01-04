import React, { useState } from 'react';
import { Zap, Plus, Target, AlertCircle, CheckCircle, Loader, ChevronRight, Shield } from 'lucide-react';
import api from '../services/api';

const Campaigns = () => {
  const [userId] = useState('user_default'); // Replace with actual auth
  const [isCreating, setIsCreating] = useState(false);
  const [difficulty, setDifficulty] = useState(2);
  const [machineCount, setMachineCount] = useState(5);
  const [createdCampaign, setCreatedCampaign] = useState(null);
  const [error, setError] = useState(null);

  const handleCreateCampaign = async () => {
    try {
      setIsCreating(true);
      setError(null);
      
      const campaign = await api.createCampaign(userId, difficulty, machineCount);
      setCreatedCampaign(campaign);
      setIsCreating(false);
    } catch (err) {
      setError(err.message);
      setIsCreating(false);
    }
  };

  const getDifficultyColor = (level) => {
    const colors = {
      1: '#10b981', // green
      2: '#3b82f6', // blue
      3: '#f59e0b', // amber
      4: '#f97316', // orange
      5: '#ef4444'  // red
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

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
            Campaign Creator
          </h1>
          <p className="text-gray-400">Generate custom cybersecurity challenges</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Creation Form */}
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-8">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-orange-500/20">
                <Plus className="w-6 h-6 text-orange-500" />
              </div>
              Create New Campaign
            </h2>

            {/* Difficulty Selector */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-400 mb-3">
                Difficulty Level
              </label>
              <div className="grid grid-cols-5 gap-2">
                {[1, 2, 3, 4, 5].map((level) => (
                  <button
                    key={level}
                    onClick={() => setDifficulty(level)}
                    className={`p-3 rounded-xl border transition-all duration-300 ${
                      difficulty === level
                        ? 'border-orange-500 bg-orange-500/20 scale-105'
                        : 'border-gray-800 hover:border-gray-700'
                    }`}
                    style={{
                      borderColor: difficulty === level ? getDifficultyColor(level) : undefined,
                      backgroundColor: difficulty === level ? `${getDifficultyColor(level)}20` : undefined
                    }}
                  >
                    <div className="text-center">
                      <Shield 
                        className="w-6 h-6 mx-auto mb-1"
                        style={{ color: difficulty === level ? getDifficultyColor(level) : '#6b7280' }}
                      />
                      <div className="text-xs font-semibold" style={{ color: difficulty === level ? getDifficultyColor(level) : '#9ca3af' }}>
                        {level}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
              <p className="mt-2 text-sm text-center" style={{ color: getDifficultyColor(difficulty) }}>
                {getDifficultyLabel(difficulty)}
              </p>
            </div>

            {/* Machine Count */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-gray-400 mb-3">
                Number of Machines
              </label>
              <div className="relative">
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={machineCount}
                  onChange={(e) => setMachineCount(parseInt(e.target.value) || 1)}
                  className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                />
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 text-sm">
                  machines
                </div>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mb-6 p-4 rounded-xl bg-red-950/20 border border-red-500/50 flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            {/* Create Button */}
            <button
              onClick={handleCreateCampaign}
              disabled={isCreating}
              className="w-full py-4 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 disabled:from-gray-700 disabled:to-gray-800 text-white font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-3 group"
            >
              {isCreating ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Creating Campaign...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 group-hover:scale-110 transition-transform" />
                  Generate Campaign
                </>
              )}
            </button>
          </div>

          {/* Campaign Result */}
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-8">
            {createdCampaign ? (
              <div className="space-y-6">
                {/* Success Header */}
                <div className="flex items-center gap-3 p-4 rounded-xl bg-green-950/20 border border-green-500/50">
                  <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-bold text-green-400">Campaign Created!</h3>
                    <p className="text-sm text-gray-400">Your machines are ready to deploy</p>
                  </div>
                </div>

                {/* Campaign Info */}
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 rounded-lg bg-black/30">
                    <span className="text-gray-400">Campaign ID</span>
                    <code className="text-orange-500 font-mono text-sm">{createdCampaign.campaign_id}</code>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-lg bg-black/30">
                    <span className="text-gray-400">Difficulty</span>
                    <span className="font-semibold" style={{ color: getDifficultyColor(createdCampaign.difficulty) }}>
                      Level {createdCampaign.difficulty}
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-lg bg-black/30">
                    <span className="text-gray-400">Machines</span>
                    <span className="text-white font-semibold">{createdCampaign.machines.length}</span>
                  </div>
                </div>

                {/* Machines List */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">Your Machines</h4>
                  <div className="space-y-2">
                    {createdCampaign.machines.map((machine, index) => (
                      <div
                        key={machine.machine_id}
                        className="p-4 rounded-xl bg-black/30 border border-gray-800 hover:border-orange-500/50 transition-all duration-300 group"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-3">
                            <div 
                              className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm"
                              style={{ backgroundColor: getDifficultyColor(machine.difficulty) }}
                            >
                              {index + 1}
                            </div>
                            <div>
                              <h5 className="text-white font-semibold">{machine.variant}</h5>
                              <p className="text-xs text-gray-500">Level {machine.difficulty}</p>
                            </div>
                          </div>
                          <Target className="w-5 h-5 text-gray-600 group-hover:text-orange-500 transition-colors" />
                        </div>
                        
                        {machine.port && (
                          <div className="mt-2 p-2 rounded-lg bg-gray-900/50 border border-gray-800">
                            <p className="text-xs text-gray-500 mb-1">Access URL</p>
                            <code className="text-orange-500 text-sm">
                              http://localhost:{machine.port}
                            </code>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Next Steps */}
                <div className="p-4 rounded-xl bg-blue-950/20 border border-blue-500/30">
                  <h4 className="text-sm font-semibold text-blue-400 mb-2">Next Steps</h4>
                  <ol className="space-y-2 text-sm text-gray-400">
                    <li className="flex items-start gap-2">
                      <span className="text-blue-500 font-bold">1.</span>
                      <span>Go to Docker Control panel</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-500 font-bold">2.</span>
                      <span>Start your containers</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-500 font-bold">3.</span>
                      <span>Access machines via the URLs above</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-500 font-bold">4.</span>
                      <span>Find vulnerabilities and capture flags!</span>
                    </li>
                  </ol>
                </div>

                {/* Action Button */}
                <button
                  onClick={() => window.location.href = '/docker'}
                  className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 group"
                >
                  Go to Docker Control
                  <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-gray-600">
                  <Target className="w-16 h-16 mx-auto mb-4 opacity-20" />
                  <p>Configure and create a campaign to see results here</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Campaigns;
