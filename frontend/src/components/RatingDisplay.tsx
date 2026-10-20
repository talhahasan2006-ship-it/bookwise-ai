import React from 'react';
import { Star } from 'lucide-react';

interface RatingDisplayProps {
  rating: number;
  ratingCount?: number;
  size?: 'sm' | 'md' | 'lg';
}

export const RatingDisplay: React.FC<RatingDisplayProps> = ({
  rating,
  ratingCount,
  size = 'md',
}) => {
  const starSize = size === 'sm' ? 14 : size === 'lg' ? 20 : 16;
  const textSize = size === 'sm' ? 'text-xs' : size === 'lg' ? 'text-base' : 'text-sm';

  return (
    <div className="flex items-center gap-1.5">
      <div className="flex items-center text-amber-400">
        {[1, 2, 3, 4, 5].map((star) => {
          const filled = rating >= star;
          const half = !filled && rating >= star - 0.5;
          return (
            <Star
              key={star}
              size={starSize}
              className={`${
                filled
                  ? 'fill-amber-400 text-amber-400'
                  : half
                  ? 'fill-amber-400/50 text-amber-400'
                  : 'text-slate-600'
              }`}
            />
          );
        })}
      </div>
      <span className={`font-semibold text-text-primary ${textSize}`}>
        {rating.toFixed(2)}
      </span>
      {ratingCount !== undefined && (
        <span className={`text-text-muted ${textSize}`}>
          ({ratingCount > 1000 ? `${(ratingCount / 1000).toFixed(1)}k` : ratingCount})
        </span>
      )}
    </div>
  );
};
