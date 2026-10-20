import React, { useState, useEffect } from 'react';
import { Bookmark, Heart, BookOpen, Trash2, CheckCircle2, Clock, Check, ShieldAlert, Sparkles } from 'lucide-react';
import { LibraryEntry } from '../types';
import { fetchLibrary, removeFromLibrary, updateLibraryEntry } from '../services/api';
import { BookCard } from '../components/BookCard';
import { EmptyState } from '../components/EmptyState';
import { ErrorMessage } from '../components/ErrorMessage';

interface LibraryPageProps {
  onSelectBook: (bookId: number) => void;
  onExploreClick: () => void;
}

export const LibraryPage: React.FC<LibraryPageProps> = ({ onSelectBook, onExploreClick }) => {
  const [entries, setEntries] = useState<LibraryEntry[]>([]);
  const [activeFilter, setActiveFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadLibraryData = async () => {
    try {
      setLoading(true);
      setError(null);
      const isFavOnly = activeFilter === 'favorites';
      const statusParam = activeFilter !== 'all' && activeFilter !== 'favorites' ? activeFilter : undefined;
      const res = await fetchLibrary(statusParam, isFavOnly);
      setEntries(res.entries || []);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to fetch library records');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLibraryData();
  }, [activeFilter]);

  const handleRemove = async (bookId: number) => {
    try {
      await removeFromLibrary(bookId);
      setEntries((prev) => prev.filter((e) => e.book_id !== bookId));
    } catch (err) {
      console.error(err);
    }
  };

  const handleStatusUpdate = async (bookId: number, status: string) => {
    try {
      await updateLibraryEntry({ book_id: bookId, status });
      setEntries((prev) =>
        prev.map((e) => (e.book_id === bookId ? { ...e, status: status as any } : e))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const statusBadges: Record<string, { label: string; color: string; icon: any }> = {
    want_to_read: { label: 'Want to Read', color: 'bg-sky-500/15 text-sky-400 border-sky-500/30', icon: Bookmark },
    currently_reading: { label: 'Currently Reading', color: 'bg-amber-500/15 text-amber-400 border-amber-500/30', icon: Clock },
    completed: { label: 'Completed', color: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30', icon: CheckCircle2 },
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Demo Profile Notice Banner */}
      <div className="bg-secondary/80 border border-border-glow rounded-3xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-card">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-xs font-mono font-bold text-accent-blue uppercase tracking-wider">
              Local Academic Demo Profile
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-['Outfit'] text-text-primary">
            My Reading Library
          </h1>
          <p className="text-xs text-text-secondary max-w-2xl leading-relaxed">
            Demonstration Scholar Profile connected to persistent SQLite storage.
            All reading lists, favorites, and custom notes are stored in local database tables.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-card p-3 rounded-2xl border border-border-subtle shrink-0">
          <div className="text-right">
            <span className="text-[10px] text-text-muted uppercase font-mono block">Active Records</span>
            <span className="text-lg font-bold font-mono text-accent-purple">{entries.length} Books</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-border-subtle pb-4">
        {[
          { id: 'all', label: 'All Saved' },
          { id: 'favorites', label: 'Favorites', icon: Heart },
          { id: 'want_to_read', label: 'Want to Read' },
          { id: 'currently_reading', label: 'Currently Reading' },
          { id: 'completed', label: 'Completed' },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeFilter === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveFilter(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-accent-purple text-white shadow-glow'
                  : 'bg-secondary text-text-secondary hover:text-white border border-border-subtle'
              }`}
            >
              {Icon && <Icon size={14} className={isActive ? 'fill-white' : ''} />}
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Error state */}
      {error && <ErrorMessage message={error} onRetry={loadLibraryData} />}

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-64 bg-card rounded-2xl border border-border-subtle"></div>
          ))}
        </div>
      ) : entries.length === 0 ? (
        <EmptyState
          title="Your Library is Empty"
          description="You haven't saved any books to this reading category yet. Browse our catalogue or AI recommendations and click 'Add to Favorites'."
          onReset={onExploreClick}
          resetText="Explore Books Now"
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {entries.map((entry) => {
            const b = entry.book;
            const badge = statusBadges[entry.status] || statusBadges['want_to_read'];
            const BadgeIcon = badge.icon;
            return (
              <div
                key={entry.id}
                className="bg-card hover:bg-card-hover rounded-2xl p-5 border border-border-subtle hover:border-accent-purple/40 transition-all flex flex-col justify-between shadow-card"
              >
                <div>
                  {/* Top Meta */}
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium border ${badge.color}`}>
                      <BadgeIcon size={12} />
                      <span>{badge.label}</span>
                    </span>
                    {entry.is_favorite && (
                      <span className="p-1 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">
                        <Heart size={14} className="fill-rose-400" />
                      </span>
                    )}
                  </div>

                  {/* Book Info */}
                  <div className="flex gap-4 items-start">
                    <div
                      onClick={() => onSelectBook(b.id || b.book_id)}
                      className="w-16 h-24 rounded-lg overflow-hidden bg-secondary shrink-0 cursor-pointer border border-border-subtle"
                    >
                      {b.cover_url ? (
                        <img src={b.cover_url} alt="" className="w-full h-full object-cover" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-accent-purple">
                          <BookOpen size={20} />
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4
                        onClick={() => onSelectBook(b.id || b.book_id)}
                        className="font-bold text-sm text-text-primary hover:text-accent-blue cursor-pointer truncate font-['Outfit']"
                      >
                        {b.title}
                      </h4>
                      <p className="text-xs text-text-secondary truncate mt-0.5">by {b.author}</p>
                      <span className="text-[10px] text-text-muted font-mono block mt-1">{b.genre}</span>
                      <p className="text-xs text-amber-400 font-semibold mt-1">★ {b.average_rating.toFixed(2)}</p>
                    </div>
                  </div>

                  {/* Status Dropdown */}
                  <div className="mt-4 pt-3 border-t border-border-subtle/60 flex items-center justify-between gap-2">
                    <span className="text-[11px] text-text-muted">Status:</span>
                    <select
                      value={entry.status}
                      onChange={(e) => handleStatusUpdate(b.id || b.book_id, e.target.value)}
                      className="bg-secondary border border-border-subtle rounded-lg px-2.5 py-1 text-xs text-text-primary focus:outline-none focus:border-accent-purple"
                    >
                      <option value="want_to_read">Want to Read</option>
                      <option value="currently_reading">Currently Reading</option>
                      <option value="completed">Completed</option>
                    </select>
                  </div>
                </div>

                {/* Footer Actions */}
                <div className="mt-4 pt-3 border-t border-border-subtle flex items-center justify-between">
                  <button
                    onClick={() => onSelectBook(b.id || b.book_id)}
                    className="text-xs text-accent-purple hover:text-accent-blue font-medium"
                  >
                    View Details →
                  </button>
                  <button
                    onClick={() => handleRemove(b.id || b.book_id)}
                    className="text-text-muted hover:text-rose-400 p-1 transition-colors"
                    title="Remove from library"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
