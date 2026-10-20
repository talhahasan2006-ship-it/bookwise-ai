import React, { useState, useEffect } from 'react';
import { Search, Filter, SlidersHorizontal, ArrowUpDown, ChevronLeft, ChevronRight, X, RotateCcw } from 'lucide-react';
import { Book, GenreItem } from '../types';
import { fetchBooks, fetchGenres } from '../services/api';
import { BookCard } from '../components/BookCard';
import { BookCardSkeleton } from '../components/LoadingSkeleton';
import { EmptyState } from '../components/EmptyState';
import { ErrorMessage } from '../components/ErrorMessage';

interface ExplorerPageProps {
  initialSearch?: string;
  initialGenre?: string;
  onSelectBook: (bookId: number) => void;
  onToggleFavorite: (bookId: number, isFav: boolean) => void;
  favorites: Set<number>;
}

export const ExplorerPage: React.FC<ExplorerPageProps> = ({
  initialSearch = '',
  initialGenre = 'All',
  onSelectBook,
  onToggleFavorite,
  favorites,
}) => {
  const [books, setBooks] = useState<Book[]>([]);
  const [genres, setGenres] = useState<GenreItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filter States
  const [search, setSearch] = useState(initialSearch);
  const [selectedGenre, setSelectedGenre] = useState(initialGenre);
  const [minRating, setMinRating] = useState<number>(0.0);
  const [sortBy, setSortBy] = useState<string>('popular');
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalBooks, setTotalBooks] = useState<number>(0);
  const [showFilterPanel, setShowFilterPanel] = useState<boolean>(false);

  useEffect(() => {
    async function loadGenres() {
      try {
        const res = await fetchGenres();
        setGenres(res.genres || []);
      } catch (err) {
        console.error(err);
      }
    }
    loadGenres();
  }, []);

  useEffect(() => {
    if (initialGenre) setSelectedGenre(initialGenre);
  }, [initialGenre]);

  useEffect(() => {
    if (initialSearch) setSearch(initialSearch);
  }, [initialSearch]);

  const loadBooks = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetchBooks({
        page,
        per_page: 12,
        q: search.trim(),
        genre: selectedGenre !== 'All' ? selectedGenre : undefined,
        min_rating: minRating > 0 ? minRating : undefined,
        sort_by: sortBy,
      });
      setBooks(res.books);
      setTotalPages(res.total_pages);
      setTotalBooks(res.total);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to fetch catalogue');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, [page, selectedGenre, minRating, sortBy]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadBooks();
  };

  const handleResetFilters = () => {
    setSearch('');
    setSelectedGenre('All');
    setMinRating(0.0);
    setSortBy('popular');
    setPage(1);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
        <div>
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-accent-purple">Catalogue Explorer</span>
          <h1 className="text-3xl font-extrabold font-['Outfit'] text-text-primary mt-1">Book Explorer</h1>
          <p className="text-xs text-text-secondary mt-1">
            Browse, search, and filter through {totalBooks} verified book records in our recommendation dataset.
          </p>
        </div>

        {/* Mobile Filter toggle */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowFilterPanel(!showFilterPanel)}
            className="md:hidden flex items-center gap-1.5 px-3 py-2 rounded-xl bg-card border border-border-subtle text-xs font-medium text-text-secondary"
          >
            <SlidersHorizontal size={14} />
            <span>Filters</span>
          </button>
        </div>
      </div>

      {/* Control Bar: Search + Sort + Quick Filters */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="md:col-span-5 relative">
          <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by title, author, or keyword..."
            className="w-full bg-secondary border border-border-subtle rounded-xl pl-10 pr-10 py-2.5 text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-purple"
          />
          {search && (
            <button
              type="button"
              onClick={() => {
                setSearch('');
                setPage(1);
              }}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-white"
            >
              <X size={14} />
            </button>
          )}
        </form>

        {/* Genre Selector */}
        <div className="md:col-span-3">
          <select
            value={selectedGenre}
            onChange={(e) => {
              setSelectedGenre(e.target.value);
              setPage(1);
            }}
            className="w-full bg-secondary border border-border-subtle rounded-xl px-3 py-2.5 text-xs text-text-primary focus:outline-none focus:border-accent-purple"
          >
            <option value="All">All Genres ({genres.reduce((a, b) => a + b.count, 0)})</option>
            {genres.map((g) => (
              <option key={g.genre} value={g.genre}>
                {g.genre} ({g.count})
              </option>
            ))}
          </select>
        </div>

        {/* Min Rating Selector */}
        <div className="md:col-span-2">
          <select
            value={minRating}
            onChange={(e) => {
              setMinRating(parseFloat(e.target.value));
              setPage(1);
            }}
            className="w-full bg-secondary border border-border-subtle rounded-xl px-3 py-2.5 text-xs text-text-primary focus:outline-none focus:border-accent-purple"
          >
            <option value="0">Any Rating</option>
            <option value="4.0">★ 4.0 & above</option>
            <option value="4.2">★ 4.2 & above</option>
            <option value="4.4">★ 4.4 & above</option>
            <option value="4.6">★ 4.6 & above</option>
          </select>
        </div>

        {/* Sort Selector */}
        <div className="md:col-span-2">
          <div className="relative">
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value);
                setPage(1);
              }}
              className="w-full bg-secondary border border-border-subtle rounded-xl px-3 py-2.5 text-xs text-text-primary focus:outline-none focus:border-accent-purple appearance-none pr-8"
            >
              <option value="popular">Most Popular</option>
              <option value="highest_rated">Highest Rated</option>
              <option value="title_asc">Title A–Z</option>
              <option value="year_desc">Newest First</option>
              <option value="year_asc">Oldest First</option>
            </select>
            <ArrowUpDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Active Filter chips */}
      {(selectedGenre !== 'All' || minRating > 0 || search) && (
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
          <span className="text-text-muted">Active Filters:</span>
          {selectedGenre !== 'All' && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-accent-purple/20 text-accent-purple border border-accent-purple/30 text-[11px]">
              Genre: {selectedGenre}
              <button onClick={() => setSelectedGenre('All')} className="hover:text-white">
                <X size={12} />
              </button>
            </span>
          )}
          {minRating > 0 && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 text-[11px]">
              ★ {minRating}+
              <button onClick={() => setMinRating(0.0)} className="hover:text-white">
                <X size={12} />
              </button>
            </span>
          )}
          {search && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/30 text-[11px]">
              Query: "{search}"
              <button onClick={() => setSearch('')} className="hover:text-white">
                <X size={12} />
              </button>
            </span>
          )}
          <button
            onClick={handleResetFilters}
            className="text-xs text-text-muted hover:text-white underline inline-flex items-center gap-1 ml-2"
          >
            <RotateCcw size={12} />
            Reset all
          </button>
        </div>
      )}

      {/* Error state */}
      {error && <ErrorMessage message={error} onRetry={loadBooks} />}

      {/* Book Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
            <BookCardSkeleton key={i} />
          ))}
        </div>
      ) : books.length === 0 ? (
        <EmptyState
          title="No Books Match Your Criteria"
          description="We couldn't find any titles matching your filter combination. Try clearing your search keyword or relaxing the minimum rating filter."
          onReset={handleResetFilters}
          resetText="Reset Filters"
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {books.map((book) => (
            <BookCard
              key={book.id || book.book_id}
              book={book}
              onSelect={onSelectBook}
              onToggleFavorite={onToggleFavorite}
              isFavorite={favorites.has(book.id || book.book_id)}
            />
          ))}
        </div>
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-6 border-t border-border-subtle">
          <p className="text-xs text-text-secondary">
            Showing Page <span className="font-semibold text-text-primary">{page}</span> of{' '}
            <span className="font-semibold text-text-primary">{totalPages}</span> ({totalBooks} books total)
          </p>
          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-xl bg-secondary border border-border-subtle disabled:opacity-40 disabled:cursor-not-allowed hover:bg-card text-text-primary transition-colors"
            >
              <ChevronLeft size={16} />
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => (
              <button
                key={pageNum}
                onClick={() => setPage(pageNum)}
                className={`w-8 h-8 rounded-xl text-xs font-semibold transition-all ${
                  page === pageNum
                    ? 'bg-accent-purple text-white shadow-glow'
                    : 'bg-secondary text-text-secondary hover:text-white border border-border-subtle'
                }`}
              >
                {pageNum}
              </button>
            ))}
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 rounded-xl bg-secondary border border-border-subtle disabled:opacity-40 disabled:cursor-not-allowed hover:bg-card text-text-primary transition-colors"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
