import React, { useState } from 'react';
import { useVisualizer } from '../../context/VisualizerContext';
import { Code, Copy, Check } from 'lucide-react';

export const SynchronizedCodeViewer: React.FC = () => {
  const { metadata, currentStep } = useVisualizer();
  const [activeLang, setActiveLang] = useState<'java' | 'python'>('java');
  const [copied, setCopied] = useState(false);

  const rawCode = activeLang === 'java' ? metadata.code.java : metadata.code.python;
  const activeLine =
    activeLang === 'java' ? currentStep.codeLine.java : currentStep.codeLine.python;

  const lines = rawCode.split('\n');

  const copyToClipboard = () => {
    navigator.clipboard.writeText(rawCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-full bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-4 shadow-apple-sm transition-colors flex flex-col gap-3">
      {/* Header with Language Tabs */}
      <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
        <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveLang('java')}
            className={`px-3 py-1 text-xs font-medium rounded-lg transition-colors ${
              activeLang === 'java'
                ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm font-semibold'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
          >
            Java
          </button>
          <button
            onClick={() => setActiveLang('python')}
            className={`px-3 py-1 text-xs font-medium rounded-lg transition-colors ${
              activeLang === 'python'
                ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm font-semibold'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
          >
            Python
          </button>
        </div>

        <button
          onClick={copyToClipboard}
          className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-xs flex items-center gap-1"
          title="Copy Code"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
          <span className="hidden sm:inline">{copied ? 'Copied' : 'Copy'}</span>
        </button>
      </div>

      {/* Code Container with line highlighting */}
      <div className="relative font-mono text-xs overflow-x-auto max-h-[300px] rounded-xl bg-zinc-950 text-zinc-200 p-3 leading-relaxed">
        {lines.map((lineText, idx) => {
          const lineNumber = idx + 1;
          const isHighlighted = lineNumber === activeLine;

          return (
            <div
              key={idx}
              className={`flex items-center gap-3 px-2 py-0.5 rounded transition-colors ${
                isHighlighted
                  ? 'bg-blue-900/60 text-white font-semibold ring-1 ring-blue-500/80 shadow-sm'
                  : 'hover:bg-zinc-900'
              }`}
            >
              {/* Line Number */}
              <span
                className={`w-6 text-right select-none ${
                  isHighlighted ? 'text-blue-400 font-bold' : 'text-zinc-600'
                }`}
              >
                {lineNumber}
              </span>

              {/* Code line content */}
              <span className="flex-1 whitespace-pre">{lineText || ' '}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
