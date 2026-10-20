import React from 'react';
import { BookOpen, Sparkles, Terminal, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-24 border-t border-border-subtle bg-secondary/40 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="md:col-span-2 space-y-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-accent-purple/20 border border-accent-purple/40 flex items-center justify-center">
              <BookOpen size={18} className="text-accent-blue" />
            </div>
            <span className="font-bold text-lg text-text-primary font-['Outfit']">BookWise AI</span>
          </div>
          <p className="text-xs text-text-secondary leading-relaxed max-w-md">
            Intelligent Book Recommendation System built for B.Tech Computer Science and Engineering (Artificial Intelligence and Machine Learning) NTCC project.
            Combines TF-IDF feature extraction, Cosine Similarity, Bayesian Weighted Rating, and Item-Based Collaborative Filtering.
          </p>
          <div className="flex flex-wrap items-center gap-2 pt-2">
            <span className="px-2.5 py-1 rounded-md bg-secondary text-slate-300 text-[11px] border border-border-subtle inline-flex items-center gap-1.5">
              <Cpu size={12} className="text-accent-purple" />
              Scikit-Learn & Python Flask
            </span>
            <span className="px-2.5 py-1 rounded-md bg-secondary text-slate-300 text-[11px] border border-border-subtle inline-flex items-center gap-1.5">
              <Sparkles size={12} className="text-accent-blue" />
              React & TypeScript & Tailwind
            </span>
            <span className="px-2.5 py-1 rounded-md bg-secondary text-slate-300 text-[11px] border border-border-subtle inline-flex items-center gap-1.5">
              <Terminal size={12} className="text-emerald-400" />
              SQLite & SQLAlchemy
            </span>
          </div>
        </div>

        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-text-primary mb-3 font-mono">Algorithms</h4>
          <ul className="space-y-2 text-xs text-text-secondary">
            <li className="hover:text-accent-purple transition-colors">TF-IDF Vectorization & Cosine Similarity</li>
            <li className="hover:text-accent-purple transition-colors">Item-Item Collaborative Filtering</li>
            <li className="hover:text-accent-purple transition-colors">Bayesian Weighted Popularity (IMDb/Goodreads)</li>
            <li className="hover:text-accent-purple transition-colors">Hybrid Linear Combination Engine</li>
            <li className="hover:text-accent-purple transition-colors">Cold-Start Bayesian Fallback</li>
          </ul>
        </div>

        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-text-primary mb-3 font-mono">Evaluation Metrics</h4>
          <ul className="space-y-2 text-xs text-text-secondary">
            <li>Precision@5: <span className="text-emerald-400 font-semibold font-mono">0.2000</span></li>
            <li>Recall@5: <span className="text-emerald-400 font-semibold font-mono">0.2493</span></li>
            <li>NDCG@5: <span className="text-emerald-400 font-semibold font-mono">0.4068</span></li>
            <li>Rating RMSE: <span className="text-emerald-400 font-semibold font-mono">0.8979</span></li>
            <li>Genre Coherence: <span className="text-emerald-400 font-semibold font-mono">93.45%</span></li>
          </ul>
        </div>
      </div>

      <div className="max-w-7xl mx-auto mt-8 pt-6 border-t border-border-subtle flex flex-col sm:flex-row items-center justify-between text-xs text-text-muted gap-3">
        <p>© 2026 BookWise AI. B.Tech CSE (AIML) NTCC Project Portfolio.</p>
        <p className="font-mono text-[11px]">Academic Open-Source Implementation</p>
      </div>
    </footer>
  );
};
