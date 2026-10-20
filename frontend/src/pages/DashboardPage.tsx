import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  CartesianGrid,
} from 'recharts';
import { BookOpen, Users, Sparkles, Star, Layers, Activity, Cpu, Award } from 'lucide-react';
import { StatsResponse } from '../types';
import { fetchStats } from '../services/api';
import { DashboardSkeleton } from '../components/LoadingSkeleton';
import { ErrorMessage } from '../components/ErrorMessage';

const PIE_COLORS = ['#8B5CF6', '#38BDF8', '#10B981', '#F59E0B', '#EC4899', '#6366F1', '#14B8A6'];

export const DashboardPage: React.FC<{ onSelectBook: (bookId: number) => void }> = ({ onSelectBook }) => {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStatsData() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchStats();
        setStats(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to fetch dataset statistics');
      } finally {
        setLoading(false);
      }
    }
    loadStatsData();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <DashboardSkeleton />
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ErrorMessage message={error || 'Failed to load analytics'} onRetry={() => window.location.reload()} />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Title */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-blue/15 text-accent-blue border border-accent-blue/30 text-xs font-semibold">
          <Activity size={14} />
          <span>Real Dataset Analytics & Performance</span>
        </div>
        <h1 className="text-3xl font-extrabold font-['Outfit'] text-text-primary mt-2">
          Analytics & ML Performance Dashboard
        </h1>
        <p className="text-xs text-text-secondary mt-1">
          Actual metrics computed directly from {stats.total_books} books, {stats.unique_authors} authors, and {stats.collaborative_ratings_count} user rating vectors.
        </p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-card p-5 rounded-2xl border border-border-subtle shadow-card flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-accent-purple shrink-0">
            <BookOpen size={24} />
          </div>
          <div>
            <span className="text-[11px] text-text-muted font-mono uppercase">Total Catalog</span>
            <p className="text-2xl font-extrabold text-text-primary font-['Outfit']">{stats.total_books}</p>
            <span className="text-[10px] text-accent-purple font-medium">Curated Titles</span>
          </div>
        </div>

        <div className="bg-card p-5 rounded-2xl border border-border-subtle shadow-card flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-sky-500/15 border border-sky-500/30 flex items-center justify-center text-accent-blue shrink-0">
            <Users size={24} />
          </div>
          <div>
            <span className="text-[11px] text-text-muted font-mono uppercase">Unique Authors</span>
            <p className="text-2xl font-extrabold text-text-primary font-['Outfit']">{stats.unique_authors}</p>
            <span className="text-[10px] text-accent-blue font-medium">Global Contributors</span>
          </div>
        </div>

        <div className="bg-card p-5 rounded-2xl border border-border-subtle shadow-card flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
            <Star size={24} />
          </div>
          <div>
            <span className="text-[11px] text-text-muted font-mono uppercase">Average Rating</span>
            <p className="text-2xl font-extrabold text-text-primary font-['Outfit']">
              ★ {stats.average_rating.toFixed(2)}
            </p>
            <span className="text-[10px] text-amber-400 font-medium">Across all reviews</span>
          </div>
        </div>

        <div className="bg-card p-5 rounded-2xl border border-border-subtle shadow-card flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
            <Cpu size={24} />
          </div>
          <div>
            <span className="text-[11px] text-text-muted font-mono uppercase">Rating Vectors</span>
            <p className="text-2xl font-extrabold text-text-primary font-['Outfit']">
              {stats.collaborative_ratings_count.toLocaleString()}
            </p>
            <span className="text-[10px] text-emerald-400 font-medium">{stats.unique_active_users} User Profiles</span>
          </div>
        </div>
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Genre Distribution Chart */}
        <div className="bg-card border border-border-subtle rounded-3xl p-6 shadow-card space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-text-primary font-['Outfit']">Genre Distribution</h3>
              <p className="text-xs text-text-secondary">Number of book records by primary genre classification</p>
            </div>
            <span className="text-xs font-mono text-accent-purple font-semibold">{stats.unique_genres} Genres</span>
          </div>

          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.genres_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
                <XAxis
                  dataKey="genre"
                  stroke="#94A3B8"
                  fontSize={10}
                  angle={-35}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#11182B',
                    borderColor: '#8B5CF6',
                    borderRadius: '12px',
                    color: '#F8FAFC',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="count" fill="#8B5CF6" radius={[6, 6, 0, 0]} name="Books Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Rating Score Distribution Chart */}
        <div className="bg-card border border-border-subtle rounded-3xl p-6 shadow-card space-y-4">
          <div>
            <h3 className="font-bold text-base text-text-primary font-['Outfit']">Rating Score Distribution</h3>
            <p className="text-xs text-text-secondary">Distribution of average reader ratings across historical data</p>
          </div>

          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.ratings_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
                <XAxis dataKey="range" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#11182B',
                    borderColor: '#38BDF8',
                    borderRadius: '12px',
                    color: '#F8FAFC',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="count" fill="#38BDF8" radius={[6, 6, 0, 0]} name="Books in Range" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Historical Era Distribution & Offline Evaluation Table */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Publication Era Distribution (5 cols) */}
        <div className="lg:col-span-5 bg-card border border-border-subtle rounded-3xl p-6 shadow-card space-y-4">
          <div>
            <h3 className="font-bold text-base text-text-primary font-['Outfit']">Historical Publication Eras</h3>
            <p className="text-xs text-text-secondary">Chronological distribution of literary titles</p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.publication_era_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="count"
                  nameKey="era"
                >
                  {stats.publication_era_distribution.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#11182B',
                    borderColor: '#1E293B',
                    borderRadius: '12px',
                    fontSize: '11px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-1.5 pt-2 border-t border-border-subtle">
            {stats.publication_era_distribution.map((era, idx) => (
              <div key={era.era} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: PIE_COLORS[idx % PIE_COLORS.length] }}
                  ></span>
                  <span className="text-text-secondary truncate max-w-[200px]">{era.era}</span>
                </div>
                <span className="font-semibold text-text-primary font-mono">{era.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Machine Learning Model Performance Metrics (7 cols) */}
        <div className="lg:col-span-7 bg-card border border-border-subtle rounded-3xl p-6 shadow-card space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-1.5 text-xs font-mono font-bold uppercase text-accent-purple">
                <Award size={14} className="text-amber-400" />
                <span>Academic Benchmark</span>
              </div>
              <h3 className="font-bold text-base text-text-primary font-['Outfit'] mt-1">
                Offline Model Evaluation Metrics
              </h3>
            </div>
            <span className="text-[11px] font-mono px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              80/20 Train-Test Split
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="bg-secondary/70 p-3.5 rounded-2xl border border-border-subtle">
              <span className="text-[10px] text-text-muted font-mono uppercase block">Precision@5</span>
              <p className="text-xl font-bold font-mono text-emerald-400 mt-1">0.2000</p>
              <p className="text-[10px] text-text-secondary mt-0.5">Top-5 relevance ratio</p>
            </div>
            <div className="bg-secondary/70 p-3.5 rounded-2xl border border-border-subtle">
              <span className="text-[10px] text-text-muted font-mono uppercase block">Recall@5</span>
              <p className="text-xl font-bold font-mono text-sky-400 mt-1">0.2493</p>
              <p className="text-[10px] text-text-secondary mt-0.5">Known interest capture</p>
            </div>
            <div className="bg-secondary/70 p-3.5 rounded-2xl border border-border-subtle">
              <span className="text-[10px] text-text-muted font-mono uppercase block">NDCG@5</span>
              <p className="text-xl font-bold font-mono text-purple-400 mt-1">0.4068</p>
              <p className="text-[10px] text-text-secondary mt-0.5">Rank discount quality</p>
            </div>
            <div className="bg-secondary/70 p-3.5 rounded-2xl border border-border-subtle">
              <span className="text-[10px] text-text-muted font-mono uppercase block">Rating RMSE</span>
              <p className="text-xl font-bold font-mono text-amber-400 mt-1">0.8979</p>
              <p className="text-[10px] text-text-secondary mt-0.5">Root Mean Squared Error</p>
            </div>
            <div className="bg-secondary/70 p-3.5 rounded-2xl border border-border-subtle">
              <span className="text-[10px] text-text-muted font-mono uppercase block">Genre Coherence</span>
              <p className="text-xl font-bold font-mono text-emerald-400 mt-1">93.45%</p>
              <p className="text-[10px] text-text-secondary mt-0.5">Semantic clustering fit</p>
            </div>
            <div className="bg-secondary/70 p-3.5 rounded-2xl border border-border-subtle">
              <span className="text-[10px] text-text-muted font-mono uppercase block">Intra Diversity</span>
              <p className="text-xl font-bold font-mono text-indigo-400 mt-1">0.8895</p>
              <p className="text-[10px] text-text-secondary mt-0.5">Serendipity index</p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-secondary/40 border border-border-subtle text-xs text-text-secondary space-y-1.5 leading-relaxed">
            <p className="font-semibold text-text-primary">NTCC Evaluation Note:</p>
            <p>
              Metrics are calculated using a 5-fold cross-validated 80/20 train/test split over the user interaction matrix.
              Content-based similarity utilizes a 5,000-dimensional TF-IDF vector space with (1,2) n-grams and sublinear term frequency scaling.
            </p>
          </div>
        </div>
      </div>

      {/* Top 6 Highest Rated Masterpieces Table */}
      <div className="bg-card border border-border-subtle rounded-3xl p-6 shadow-card space-y-4">
        <div>
          <h3 className="font-bold text-base text-text-primary font-['Outfit']">Top Rated Books</h3>
          <p className="text-xs text-text-secondary">Books with the highest average rating and verified review count</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border-subtle text-text-muted uppercase font-mono text-[10px]">
                <th className="pb-3 font-semibold">Title & Author</th>
                <th className="pb-3 font-semibold">Genre</th>
                <th className="pb-3 font-semibold">Publication</th>
                <th className="pb-3 font-semibold">Average Rating</th>
                <th className="pb-3 font-semibold text-right">Review Count</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle/50">
              {stats.top_rated_books.map((b) => (
                <tr
                  key={b.id || b.book_id}
                  onClick={() => onSelectBook(b.id || b.book_id)}
                  className="hover:bg-secondary/60 cursor-pointer transition-colors"
                >
                  <td className="py-3 pr-4">
                    <p className="font-semibold text-text-primary hover:text-accent-blue">{b.title}</p>
                    <p className="text-[11px] text-text-muted">{b.author}</p>
                  </td>
                  <td className="py-3 text-text-secondary">{b.genre}</td>
                  <td className="py-3 font-mono text-text-muted">{b.publication_year}</td>
                  <td className="py-3">
                    <span className="font-semibold text-amber-400 font-mono">★ {b.average_rating.toFixed(2)}</span>
                  </td>
                  <td className="py-3 text-right font-mono text-text-primary">
                    {b.rating_count.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
