import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Target, Cpu, Zap, TrendingUp, Activity, Play, Shield, Server,
  Terminal, ChevronRight, Sparkles, AlertCircle, Flag, Clock,
  Award, Eye, Lock, Unlock, ArrowUpRight, MoreHorizontal,
  Flame, GitBranch, BoxIcon, Layers, Search
} from 'lucide-react';
import api from '../services/api';

// ─── Animated Counter Hook ───────────────────────────────────────────────────
const useCounter = (target, duration = 1200) => {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  useEffect(() => {
    if (target === 0) return;
    const start = performance.now();
    const animate = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCount(Math.round(eased * target));
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [target, duration]);
  return count;
};

// ─── Particle Canvas Background ──────────────────────────────────────────────
const ParticleCanvas = () => {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animId;

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    for (let i = 0; i < 60; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.5 + 0.3,
        dx: (Math.random() - 0.5) * 0.4,
        dy: (Math.random() - 0.5) * 0.4,
        opacity: Math.random() * 0.4 + 0.1,
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach((p, i) => {
        p.x += p.dx;
        p.y += p.dy;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 115, 0, ${p.opacity})`;
        ctx.fill();

        // Lines between nearby particles
        for (let j = i + 1; j < particles.length; j++) {
          const q = particles[j];
          const dist = Math.hypot(p.x - q.x, p.y - q.y);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = `rgba(255, 115, 0, ${0.06 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      });
      animId = requestAnimationFrame(draw);
    };
    draw();
    return () => { cancelAnimationFrame(animId); window.removeEventListener('resize', resize); };
  }, []);
  return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full pointer-events-none" />;
};

// ─── Mini Sparkline (SVG) ─────────────────────────────────────────────────────
const Sparkline = ({ data, color = '#ff7300', width = 120, height = 36 }) => {
  if (!data || data.length < 2) return null;
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const step = width / (data.length - 1);
  const points = data.map((v, i) => `${i * step},${height - ((v - min) / range) * (height - 4) - 2}`).join(' ');
  const areaPoints = points + ` ${width},${height} 0,${height}`;
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      <defs>
        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon points={areaPoints} fill="url(#sparkGrad)" />
      <polyline points={points} fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
};

// ─── Fake data generators (replace with real API later) ──────────────────────
const genSparkline = (base, variance = 3) => Array.from({ length: 12 }, () => base + Math.floor(Math.random() * variance));
const MOCK_ACTIVITY = [
  { time: '2m ago', action: 'Flag submitted', machine: 'WebShell-01', correct: true },
  { time: '15m ago', action: 'Hint used', machine: 'SQLi-Maze', correct: null },
  { time: '42m ago', action: 'Machine started', machine: 'RCE-Lab', correct: null },
  { time: '1h ago', action: 'Flag submitted', machine: 'XSS-Arena', correct: false },
  { time: '2h ago', action: 'Campaign created', machine: 'Web Basics', correct: null },
  { time: '3h ago', action: 'Achievement earned', machine: 'First Blood', correct: null },
];
const MOCK_MACHINES = [
  { id: 1, name: 'SQLi-Maze', difficulty: 'Medium', category: 'Database', solvers: 142, progress: 60, status: 'running' },
  { id: 2, name: 'XSS-Arena', difficulty: 'Easy', category: 'Web', solvers: 389, progress: 100, status: 'solved' },
  { id: 3, name: 'RCE-Lab', difficulty: 'Hard', category: 'Pwn', solvers: 67, progress: 25, status: 'running' },
  { id: 4, name: 'WebShell-01', difficulty: 'Medium', category: 'Web', solvers: 201, progress: 80, status: 'running' },
  { id: 5, name: 'Crypto-Vault', difficulty: 'Expert', category: 'Crypto', solvers: 18, progress: 0, status: 'locked' },
];
const MOCK_LEADERBOARD = [
  { rank: 1, name: 'ShadowHex', points: 4820, avatar: 'SH', streak: 12 },
  { rank: 2, name: 'You', points: 3150, avatar: 'YO', streak: 5, isYou: true },
  { rank: 3, name: 'NullPtr', points: 2980, avatar: 'NP', streak: 8 },
  { rank: 4, name: 'b1tfl1p', points: 2710, avatar: 'BF', streak: 3 },
  { rank: 5, name: 'r00tkit', points: 2540, avatar: 'RK', streak: 7 },
];

// ─── Difficulty badge ────────────────────────────────────────────────────────
const diffColors = { Easy: '#10b981', Medium: '#f59e0b', Hard: '#ef4444', Expert: '#a855f7', Insane: '#ec4899' };
const DiffBadge = ({ level }) => (
  <span style={{ color: diffColors[level], borderColor: diffColors[level] + '50', background: diffColors[level] + '12' }}
    className="text-xs font-bold px-2 py-0.5 rounded-full border">
    {level}
  </span>
);

// ─── Main Dashboard ──────────────────────────────────────────────────────────
const ModernDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ blueprints: 12, machines: 38, campaigns: 7, running: 3 });
  const [dockerStatus, setDockerStatus] = useState({ total: 5, running: 3 });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('activity'); // activity | machines | leaderboard

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDockerStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [statsData, dockerData] = await Promise.all([
        api.getStats().catch(() => ({ total_blueprints: 12, total_machines: 38, total_campaigns: 7 })),
        api.getDockerStatus().catch(() => ({ total: 5, running: 3 })),
      ]);
      setStats({
        blueprints: statsData.total_blueprints || 12,
        machines: statsData.total_machines || 38,
        campaigns: statsData.total_campaigns || 7,
        running: dockerData.running || 3,
      });
      setDockerStatus(dockerData);
      setIsLoading(false);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  const fetchDockerStatus = async () => {
    try {
      const d = await api.getDockerStatus();
      setDockerStatus(d);
      setStats(prev => ({ ...prev, running: d.running || 0 }));
    } catch {}
  };

  // ── Stat Card ──
  const StatCard = ({ icon: Icon, label, value, accent, delay, isLive, sparkData }) => {
    const animated = useCounter(value, 1000);
    return (
      <div className="relative group overflow-hidden rounded-xl border transition-all duration-500 hover:-translate-y-1"
        style={{ background: 'linear-gradient(145deg, #141414, #0a0a0a)', borderColor: accent + '25', animation: `fadeUp 0.5s ease ${delay}s both` }}>
        {/* glow line top */}
        <div className="absolute top-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg, transparent, ${accent}, transparent)` }} />

        <div className="p-5">
          <div className="flex items-start justify-between mb-3">
            <div className="p-2.5 rounded-lg" style={{ background: accent + '15' }}>
              <Icon className="w-5 h-5" style={{ color: accent }} />
            </div>
            {isLive && <span className="flex items-center gap-1.5 text-xs text-green-400 font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" /> LIVE
            </span>}
          </div>
          <p className="text-3xl font-bold text-white tabular-nums">{animated}</p>
          <p className="text-gray-500 text-xs font-medium mt-0.5 tracking-wide uppercase">{label}</p>
          {sparkData && <div className="mt-3"><Sparkline data={sparkData} color={accent} width={100} height={24} /></div>}
        </div>
      </div>
    );
  };

  // ── Activity Feed ──
  const ActivityFeed = () => (
    <div className="space-y-0">
      {MOCK_ACTIVITY.map((item, i) => (
        <div key={i} className="flex items-start gap-3 px-4 py-3 border-b border-gray-900/60 hover:bg-gray-900/20 transition-colors group">
          <div className="mt-0.5 w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0"
            style={{ background: item.correct === true ? '#10b98115' : item.correct === false ? '#ef444415' : '#ff730015' }}>
            {item.correct === true ? <Flag className="w-3.5 h-3.5 text-green-500" /> :
             item.correct === false ? <Flag className="w-3.5 h-3.5 text-red-500" /> :
             <Activity className="w-3.5 h-3.5 text-orange-500" />}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm text-gray-200 font-medium">{item.action}</span>
              {item.correct === true && <span className="text-xs text-green-500 font-semibold bg-green-500/10 px-1.5 py-0.5 rounded">+100 pts</span>}
              {item.correct === false && <span className="text-xs text-red-500 font-semibold bg-red-500/10 px-1.5 py-0.5 rounded">Wrong</span>}
            </div>
            <p className="text-xs text-gray-600 mt-0.5">{item.machine} · {item.time}</p>
          </div>
        </div>
      ))}
    </div>
  );

  // ── Machine List ──
  const MachineList = () => (
    <div className="space-y-0">
      {MOCK_MACHINES.map((m, i) => (
        <div key={m.id} className="flex items-center gap-4 px-4 py-3 border-b border-gray-900/60 hover:bg-gray-900/20 transition-colors cursor-pointer group"
          onClick={() => navigate('/machines')}>
          <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-gray-900 border border-gray-800">
            {m.status === 'solved' ? <Unlock className="w-4 h-4 text-green-500" /> :
             m.status === 'locked' ? <Lock className="w-4 h-4 text-gray-600" /> :
             <Cpu className="w-4 h-4 text-orange-500" />}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-100 font-semibold">{m.name}</span>
              <DiffBadge level={m.difficulty} />
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <div className="flex-1 max-w-24 h-1.5 rounded-full bg-gray-800 overflow-hidden">
                <div className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${m.progress}%`, background: m.progress === 100 ? '#10b981' : '#ff7300' }} />
              </div>
              <span className="text-xs text-gray-600">{m.progress}%</span>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-gray-500">{m.solvers} solvers</p>
            <span className="text-xs text-gray-600">{m.category}</span>
          </div>
          <ArrowUpRight className="w-4 h-4 text-gray-700 group-hover:text-orange-500 transition-colors" />
        </div>
      ))}
    </div>
  );

  // ── Mini Leaderboard ──
  const MiniLeaderboard = () => (
    <div className="space-y-0">
      {MOCK_LEADERBOARD.map((u, i) => (
        <div key={i} className={`flex items-center gap-3 px-4 py-2.5 border-b border-gray-900/60 transition-colors
          ${u.isYou ? 'bg-orange-500/8 border-l-2 border-l-orange-500' : 'hover:bg-gray-900/20'}`}>
          <span className={`text-sm font-bold w-5 text-center tabular-nums ${i === 0 ? 'text-yellow-400' : i === 1 ? 'text-gray-300' : i === 2 ? 'text-amber-600' : 'text-gray-600'}`}>
            {u.rank}
          </span>
          <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white"
            style={{ background: u.isYou ? '#ff7300' : '#1f1f1f' }}>{u.avatar}</div>
          <div className="flex-1">
            <span className={`text-sm font-semibold ${u.isYou ? 'text-orange-400' : 'text-gray-200'}`}>{u.name}</span>
            {u.streak > 4 && <span className="ml-2 text-xs text-orange-500"><Flame className="w-3 h-3 inline" /> {u.streak}</span>}
          </div>
          <span className="text-sm font-bold text-white tabular-nums">{u.points.toLocaleString()}</span>
        </div>
      ))}
      <div className="px-4 pt-3">
        <button onClick={() => navigate('/leaderboard')} className="text-xs text-orange-500 hover:text-orange-400 font-semibold flex items-center gap-1 transition-colors">
          View Full Leaderboard <ArrowUpRight className="w-3 h-3" />
        </button>
      </div>
    </div>
  );

  // ── Loading / Error ──
  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="relative w-14 h-14 mx-auto mb-4">
            <div className="absolute inset-0 rounded-full border-2 border-orange-500/20" />
            <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-orange-500 animate-spin" />
          </div>
          <p className="text-orange-500 text-sm font-semibold tracking-widest uppercase">Loading</p>
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-red-950/20 border border-red-500/30 rounded-xl p-8 text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-3" />
          <h2 className="text-xl font-bold text-white mb-1">Connection Error</h2>
          <p className="text-gray-500 text-sm mb-5">{error}</p>
          <button onClick={fetchDashboardData} className="px-5 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm rounded-lg transition-colors font-semibold">Retry</button>
        </div>
      </div>
    );
  }

  // ── Render ──
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      <style>{`
        @keyframes fadeUp { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
        .tab-active { color:#ff7300; border-bottom-color:#ff7300; }
        .tab-inactive { color:#555; border-bottom-color:transparent; }
        .tab-inactive:hover { color:#888; }
      `}</style>

      {/* Particle BG */}
      <div className="fixed inset-0 pointer-events-none">
        <ParticleCanvas />
        {/* subtle radial glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-96 rounded-full blur-3xl opacity-20 pointer-events-none" style={{ background: 'radial-gradient(ellipse, #ff7300, transparent 70%)' }} />
      </div>

      <main className="relative z-10 max-w-7xl mx-auto px-5 py-7">

        {/* ── Header ── */}
        <div className="flex items-start justify-between mb-7" style={{ animation: 'fadeUp 0.4s ease both' }}>
          <div>
            <div className="flex items-center gap-2.5 mb-1">
              <div className="w-8 h-8 rounded-lg bg-orange-500/15 border border-orange-500/30 flex items-center justify-center">
                <Shield className="w-4.5 h-4.5 text-orange-500" />
              </div>
              <h1 className="text-2xl font-bold text-white">HackForge</h1>
            </div>
            <p className="text-gray-600 text-sm ml-10.5">Welcome back, <span className="text-orange-500 font-semibold">Hacker</span> — ready to break something?</p>
          </div>
          {/* Search */}
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-4 h-4 text-gray-600 absolute left-3 top-1/2 -translate-y-1/2" />
              <input type="text" placeholder="Search machines..." className="bg-gray-900/60 border border-gray-800 text-gray-300 text-sm pl-9 pr-4 py-2 rounded-lg w-52 focus:outline-none focus:border-orange-500/50 transition-colors placeholder-gray-700" />
            </div>
          </div>
        </div>

        {/* ── Stat Cards ── */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard icon={Shield} label="Blueprints" value={stats.blueprints} accent="#ff7300" delay={0} sparkData={genSparkline(stats.blueprints, 4)} />
          <StatCard icon={Server} label="Machines" value={stats.machines} accent="#ff7300" delay={0.08} sparkData={genSparkline(stats.machines, 6)} />
          <StatCard icon={Zap} label="Campaigns" value={stats.campaigns} accent="#ff7300" delay={0.16} sparkData={genSparkline(stats.campaigns, 2)} />
          <StatCard icon={Activity} label="Running" value={stats.running} accent="#10b981" delay={0.24} isLive={true} />
        </div>

        {/* ── Progress Overview Row ── */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6" style={{ animation: 'fadeUp 0.5s ease 0.3s both' }}>
          {/* Current Campaign Progress */}
          <div className="rounded-xl border border-gray-900 bg-gray-950/60 p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4 text-orange-500" />
                <span className="text-sm font-semibold text-gray-200">Active Campaign</span>
              </div>
              <span className="text-xs text-orange-500 font-semibold bg-orange-500/10 px-2 py-0.5 rounded">3/5 done</span>
            </div>
            <p className="text-xs text-gray-600 mb-2">Web Penetration Basics</p>
            <div className="w-full h-2 rounded-full bg-gray-800 overflow-hidden">
              <div className="h-full rounded-full bg-gradient-to-r from-orange-500 to-orange-400 transition-all duration-1000" style={{ width: '60%' }} />
            </div>
            <div className="flex justify-between mt-2">
              <span className="text-xs text-gray-600">60% complete</span>
              <span className="text-xs text-orange-500 font-semibold cursor-pointer hover:text-orange-400">Continue →</span>
            </div>
          </div>

          {/* Today's Stats */}
          <div className="rounded-xl border border-gray-900 bg-gray-950/60 p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-500" />
                <span className="text-sm font-semibold text-gray-200">Today's Stats</span>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {[{ label: 'Solved', val: '2', color: '#10b981' }, { label: 'Flags', val: '7', color: '#ff7300' }, { label: 'Hrs', val: '1.5', color: '#60a5fa' }].map(s => (
                <div key={s.label} className="text-center">
                  <p className="text-lg font-bold" style={{ color: s.color }}>{s.val}</p>
                  <p className="text-xs text-gray-600">{s.label}</p>
                </div>
              ))}
            </div>
            <div className="mt-3 flex items-center gap-2">
              <Flame className="w-3.5 h-3.5 text-orange-500" />
              <span className="text-xs text-gray-500">5-day streak — keep it going!</span>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="rounded-xl border border-gray-900 bg-gray-950/60 p-4">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-4 h-4 text-yellow-500" />
              <span className="text-sm font-semibold text-gray-200">Quick Actions</span>
            </div>
            <div className="space-y-2">
              {[
                { icon: Play, label: 'New Campaign', color: '#ff7300', route: '/campaigns' },
                { icon: Cpu, label: 'Browse Machines', color: '#60a5fa', route: '/machines' },
                { icon: Terminal, label: 'Docker Control', color: '#10b981', route: '/docker' },
              ].map(a => (
                <button key={a.label} onClick={() => navigate(a.route)}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-lg border border-gray-800 hover:border-gray-700 bg-gray-900/40 hover:bg-gray-900/70 transition-all group">
                  <div className="flex items-center gap-2.5">
                    <a.icon className="w-4 h-4" style={{ color: a.color }} />
                    <span className="text-sm text-gray-300 group-hover:text-white transition-colors">{a.label}</span>
                  </div>
                  <ChevronRight className="w-3.5 h-3.5 text-gray-700 group-hover:text-orange-500 group-hover:translate-x-0.5 transition-all" />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ── Bottom Grid: Tabbed Panel + Docker + Achievements ── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4" style={{ animation: 'fadeUp 0.5s ease 0.4s both' }}>

          {/* Tabbed Panel (Activity / Machines / Leaderboard) */}
          <div className="lg:col-span-2 rounded-xl border border-gray-900 bg-gray-950/60 overflow-hidden">
            {/* Tabs */}
            <div className="flex border-b border-gray-900 px-4">
              {[
                { key: 'activity', label: 'Activity', icon: Activity },
                { key: 'machines', label: 'Machines', icon: Cpu },
                { key: 'leaderboard', label: 'Leaderboard', icon: Award },
              ].map(t => (
                <button key={t.key} onClick={() => setActiveTab(t.key)}
                  className={`flex items-center gap-1.5 px-4 py-3 text-sm font-semibold border-b-2 -mb-px transition-colors ${activeTab === t.key ? 'tab-active' : 'tab-inactive'}`}>
                  <t.icon className="w-3.5 h-3.5" />
                  {t.label}
                </button>
              ))}
              <div className="ml-auto flex items-center">
                <button className="text-gray-600 hover:text-gray-400 transition-colors">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            </div>
            {/* Content */}
            <div className="max-h-80 overflow-y-auto" style={{ scrollbarWidth: 'thin', scrollbarColor: '#333 transparent' }}>
              {activeTab === 'activity' && <ActivityFeed />}
              {activeTab === 'machines' && <MachineList />}
              {activeTab === 'leaderboard' && <MiniLeaderboard />}
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-4">
            {/* Docker Status */}
            <div className="rounded-xl border border-gray-900 bg-gray-950/60 p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-blue-500" />
                  <span className="text-sm font-semibold text-gray-200">Docker</span>
                </div>
                <span className="flex items-center gap-1 text-xs text-green-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" /> Live
                </span>
              </div>
              <div className="space-y-3">
                {[
                  { label: 'Total', value: dockerStatus?.total || 0, color: '#6366f1' },
                  { label: 'Running', value: dockerStatus?.running || 0, color: '#10b981' },
                  { label: 'Stopped', value: (dockerStatus?.total || 0) - (dockerStatus?.running || 0), color: '#ef4444' },
                ].map(item => (
                  <div key={item.label} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full" style={{ background: item.color }} />
                      <span className="text-xs text-gray-500">{item.label}</span>
                    </div>
                    <span className="text-sm font-bold" style={{ color: item.color }}>{item.value}</span>
                  </div>
                ))}
              </div>
              <button onClick={() => navigate('/docker')} className="mt-4 w-full text-xs text-blue-500 hover:text-blue-400 font-semibold flex items-center justify-center gap-1 transition-colors">
                Manage Containers <ArrowUpRight className="w-3 h-3" />
              </button>
            </div>

            {/* Achievements */}
            <div className="rounded-xl border border-gray-900 bg-gray-950/60 p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-yellow-500" />
                  <span className="text-sm font-semibold text-gray-200">Achievements</span>
                </div>
                <span className="text-xs text-gray-600">3/8</span>
              </div>
              <div className="space-y-2.5">
                {[
                  { name: 'First Blood', desc: 'Solve your first machine', done: true, icon: '🩸' },
                  { name: 'Speed Demon', desc: 'Solve in under 10 min', done: true, icon: '⚡' },
                  { name: 'Streak Master', desc: '7-day solving streak', done: false, icon: '🔥', progress: 71 },
                  { name: 'Perfectionist', desc: 'Solve with no wrong flags', done: false, icon: '🎯', progress: 40 },
                ].map((a, i) => (
                  <div key={i} className={`flex items-center gap-3 px-2.5 py-2 rounded-lg transition-colors ${a.done ? 'bg-green-500/8' : 'bg-gray-900/40'}`}>
                    <span className="text-base">{a.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className={`text-xs font-semibold ${a.done ? 'text-green-400' : 'text-gray-300'}`}>{a.name}</span>
                        {a.done && <span className="text-xs text-green-500">✓</span>}
                      </div>
                      {!a.done && (
                        <>
                          <p className="text-xs text-gray-600">{a.desc}</p>
                          <div className="w-full h-1 rounded-full bg-gray-800 mt-1 overflow-hidden">
                            <div className="h-full rounded-full bg-orange-500 transition-all" style={{ width: `${a.progress}%` }} />
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ModernDashboard;
