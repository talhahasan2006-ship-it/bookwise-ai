import React from 'react';
import { AlertCircle, RotateCcw } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <div className="bg-rose-950/40 border border-rose-800/60 rounded-xl p-5 my-6 flex items-start gap-4 text-rose-200">
      <AlertCircle className="text-rose-400 shrink-0 mt-0.5" size={20} />
      <div className="flex-1">
        <h4 className="font-semibold text-rose-100 text-sm">Operation Failed</h4>
        <p className="text-xs text-rose-300 mt-1">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-900/50 hover:bg-rose-900 border border-rose-700/60 text-xs font-medium text-rose-200 transition-colors"
        >
          <RotateCcw size={14} />
          Retry
        </button>
      )}
    </div>
  );
};
