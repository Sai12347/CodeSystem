import React from 'react';
import { useVisualizer } from '../../context/VisualizerContext';
import { VisualizerCanvas } from './VisualizerCanvas';
import { ControlsBar } from './ControlsBar';
import { VariableTable } from './VariableTable';
import { SynchronizedCodeViewer } from './SynchronizedCodeViewer';
import { ComplexityCard } from './ComplexityCard';
import { PredictPlayUnderstandModal } from './PredictPlayUnderstandModal';
import { ALGORITHM_REGISTRY } from '../../engine/core/AlgorithmEngine';
import { AlgorithmId } from '../../types/algorithm';
import { Sparkles, ChevronDown } from 'lucide-react';

export const AlgorithmVisualizer: React.FC = () => {
  const { algorithmId, selectAlgorithm } = useVisualizer();

  const algoList = Object.keys(ALGORITHM_REGISTRY) as AlgorithmId[];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Selector & Intro Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-gradient-to-r from-blue-500/10 via-indigo-500/10 to-transparent p-6 rounded-3xl border border-blue-500/20 backdrop-blur-sm">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1 rounded-lg bg-blue-600 text-white shadow-sm">
              <Sparkles className="w-4 h-4" />
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
              Interactive Execution Engine
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white mt-1">
            Algorithm Visualizer & Dry-Runner
          </h1>
          <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-1 max-w-2xl">
            Step through deterministic algorithm executions, inspect variable states, predict next moves, and master code behavior line-by-line.
          </p>
        </div>

        {/* Algorithm Select Dropdown */}
        <div className="relative min-w-[220px]">
          <label className="block text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 mb-1">
            Select Algorithm
          </label>
          <div className="relative">
            <select
              value={algorithmId}
              onChange={(e) => selectAlgorithm(e.target.value as AlgorithmId)}
              className="w-full appearance-none px-4 py-2.5 rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm font-semibold text-zinc-900 dark:text-white shadow-apple-sm focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10 cursor-pointer"
            >
              {algoList.map((id) => (
                <option key={id} value={id}>
                  {ALGORITHM_REGISTRY[id].metadata.title}
                </option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 text-zinc-400 absolute right-3 top-3 pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Main Visualizer Canvas */}
      <VisualizerCanvas />

      {/* Playback Controls Bar */}
      <ControlsBar />

      {/* Lower Dual Grid: Left = Variable Table & Complexity; Right = Synchronized Code Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6 flex flex-col gap-6">
          <VariableTable />
          <ComplexityCard />
        </div>
        <div className="lg:col-span-6">
          <SynchronizedCodeViewer />
        </div>
      </div>

      {/* Predict-Play-Understand Modal (triggered on steps with prediction when predict mode is on) */}
      <PredictPlayUnderstandModal />
    </div>
  );
};
