import React, { useState, useEffect } from 'react';
import { Sparkles, Sliders, RefreshCw, Layers, CheckCircle2, BookOpen, Search, Info } from 'lucide-react';
import { Book, Recommendation, GenreItem } from '../types';
import { fetchGenres, fetchBooks, fetchPersonalizedRecommendations } from '../services/api';
import { BookCard } from '../components/BookCard';
import { BookCardSkeleton } from '../components/LoadingSkeleton';
import { ErrorMessage } from '../components/ErrorMessage';
import { EmptyState } from '../components/EmptyState';

interface RecommendationsPageProps {
  onSelectBook: (bookId: number) => void;
  onToggleFavorite: (bookId: number, isFav: boolean) => void;
  favorites: Set<number>;
}

export const RecommendationsPage: React.FC<RecommendationsPageProps> = ({
  onSelectBook,
  onToggleFavorite,
  favorites,
}) => {
  const [genres, setGenres] = useState<GenreItem[]>([]);
  const [seedSearch, setSeedSearch] = useState('');
  const [seedSearchResults, setSeedSearchResults] = useState<Book[]>([]);
  const [selectedSeedBook, setSelectedSeedBook] = useState<Book | null>(null);
  const [selectedGenres, setSelectedGenres] = useState<string[]>(['Science Fiction']);
  const [minRating, setMinRating] = useState<number>(4.0);
  const [limit, setLimit] = useState<number>(8);
  const [algorithm, setAlgorithm] = useState<'hybrid' | 'content' | 'collaborative' | 'popular'>('hybrid');
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generatedOnce, setGeneratedOnce] = useState(false);

  useEffect(() => {
    async function init() {
      try {
        const res = await fetchGenres();
        setGenres(res.genres || []);
        // Pick initial seed book: Dune
        const bRes = await fetchBooks({ q: 'Dune', per_page: 1 });
        if (bRes.books.length > 0) {
          setSelectedSeedBook(bRes.books[0]);
        }
      } catch (err) {
        console.error(err);
      }
    }
    init();
  }, []);

  // Search for seed book
  useEffect(() => {
    if (seedSearch.trim().length >= 2) {
      const timer = setTimeout(async () => {
        try {
          const res = await fetchBooks({ q: seedSearch.trim(), per_page: 5 });
          setSeedSearchResults(res.books);
        } catch {
          setSeedSearchResults([]);
        }
      }, 200);
      return () => clearTimeout(timer);
    } else {
      setSeedSearchResults([]);
    }
  }, [seedSearch]);

  const handleGenerate = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetchPersonalizedRecommendations({
        seed_book_id: selectedSeedBook ? (selectedSeedBook.id || selectedSeedBook.book_id) : undefined,
        preferred_genres: selectedGenres.length > 0 ? selectedGenres : undefined,
        min_rating: minRating,
        limit,
        algorithm,
      });
      setRecommendations(res.recommendations || []);
      setGeneratedOnce(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Recommendation failed');
    } finally {
      setLoading(false);
    }
  };

  // Run automatically on first mount after initial seed is set
  useEffect(() => {
    if (selectedSeedBook && !generatedOnce) {
      handleGenerate();
    }
  }, [selectedSeedBook]);

  const toggleGenre = (genreName: string) => {
    if (selectedGenres.includes(genreName)) {
      setSelectedGenres(selectedGenres.filter((g) => g !== genreName));
    } else {
      setSelectedGenres([...selectedGenres, genreName]);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Title */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-purple/20 text-accent-purple border border-accent-purple/30 text-xs font-semibold">
          <Sparkles size={14} className="text-accent-blue" />
          <span>Interactive Machine Learning Laboratory</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold font-['Outfit'] text-text-primary mt-2">
          AI Recommendations Engine
        </h1>
        <p className="text-xs sm:text-sm text-text-secondary mt-1 max-w-3xl">
          Customize machine learning parameters, choose between Content-Based (TF-IDF), Item Collaborative Filtering,
          or our Hybrid Ensembling Recommender.
        </p>
      </div>

      {/* Control Console */}
      <div className="bg-card border border-border-subtle rounded-3xl p-6 sm:p-8 shadow-card space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Step 1: Select Seed Book (4 cols) */}
          <div className="lg:col-span-5 space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold uppercase tracking-wider text-text-primary font-mono flex items-center gap-2">
                <span>1. Anchor / Seed Book</span>
                <span className="text-accent-purple text-[10px] normal-case">(Reference point)</span>
              </label>
              {selectedSeedBook && (
                <button
                  onClick={() => setSelectedSeedBook(null)}
                  className="text-[11px] text-text-muted hover:text-rose-400"
                >
                  Clear Anchor
                </button>
              )}
            </div>

            {selectedSeedBook ? (
              <div className="p-4 rounded-2xl bg-secondary/80 border border-accent-purple/40 flex items-center gap-4">
                <div className="w-14 h-20 rounded-lg overflow-hidden bg-slate-800 shrink-0 border border-border-subtle">
                  {selectedSeedBook.cover_url ? (
                    <img src={selectedSeedBook.cover_url} alt="" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-accent-purple">
                      <BookOpen size={20} />
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-accent-purple/20 text-accent-purple">
                    Selected Anchor
                  </span>
                  <h4 className="font-bold text-sm text-text-primary truncate mt-1">{selectedSeedBook.title}</h4>
                  <p className="text-xs text-text-secondary truncate">by {selectedSeedBook.author}</p>
                  <p className="text-[11px] text-text-muted font-mono mt-0.5">{selectedSeedBook.genre}</p>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-2xl bg-secondary/40 border border-dashed border-border-subtle text-center space-y-2">
                <p className="text-xs text-text-muted">No seed book selected. System will operate in cold-start mode.</p>
              </div>
            )}

            {/* Seed Search Input */}
            <div className="relative">
              <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" />
              <input
                type="text"
                value={seedSearch}
                onChange={(e) => setSeedSearch(e.target.value)}
                placeholder="Search to pick another anchor book..."
                className="w-full bg-secondary border border-border-subtle rounded-xl pl-10 pr-4 py-2.5 text-xs text-text-primary focus:outline-none focus:border-accent-purple"
              />
              {seedSearchResults.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-secondary border border-border-glow rounded-xl shadow-card overflow-hidden z-30">
                  {seedSearchResults.map((b) => (
                    <div
                      key={b.id || b.book_id}
                      onClick={() => {
                        setSelectedSeedBook(b);
                        setSeedSearch('');
                        setSeedSearchResults([]);
                      }}
                      className="p-2.5 hover:bg-card cursor-pointer border-b border-border-subtle last:border-none flex items-center justify-between"
                    >
                      <div className="truncate mr-2">
                        <p className="text-xs font-semibold text-text-primary truncate">{b.title}</p>
                        <p className="text-[10px] text-text-secondary truncate">{b.author} • {b.genre}</p>
                      </div>
                      <span className="text-[10px] text-accent-purple shrink-0 font-medium">Select</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Step 2: Algorithm Mode & Parameters (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            {/* Algorithm Radio Cards */}
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-text-primary font-mono block mb-2">
                2. Recommendation Model
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {[
                  {
                    id: 'hybrid',
                    name: 'Hybrid Ensembling',
                    desc: 'Content + Collab + Popularity',
                    badge: 'Recommended',
                  },
                  {
                    id: 'content',
                    name: 'Content-Based',
                    desc: 'TF-IDF & Cosine Similarity',
                    badge: 'Text NLP',
                  },
                  {
                    id: 'collaborative',
                    name: 'Collaborative',
                    desc: 'Item-Item Rating Vectors',
                    badge: 'Multi-User',
                  },
                  {
                    id: 'popular',
                    name: 'Bayesian Popular',
                    desc: 'Weighted Score Formula',
                    badge: 'Statistical',
                  },
                ].map((m) => (
                  <button
                    key={m.id}
                    type="button"
                    onClick={() => setAlgorithm(m.id as any)}
                    className={`p-3 rounded-2xl text-left border transition-all ${
                      algorithm === m.id
                        ? 'bg-accent-purple/20 border-accent-purple text-white shadow-glow'
                        : 'bg-secondary/60 border-border-subtle text-text-secondary hover:text-white'
                    }`}
                  >
                    <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-accent-purple/30 text-accent-purple font-semibold">
                      {m.badge}
                    </span>
                    <h5 className="font-bold text-xs text-text-primary mt-1.5">{m.name}</h5>
                    <p className="text-[10px] text-text-muted mt-0.5 line-clamp-1">{m.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Preferred Genre Filters */}
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-text-primary font-mono block mb-2">
                3. Genre Preferences
              </label>
              <div className="flex flex-wrap gap-2">
                {genres.map((g) => {
                  const isSelected = selectedGenres.includes(g.genre);
                  return (
                    <button
                      key={g.genre}
                      type="button"
                      onClick={() => toggleGenre(g.genre)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                        isSelected
                          ? 'bg-accent-blue/20 text-accent-blue border border-accent-blue/40 shadow-sm'
                          : 'bg-secondary text-text-secondary hover:text-white border border-border-subtle'
                      }`}
                    >
                      {g.genre}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Sliders: Min Rating & Recommendations Count */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="space-y-1.5 bg-secondary/50 p-3.5 rounded-2xl border border-border-subtle">
                <div className="flex justify-between text-xs">
                  <span className="text-text-secondary">Minimum Rating:</span>
                  <span className="font-bold text-amber-400 font-mono">★ {minRating.toFixed(1)}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="4.6"
                  step="0.1"
                  value={minRating}
                  onChange={(e) => setMinRating(parseFloat(e.target.value))}
                  className="w-full accent-accent-purple"
                />
              </div>

              <div className="space-y-1.5 bg-secondary/50 p-3.5 rounded-2xl border border-border-subtle">
                <div className="flex justify-between text-xs">
                  <span className="text-text-secondary">Recommendations Count:</span>
                  <span className="font-bold text-accent-blue font-mono">{limit} books</span>
                </div>
                <input
                  type="range"
                  min="4"
                  max="12"
                  step="2"
                  value={limit}
                  onChange={(e) => setLimit(parseInt(e.target.value))}
                  className="w-full accent-accent-blue"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Generate CTA */}
        <div className="pt-4 border-t border-border-subtle flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-xs text-text-muted">
            <Info size={14} className="text-accent-blue" />
            <span>
              Engine: <strong className="text-text-primary capitalize">{algorithm}</strong> | Seed:{' '}
              <strong className="text-text-primary">{selectedSeedBook ? selectedSeedBook.title : 'Cold Start'}</strong>
            </span>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full sm:w-auto px-8 py-3 rounded-2xl bg-gradient-to-r from-accent-purple to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-sm shadow-card flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            <span>{loading ? 'Computing Vectors...' : 'Generate Recommendations'}</span>
          </button>
        </div>
      </div>

      {/* Error alert */}
      {error && <ErrorMessage message={error} onRetry={handleGenerate} />}

      {/* Results Section */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold font-['Outfit'] text-text-primary">Generated Recommendations</h2>
            <p className="text-xs text-text-secondary mt-0.5">
              Ranked with algorithmic similarity scores and transparent explanation breakdown.
            </p>
          </div>
          {recommendations.length > 0 && (
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-semibold">
              {recommendations.length} Results
            </span>
          )}
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <BookCardSkeleton key={i} />
            ))}
          </div>
        ) : recommendations.length === 0 ? (
          <EmptyState
            title="Ready to Generate"
            description="Adjust your preferences above and click 'Generate Recommendations' to activate the recommendation model."
            onReset={handleGenerate}
            resetText="Generate Recommendations"
          />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {recommendations.map((item) => (
              <BookCard
                key={item.book.id || item.book.book_id}
                book={item.book}
                onSelect={onSelectBook}
                onToggleFavorite={onToggleFavorite}
                isFavorite={favorites.has(item.book.id || item.book.book_id)}
                similarityScore={item.similarity_score}
                explanation={item.explanation}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
};
