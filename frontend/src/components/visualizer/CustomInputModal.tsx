import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import { useVisualizer } from '../../context/VisualizerContext';

interface CustomInputModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CustomInputModal: React.FC<CustomInputModalProps> = ({ isOpen, onClose }) => {
  const { algorithmId, applyCustomInput } = useVisualizer();

  const [arrayStr, setArrayStr] = useState('2, 5, 8, 12, 16, 23, 38');
  const [targetVal, setTargetVal] = useState('16');
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleApply = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const numbers = arrayStr
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s.length > 0)
        .map((s) => {
          const num = Number(s);
          if (isNaN(num)) throw new Error(`"${s}" is not a valid number`);
          return num;
        });

      if (numbers.length < 2) {
        setError('Please enter at least 2 numbers.');
        return;
      }
      if (numbers.length > 15) {
        setError('Maximum 15 numbers recommended for optimal visualization.');
        return;
      }

      if (algorithmId === 'binary-search') {
        const sorted = [...numbers].sort((a, b) => a - b);
        const target = Number(targetVal);
        if (isNaN(target)) throw new Error('Target must be a valid number.');
        applyCustomInput({ array: sorted, target });
      } else if (algorithmId === 'linear-search') {
        const target = Number(targetVal);
        if (isNaN(target)) throw new Error('Target must be a valid number.');
        applyCustomInput({ array: numbers, target });
      } else if (algorithmId === 'two-pointers') {
        const sorted = [...numbers].sort((a, b) => a - b);
        const target = Number(targetVal);
        applyCustomInput({ array: sorted, target });
      } else if (algorithmId === 'sliding-window') {
        const k = Math.min(numbers.length - 1, Math.max(2, Number(targetVal) || 3));
        applyCustomInput({ array: numbers, k });
      } else {
        applyCustomInput(numbers);
      }

      onClose();
    } catch (err: any) {
      setError(err.message || 'Invalid input format.');
    }
  };

  const isSearchAlgo =
    algorithmId === 'binary-search' ||
    algorithmId === 'linear-search' ||
    algorithmId === 'two-pointers';

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="input-modal-title"
    >
      <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex items-center justify-between pb-4 border-b border-zinc-100 dark:border-zinc-800">
          <h2 id="input-modal-title" className="text-base font-semibold text-zinc-900 dark:text-white">
            Customize Input Data
          </h2>
          <button
            onClick={onClose}
            aria-label="Close custom input"
            className="p-1 rounded-lg text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleApply} className="mt-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Comma-Separated Array
            </label>
            <input
              type="text"
              value={arrayStr}
              onChange={(e) => setArrayStr(e.target.value)}
              placeholder="e.g. 10, 25, 4, 18, 30"
              className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-[11px] text-zinc-400 mt-1">
              {algorithmId === 'binary-search' ? 'Will be sorted automatically.' : 'Enter 2 to 15 numbers.'}
            </p>
          </div>

          {isSearchAlgo && (
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Value
              </label>
              <input
                type="number"
                value={targetVal}
                onChange={(e) => setTargetVal(e.target.value)}
                placeholder="16"
                className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          {algorithmId === 'sliding-window' && (
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Window Size (K)
              </label>
              <input
                type="number"
                value={targetVal}
                onChange={(e) => setTargetVal(e.target.value)}
                placeholder="3"
                className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          {error && (
            <p className="text-xs text-rose-500 bg-rose-500/10 p-2 rounded-lg font-medium">
              {error}
            </p>
          )}

          <div className="pt-2 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-xl"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl flex items-center gap-1.5 shadow-sm"
            >
              <Check className="w-3.5 h-3.5" />
              <span>Apply Input</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
