import React, { useState } from 'react';
import { BookOpen, Sparkles, Compass, Library, BarChart3, Search, UserCheck } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  libraryCount: number;
  onSearchSubmit: (query: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  libraryCount,
  onSearchSubmit,
}) => {
  const [navSearch, setNavSearch] = useState('');

  const handleSearchKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && navSearch.trim()) {
      onSearchSubmit(navSearch.trim());
      setActiveTab('explorer');
    }
  };

  const navLinks = [
    { id: 'discover', label: 'Discover', icon: Compass },
    { id: 'explorer', label: 'Book Explorer', icon: BookOpen },
    { id: 'recommendations', label: 'AI Recommender', icon: Sparkles },
    { id: 'library', label: 'My Library', icon: Library, badge: libraryCount },
    { id: 'dashboard', label: 'Analytics', icon: BarChart3 },
  ];

  return (
    <nav className="sticky top-0 z-50 glass-nav">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-4">
          {/* Logo */}
          <div
            onClick={() => setActiveTab('discover')}
            className="flex items-center gap-3 cursor-pointer select-none group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-accent-purple to-accent-blue p-0.5 shadow-glow flex items-center justify-center">
              <div className="w-full h-full bg-background rounded-[10px] flex items-center justify-center">
                <BookOpen size={20} className="text-accent-blue group-hover:scale-110 transition-transform" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight font-['Outfit'] bg-gradient-to-r from-white via-slate-100 to-accent-blue bg-clip-text text-transparent">
                  BookWise
                </span>
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-accent-purple/30 text-accent-purple border border-accent-purple/50">
                  AI
                </span>
              </div>
              <p className="text-[10px] text-text-muted hidden sm:block">Intelligent Book Recommendation</p>
            </div>
          </div>

          {/* Search bar inside header */}
          <div className="hidden md:flex items-center flex-1 max-w-xs relative">
            <Search size={16} className="absolute left-3 text-text-muted" />
            <input
              type="text"
              value={navSearch}
              onChange={(e) => setNavSearch(e.target.value)}
              onKeyDown={handleSearchKey}
              placeholder="Quick search titles, authors..."
              className="w-full bg-secondary/80 border border-border-subtle rounded-xl pl-9 pr-3 py-1.5 text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-purple transition-all"
            />
          </div>

          {/* Navigation Links */}
          <div className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = activeTab === link.id;
              return (
                <button
                  key={link.id}
                  onClick={() => setActiveTab(link.id)}
                  className={`relative flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                    isActive
                      ? 'text-white bg-accent-purple/20 border border-accent-purple/40 shadow-sm'
                      : 'text-text-secondary hover:text-text-primary hover:bg-secondary/60'
                  }`}
                >
                  <Icon size={16} className={isActive ? 'text-accent-blue' : ''} />
                  <span>{link.label}</span>
                  {link.badge !== undefined && link.badge > 0 && (
                    <span className="ml-0.5 px-1.5 py-0.2 rounded-full bg-accent-purple text-white text-[10px] font-bold">
                      {link.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Local Demo User Profile badge */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 bg-secondary/70 border border-border-subtle px-3 py-1.5 rounded-full text-xs">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
              <UserCheck size={14} className="text-accent-blue" />
              <span className="text-text-secondary text-xs hidden sm:inline">Demo Scholar</span>
            </div>
          </div>
        </div>

        {/* Mobile Navigation bar */}
        <div className="flex lg:hidden overflow-x-auto py-2 gap-1 border-t border-border-subtle scrollbar-none">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = activeTab === link.id;
            return (
              <button
                key={link.id}
                onClick={() => setActiveTab(link.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs whitespace-nowrap font-medium transition-colors ${
                  isActive
                    ? 'text-white bg-accent-purple/25 border border-accent-purple/40'
                    : 'text-text-secondary hover:text-white'
                }`}
              >
                <Icon size={14} />
                <span>{link.label}</span>
                {link.badge !== undefined && link.badge > 0 && (
                  <span className="px-1.5 py-0.2 rounded-full bg-accent-purple text-white text-[10px]">
                    {link.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};
