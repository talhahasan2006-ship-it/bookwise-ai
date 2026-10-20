import React, { useState } from 'react';
import { Bookmark, Heart, Sparkles, BookOpen } from 'lucide-react';
import { Book } from '../types';
import { RatingDisplay } from './RatingDisplay';

interface BookCardProps {
  book: Book;
  onSelect: (bookId: number) => void;
  onToggleFavorite?: (bookId: number, isFav: boolean) => void;
  isFavorite?: boolean;
  isInLibrary?: boolean;
  similarityScore?: number;
  explanation?: string;
}

export const BookCard: React.FC<BookCardProps> = ({
  book,
  onSelect,
  onToggleFavorite,
  isFavorite = false,
  similarityScore,
  explanation,
}) => {
  const [imgError, setImgError] = useState(false);

  // Genre badge color mapping
  const getGenreColor = (genre: string) => {
    const g = genre.toLowerCase();
    if (g.includes('sci') || g.includes('science fiction')) return 'bg-sky-500/15 text-sky-400 border-sky-500/30';
    if (g.includes('computer') || g.includes('ai')) return 'bg-purple-500/15 text-purple-400 border-purple-500/30';
    if (g.includes('fantasy')) return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
    if (g.includes('mystery') || g.includes('thriller')) return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
    if (g.includes('philosophy') || g.includes('psychology')) return 'bg-indigo-500/15 text-indigo-400 border-indigo-500/30';
    if (g.includes('classic') || g.includes('history')) return 'bg-rose-500/15 text-rose-400 border-rose-500/30';
    return 'bg-slate-700/30 text-slate-300 border-slate-600/40';
  };

  return (
    <div className="group relative bg-card hover:bg-card-hover rounded-2xl p-4 border border-border-subtle hover:border-accent-purple/50 transition-all duration-300 hover:shadow-card-hover flex flex-col h-full overflow-hidden">
      {/* Similarity score badge if present */}
      {similarityScore !== undefined && (
        <div className="absolute top-3 left-3 z-10 flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-accent-purple/90 backdrop-blur-md text-white text-xs font-semibold shadow-lg">
          <Sparkles size={12} className="animate-spin-slow" />
          <span>{Math.round(similarityScore * 100)}% Match</span>
        </div>
      )}

      {/* Favorite Toggle button */}
      {onToggleFavorite && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onToggleFavorite(book.id || book.book_id, !isFavorite);
          }}
          className={`absolute top-3 right-3 z-10 p-2 rounded-full backdrop-blur-md transition-all ${
            isFavorite
              ? 'bg-rose-500/90 text-white shadow-lg shadow-rose-500/30'
              : 'bg-black/40 text-slate-300 hover:text-white hover:bg-black/60'
          }`}
          title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
        >
          <Heart size={16} className={isFavorite ? 'fill-white' : ''} />
        </button>
      )}

      {/* Book Cover Container with reliable fallback */}
      <div
        onClick={() => onSelect(book.id || book.book_id)}
        className="relative w-full h-56 rounded-xl overflow-hidden mb-3.5 bg-secondary cursor-pointer flex items-center justify-center border border-border-subtle/50 group-hover:scale-[1.02] transition-transform duration-300"
      >
        {book.cover_url && !imgError ? (
          <img
            src={book.cover_url}
            alt={book.title}
            onError={() => setImgError(true)}
            className="w-full h-full object-cover object-center"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full p-4 flex flex-col justify-between items-center text-center bg-gradient-to-br from-secondary via-card to-secondary border border-border-glow">
            <BookOpen size={36} className="text-accent-purple/70 mt-4" />
            <div>
              <p className="font-bold text-sm text-text-primary line-clamp-2 font-['Outfit']">{book.title}</p>
              <p className="text-xs text-text-secondary mt-1">{book.author}</p>
            </div>
            <span className="text-[10px] tracking-wider uppercase text-accent-blue/80 font-mono">BookWise Edition</span>
          </div>
        )}
      </div>

      {/* Meta Content */}
      <div className="flex-1 flex flex-col">
        {/* Genre Badge */}
        <div className="flex items-center justify-between gap-2 mb-2">
          <span
            className={`text-[11px] font-medium px-2.5 py-0.5 rounded-full border ${getGenreColor(
              book.genre
            )}`}
          >
            {book.genre}
          </span>
          <span className="text-[11px] text-text-muted">{book.publication_year}</span>
        </div>

        {/* Title */}
        <h3
          onClick={() => onSelect(book.id || book.book_id)}
          className="font-bold text-base text-text-primary group-hover:text-accent-blue transition-colors cursor-pointer line-clamp-1 font-['Outfit'] mb-1"
          title={book.title}
        >
          {book.title}
        </h3>

        {/* Author */}
        <p className="text-xs text-text-secondary mb-2 line-clamp-1">by {book.author}</p>

        {/* Rating */}
        <div className="mb-2.5">
          <RatingDisplay rating={book.average_rating} ratingCount={book.rating_count} size="sm" />
        </div>

        {/* Explanation snippet if recommendation card */}
        {explanation ? (
          <p className="text-[11px] text-purple-300/90 bg-accent-purple/10 border border-purple-500/20 rounded-lg p-2 mb-3 line-clamp-2 leading-relaxed">
            {explanation}
          </p>
        ) : (
          <p className="text-xs text-text-muted line-clamp-2 mb-3 leading-relaxed">
            {book.description || 'No summary available for this catalog entry.'}
          </p>
        )}

        {/* Action Button */}
        <div className="mt-auto pt-2 border-t border-border-subtle flex items-center justify-between">
          <button
            onClick={() => onSelect(book.id || book.book_id)}
            className="text-xs font-medium text-accent-purple group-hover:text-accent-blue hover:underline inline-flex items-center gap-1 transition-colors"
          >
            <span>Explore Details</span>
            <span>→</span>
          </button>
          {book.isbn && (
            <span className="text-[10px] text-text-muted font-mono">
              ISBN: {String(book.isbn).slice(-4)}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
