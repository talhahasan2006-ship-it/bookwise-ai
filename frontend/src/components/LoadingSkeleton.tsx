import React from 'react';

export const BookCardSkeleton: React.FC = () => {
  return (
    <div className="bg-card rounded-xl p-4 border border-border-subtle animate-pulse flex flex-col h-[400px]">
      <div className="w-full h-52 bg-slate-800 rounded-lg mb-3"></div>
      <div className="h-5 bg-slate-800 rounded w-3/4 mb-2"></div>
      <div className="h-4 bg-slate-800 rounded w-1/2 mb-4"></div>
      <div className="h-3 bg-slate-800 rounded w-full mb-2"></div>
      <div className="h-3 bg-slate-800 rounded w-4/5 mb-4"></div>
      <div className="mt-auto pt-3 border-t border-slate-800 flex justify-between items-center">
        <div className="h-4 bg-slate-800 rounded w-1/3"></div>
        <div className="h-8 bg-slate-800 rounded w-20"></div>
      </div>
    </div>
  );
};

export const DashboardSkeleton: React.FC = () => {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-28 bg-card rounded-xl border border-border-subtle"></div>
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-80 bg-card rounded-xl border border-border-subtle"></div>
        <div className="h-80 bg-card rounded-xl border border-border-subtle"></div>
      </div>
    </div>
  );
};
