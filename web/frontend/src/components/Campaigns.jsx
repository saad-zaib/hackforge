import React, { useState, useEffect } from 'react';
import { Zap, Plus, Target, AlertCircle, CheckCircle, Loader, ChevronRight, Shield, List, Eye, Check, Search, Layers, TrendingUp, Clock, ArrowUpRight, X, Filter } from 'lucide-react';

// ─── Category icons / colors ─────────────────────────────────────────────────
const CAT_META = {
  injection:      { color: '#3b82f6', label: 'Injection',      emoji: '💉' },
  authentication: { color: '#10b981', label: 'Authentication', emoji: '🔐' },
  authorization:  { color: '#f59e0b', label: 'Authorization',  emoji: '🛡️' },
  cryptography:   { color: '#8b5cf6', label: 'Cryptography',   emoji: '🔒' },
  web:            { color: '#ec4899', label: 'Web',            emoji: '🌐' },
  default:        { color: '#6b7280', label: 'Other',          emoji: '📦' },
};
const getCat = (c) => CAT_META[c] || CAT_META.default;

const DIFF_COLORS = { 1: '#10b981', 2: '#3b82f6', 3: '#f59e0b', 4: '#f97316', 5: '#ef4444' };
const DIFF_LABELS = { 1: 'Beginner', 2: 'Easy', 3: 'Medium', 4: 'Hard', 5: 'Expert' };
const getDiffColor = (l) => DIFF_COLORS[l] || '#ff7300';
const getDiffLabel = (l) => DIFF_LABELS[l] || 'Unknown';

// ─── Tiny animated progress ring ─────────────────────────────────────────────
const ProgressRing = ({ pct, size = 44, stroke = 4, color = '#ff7300' }) => {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;
  return (
    <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1f1f1f" strokeWidth={stroke} />
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={stroke}
        strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
        style={{ transition: 'stroke-dashoffset 0.6s ease' }} />
    </svg>
  );
};

// ─── Campaigns Page ──────────────────────────────────────────────────────────
const Campaigns = () => {
  const [userId] = useState('user_default');

  // Form state
  const [isCreating, setIsCreating] = useState(false);
  const [difficulty, setDifficulty] = useState(2);
  const [machineCount, setMachineCount] = useState(5);
  const [campaignName, setCampaignName] = useState('');
  const [createdCampaign, setCreatedCampaign] = useState(null);
  const [error, setError] = useState(null);

  // Blueprints
  const [blueprints, setBlueprints] = useState([]);
  const [selectedBlueprints, setSelectedBlueprints] = useState([]);
  const [loadingBlueprints, setLoadingBlueprints] = useState(true);
  const [bpSearch, setBpSearch] = useState('');
  const [bpFilter, setBpFilter] = useState('all');

  // Campaign list
  const [myCampaigns, setMyCampaigns] = useState([]);
  const [loadingCampaigns, setLoadingCampaigns] = useState(true);
  const [campaignSearch, setCampaignSearch] = useState('');

  // View mode
  const [showCreateForm, setShowCreateForm] = useState(false);

  // api
  const [api, setApi] = useState(null);

  useEffect(() => {
    import('../services/api').then(m => setApi(m.default));
  }, []);

  useEffect(() => {
    if (api) { fetchMyCampaigns(); fetchBlueprints(); }
  }, [api]);

  const fetchBlueprints = async () => {
    if (!api) return;
    try {
      setLoadingBlueprints(true);
      const data = await api.getBlueprints();
      setBlueprints(data);
      setSelectedBlueprints(data.map(bp => bp.blueprint_id));
    } catch (err) { console.error(err); }
    finally { setLoadingBlueprints(false); }
  };

  const fetchMyCampaigns = async () => {
    if (!api) return;
    try {
      setLoadingCampaigns(true);
      setMyCampaigns(await api.getUserCampaigns(userId));
    } catch (err) { console.error(err); }
    finally { setLoadingCampaigns(false); }
  };

  const toggleBp = (id) => setSelectedBlueprints(prev =>
    prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
  );

  const filteredBlueprints = blueprints.filter(bp => {
    const matchesSearch = bp.name.toLowerCase().includes(bpSearch.toLowerCase());
    const matchesFilter = bpFilter === 'all' || bp.category === bpFilter;
    return matchesSearch && matchesFilter;
  });

  const filteredCampaigns = myCampaigns.filter(c =>
    (c.campaign_name || '').toLowerCase().includes(campaignSearch.toLowerCase())
  );

  const handleCreateCampaign = async () => {
    if (!campaignName.trim()) { setError('Please enter a campaign name'); return; }
    if (selectedBlueprints.length === 0) { setError('Select at least one blueprint'); return; }
    try {
      setIsCreating(true); setError(null);
      const campaign = await api.createCampaign(userId, campaignName, difficulty, machineCount, selectedBlueprints);
      setCreatedCampaign(campaign);
      setCampaignName('');
      fetchMyCampaigns();
    } catch (err) { setError(err.message); }
    finally { setIsCreating(false); }
  };

  const navigateToCampaign = (id) => { window.location.href = `/campaigns/${id}`; };

  // ── Loading ──
  if (!api) return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <Loader className="w-10 h-10 text-orange-500 animate-spin" />
    </div>
  );

  // ── Main ──
  return (
    <div className="min-h-screen bg-black text-white relative">
      {/* Subtle top glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-64 rounded-full blur-3xl opacity-10 pointer-events-none" style={{ background: 'radial-gradient(ellipse, #ff7300, transparent 70%)' }} />

      <style>{`
        @keyframes fadeUp { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
        .anim-row { animation: fadeUp 0.4s ease both; }
      `}</style>

      <div className="relative z-10 max-w-7xl mx-auto px-5 py-7">

        {/* ── Header ── */}
        <div className="flex items-start justify-between mb-6" style={{ animation: 'fadeUp 0.35s ease both' }}>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-7 h-7 rounded-lg bg-orange-500/15 border border-orange-500/30 flex items-center justify-center">
                <Target className="w-4 h-4 text-orange-500" />
              </div>
              <h1 className="text-xl font-bold text-white">Campaign Manager</h1>
            </div>
            <p className="text-gray-600 text-sm ml-9">Create, manage, and track your cybersecurity campaigns</p>
          </div>
          <button onClick={() => { setShowCreateForm(true); setCreatedCampaign(null); setError(null); }}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-orange-500 hover:bg-orange-600 text-white text-sm font-semibold transition-all active:scale-95">
            <Plus className="w-4 h-4" /> New Campaign
          </button>
        </div>

        {/* ── Summary row ── */}
        <div className="grid grid-cols-3 gap-3 mb-6" style={{ animation: 'fadeUp 0.4s ease 0.06s both' }}>
          {[
            { icon: Layers, label: 'Total Campaigns', value: myCampaigns.length, color: '#ff7300' },
            { icon: CheckCircle, label: 'Completed', value: myCampaigns.filter(c => (c.progress_percentage || 0) >= 100).length, color: '#10b981' },
            { icon: TrendingUp, label: 'Blueprints Available', value: blueprints.length, color: '#60a5fa' },
          ].map((s, i) => (
            <div key={i} className="rounded-xl border border-gray-900 bg-gray-950/70 px-4 py-3 flex items-center gap-3">
              <div className="p-2 rounded-lg" style={{ background: s.color + '15' }}>
                <s.icon className="w-4 h-4" style={{ color: s.color }} />
              </div>
              <div>
                <p className="text-lg font-bold text-white tabular-nums">{s.value}</p>
                <p className="text-xs text-gray-600">{s.label}</p>
              </div>
            </div>
          ))}
        </div>

        {/* ── Create Form Modal Overlay ── */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-start justify-center p-6 pt-16 overflow-y-auto">
            <div className="bg-gray-950 border border-gray-800 rounded-2xl w-full max-w-2xl shadow-2xl" style={{ animation: 'fadeUp 0.3s ease both' }}>
              {/* header */}
              <div className="flex items-center justify-between px-6 pt-5 pb-4 border-b border-gray-900">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-orange-500/15 border border-orange-500/30 flex items-center justify-center">
                    <Plus className="w-4 h-4 text-orange-500" />
                  </div>
                  <h2 className="text-lg font-bold text-white">Create New Campaign</h2>
                </div>
                <button onClick={() => setShowCreateForm(false)} className="text-gray-600 hover:text-gray-300 transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="p-6 space-y-5">
                {/* Name */}
                <div>
                  <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Campaign Name *</label>
                  <input type="text" value={campaignName} onChange={e => setCampaignName(e.target.value)}
                    placeholder="e.g. Web Security Training"
                    className="w-full px-4 py-2.5 bg-black border border-gray-800 rounded-lg text-white text-sm focus:outline-none focus:border-orange-500 transition-colors placeholder-gray-700" />
                </div>

                {/* Blueprint selection */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Blueprints <span className="text-orange-500">({selectedBlueprints.length} selected)</span></label>
                    <div className="flex gap-1.5">
                      <button onClick={() => setSelectedBlueprints(blueprints.map(b => b.blueprint_id))}
                        className="text-xs px-2.5 py-0.5 bg-blue-500/15 hover:bg-blue-500/25 text-blue-400 rounded transition-colors">All</button>
                      <button onClick={() => setSelectedBlueprints([])}
                        className="text-xs px-2.5 py-0.5 bg-gray-800 hover:bg-gray-700 text-gray-400 rounded transition-colors">None</button>
                    </div>
                  </div>

                  {/* search + filter row */}
                  <div className="flex gap-2 mb-2">
                    <div className="relative flex-1">
                      <Search className="w-3.5 h-3.5 text-gray-600 absolute left-3 top-1/2 -translate-y-1/2" />
                      <input type="text" value={bpSearch} onChange={e => setBpSearch(e.target.value)} placeholder="Search blueprints..."
                        className="w-full pl-8 pr-3 py-1.5 bg-black border border-gray-800 rounded-lg text-xs text-gray-300 focus:outline-none focus:border-orange-500 placeholder-gray-700" />
                    </div>
                    <select value={bpFilter} onChange={e => setBpFilter(e.target.value)}
                      className="px-2.5 py-1.5 bg-black border border-gray-800 rounded-lg text-xs text-gray-400 focus:outline-none focus:border-orange-500 cursor-pointer">
                      <option value="all">All Categories</option>
                      {[...new Set(blueprints.map(b => b.category))].map(c => (
                        <option key={c} value={c}>{getCat(c).label}</option>
                      ))}
                    </select>
                  </div>

                  {loadingBlueprints ? (
                    <div className="flex items-center justify-center py-6"><Loader className="w-5 h-5 text-orange-500 animate-spin" /></div>
                  ) : (
                    <div className="max-h-52 overflow-y-auto rounded-lg border border-gray-800 bg-black/40" style={{ scrollbarWidth: 'thin', scrollbarColor: '#333 transparent' }}>
                      {filteredBlueprints.length === 0 && (
                        <div className="py-6 text-center text-gray-600 text-xs">No blueprints match your filter</div>
                      )}
                      {filteredBlueprints.map((bp, i) => {
                        const sel = selectedBlueprints.includes(bp.blueprint_id);
                        const cat = getCat(bp.category);
                        return (
                          <div key={bp.blueprint_id} onClick={() => toggleBp(bp.blueprint_id)}
                            className={`flex items-center gap-3 px-3.5 py-2.5 cursor-pointer border-b border-gray-900/60 last:border-0 transition-colors
                              ${sel ? 'bg-orange-500/6' : 'hover:bg-gray-900/30'}`}>
                            {/* checkbox */}
                            <div className={`w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors
                              ${sel ? 'border-orange-500 bg-orange-500' : 'border-gray-600'}`}>
                              {sel && <Check className="w-2.5 h-2.5 text-white" />}
                            </div>
                            {/* emoji */}
                            <span className="text-sm">{cat.emoji}</span>
                            {/* info */}
                            <div className="flex-1 min-w-0">
                              <span className="text-xs font-semibold text-gray-200">{bp.name}</span>
                              <span className="text-xs text-gray-600 ml-2">{bp.variants?.length || 0} variants</span>
                            </div>
                            {/* category pill */}
                            <span className="text-xs px-2 py-0.5 rounded-full font-semibold" style={{ color: cat.color, background: cat.color + '18' }}>{cat.label}</span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Difficulty */}
                <div>
                  <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Difficulty Level</label>
                  <div className="flex gap-2">
                    {[1,2,3,4,5].map(l => {
                      const active = difficulty === l;
                      const c = getDiffColor(l);
                      return (
                        <button key={l} onClick={() => setDifficulty(l)}
                          className={`flex-1 py-2.5 rounded-lg border text-center transition-all duration-200 ${active ? 'scale-105' : 'hover:border-gray-700'}`}
                          style={{ borderColor: active ? c : '#374151', background: active ? c + '18' : 'transparent' }}>
                          <p className="text-sm font-bold" style={{ color: active ? c : '#9ca3af' }}>{l}</p>
                          <p className="text-xs mt-0.5" style={{ color: active ? c : '#6b7280' }}>{getDiffLabel(l).slice(0,3)}</p>
                        </button>
                      );
                    })}
                  </div>
                  <p className="text-xs mt-1.5 text-center font-semibold" style={{ color: getDiffColor(difficulty) }}>{getDiffLabel(difficulty)}</p>
                </div>

                {/* Machine count */}
                <div>
                  <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Machines per Blueprint</label>
                  <div className="flex items-center gap-3">
                    <input type="number" min="1" max="10" value={machineCount} onChange={e => setMachineCount(parseInt(e.target.value) || 1)}
                      className="w-24 px-3 py-2 bg-black border border-gray-800 rounded-lg text-white text-sm focus:outline-none focus:border-orange-500" />
                    <p className="text-xs text-gray-600">→ <span className="text-orange-500 font-semibold">{selectedBlueprints.length * machineCount}</span> total machines</p>
                  </div>
                </div>

                {/* Error */}
                {error && (
                  <div className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg bg-red-500/8 border border-red-500/25">
                    <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                    <p className="text-red-400 text-xs">{error}</p>
                  </div>
                )}

                {/* Submit */}
                <button onClick={handleCreateCampaign} disabled={isCreating || selectedBlueprints.length === 0}
                  className="w-full py-2.5 rounded-lg bg-orange-500 hover:bg-orange-600 disabled:bg-gray-800 disabled:text-gray-600 text-white text-sm font-semibold transition-all flex items-center justify-center gap-2 active:scale-95">
                  {isCreating ? <><Loader className="w-4 h-4 animate-spin" /> Generating...</> : <><Zap className="w-4 h-4" /> Generate Campaign</>}
                </button>
              </div>

              {/* Created result inside modal */}
              {createdCampaign && (
                <div className="border-t border-gray-900 p-6">
                  <div className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg bg-green-500/8 border border-green-500/25 mb-4">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <div>
                      <p className="text-sm font-semibold text-green-400">Campaign Created!</p>
                      <p className="text-xs text-gray-600">{createdCampaign.campaign_name} · {createdCampaign.machines?.length} machines</p>
                    </div>
                  </div>

                  {/* machines list */}
                  <div className="max-h-44 overflow-y-auto rounded-lg border border-gray-800 bg-black/40 mb-4" style={{ scrollbarWidth: 'thin', scrollbarColor: '#333 transparent' }}>
                    {createdCampaign.machines?.map((m, i) => (
                      <div key={m.machine_id} className="flex items-center gap-3 px-3.5 py-2.5 border-b border-gray-900/60 last:border-0">
                        <div className="w-6 h-6 rounded-md flex items-center justify-center text-white text-xs font-bold" style={{ background: getDiffColor(m.difficulty) }}>{i + 1}</div>
                        <div className="flex-1">
                          <p className="text-xs font-semibold text-gray-200">{m.variant}</p>
                          {m.port && <code className="text-xs text-orange-500 font-mono">http://4.231.90.52:{m.port}</code>}
                        </div>
                        <span className="text-xs text-gray-600">Lv {m.difficulty}</span>
                      </div>
                    ))}
                  </div>

                  <button onClick={() => navigateToCampaign(createdCampaign.campaign_id)}
                    className="w-full py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold transition-colors flex items-center justify-center gap-2">
                    View Campaign <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── Campaigns List ── */}
        <div style={{ animation: 'fadeUp 0.4s ease 0.12s both' }}>
          {/* search bar */}
          <div className="flex items-center justify-between mb-3">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-gray-600 absolute left-3 top-1/2 -translate-y-1/2" />
              <input type="text" value={campaignSearch} onChange={e => setCampaignSearch(e.target.value)} placeholder="Search campaigns..."
                className="pl-8 pr-4 py-1.5 bg-gray-900/60 border border-gray-800 rounded-lg text-xs text-gray-300 w-48 focus:outline-none focus:border-orange-500 placeholder-gray-700" />
            </div>
            <span className="text-xs text-gray-600">{filteredCampaigns.length} campaign{filteredCampaigns.length !== 1 ? 's' : ''}</span>
          </div>

          {loadingCampaigns ? (
            <div className="flex items-center justify-center py-16">
              <Loader className="w-7 h-7 text-orange-500 animate-spin" />
            </div>
          ) : filteredCampaigns.length === 0 ? (
            <div className="rounded-xl border border-gray-900 bg-gray-950/50 py-16 text-center">
              <Target className="w-12 h-12 text-gray-800 mx-auto mb-3" />
              <p className="text-gray-600 text-sm">No campaigns yet — click <span className="text-orange-500 font-semibold">New Campaign</span> to get started</p>
            </div>
          ) : (
            <div className="rounded-xl border border-gray-900 bg-gray-950/50 overflow-hidden">
              {filteredCampaigns.map((campaign, idx) => {
                const pct = Math.round(campaign.progress_percentage || 0);
                const isComplete = pct >= 100;
                return (
                  <div key={campaign.campaign_id} className="anim-row" style={{ animationDelay: `${idx * 0.04}s` }}>
                    <div onClick={() => navigateToCampaign(campaign.campaign_id)}
                      className={`flex items-center gap-4 px-5 py-4 border-b border-gray-900/60 last:border-0 cursor-pointer transition-colors group
                        ${isComplete ? 'hover:bg-green-500/4' : 'hover:bg-gray-900/30'}`}>

                      {/* progress ring */}
                      <div className="relative flex-shrink-0">
                        <ProgressRing pct={pct} color={isComplete ? '#10b981' : '#ff7300'} />
                        <div className="absolute inset-0 flex items-center justify-center">
                          {isComplete
                            ? <CheckCircle className="w-5 h-5 text-green-500" />
                            : <span className="text-xs font-bold text-white tabular-nums">{pct}%</span>
                          }
                        </div>
                      </div>

                      {/* info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2.5 mb-0.5">
                          <h3 className={`text-sm font-bold transition-colors ${isComplete ? 'text-green-400' : 'text-gray-100 group-hover:text-orange-400'}`}>
                            {campaign.campaign_name || 'Unnamed Campaign'}
                          </h3>
                          <span className="text-xs font-semibold px-2 py-0.5 rounded-full"
                            style={{ color: getDiffColor(campaign.difficulty), background: getDiffColor(campaign.difficulty) + '18' }}>
                            Level {campaign.difficulty}
                          </span>
                          {isComplete && <span className="text-xs text-green-500 font-semibold">✓ Complete</span>}
                        </div>
                        <div className="flex items-center gap-3 text-xs text-gray-600">
                          <span>{campaign.machine_count} machines</span>
                          <span>·</span>
                          <span>{campaign.machines_solved || 0} solved</span>
                          {campaign.created_at && (
                            <><span>·</span><span className="flex items-center gap-1"><Clock className="w-2.5 h-2.5" /> {new Date(campaign.created_at).toLocaleDateString()}</span></>
                          )}
                        </div>
                      </div>

                      {/* arrow */}
                      <ArrowUpRight className="w-4 h-4 text-gray-700 group-hover:text-orange-500 transition-colors" />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Campaigns;
