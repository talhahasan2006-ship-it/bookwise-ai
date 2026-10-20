export interface Book {
  id?: number;
  book_id: number;
  title: string;
  author: string;
  genre: string;
  publication_year: number;
  publisher?: string;
  isbn?: string | number;
  average_rating: number;
  rating_count: number;
  description: string;
  cover_url: string;
}

export interface Recommendation {
  book: Book;
  similarity_score: number;
  score_breakdown?: {
    content: number;
    collaborative: number;
    popularity: number;
  };
  shared_keywords?: string[];
  explanation: string;
  algorithm: string;
}

export interface BooksResponse {
  books: Book[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  has_prev: boolean;
  has_next: boolean;
}

export interface LibraryEntry {
  id: number;
  user_id: string;
  book_id: number;
  status: 'want_to_read' | 'currently_reading' | 'completed';
  is_favorite: boolean;
  user_rating?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
  book: Book;
}

export interface LibraryResponse {
  user_profile: {
    username: string;
    user_id: string;
    is_demo: boolean;
    note: string;
  };
  count: number;
  entries: LibraryEntry[];
}

export interface StatsResponse {
  total_books: number;
  unique_authors: number;
  unique_genres: number;
  average_rating: number;
  total_ratings_volume: number;
  collaborative_ratings_count: number;
  unique_active_users: number;
  genres_distribution: { genre: string; count: number }[];
  ratings_distribution: { range: string; count: number }[];
  publication_era_distribution: { era: string; count: number }[];
  top_rated_books: Book[];
}

export interface GenreItem {
  genre: string;
  count: number;
}
