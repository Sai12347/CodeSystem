import React from 'react';
import { Sparkles, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-zinc-200 dark:border-zinc-800/80 bg-zinc-50 dark:bg-black py-8 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-zinc-500 dark:text-zinc-500">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded bg-blue-600 flex items-center justify-center text-white">
            <Sparkles className="w-3 h-3" />
          </div>
          <span className="font-semibold text-zinc-700 dark:text-zinc-300">CodeSystem</span>
          <span>— Production Interactive DSA Learning Platform</span>
        </div>

        <div className="flex items-center gap-1">
          <span>Engineered with</span>
          <Heart className="w-3.5 h-3.5 text-red-500 fill-current inline" />
          <span>for deep algorithmic mastery & interview excellence</span>
        </div>

        <div className="flex items-center gap-4">
          <span>WCAG 2.2 AA Compliant</span>
          <span>•</span>
          <span>Deterministic TS Engine</span>
        </div>
      </div>
    </footer>
  );
};
