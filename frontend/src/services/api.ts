import { Book, BooksResponse, Recommendation, LibraryResponse, StatsResponse, GenreItem } from '../types';
import { clientRecommender } from './clientRecommender';

const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || '/api';
let isBackendAvailable: boolean | null = null;

// Probe backend availability once on startup
async function checkBackend(): Promise<boolean> {
  if (isBackendAvailable !== null) return isBackendAvailable;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1200);
    const res = await fetch(`${API_BASE_URL}/health`, { signal: controller.signal });
    clearTimeout(timeoutId);
    isBackendAvailable = res.ok;
  } catch {
    isBackendAvailable = false;
  }
  return isBackendAvailable;
}

export async function fetchBooks(params: {
  page?: number;
  per_page?: number;
  q?: string;
  genre?: string;
  author?: string;
  min_rating?: number;
  year_from?: number;
  year_to?: number;
  sort_by?: string;
}): Promise<BooksResponse> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return clientRecommender.getBooks(params);
  }

  try {
    const query = new URLSearchParams();
    if (params.page) query.set('page', params.page.toString());
    if (params.per_page) query.set('per_page', params.per_page.toString());
    if (params.q) query.set('q', params.q);
    if (params.genre && params.genre !== 'All') query.set('genre', params.genre);
    if (params.author && params.author !== 'All') query.set('author', params.author);
    if (params.min_rating) query.set('min_rating', params.min_rating.toString());
    if (params.year_from) query.set('year_from', params.year_from.toString());
    if (params.year_to) query.set('year_to', params.year_to.toString());
    if (params.sort_by) query.set('sort_by', params.sort_by);

    const res = await fetch(`${API_BASE_URL}/books?${query.toString()}`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return clientRecommender.getBooks(params);
  }
}

export async function fetchBookDetails(bookId: number): Promise<{ book: Book }> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    const book = clientRecommender.getBookById(bookId);
    if (!book) throw new Error('Book not found');
    return { book };
  }

  try {
    const res = await fetch(`${API_BASE_URL}/books/${bookId}`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    const book = clientRecommender.getBookById(bookId);
    if (!book) throw new Error('Book not found');
    return { book };
  }
}

export async function fetchSimilarBooks(bookId: number, limit = 6): Promise<{ source_book: Book; recommendations: Recommendation[] }> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    const source = clientRecommender.getBookById(bookId);
    if (!source) throw new Error('Source book not found');
    const recs = clientRecommender.recommendContent(bookId, limit);
    return { source_book: source, recommendations: recs };
  }

  try {
    const res = await fetch(`${API_BASE_URL}/books/${bookId}/similar?limit=${limit}`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    const source = clientRecommender.getBookById(bookId);
    if (!source) throw new Error('Source book not found');
    const recs = clientRecommender.recommendContent(bookId, limit);
    return { source_book: source, recommendations: recs };
  }
}

export async function fetchPopularRecommendations(limit = 8, genre?: string): Promise<{ algorithm: string; recommendations: Recommendation[] }> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    const recs = clientRecommender.recommendPopular(limit, genre);
    return { algorithm: 'Bayesian Weighted Popularity Ranking', recommendations: recs };
  }

  try {
    const query = new URLSearchParams();
    query.set('limit', limit.toString());
    if (genre && genre !== 'All') query.set('genre', genre);
    const res = await fetch(`${API_BASE_URL}/recommendations/popular?${query.toString()}`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    const recs = clientRecommender.recommendPopular(limit, genre);
    return { algorithm: 'Bayesian Weighted Popularity Ranking', recommendations: recs };
  }
}

export async function fetchPersonalizedRecommendations(payload: {
  seed_book_id?: number;
  preferred_genres?: string[];
  min_rating?: number;
  limit?: number;
  algorithm?: 'hybrid' | 'content' | 'collaborative' | 'popular';
}): Promise<{
  algorithm: string;
  seed_book: Book | null;
  recommendations: Recommendation[];
}> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return clientRecommender.recommendPersonalized(payload);
  }

  try {
    const res = await fetch(`${API_BASE_URL}/recommendations/personalized`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return clientRecommender.recommendPersonalized(payload);
  }
}

export async function fetchGenres(): Promise<{ genres: GenreItem[] }> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return { genres: clientRecommender.getGenres() };
  }

  try {
    const res = await fetch(`${API_BASE_URL}/genres`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return { genres: clientRecommender.getGenres() };
  }
}

export async function fetchStats(): Promise<StatsResponse> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return clientRecommender.getStats();
  }

  try {
    const res = await fetch(`${API_BASE_URL}/stats`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return clientRecommender.getStats();
  }
}

export async function fetchLibrary(status?: string, favoritesOnly = false): Promise<LibraryResponse> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return clientRecommender.getLibrary(status, favoritesOnly);
  }

  try {
    const query = new URLSearchParams();
    if (status && status !== 'All') query.set('status', status);
    if (favoritesOnly) query.set('favorites', 'true');
    const res = await fetch(`${API_BASE_URL}/library?${query.toString()}`);
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return clientRecommender.getLibrary(status, favoritesOnly);
  }
}

export async function updateLibraryEntry(payload: {
  book_id: number;
  status?: string;
  is_favorite?: boolean;
  user_rating?: number;
  notes?: string;
}): Promise<{ message: string; entry: unknown }> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return clientRecommender.saveLibraryEntry(payload);
  }

  try {
    const res = await fetch(`${API_BASE_URL}/library`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return clientRecommender.saveLibraryEntry(payload);
  }
}

export async function removeFromLibrary(bookId: number): Promise<{ message: string }> {
  const hasBackend = await checkBackend();
  if (!hasBackend) {
    return clientRecommender.removeLibraryEntry(bookId);
  }

  try {
    const res = await fetch(`${API_BASE_URL}/library/${bookId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Backend failed');
    return await res.json();
  } catch {
    return clientRecommender.removeLibraryEntry(bookId);
  }
}
