import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useVisualizer } from '../../context/VisualizerContext';
import { VisualElement } from '../../types/algorithm';

export const VisualizerCanvas: React.FC = () => {
  const { currentStep, metadata } = useVisualizer();
  const elements = currentStep.elements;

  const getStateClasses = (state: VisualElement['state']) => {
    switch (state) {
      case 'comparing':
        return 'bg-amber-500 text-white border-amber-600 dark:border-amber-400 shadow-md shadow-amber-500/30 scale-105';
      case 'swapping':
        return 'bg-rose-500 text-white border-rose-600 dark:border-rose-400 shadow-md shadow-rose-500/30 scale-110';
      case 'sorted':
        return 'bg-emerald-500 text-white border-emerald-600 dark:border-emerald-400 shadow-sm shadow-emerald-500/20';
      case 'found':
        return 'bg-emerald-600 text-white border-emerald-400 ring-4 ring-emerald-400/30 shadow-lg shadow-emerald-600/40 scale-110';
      case 'active':
        return 'bg-blue-600 text-white border-blue-500 shadow-md shadow-blue-500/30 scale-105';
      case 'pivot':
        return 'bg-purple-600 text-white border-purple-400 shadow-md shadow-purple-500/30 scale-105';
      case 'window':
        return 'bg-indigo-500/20 text-indigo-700 dark:text-indigo-300 border-indigo-400 ring-2 ring-indigo-500/40';
      case 'eliminated':
        return 'bg-zinc-200/50 dark:bg-zinc-800/40 text-zinc-400 dark:text-zinc-600 border-zinc-200 dark:border-zinc-800 opacity-40';
      case 'default':
      default:
        return 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 border-zinc-200 dark:border-zinc-700 shadow-apple-sm';
    }
  };

  return (
    <div className="relative w-full min-h-[340px] md:min-h-[380px] bg-zinc-50 dark:bg-zinc-950/60 rounded-3xl p-6 border border-zinc-200/80 dark:border-zinc-800/80 flex flex-col justify-between overflow-hidden shadow-sm transition-colors">
      {/* Canvas Top Bar: Algorithm Name & Step Description */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-4 border-b border-zinc-200/60 dark:border-zinc-800/60">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold tracking-tight text-zinc-900 dark:text-white">
              {metadata.title}
            </h2>
            <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400">
              {metadata.difficulty}
            </span>
          </div>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            {metadata.subcategory}
          </p>
        </div>

        {/* Step Badge */}
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-mono font-medium bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border border-zinc-200 dark:border-zinc-700">
            Step {currentStep.stepIndex + 1} of {currentStep.totalSteps || elements.length}
          </span>
        </div>
      </div>

      {/* Step Explanation Banner */}
      <motion.div
        key={currentStep.stepIndex}
        initial={{ opacity: 0, y: -4 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
        className="my-3 px-4 py-2.5 rounded-2xl bg-white/80 dark:bg-zinc-900/80 border border-zinc-200/60 dark:border-zinc-800/60 backdrop-blur-sm"
      >
        <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 leading-snug">
          {currentStep.description}
        </p>
      </motion.div>

      {/* Main Elements Canvas */}
      <div className="flex-1 flex items-end justify-center gap-2 md:gap-4 py-6 px-2 overflow-x-auto min-h-[180px]">
        <AnimatePresence mode="popLayout">
          {elements.map((el) => {
            const height = el.heightPercent ? `${el.heightPercent}%` : '80px';
            const stateClass = getStateClasses(el.state);

            return (
              <motion.div
                key={el.id}
                layout
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ type: 'spring', stiffness: 400, damping: 28 }}
                className="flex flex-col items-center gap-2 min-w-[44px] md:min-w-[54px]"
              >
                {/* Pointer / SubLabel Tag at the Top */}
                <div className="h-6 flex items-center justify-center">
                  {el.subLabel ? (
                    <motion.span
                      initial={{ scale: 0.7 }}
                      animate={{ scale: 1 }}
                      className="px-2 py-0.5 rounded-full text-[11px] font-bold font-mono uppercase bg-blue-600 text-white shadow-sm"
                    >
                      {el.subLabel}
                    </motion.span>
                  ) : null}
                </div>

                {/* Animated Box / Bar */}
                <div
                  style={{ minHeight: '64px', height: height }}
                  className={`w-full max-w-[64px] rounded-2xl border-2 flex flex-col items-center justify-center p-2 font-mono font-bold text-base md:text-lg transition-colors duration-200 ${stateClass}`}
                >
                  <span>{el.value}</span>
                </div>

                {/* Index / Bottom Label */}
                <div className="h-5 flex items-center justify-center">
                  <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400">
                    [{el.label}]
                  </span>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Color Legend */}
      <div className="pt-3 border-t border-zinc-200/60 dark:border-zinc-800/60 flex flex-wrap items-center justify-center gap-4 text-xs text-zinc-600 dark:text-zinc-400">
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-md bg-amber-500"></span>
          <span>Comparing</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-md bg-rose-500"></span>
          <span>Swapping / Shift</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-md bg-emerald-500"></span>
          <span>Sorted / Found</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-md bg-blue-600"></span>
          <span>Active / Low / Mid</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-md bg-zinc-300 dark:bg-zinc-700"></span>
          <span>Eliminated</span>
        </div>
      </div>
    </div>
  );
};
