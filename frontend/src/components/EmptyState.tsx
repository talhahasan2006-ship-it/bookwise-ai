import React from 'react';
import { BookOpen, RefreshCw } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  onReset?: () => void;
  resetText?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No books found',
  description = 'Try adjusting your search criteria, filters, or minimum rating threshold.',
  onReset,
  resetText = 'Clear Filters',
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center bg-card/60 rounded-2xl border border-border-subtle max-w-lg mx-auto my-8">
      <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center text-accent-purple mb-4 border border-border-glow">
        <BookOpen size={32} />
      </div>
      <h3 className="text-xl font-bold text-text-primary mb-2 font-['Outfit']">{title}</h3>
      <p className="text-text-secondary text-sm mb-6 leading-relaxed">{description}</p>
      {onReset && (
        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-accent-purple/20 text-accent-purple hover:bg-accent-purple/30 border border-accent-purple/40 text-sm font-medium transition-all"
        >
          <RefreshCw size={16} />
          {resetText}
        </button>
      )}
    </div>
  );
};
