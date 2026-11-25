import React, { useState } from 'react';
import { HelpCircle, CheckCircle2, XCircle, ArrowRight, Lightbulb, Play } from 'lucide-react';
import { useVisualizer } from '../../context/VisualizerContext';
import { useUser } from '../../context/UserContext';
import { motion, AnimatePresence } from 'framer-motion';

export const PredictPlayUnderstandModal: React.FC = () => {
  const {
    isPredictModalOpen,
    closePredictModal,
    currentStep,
    nextStep,
    answerPrediction,
    predictionAnswered,
    predictionFeedback,
  } = useVisualizer();

  const { awardXp } = useUser();
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [showHint, setShowHint] = useState<boolean>(false);

  if (!isPredictModalOpen || !currentStep.prediction) return null;

  const challenge = currentStep.prediction;

  const handleSelectOption = (idx: number) => {
    if (predictionAnswered) return;
    setSelectedOption(idx);
    answerPrediction(idx);

    if (idx === challenge.correctOptionIndex) {
      awardXp(30, 'Correct algorithm state prediction!');
    }
  };

  const handlePlayNext = () => {
    closePredictModal();
    nextStep();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md"
      role="dialog"
      aria-modal="true"
      aria-labelledby="predict-title"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl max-w-lg w-full p-6 shadow-2xl overflow-hidden"
      >
        {/* Header with 3 Phase Pills */}
        <div className="flex items-center justify-between pb-4 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-1.5">
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-700 dark:bg-purple-950/80 dark:text-purple-300">
              1. PREDICT
            </span>
            <span className="text-zinc-400">→</span>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700 dark:bg-blue-950/80 dark:text-blue-300">
              2. PLAY
            </span>
            <span className="text-zinc-400">→</span>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-950/80 dark:text-emerald-300">
              3. UNDERSTAND
            </span>
          </div>

          <button
            onClick={closePredictModal}
            className="text-xs text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
          >
            Skip
          </button>
        </div>

        {/* Question Title */}
        <div className="mt-4">
          <div className="flex items-start gap-2.5">
            <HelpCircle className="w-5 h-5 text-purple-600 dark:text-purple-400 flex-shrink-0 mt-0.5" />
            <h3 id="predict-title" className="text-base font-semibold text-zinc-900 dark:text-white leading-snug">
              {challenge.question}
            </h3>
          </div>
        </div>

        {/* Options List */}
        <div className="mt-4 space-y-2">
          {challenge.options.map((opt, i) => {
            const isSelected = selectedOption === i;
            const isCorrect = i === challenge.correctOptionIndex;
            let btnStyle =
              'border-zinc-200 dark:border-zinc-800 hover:border-purple-400 dark:hover:border-purple-600 bg-zinc-50 dark:bg-zinc-800/50 text-zinc-800 dark:text-zinc-200';

            if (predictionAnswered) {
              if (isCorrect) {
                btnStyle = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 ring-2 ring-emerald-500/30';
              } else if (isSelected && !isCorrect) {
                btnStyle = 'border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 ring-2 ring-rose-500/30';
              } else {
                btnStyle = 'opacity-40 border-zinc-200 dark:border-zinc-800';
              }
            }

            return (
              <button
                key={i}
                disabled={predictionAnswered}
                onClick={() => handleSelectOption(i)}
                className={`w-full text-left p-3 rounded-2xl border text-sm font-medium transition-all flex items-center justify-between ${btnStyle}`}
              >
                <span>{opt}</span>
                {predictionAnswered && isCorrect && <CheckCircle2 className="w-4 h-4 text-emerald-500 ml-2" />}
                {predictionAnswered && isSelected && !isCorrect && (
                  <XCircle className="w-4 h-4 text-rose-500 ml-2" />
                )}
              </button>
            );
          })}
        </div>

        {/* Hint Accordion */}
        {!predictionAnswered && (
          <div className="mt-3">
            <button
              onClick={() => setShowHint((prev) => !prev)}
              className="text-xs text-amber-600 dark:text-amber-400 flex items-center gap-1 font-medium hover:underline"
            >
              <Lightbulb className="w-3.5 h-3.5" />
              <span>{showHint ? 'Hide Hint' : 'Need a hint?'}</span>
            </button>
            {showHint && (
              <p className="mt-1 text-xs text-zinc-600 dark:text-zinc-400 bg-amber-500/10 p-2.5 rounded-xl border border-amber-500/20">
                {challenge.hint}
              </p>
            )}
          </div>
        )}

        {/* Phase 3: UNDERSTAND Feedback after user answers */}
        <AnimatePresence>
          {predictionAnswered && predictionFeedback && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 p-4 rounded-2xl bg-zinc-100 dark:bg-zinc-800/80 border border-zinc-200 dark:border-zinc-700/80 space-y-2"
            >
              <div className="flex items-center gap-1.5 font-bold text-xs uppercase tracking-wide">
                {predictionFeedback.correct ? (
                  <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-4 h-4" /> Correct Prediction! (+30 XP)
                  </span>
                ) : (
                  <span className="text-rose-600 dark:text-rose-400 flex items-center gap-1">
                    <XCircle className="w-4 h-4" /> Nice Try! Here is why:
                  </span>
                )}
              </div>
              <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
                {predictionFeedback.explanation}
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer Actions */}
        <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-end gap-3">
          {predictionAnswered ? (
            <button
              onClick={handlePlayNext}
              className="w-full py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm flex items-center justify-center gap-2 transition-all shadow-md shadow-blue-500/20"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Play & Advance Step</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={() => {
                // Auto choose first to proceed if user prefers
                handleSelectOption(challenge.correctOptionIndex);
              }}
              className="text-xs text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 underline"
            >
              Reveal answer
            </button>
          )}
        </div>
      </motion.div>
    </div>
  );
};
