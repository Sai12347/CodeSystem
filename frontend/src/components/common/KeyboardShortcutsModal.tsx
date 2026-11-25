import React from 'react';
import { X, Command } from 'lucide-react';

interface KeyboardShortcutsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const KeyboardShortcutsModal: React.FC<KeyboardShortcutsModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const shortcuts = [
    { key: 'Space or K', desc: 'Play / Pause algorithm execution' },
    { key: '→ or L', desc: 'Advance one step forward' },
    { key: '← or J', desc: 'Step back to previous step' },
    { key: 'R', desc: 'Reset algorithm to initial step' },
    { key: 'P', desc: 'Toggle Predict-Play-Understand mode' },
    { key: 'Esc', desc: 'Close dialogs and modals' },
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="shortcuts-title"
    >
      <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex items-center justify-between pb-4 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-2">
            <Command className="w-5 h-5 text-blue-500" />
            <h2 id="shortcuts-title" className="text-lg font-semibold text-zinc-900 dark:text-white">
              Keyboard Shortcuts
            </h2>
          </div>
          <button
            onClick={onClose}
            aria-label="Close shortcuts dialog"
            className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-500"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-4 space-y-3">
          {shortcuts.map((sc, i) => (
            <div key={i} className="flex items-center justify-between py-1.5 text-sm">
              <span className="text-zinc-600 dark:text-zinc-400">{sc.desc}</span>
              <kbd className="px-2.5 py-1 text-xs font-mono font-semibold bg-zinc-100 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-md text-zinc-800 dark:text-zinc-200 shadow-sm">
                {sc.key}
              </kbd>
            </div>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800 text-center">
          <button
            onClick={onClose}
            className="w-full py-2 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors shadow-sm"
          >
            Got it
          </button>
        </div>
      </div>
    </div>
  );
};
