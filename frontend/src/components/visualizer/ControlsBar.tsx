import React, { useState } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  SlidersHorizontal,
  Shuffle,
  HelpCircle,
  Edit3,
} from 'lucide-react';
import { useVisualizer } from '../../context/VisualizerContext';
import { CustomInputModal } from './CustomInputModal';

export const ControlsBar: React.FC = () => {
  const {
    isPlaying,
    togglePlay,
    nextStep,
    previousStep,
    reset,
    speed,
    setSpeed,
    predictMode,
    togglePredictMode,
    currentStepIndex,
    totalSteps,
    jumpToStep,
    generateRandomInput,
  } = useVisualizer();

  const [isInputModalOpen, setIsInputModalOpen] = useState(false);
  const speeds = [0.25, 0.5, 1, 2, 4];

  return (
    <>
      <div className="w-full bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-4 shadow-apple-sm flex flex-col gap-4 transition-colors">
        {/* Scrubber & Step Slider */}
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 min-w-[28px]">
            {currentStepIndex + 1}
          </span>
          <input
            type="range"
            min={0}
            max={Math.max(0, totalSteps - 1)}
            value={currentStepIndex}
            onChange={(e) => jumpToStep(Number(e.target.value))}
            aria-label="Algorithm execution step slider"
            className="flex-1 h-2 bg-zinc-200 dark:bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-blue-600 focus:outline-none"
          />
          <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 min-w-[28px] text-right">
            {totalSteps}
          </span>
        </div>

        {/* Buttons Row */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          {/* Playback Controls */}
          <div className="flex items-center gap-1 sm:gap-2">
            {/* Reset */}
            <button
              onClick={reset}
              aria-label="Reset algorithm"
              title="Reset (R)"
              className="p-2.5 rounded-xl text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            {/* Previous Step */}
            <button
              onClick={previousStep}
              disabled={currentStepIndex <= 0}
              aria-label="Previous step"
              title="Previous Step (← or J)"
              className="p-2.5 rounded-xl text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <SkipBack className="w-4 h-4" />
            </button>

            {/* Play / Pause Primary Button */}
            <button
              onClick={togglePlay}
              aria-label={isPlaying ? 'Pause' : 'Play'}
              title="Play / Pause (Space)"
              className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm flex items-center gap-2 shadow-sm shadow-blue-500/20 active:scale-95 transition-all"
            >
              {isPlaying ? (
                <>
                  <Pause className="w-4 h-4 fill-current" />
                  <span>Pause</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  <span>Play</span>
                </>
              )}
            </button>

            {/* Next Step */}
            <button
              onClick={nextStep}
              disabled={currentStepIndex >= totalSteps - 1}
              aria-label="Next step"
              title="Next Step (→ or L)"
              className="p-2.5 rounded-xl text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <SkipForward className="w-4 h-4" />
            </button>
          </div>

          {/* Speed Selector */}
          <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl">
            <SlidersHorizontal className="w-3.5 h-3.5 text-zinc-400 ml-1.5 mr-0.5 hidden sm:inline" />
            {speeds.map((s) => (
              <button
                key={s}
                onClick={() => setSpeed(s)}
                className={`px-2 py-1 text-xs font-mono font-medium rounded-lg transition-colors ${
                  speed === s
                    ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm'
                    : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>

          {/* Predict Mode & Inputs */}
          <div className="flex items-center gap-2">
            {/* Predict Mode Toggle */}
            <button
              onClick={togglePredictMode}
              title="Toggle Predict - Play - Understand Mode"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                predictMode
                  ? 'bg-purple-600 text-white shadow-sm shadow-purple-500/20'
                  : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
              }`}
            >
              <HelpCircle className="w-3.5 h-3.5" />
              <span>Predict Mode</span>
              {predictMode && (
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              )}
            </button>

            {/* Random Input */}
            <button
              onClick={generateRandomInput}
              title="Generate Random Input"
              className="p-2 rounded-xl text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              <Shuffle className="w-4 h-4" />
            </button>

            {/* Custom Input */}
            <button
              onClick={() => setIsInputModalOpen(true)}
              title="Configure Custom Input"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-xs font-medium transition-colors"
            >
              <Edit3 className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Custom Input</span>
            </button>
          </div>
        </div>
      </div>

      <CustomInputModal isOpen={isInputModalOpen} onClose={() => setIsInputModalOpen(false)} />
    </>
  );
};
