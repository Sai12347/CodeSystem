import React from 'react';
import { useVisualizer } from '../../context/VisualizerContext';
import { Clock, HardDrive, AlertTriangle } from 'lucide-react';

export const ComplexityCard: React.FC = () => {
  const { metadata } = useVisualizer();

  return (
    <div className="w-full bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-4 shadow-apple-sm transition-colors flex flex-col gap-4">
      {/* Time & Space Complexity */}
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-3">
          Complexity Analysis
        </h3>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/60 dark:border-zinc-800/60">
            <div className="flex items-center gap-1.5 text-zinc-500 dark:text-zinc-400 mb-1">
              <Clock className="w-3.5 h-3.5" />
              <span>Time Complexity</span>
            </div>
            <div className="space-y-1 font-mono text-[11px]">
              <div>
                <span className="text-zinc-400">Best:</span>{' '}
                <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                  {metadata.timeComplexity.best}
                </span>
              </div>
              <div>
                <span className="text-zinc-400">Avg:</span>{' '}
                <span className="font-semibold text-amber-600 dark:text-amber-400">
                  {metadata.timeComplexity.average}
                </span>
              </div>
              <div>
                <span className="text-zinc-400">Worst:</span>{' '}
                <span className="font-semibold text-rose-600 dark:text-rose-400">
                  {metadata.timeComplexity.worst}
                </span>
              </div>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/60 dark:border-zinc-800/60 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-1.5 text-zinc-500 dark:text-zinc-400 mb-1">
                <HardDrive className="w-3.5 h-3.5" />
                <span>Space Complexity</span>
              </div>
              <p className="font-mono text-xs font-semibold text-blue-600 dark:text-blue-400 mt-1">
                {metadata.spaceComplexity}
              </p>
            </div>
            <p className="text-[10px] text-zinc-400 mt-2">
              Auxiliary memory allocated during execution
            </p>
          </div>
        </div>
      </div>

      {/* Common Mistakes */}
      {metadata.commonMistakes && metadata.commonMistakes.length > 0 && (
        <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-600 dark:text-amber-400 mb-2">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Common Pitfalls</span>
          </div>
          <ul className="space-y-1 text-xs text-zinc-600 dark:text-zinc-400 list-disc list-inside">
            {metadata.commonMistakes.map((m, i) => (
              <li key={i} className="leading-relaxed">
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
