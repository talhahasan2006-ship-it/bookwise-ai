import React, { useEffect, useState } from 'react';
import { ArrowLeft, BookOpen, Heart, Sparkles, Calendar, Building, Hash, Share2, Check, Bookmark } from 'lucide-react';
import { Book, Recommendation } from '../types';
import { fetchBookDetails, fetchSimilarBooks, updateLibraryEntry } from '../services/api';
import { RatingDisplay } from '../components/RatingDisplay';
import { BookCard } from '../components/BookCard';
import { BookCardSkeleton } from '../components/LoadingSkeleton';
import { ErrorMessage } from '../components/ErrorMessage';

interface BookDetailsPageProps {
  bookId: number;
  onBack: () => void;
  onSelectBook: (bookId: number) => void;
  onToggleFavorite: (bookId: number, isFav: boolean) => void;
  isFavorite: boolean;
  onLibraryUpdated?: () => void;
}

export const BookDetailsPage: React.FC<BookDetailsPageProps> = ({
  bookId,
  onBack,
  onSelectBook,
  onToggleFavorite,
  isFavorite,
  onLibraryUpdated,
}) => {
  const [book, setBook] = useState<Book | null>(null);
  const [similarBooks, setSimilarBooks] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [similarLoading, setSimilarLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [imgError, setImgError] = useState(false);
  const [readingStatus, setReadingStatus] = useState<string>('want_to_read');
  const [statusSaved, setStatusSaved] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError(null);
        setImgError(false);
        const bookRes = await fetchBookDetails(bookId);
        setBook(bookRes.book);

        // Load similar books from recommender engine
        setSimilarLoading(true);
        const simRes = await fetchSimilarBooks(bookId, 4);
        setSimilarBooks(simRes.recommendations || []);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load book details');
      } finally {
        setLoading(false);
        setSimilarLoading(false);
      }
    }
    loadData();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [bookId]);

  const handleStatusChange = async (newStatus: string) => {
    setReadingStatus(newStatus);
    try {
      await updateLibraryEntry({
        book_id: bookId,
        status: newStatus,
        is_favorite: isFavorite,
      });
      setStatusSaved(true);
      if (onLibraryUpdated) onLibraryUpdated();
      setTimeout(() => setStatusSaved(false), 2000);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12 space-y-8 animate-pulse">
        <div className="h-8 w-32 bg-slate-800 rounded-lg"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="h-96 bg-slate-800 rounded-2xl"></div>
          <div className="md:col-span-2 space-y-4">
            <div className="h-10 bg-slate-800 rounded w-3/4"></div>
            <div className="h-5 bg-slate-800 rounded w-1/3"></div>
            <div className="h-32 bg-slate-800 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs text-text-secondary hover:text-white mb-6"
        >
          <ArrowLeft size={16} />
          <span>Back to Catalogue</span>
        </button>
        <ErrorMessage message={error || 'Book could not be found.'} onRetry={() => window.location.reload()} />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* Navigation Breadcrumb */}
      <div>
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-secondary/80 hover:bg-card border border-border-subtle text-xs text-text-secondary hover:text-white transition-colors"
        >
          <ArrowLeft size={14} />
          <span>Back</span>
        </button>
      </div>

      {/* Main Details Hero */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start bg-card/70 border border-border-subtle rounded-3xl p-6 sm:p-10 shadow-card">
        {/* Book Cover Column */}
        <div className="lg:col-span-4 flex flex-col items-center">
          <div className="relative w-64 h-96 rounded-2xl overflow-hidden shadow-2xl bg-secondary border border-border-glow flex items-center justify-center">
            {book.cover_url && !imgError ? (
              <img
                src={book.cover_url}
                alt={book.title}
                onError={() => setImgError(true)}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full p-6 flex flex-col justify-between items-center text-center bg-gradient-to-br from-secondary via-card to-secondary border border-border-glow">
                <BookOpen size={48} className="text-accent-purple/70 mt-6" />
                <div>
                  <h3 className="font-extrabold text-base text-text-primary line-clamp-3 font-['Outfit']">{book.title}</h3>
                  <p className="text-xs text-text-secondary mt-2">by {book.author}</p>
                </div>
                <span className="text-[10px] tracking-wider uppercase text-accent-blue/80 font-mono">BookWise Curated</span>
              </div>
            )}
          </div>

          {/* Quick Action Buttons */}
          <div className="w-64 mt-5 space-y-2.5">
            <button
              onClick={() => onToggleFavorite(book.id || book.book_id, !isFavorite)}
              className={`w-full py-2.5 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                isFavorite
                  ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40 hover:bg-rose-500/30'
                  : 'bg-secondary hover:bg-slate-800 text-text-primary border border-border-subtle'
              }`}
            >
              <Heart size={16} className={isFavorite ? 'fill-rose-400 text-rose-400' : ''} />
              <span>{isFavorite ? 'Saved to Favorites' : 'Add to Favorites'}</span>
            </button>

            {/* Reading List Selector */}
            <div className="relative">
              <select
                value={readingStatus}
                onChange={(e) => handleStatusChange(e.target.value)}
                className="w-full bg-secondary border border-border-subtle text-text-primary text-xs rounded-xl px-3 py-2.5 focus:outline-none focus:border-accent-purple"
              >
                <option value="want_to_read">Reading List: Want to Read</option>
                <option value="currently_reading">Status: Currently Reading</option>
                <option value="completed">Status: Completed</option>
              </select>
              {statusSaved && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2 text-emerald-400 flex items-center gap-1 text-[11px] font-mono">
                  <Check size={14} />
                  <span>Saved</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Book Metadata Column */}
        <div className="lg:col-span-8 space-y-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-purple/15 text-accent-purple border border-accent-purple/30 text-xs font-semibold">
              <Sparkles size={12} className="text-accent-blue" />
              <span>{book.genre}</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-text-primary font-['Outfit'] leading-tight">
              {book.title}
            </h1>
            <p className="text-base text-text-secondary">
              by <span className="font-semibold text-text-primary">{book.author}</span>
            </p>
          </div>

          {/* Rating */}
          <div className="flex items-center gap-3 py-3 border-y border-border-subtle">
            <RatingDisplay rating={book.average_rating} ratingCount={book.rating_count} size="lg" />
            <span className="text-xs text-text-muted">•</span>
            <span className="text-xs text-emerald-400 font-mono">Verified Metric</span>
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-secondary/70 p-3 rounded-xl border border-border-subtle">
              <span className="text-[10px] text-text-muted uppercase font-mono flex items-center gap-1">
                <Calendar size={12} /> Publication
              </span>
              <p className="font-semibold text-sm text-text-primary mt-1">{book.publication_year || 'Unknown'}</p>
            </div>
            <div className="bg-secondary/70 p-3 rounded-xl border border-border-subtle">
              <span className="text-[10px] text-text-muted uppercase font-mono flex items-center gap-1">
                <Building size={12} /> Publisher
              </span>
              <p className="font-semibold text-xs text-text-primary mt-1 truncate">{book.publisher || 'Independent'}</p>
            </div>
            <div className="bg-secondary/70 p-3 rounded-xl border border-border-subtle">
              <span className="text-[10px] text-text-muted uppercase font-mono flex items-center gap-1">
                <Hash size={12} /> ISBN
              </span>
              <p className="font-semibold text-xs text-text-primary mt-1 font-mono">{book.isbn || 'N/A'}</p>
            </div>
            <div className="bg-secondary/70 p-3 rounded-xl border border-border-subtle">
              <span className="text-[10px] text-text-muted uppercase font-mono">Catalog ID</span>
              <p className="font-semibold text-xs text-text-primary mt-1 font-mono">#{book.id || book.book_id}</p>
            </div>
          </div>

          {/* Synopsis */}
          <div className="space-y-2">
            <h3 className="text-sm font-bold uppercase tracking-wider text-text-primary font-mono">Synopsis & Thematic Overview</h3>
            <p className="text-sm text-text-secondary leading-relaxed bg-secondary/40 p-4 rounded-xl border border-border-subtle">
              {book.description || 'No detailed description available for this catalog entry.'}
            </p>
          </div>
        </div>
      </div>

      {/* "Readers Also Explore" Recommendation Section */}
      <section className="space-y-6 pt-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-accent-purple">
            <Sparkles size={14} className="text-accent-blue" />
            <span>AI Similarity Engine</span>
          </div>
          <h2 className="text-2xl font-bold font-['Outfit'] text-text-primary mt-1">Readers Also Explore</h2>
          <p className="text-xs text-text-secondary mt-1">
            Similar books dynamically computed using natural language TF-IDF similarity and multi-user rating correlations.
          </p>
        </div>

        {similarLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <BookCardSkeleton key={i} />
            ))}
          </div>
        ) : similarBooks.length === 0 ? (
          <p className="text-xs text-text-muted">No similar books found in this specific cluster.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {similarBooks.map((item) => (
              <BookCard
                key={item.book.id || item.book.book_id}
                book={item.book}
                onSelect={onSelectBook}
                onToggleFavorite={onToggleFavorite}
                isFavorite={isFavorite}
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
