import React, { useEffect, useState } from 'react';
import { Search, Sparkles, BookOpen, Compass, ChevronRight, Star, Flame, Brain, Cpu, Shield, Globe } from 'lucide-react';
import { Book, Recommendation, GenreItem } from '../types';
import { fetchPopularRecommendations, fetchGenres, fetchPersonalizedRecommendations, fetchBooks } from '../services/api';
import { BookCard } from '../components/BookCard';
import { BookCardSkeleton } from '../components/LoadingSkeleton';

interface DiscoverPageProps {
  onSelectBook: (bookId: number) => void;
  onExploreGenre: (genre: string) => void;
  onSearch: (query: string) => void;
  onOpenExplorer: () => void;
  onToggleFavorite: (bookId: number, isFav: boolean) => void;
  favorites: Set<number>;
}

export const DiscoverPage: React.FC<DiscoverPageProps> = ({
  onSelectBook,
  onExploreGenre,
  onSearch,
  onOpenExplorer,
  onToggleFavorite,
  favorites,
}) => {
  const [heroSearch, setHeroSearch] = useState('');
  const [suggestions, setSuggestions] = useState<Book[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [popularBooks, setPopularBooks] = useState<Recommendation[]>([]);
  const [curatedRecs, setCuratedRecs] = useState<Recommendation[]>([]);
  const [selectedMoodGenre, setSelectedMoodGenre] = useState<string>('Science Fiction');
  const [genres, setGenres] = useState<GenreItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true);
        const [popRes, genreRes] = await Promise.all([
          fetchPopularRecommendations(8),
          fetchGenres(),
        ]);
        setPopularBooks(popRes.recommendations || []);
        setGenres(genreRes.genres || []);

        // Load mood recommendations for default genre
        const recRes = await fetchPersonalizedRecommendations({
          preferred_genres: ['Science Fiction'],
          limit: 4,
          algorithm: 'hybrid',
        });
        setCuratedRecs(recRes.recommendations || []);
      } catch (err) {
        console.error('Error loading discover page data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadInitialData();
  }, []);

  // Quick suggestions as user types in hero search
  useEffect(() => {
    if (heroSearch.trim().length >= 2) {
      const timer = setTimeout(async () => {
        try {
          const res = await fetchBooks({ q: heroSearch.trim(), per_page: 5 });
          setSuggestions(res.books);
          setShowSuggestions(true);
        } catch {
          setSuggestions([]);
        }
      }, 250);
      return () => clearTimeout(timer);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [heroSearch]);

  const handleMoodChange = async (genre: string) => {
    setSelectedMoodGenre(genre);
    try {
      const recRes = await fetchPersonalizedRecommendations({
        preferred_genres: [genre],
        limit: 4,
        algorithm: 'hybrid',
      });
      setCuratedRecs(recRes.recommendations || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleHeroSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (heroSearch.trim()) {
      onSearch(heroSearch.trim());
      onOpenExplorer();
    }
  };

  const genreIcons: Record<string, React.ReactNode> = {
    'Science Fiction': <Globe className="text-sky-400" size={24} />,
    'Computer Science & AI': <Cpu className="text-purple-400" size={24} />,
    'Fantasy': <Sparkles className="text-emerald-400" size={24} />,
    'Mystery & Thriller': <Shield className="text-amber-400" size={24} />,
    'Science & Philosophy': <Brain className="text-indigo-400" size={24} />,
    'Psychology & Self-Help': <Flame className="text-rose-400" size={24} />,
  };

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-16 px-4 sm:px-6 lg:px-8 text-center max-w-5xl mx-auto">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-accent-purple/15 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="absolute top-1/3 left-1/4 w-[400px] h-[250px] bg-accent-blue/10 rounded-full blur-[100px] pointer-events-none"></div>

        <div className="relative z-10 space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-accent-purple/10 border border-accent-purple/30 text-accent-purple text-xs font-semibold backdrop-blur-md">
            <Sparkles size={14} className="text-accent-blue" />
            <span>Machine Learning Powered Book Discovery</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight font-['Outfit'] text-text-primary leading-tight">
            Discover Your Next <br />
            <span className="bg-gradient-to-r from-accent-purple via-sky-400 to-indigo-300 bg-clip-text text-transparent">
              Favourite Book
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-base sm:text-lg text-text-secondary leading-relaxed">
            Personalized book recommendations powered by machine learning, designed around your interests, reading preferences, and literary themes.
          </p>

          {/* Search Bar with live autocomplete */}
          <div className="max-w-2xl mx-auto relative mt-8">
            <form onSubmit={handleHeroSubmit} className="relative flex items-center">
              <Search className="absolute left-4 text-text-muted" size={20} />
              <input
                type="text"
                value={heroSearch}
                onChange={(e) => setHeroSearch(e.target.value)}
                onFocus={() => heroSearch.trim().length >= 2 && setShowSuggestions(true)}
                placeholder="Search by book title, author, or genre (e.g. Dune, Orwell, AI)..."
                className="w-full bg-secondary/90 border border-border-subtle focus:border-accent-purple rounded-2xl pl-12 pr-32 py-4 text-sm text-text-primary placeholder:text-text-muted focus:outline-none shadow-card transition-all"
              />
              <button
                type="submit"
                className="absolute right-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-accent-purple to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium text-xs shadow-md transition-all flex items-center gap-1.5"
              >
                <span>Explore Books</span>
                <ChevronRight size={14} />
              </button>
            </form>

            {/* Suggestions dropdown */}
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-secondary border border-border-glow rounded-2xl shadow-card overflow-hidden z-30 text-left">
                {suggestions.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => {
                      onSelectBook(item.id || item.book_id);
                      setShowSuggestions(false);
                    }}
                    className="p-3 hover:bg-card flex items-center gap-3 cursor-pointer border-b border-border-subtle last:border-none transition-colors"
                  >
                    <BookOpen size={16} className="text-accent-blue shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-text-primary truncate">{item.title}</p>
                      <p className="text-xs text-text-secondary truncate">by {item.author} • {item.genre}</p>
                    </div>
                    <span className="text-xs text-amber-400 font-mono font-semibold">★ {item.average_rating.toFixed(1)}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Quick Filter Tags */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
            <span className="text-text-muted mr-1">Trending Searches:</span>
            {['Dune', 'Deep Learning', 'Brandon Sanderson', '1984', 'Marcus Aurelius'].map((tag) => (
              <button
                key={tag}
                onClick={() => {
                  onSearch(tag);
                  onOpenExplorer();
                }}
                className="px-3 py-1 rounded-full bg-secondary/60 hover:bg-card border border-border-subtle text-slate-300 hover:text-white transition-all text-[11px]"
              >
                {tag}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Bayesian Popular Books */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-accent-purple font-mono">
              <Flame size={14} className="text-amber-400" />
              <span>Verified Masterpieces</span>
            </div>
            <h2 className="text-2xl font-bold font-['Outfit'] text-text-primary mt-1">Featured Popular Books</h2>
          </div>
          <button
            onClick={onOpenExplorer}
            className="text-xs font-semibold text-accent-blue hover:underline flex items-center gap-1"
          >
            <span>View Catalogue ({genres.reduce((acc, g) => acc + g.count, 0)} Books)</span>
            <ChevronRight size={14} />
          </button>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <BookCardSkeleton key={i} />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {popularBooks.slice(0, 4).map((item) => (
              <BookCard
                key={item.book.id || item.book.book_id}
                book={item.book}
                onSelect={onSelectBook}
                onToggleFavorite={onToggleFavorite}
                isFavorite={favorites.has(item.book.id || item.book.book_id)}
                explanation={item.explanation}
              />
            ))}
          </div>
        )}
      </section>

      {/* Interactive Mood Recommender Teaser */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-card via-secondary to-card border border-border-glow rounded-3xl p-6 sm:p-8 relative overflow-hidden shadow-card">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-accent-blue">Interactive AI Lab</span>
              <h2 className="text-2xl font-bold font-['Outfit'] text-text-primary mt-1">What are you in the mood to read?</h2>
              <p className="text-xs text-text-secondary mt-1">Select a genre to see personalized hybrid recommendations instantly generated.</p>
            </div>
            {/* Genre Pills */}
            <div className="flex flex-wrap gap-2">
              {[
                'Science Fiction',
                'Computer Science & AI',
                'Fantasy',
                'Science & Philosophy',
                'Psychology & Self-Help',
                'Mystery & Thriller'
              ].map((genre) => (
                <button
                  key={genre}
                  onClick={() => handleMoodChange(genre)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all ${
                    selectedMoodGenre === genre
                      ? 'bg-accent-purple text-white shadow-glow'
                      : 'bg-secondary text-text-secondary hover:text-white border border-border-subtle'
                  }`}
                >
                  {genre}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {curatedRecs.map((item) => (
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
        </div>
      </section>

      {/* Genre Exploration Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-accent-purple">Taxonomy & Categories</span>
          <h2 className="text-2xl font-bold font-['Outfit'] text-text-primary mt-1">Explore Literary Genres</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {genres.slice(0, 6).map((g) => (
            <div
              key={g.genre}
              onClick={() => onExploreGenre(g.genre)}
              className="group p-5 rounded-2xl bg-card border border-border-subtle hover:border-accent-purple/50 cursor-pointer transition-all hover:shadow-card-hover flex items-center justify-between"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-secondary flex items-center justify-center border border-border-subtle group-hover:scale-110 transition-transform">
                  {genreIcons[g.genre] || <BookOpen size={24} className="text-slate-400" />}
                </div>
                <div>
                  <h3 className="font-bold text-sm text-text-primary group-hover:text-accent-blue transition-colors font-['Outfit']">
                    {g.genre}
                  </h3>
                  <p className="text-xs text-text-muted mt-0.5">{g.count} titles in dataset</p>
                </div>
              </div>
              <ChevronRight size={18} className="text-text-muted group-hover:text-accent-purple group-hover:translate-x-1 transition-all" />
            </div>
          ))}
        </div>
      </section>

      {/* Trending Books Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-accent-blue">Community Engagement</span>
          <h2 className="text-2xl font-bold font-['Outfit'] text-text-primary mt-1">Trending Among Readers</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {popularBooks.slice(4, 8).map((item) => (
            <BookCard
              key={item.book.id || item.book.book_id}
              book={item.book}
              onSelect={onSelectBook}
              onToggleFavorite={onToggleFavorite}
              isFavorite={favorites.has(item.book.id || item.book.book_id)}
              explanation={item.explanation}
            />
          ))}
        </div>
      </section>
    </div>
  );
};
