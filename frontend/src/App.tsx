import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { DiscoverPage } from './pages/DiscoverPage';
import { ExplorerPage } from './pages/ExplorerPage';
import { BookDetailsPage } from './pages/BookDetailsPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { LibraryPage } from './pages/LibraryPage';
import { DashboardPage } from './pages/DashboardPage';
import { fetchLibrary, updateLibraryEntry } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('discover');
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [explorerSearch, setExplorerSearch] = useState<string>('');
  const [explorerGenre, setExplorerGenre] = useState<string>('All');
  const [favorites, setFavorites] = useState<Set<number>>(new Set());
  const [libraryCount, setLibraryCount] = useState<number>(0);

  // Sync favorites & library count from SQLite
  const refreshLibraryState = async () => {
    try {
      const res = await fetchLibrary();
      const favSet = new Set<number>();
      res.entries.forEach((e) => {
        if (e.is_favorite) favSet.add(e.book_id);
      });
      setFavorites(favSet);
      setLibraryCount(res.count);
    } catch (err) {
      console.error('Error fetching library state:', err);
    }
  };

  useEffect(() => {
    refreshLibraryState();
  }, []);

  const handleSelectBook = (bookId: number) => {
    setSelectedBookId(bookId);
    setActiveTab('details');
  };

  const handleExploreGenre = (genre: string) => {
    setExplorerGenre(genre);
    setExplorerSearch('');
    setActiveTab('explorer');
  };

  const handleGlobalSearch = (query: string) => {
    setExplorerSearch(query);
    setExplorerGenre('All');
    setActiveTab('explorer');
  };

  const handleToggleFavorite = async (bookId: number, isFav: boolean) => {
    try {
      await updateLibraryEntry({
        book_id: bookId,
        is_favorite: isFav,
        status: isFav ? 'want_to_read' : undefined,
      });

      setFavorites((prev) => {
        const next = new Set(prev);
        if (isFav) next.add(bookId);
        else next.delete(bookId);
        return next;
      });

      refreshLibraryState();
    } catch (err) {
      console.error('Failed to toggle favorite:', err);
    }
  };

  return (
    <div className="min-h-screen bg-background text-text-primary flex flex-col selection:bg-accent-purple/30 selection:text-white">
      {/* Sticky Glass Navbar */}
      <Navbar
        activeTab={activeTab === 'details' ? 'explorer' : activeTab}
        setActiveTab={(tab) => {
          setSelectedBookId(null);
          setActiveTab(tab);
        }}
        libraryCount={libraryCount}
        onSearchSubmit={handleGlobalSearch}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeTab === 'discover' && (
          <DiscoverPage
            onSelectBook={handleSelectBook}
            onExploreGenre={handleExploreGenre}
            onSearch={handleGlobalSearch}
            onOpenExplorer={() => setActiveTab('explorer')}
            onToggleFavorite={handleToggleFavorite}
            favorites={favorites}
          />
        )}

        {activeTab === 'explorer' && (
          <ExplorerPage
            initialSearch={explorerSearch}
            initialGenre={explorerGenre}
            onSelectBook={handleSelectBook}
            onToggleFavorite={handleToggleFavorite}
            favorites={favorites}
          />
        )}

        {activeTab === 'details' && selectedBookId !== null && (
          <BookDetailsPage
            bookId={selectedBookId}
            onBack={() => setActiveTab('explorer')}
            onSelectBook={handleSelectBook}
            onToggleFavorite={handleToggleFavorite}
            isFavorite={favorites.has(selectedBookId)}
            onLibraryUpdated={refreshLibraryState}
          />
        )}

        {activeTab === 'recommendations' && (
          <RecommendationsPage
            onSelectBook={handleSelectBook}
            onToggleFavorite={handleToggleFavorite}
            favorites={favorites}
          />
        )}

        {activeTab === 'library' && (
          <LibraryPage
            onSelectBook={handleSelectBook}
            onExploreClick={() => setActiveTab('explorer')}
          />
        )}

        {activeTab === 'dashboard' && (
          <DashboardPage onSelectBook={handleSelectBook} />
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
