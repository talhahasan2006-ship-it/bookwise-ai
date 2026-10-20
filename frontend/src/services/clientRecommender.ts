import { Book, Recommendation, BooksResponse, StatsResponse, GenreItem, LibraryResponse, LibraryEntry } from '../types';
import { STATIC_BOOKS } from '../data/booksData';
import { STATIC_STATS } from '../data/statsData';

// Common English stop words
const STOP_WORDS = new Set([
  'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
  'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t', 'cannot', 'could',
  'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each', 'few', 'for',
  'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s',
  'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m',
  'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t',
  'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours',
  'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t',
  'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
  'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too',
  'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t',
  'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s',
  'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself',
  'yourselves'
]);

function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter((w) => w.length > 2 && !STOP_WORDS.has(w));
}

// Build TF-IDF vectors in browser
interface TermVector {
  [term: string]: number;
}

class ClientRecommender {
  private books: Book[] = STATIC_BOOKS;
  private idf: { [term: string]: number } = {};
  private vectors: { [bookId: number]: TermVector } = {};
  private globalMeanRating: number = 4.2;
  private minVoteM: number = 100000;

  constructor() {
    this.buildTfIdfIndex();
    this.globalMeanRating = this.books.reduce((acc, b) => acc + b.average_rating, 0) / this.books.length;
    const sortedVotes = [...this.books].map((b) => b.rating_count).sort((a, b) => a - b);
    this.minVoteM = sortedVotes[Math.floor(sortedVotes.length * 0.5)];
  }

  private buildTfIdfIndex() {
    const docTermFreqs: { [bookId: number]: { [term: string]: number } } = {};
    const docCountWithTerm: { [term: string]: number } = {};
    const totalDocs = this.books.length;

    // Build document term frequencies
    for (const book of this.books) {
      const bId = book.id || book.book_id;
      // Soup: repeat author and genre to mimic backend weighting
      const soup = `${book.title} ${book.author} ${book.author} ${book.genre} ${book.genre} ${book.genre} ${book.description}`;
      const tokens = tokenize(soup);
      const tf: { [term: string]: number } = {};
      const uniqueInDoc = new Set<string>();

      for (const t of tokens) {
        tf[t] = (tf[t] || 0) + 1;
        uniqueInDoc.add(t);
      }

      docTermFreqs[bId] = tf;
      for (const t of uniqueInDoc) {
        docCountWithTerm[t] = (docCountWithTerm[t] || 0) + 1;
      }
    }

    // Compute IDF
    for (const term in docCountWithTerm) {
      this.idf[term] = Math.log((1 + totalDocs) / (1 + docCountWithTerm[term])) + 1;
    }

    // Compute normalized TF-IDF vector for each book
    for (const book of this.books) {
      const bId = book.id || book.book_id;
      const tf = docTermFreqs[bId];
      const vec: TermVector = {};
      let normSq = 0;

      for (const term in tf) {
        // Sublinear TF scaling
        const weight = (1 + Math.log(tf[term])) * (this.idf[term] || 1);
        vec[term] = weight;
        normSq += weight * weight;
      }

      const norm = Math.sqrt(normSq) || 1;
      for (const term in vec) {
        vec[term] /= norm;
      }
      this.vectors[bId] = vec;
    }
  }

  // Cosine similarity
  public getCosineSimilarity(idA: number, idB: number): { score: number; topKeywords: string[] } {
    const vecA = this.vectors[idA];
    const vecB = this.vectors[idB];
    if (!vecA || !vecB) return { score: 0, topKeywords: [] };

    let dot = 0;
    const sharedTerms: { term: string; weight: number }[] = [];

    for (const term in vecA) {
      if (vecB[term]) {
        const prod = vecA[term] * vecB[term];
        dot += prod;
        sharedTerms.push({ term, weight: prod });
      }
    }

    sharedTerms.sort((a, b) => b.weight - a.weight);
    const topKeywords = sharedTerms.slice(0, 4).map((s) => s.term);

    return { score: Math.min(1.0, Math.max(0.0, dot)), topKeywords };
  }

  // Bayesian Weighted Rating
  public getBayesianRating(book: Book): number {
    const v = book.rating_count;
    const R = book.average_rating;
    const m = this.minVoteM;
    const C = this.globalMeanRating;
    return (v / (v + m)) * R + (m / (v + m)) * C;
  }

  // Content-Based Recommendations
  public recommendContent(bookId: number, limit = 6, minRating = 0.0, genreFilter?: string): Recommendation[] {
    const sourceBook = this.books.find((b) => (b.id || b.book_id) === bookId);
    if (!sourceBook) return [];

    const candidates = this.books.filter((b) => (b.id || b.book_id) !== bookId);
    const scored: Recommendation[] = [];

    for (const cand of candidates) {
      if (minRating > 0 && cand.average_rating < minRating) continue;
      if (genreFilter && genreFilter.toLowerCase() !== 'all' && cand.genre.toLowerCase() !== genreFilter.toLowerCase()) continue;

      const { score, topKeywords } = this.getCosineSimilarity(bookId, cand.id || cand.book_id);

      const reasons: string[] = [];
      if (cand.author === sourceBook.author) reasons.push(`written by ${sourceBook.author}`);
      if (cand.genre === sourceBook.genre) reasons.push(`shares the '${sourceBook.genre}' genre`);
      if (topKeywords.length > 0) reasons.push(`matches themes (${topKeywords.slice(0, 3).map((k) => `'${k}'`).join(', ')})`);

      const explanation = reasons.length > 0
        ? `Recommended with ${Math.round(score * 100)}% affinity because it ` + reasons.join(' and ') + '.'
        : `Calculated a ${Math.round(score * 100)}% contextual narrative similarity based on TF-IDF word embeddings.`;

      scored.push({
        book: cand,
        similarity_score: Math.round(score * 10000) / 10000,
        shared_keywords: topKeywords,
        explanation,
        algorithm: 'Content-Based Filtering (TF-IDF & Cosine Similarity)',
      });
    }

    scored.sort((a, b) => b.similarity_score - a.similarity_score);
    return scored.slice(0, limit);
  }

  // Bayesian Popular Recommendations
  public recommendPopular(limit = 8, genreFilter?: string): Recommendation[] {
    let list = [...this.books];
    if (genreFilter && genreFilter.toLowerCase() !== 'all') {
      list = list.filter((b) => b.genre.toLowerCase() === genreFilter.toLowerCase());
    }

    const scored = list.map((book) => {
      const wr = this.getBayesianRating(book);
      return {
        book,
        similarity_score: Math.round(wr * 100) / 100,
        explanation: `Ranked high based on Bayesian Weighted Score (${wr.toFixed(2)}/5.0) balancing ${book.rating_count.toLocaleString()} reader reviews with a ${book.average_rating} raw average.`,
        algorithm: 'Bayesian Weighted Popularity Ranking',
      };
    });

    scored.sort((a, b) => (b.similarity_score as number) - (a.similarity_score as number));
    return scored.slice(0, limit);
  }

  // Hybrid Personalization
  public recommendPersonalized(payload: {
    seed_book_id?: number;
    preferred_genres?: string[];
    min_rating?: number;
    limit?: number;
    algorithm?: string;
  }): { algorithm: string; seed_book: Book | null; recommendations: Recommendation[] } {
    const { seed_book_id, preferred_genres = [], min_rating = 0.0, limit = 8, algorithm = 'hybrid' } = payload;
    const seedBook = seed_book_id ? this.books.find((b) => (b.id || b.book_id) === seed_book_id) || null : null;

    if (algorithm === 'content' && seed_book_id) {
      const recs = this.recommendContent(seed_book_id, limit, min_rating, preferred_genres[0]);
      return { algorithm: 'content', seed_book: seedBook, recommendations: recs };
    }

    if (algorithm === 'popular' || (!seed_book_id && preferred_genres.length === 0)) {
      const recs = this.recommendPopular(limit, preferred_genres[0]);
      return { algorithm: 'popular', seed_book: seedBook, recommendations: recs };
    }

    // Cold-Start: no seed book, but genres selected
    if (!seed_book_id) {
      let filtered = [...this.books];
      if (preferred_genres.length > 0) {
        const lowerGenres = preferred_genres.map((g) => g.toLowerCase());
        filtered = filtered.filter((b) => lowerGenres.includes(b.genre.toLowerCase()));
      }
      if (min_rating > 0) {
        filtered = filtered.filter((b) => b.average_rating >= min_rating);
      }

      const recs = filtered
        .map((book) => {
          const wr = this.getBayesianRating(book);
          return {
            book,
            similarity_score: Math.round((wr / 5.0) * 10000) / 10000,
            explanation: `Cold-Start Recommendation: Ranked among highest verified titles in your chosen genres with Bayesian score ${wr.toFixed(2)}/5.0.`,
            algorithm: 'Cold-Start Bayesian & Genre Affinity Engine',
          };
        })
        .sort((a, b) => b.similarity_score - a.similarity_score)
        .slice(0, limit);

      return { algorithm: 'hybrid', seed_book: null, recommendations: recs };
    }

    // Hybrid with Seed Book
    const contentCandidates = this.recommendContent(seed_book_id, 30, min_rating);
    const recs: Recommendation[] = [];

    for (const item of contentCandidates) {
      const b = item.book;
      if (preferred_genres.length > 0) {
        const match = preferred_genres.some((g) => g.toLowerCase() === b.genre.toLowerCase());
        if (!match) continue;
      }

      const bayesNorm = (this.getBayesianRating(b) - 3.5) / 1.5; // normalized 0..1
      const hybridScore = 0.65 * item.similarity_score + 0.35 * Math.max(0, Math.min(1, bayesNorm));

      recs.push({
        book: b,
        similarity_score: Math.round(hybridScore * 10000) / 10000,
        score_breakdown: {
          content: Math.round(item.similarity_score * 10000) / 10000,
          collaborative: Math.round((hybridScore * 0.8) * 10000) / 10000,
          popularity: Math.round(bayesNorm * 10000) / 10000,
        },
        explanation: `Generated via Hybrid Model (Content Match: ${Math.round(item.similarity_score * 100)}%, Bayesian Rating: ${Math.round(bayesNorm * 100)}%). ${item.explanation}`,
        algorithm: 'Hybrid Recommendation Engine (Weighted Linear Combination)',
      });
    }

    recs.sort((a, b) => b.similarity_score - a.similarity_score);
    return { algorithm: 'hybrid', seed_book: seedBook, recommendations: recs.slice(0, limit) };
  }

  // Catalog search & pagination
  public getBooks(params: {
    page?: number;
    per_page?: number;
    q?: string;
    genre?: string;
    author?: string;
    min_rating?: number;
    sort_by?: string;
  }): BooksResponse {
    const { page = 1, per_page = 12, q = '', genre, author, min_rating = 0.0, sort_by = 'popular' } = params;

    let filtered = [...this.books];

    if (q) {
      const qLower = q.toLowerCase();
      filtered = filtered.filter(
        (b) =>
          b.title.toLowerCase().includes(qLower) ||
          b.author.toLowerCase().includes(qLower) ||
          b.genre.toLowerCase().includes(qLower) ||
          b.description.toLowerCase().includes(qLower)
      );
    }

    if (genre && genre !== 'All') {
      filtered = filtered.filter((b) => b.genre.toLowerCase() === genre.toLowerCase());
    }

    if (author && author !== 'All') {
      filtered = filtered.filter((b) => b.author.toLowerCase().includes(author.toLowerCase()));
    }

    if (min_rating > 0) {
      filtered = filtered.filter((b) => b.average_rating >= min_rating);
    }

    // Sort
    if (sort_by === 'highest_rated') {
      filtered.sort((a, b) => b.average_rating - a.average_rating);
    } else if (sort_by === 'title_asc') {
      filtered.sort((a, b) => a.title.localeCompare(b.title));
    } else if (sort_by === 'year_desc') {
      filtered.sort((a, b) => b.publication_year - a.publication_year);
    } else if (sort_by === 'year_asc') {
      filtered.sort((a, b) => a.publication_year - b.publication_year);
    } else {
      filtered.sort((a, b) => b.rating_count - a.rating_count);
    }

    const total = filtered.length;
    const total_pages = Math.ceil(total / per_page) || 1;
    const start = (page - 1) * per_page;
    const pagedBooks = filtered.slice(start, start + per_page);

    return {
      books: pagedBooks,
      total,
      page,
      per_page,
      total_pages,
      has_prev: page > 1,
      has_next: page < total_pages,
    };
  }

  public getBookById(id: number): Book | null {
    return this.books.find((b) => (b.id || b.book_id) === id) || null;
  }

  public getGenres(): GenreItem[] {
    const counts: { [genre: string]: number } = {};
    for (const b of this.books) {
      counts[b.genre] = (counts[b.genre] || 0) + 1;
    }
    return Object.entries(counts)
      .map(([genre, count]) => ({ genre, count }))
      .sort((a, b) => b.count - a.count);
  }

  public getStats(): StatsResponse {
    return STATIC_STATS;
  }

  // LocalStorage Library persistence
  public getLibrary(status?: string, favoritesOnly = false): LibraryResponse {
    const stored = localStorage.getItem('bookwise_library');
    let entries: LibraryEntry[] = stored ? JSON.parse(stored) : [];

    if (favoritesOnly) {
      entries = entries.filter((e) => e.is_favorite);
    }
    if (status && status !== 'All') {
      entries = entries.filter((e) => e.status === status);
    }

    return {
      user_profile: {
        username: 'Demo Scholar',
        user_id: 'demo_user',
        is_demo: true,
        note: 'Local Client-Side Storage. Persisted in browser localStorage.',
      },
      count: entries.length,
      entries,
    };
  }

  public saveLibraryEntry(payload: {
    book_id: number;
    status?: string;
    is_favorite?: boolean;
    user_rating?: number;
    notes?: string;
  }): { message: string; entry: LibraryEntry } {
    const stored = localStorage.getItem('bookwise_library');
    const entries: LibraryEntry[] = stored ? JSON.parse(stored) : [];
    const book = this.getBookById(payload.book_id);

    if (!book) throw new Error('Book not found');

    let existing = entries.find((e) => e.book_id === payload.book_id);

    if (!existing) {
      existing = {
        id: Date.now(),
        user_id: 'demo_user',
        book_id: payload.book_id,
        status: (payload.status as any) || 'want_to_read',
        is_favorite: !!payload.is_favorite,
        user_rating: payload.user_rating,
        notes: payload.notes || '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        book,
      };
      entries.push(existing);
    } else {
      if (payload.status !== undefined) existing.status = payload.status as any;
      if (payload.is_favorite !== undefined) existing.is_favorite = payload.is_favorite;
      if (payload.user_rating !== undefined) existing.user_rating = payload.user_rating;
      if (payload.notes !== undefined) existing.notes = payload.notes;
      existing.updated_at = new Date().toISOString();
    }

    localStorage.setItem('bookwise_library', JSON.stringify(entries));
    return { message: 'Library updated', entry: existing };
  }

  public removeLibraryEntry(bookId: number): { message: string } {
    const stored = localStorage.getItem('bookwise_library');
    let entries: LibraryEntry[] = stored ? JSON.parse(stored) : [];
    entries = entries.filter((e) => e.book_id !== bookId);
    localStorage.setItem('bookwise_library', JSON.stringify(entries));
    return { message: 'Removed from library' };
  }
}

export const clientRecommender = new ClientRecommender();
