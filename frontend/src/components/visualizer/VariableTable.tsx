import React from 'react';
import { useVisualizer } from '../../context/VisualizerContext';
import { motion } from 'framer-motion';

export const VariableTable: React.FC = () => {
  const { currentStep } = useVisualizer();
  const variables = currentStep.variables;
  const changedVars = currentStep.changedVariables || [];

  const entries = Object.entries(variables);

  return (
    <div className="w-full bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-4 shadow-apple-sm transition-colors flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
          Live Variable Tracking
        </h3>
        <span className="text-[11px] text-zinc-400">
          Updated dynamically per step
        </span>
      </div>

      {entries.length === 0 ? (
        <p className="text-xs text-zinc-400 italic py-2">No active variables for this step.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5">
          {entries.map(([key, value]) => {
            const isChanged = changedVars.includes(key);
            const displayVal = value !== null && value !== undefined ? String(value) : '—';

            return (
              <motion.div
                key={key}
                animate={isChanged ? { scale: [1, 1.05, 1] } : {}}
                transition={{ duration: 0.3 }}
                className={`p-2.5 rounded-xl border flex flex-col justify-between transition-colors ${
                  isChanged
                    ? 'bg-blue-50 dark:bg-blue-950/40 border-blue-400/80 dark:border-blue-600'
                    : 'bg-zinc-50 dark:bg-zinc-800/50 border-zinc-200/60 dark:border-zinc-800/60'
                }`}
              >
                <span className="text-[11px] font-mono font-semibold text-zinc-500 dark:text-zinc-400 truncate">
                  {key}
                </span>
                <span
                  className={`text-sm font-mono font-bold truncate mt-0.5 ${
                    isChanged
                      ? 'text-blue-600 dark:text-blue-400'
                      : 'text-zinc-900 dark:text-zinc-100'
                  }`}
                >
                  {displayVal}
                </span>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};
