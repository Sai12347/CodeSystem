import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  Sparkles,
  Shuffle,
  Edit3,
  CheckCircle2,
  HelpCircle,
  Layers,
  ArrowRight,
  RefreshCw,
} from 'lucide-react';
import { QuestionItem, VisualElementFrame } from '../../data/questionBank';
import {
  getAvailableTestCasesForQuestion,
  generateAutomaticSystemTestCase,
  parseUserTestCaseString,
  generateDynamicDryRun,
  PredefinedTestCase,
} from '../../engine/core/dynamicTestCaseDryRun';

interface QuestionAnimationModalProps {
  question: QuestionItem | null;
  isOpen: boolean;
  onClose: () => void;
  initialPrompt?: boolean;
}

export const QuestionAnimationModal: React.FC<QuestionAnimationModalProps> = ({
  question,
  isOpen,
  onClose,
  initialPrompt = true,
}) => {
  // Phase state: 'ASK_CASE' (prompting user for custom vs auto test case) or 'PLAYING_ANIMATION'
  const [phase, setPhase] = useState<'ASK_CASE' | 'PLAYING_ANIMATION'>('ASK_CASE');

  // Active test case array & target
  const [activeArray, setActiveArray] = useState<number[]>([]);
  const [activeTarget, setActiveTarget] = useState<number | undefined>(undefined);
  const [activeCaseLabel, setActiveCaseLabel] = useState<string>('Automatic Case');

  // User input field
  const [customInputText, setCustomInputText] = useState<string>('');
  const [inputError, setInputError] = useState<string | null>(null);

  // Animation Playback states
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [testedCaseCount, setTestedCaseCount] = useState<number>(0);
  const timerRef = useRef<number | null>(null);

  // Available predefined edge cases
  const [predefinedCases, setPredefinedCases] = useState<PredefinedTestCase[]>([]);

  // When question changes, reset to ask phase
  useEffect(() => {
    if (question) {
      const cases = getAvailableTestCasesForQuestion(question);
      setPredefinedCases(cases);
      setCustomInputText('');
      setInputError(null);
      setCurrentStepIndex(0);
      setIsPlaying(false);
      setTestedCaseCount(0);
      setPhase('ASK_CASE');
    }
  }, [question]);

  useEffect(() => {
    if (!isOpen) {
      setIsPlaying(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  }, [isOpen]);

  // Handle confirmation of test case
  const handleStartAnimationWithCase = (arr: number[], label: string, target?: number) => {
    setActiveArray(arr);
    setActiveCaseLabel(label);
    setActiveTarget(target);
    setCurrentStepIndex(0);
    setIsPlaying(false);
    setTestedCaseCount((prev) => prev + 1);
    setPhase('PLAYING_ANIMATION');
  };

  // User submits custom text case
  const handleApplyCustomCase = (e: React.FormEvent) => {
    e.preventDefault();
    setInputError(null);

    // If user provided no text, automatically use system test case!
    if (!customInputText.trim()) {
      handleUseAutomaticSystemCase();
      return;
    }

    try {
      const parsed = parseUserTestCaseString(customInputText);
      if (parsed.length > 15) {
        setInputError('Please enter at most 15 numbers for clear visualization.');
        return;
      }
      handleStartAnimationWithCase(parsed, `User Custom Case (${parsed.length} items)`);
    } catch (err: any) {
      setInputError(err.message || 'Invalid number format. Use comma or spaces.');
    }
  };

  // User selects an automatic system test case
  const handleUseAutomaticSystemCase = () => {
    const auto = generateAutomaticSystemTestCase(6);
    handleStartAnimationWithCase(auto.array, 'Automatic System Case', auto.target);
  };

  // Prompt user again for another testcase
  const handleAskForAnotherCase = () => {
    setIsPlaying(false);
    setPhase('ASK_CASE');
    setInputError(null);
  };

  // Compute dynamic steps for current active array
  const steps = React.useMemo(() => {
    if (!question || activeArray.length === 0) return [];
    return generateDynamicDryRun(question, activeArray, activeTarget);
  }, [question, activeArray, activeTarget]);

  const totalSteps = steps.length;
  const currentStep = steps[currentStepIndex] || steps[0];
  const maxVal = Math.max(...activeArray, 1);

  // Playback timer
  useEffect(() => {
    if (isPlaying && totalSteps > 0) {
      const delay = Math.max(300, 1400 / speed);
      timerRef.current = window.setInterval(() => {
        setCurrentStepIndex((prev) => {
          if (prev < totalSteps - 1) {
            return prev + 1;
          } else {
            setIsPlaying(false);
            return prev;
          }
        });
      }, delay);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, speed, totalSteps]);

  if (!isOpen || !question) return null;

  const getStateClasses = (state: VisualElementFrame['state']) => {
    switch (state) {
      case 'comparing':
        return 'bg-amber-500 text-white border-amber-600 shadow-md shadow-amber-500/30 scale-105';
      case 'swapping':
        return 'bg-rose-500 text-white border-rose-600 shadow-md shadow-rose-500/30 scale-110';
      case 'sorted':
        return 'bg-emerald-500 text-white border-emerald-600 shadow-sm';
      case 'found':
        return 'bg-emerald-600 text-white border-emerald-400 ring-4 ring-emerald-400/40 shadow-lg scale-110';
      case 'active':
        return 'bg-blue-600 text-white border-blue-500 shadow-md shadow-blue-500/30 scale-105';
      case 'window':
        return 'bg-indigo-500/20 text-indigo-700 dark:text-indigo-300 border-indigo-400 ring-2 ring-indigo-500/30';
      case 'eliminated':
        return 'bg-zinc-200/50 dark:bg-zinc-800/40 text-zinc-400 opacity-40';
      default:
        return 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 border-zinc-200 dark:border-zinc-700 shadow-sm';
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/65 backdrop-blur-md"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-anim-title"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl max-w-3xl w-full p-6 shadow-2xl flex flex-col gap-4 overflow-hidden relative"
      >
        {/* Top Header */}
        <div className="flex items-center justify-between pb-3 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-purple-600 text-white flex items-center justify-center shadow-sm">
              <Sparkles className="w-4 h-4 fill-current" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-blue-600 dark:text-blue-400">
                  Question #{question.number}
                </span>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300">
                  {question.difficulty}
                </span>
                <span className="text-xs text-zinc-400">• {question.subtopic}</span>
              </div>
              <h2 id="modal-anim-title" className="text-base font-bold text-zinc-900 dark:text-white mt-0.5">
                {question.title}
              </h2>
            </div>
          </div>

          <button
            onClick={onClose}
            aria-label="Close animation modal"
            className="p-1.5 rounded-xl text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* ======================================================== */}
        {/* PHASE 1: ASK USER FOR TEST CASE SELECTION OR CUSTOM CASE */}
        {/* ======================================================== */}
        {phase === 'ASK_CASE' && (
          <div className="space-y-4 py-2">
            <div className="p-4 rounded-2xl bg-purple-500/10 border border-purple-500/20 text-xs">
              <div className="flex items-center gap-2 text-purple-700 dark:text-purple-300 font-bold mb-1">
                <HelpCircle className="w-4 h-4" />
                <span>Test Case Selection</span>
              </div>
              <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed">
                Do you want to see the dry-run animation for a specific custom test case, or explore edge cases?
                If you leave it empty or choose automatic, the system generates a case for you!
              </p>
            </div>

            {/* Custom Input Form */}
            <form onSubmit={handleApplyCustomCase} className="space-y-2">
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                1. Enter Your Custom Test Case Array:
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={customInputText}
                  onChange={(e) => setCustomInputText(e.target.value)}
                  placeholder="e.g. 10, 4, 8, 1, 15, 6 (or leave blank for automatic)"
                  className="flex-1 px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-900 dark:text-white font-mono focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-sm transition-all whitespace-nowrap"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Run Custom Case</span>
                </button>
              </div>
              {inputError && (
                <p className="text-xs text-rose-500 font-medium">{inputError}</p>
              )}
            </form>

            {/* Predefined Edge Cases */}
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-2">
                2. Or Pick a Boundary Edge Case to Test:
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {predefinedCases.map((tc, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleStartAnimationWithCase(tc.array, tc.label, tc.target)}
                    className="p-3 rounded-2xl border border-zinc-200/80 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/60 hover:border-purple-400 dark:hover:border-purple-500 text-left transition-all group"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-zinc-800 dark:text-zinc-200 group-hover:text-purple-600">
                        {tc.label}
                      </span>
                      <ArrowRight className="w-3 h-3 text-zinc-400 group-hover:translate-x-0.5 transition-transform" />
                    </div>
                    <p className="text-[11px] font-mono text-zinc-500 mt-1 truncate">
                      [{tc.array.join(', ')}]
                    </p>
                    <p className="text-[10px] text-zinc-400 mt-0.5">{tc.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Automatic System Case Option */}
            <div className="pt-2 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
              <span className="text-xs text-zinc-500">
                Don't have a test case? The system will create one automatically.
              </span>
              <button
                type="button"
                onClick={handleUseAutomaticSystemCase}
                className="px-4 py-2 rounded-xl bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 font-semibold text-xs flex items-center gap-1.5 transition-colors"
              >
                <Shuffle className="w-3.5 h-3.5" />
                <span>Use Automatic System Case</span>
              </button>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* PHASE 2: INTERACTIVE DRY-RUN ANIMATION PLAYER */}
        {/* ======================================================== */}
        {phase === 'PLAYING_ANIMATION' && (
          <>
            {/* Case Info & "Test Another Case" Action Banner */}
            <div className="flex flex-wrap items-center justify-between gap-2 p-3 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200/60 dark:border-zinc-700/60 text-xs">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded-md font-bold text-[11px] bg-purple-500/10 text-purple-600 dark:text-purple-400">
                  {activeCaseLabel}
                </span>
                <span className="text-zinc-500 font-mono text-[11px]">
                  [{activeArray.join(', ')}]
                </span>
                {testedCaseCount > 1 && (
                  <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold">
                    ({testedCaseCount} cases tested)
                  </span>
                )}
              </div>

              {/* Prompt to test another case multiple times! */}
              <button
                onClick={handleAskForAnotherCase}
                className="px-3 py-1 rounded-xl bg-white dark:bg-zinc-700 border border-zinc-200 dark:border-zinc-600 text-purple-600 dark:text-purple-300 font-semibold text-xs flex items-center gap-1.5 hover:bg-purple-50 dark:hover:bg-zinc-600 transition-colors shadow-sm"
                title="Test another custom or edge testcase on this problem"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Test Another Case</span>
              </button>
            </div>

            {/* Current Step Narration */}
            {currentStep && (
              <div className="p-3.5 rounded-2xl bg-white dark:bg-zinc-950/80 border border-zinc-200/70 dark:border-zinc-800 text-xs shadow-sm">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-purple-600 dark:text-purple-400 font-mono">
                    Step {currentStepIndex + 1} of {totalSteps}
                  </span>
                  <span className="text-zinc-400 text-[11px]">{question.timeComplexity} Optimal</span>
                </div>
                <p className="font-medium text-zinc-800 dark:text-zinc-200">{currentStep.description}</p>
                <p className="text-zinc-500 dark:text-zinc-400 mt-1 text-[11px] leading-relaxed">
                  {currentStep.explanation}
                </p>
              </div>
            )}

            {/* Dynamic Element Bar Canvas with Framer Motion */}
            <div className="w-full min-h-[170px] bg-zinc-100/60 dark:bg-zinc-950/60 rounded-2xl p-4 border border-zinc-200/60 dark:border-zinc-800/60 flex items-end justify-center gap-2.5 overflow-x-auto">
              <AnimatePresence mode="popLayout">
                {currentStep && currentStep.elements.map((el) => {
                  const numVal = typeof el.value === 'number' ? el.value : 10;
                  const height = `${Math.max(25, Math.min(100, (Math.abs(numVal) / maxVal) * 100))}%`;
                  const stateClass = getStateClasses(el.state);

                  return (
                    <motion.div
                      key={el.id}
                      layout
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      transition={{ type: 'spring', stiffness: 350, damping: 25 }}
                      className="flex flex-col items-center gap-1.5 min-w-[42px]"
                    >
                      {el.subLabel ? (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-600 text-white shadow-sm">
                          {el.subLabel}
                        </span>
                      ) : (
                        <div className="h-4" />
                      )}

                      <div
                        style={{ minHeight: '52px', height }}
                        className={`w-full max-w-[48px] rounded-xl border-2 flex items-center justify-center font-mono font-bold text-sm ${stateClass}`}
                      >
                        {el.value}
                      </div>

                      <span className="text-[10px] font-mono text-zinc-400">[{el.label}]</span>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>

            {/* Live Variable Monitoring Table */}
            {currentStep && (
              <div className="p-3 rounded-2xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200/50 dark:border-zinc-800/50">
                <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 block mb-1.5">
                  Dynamic State Variables
                </span>
                <div className="flex flex-wrap gap-2 text-xs font-mono">
                  {Object.entries(currentStep.variables).map(([k, v]) => (
                    <span
                      key={k}
                      className="px-2 py-1 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300"
                    >
                      <span className="text-zinc-400">{k}:</span>{' '}
                      <span className="font-bold text-purple-600 dark:text-purple-400">{String(v)}</span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Playback Controls & Progress Bar */}
            <div className="flex items-center justify-between pt-2">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentStepIndex(0)}
                  className="p-2 rounded-xl text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800"
                  title="Reset"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setCurrentStepIndex((p) => Math.max(0, p - 1))}
                  disabled={currentStepIndex <= 0}
                  className="p-2 rounded-xl text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
                  title="Previous Step"
                >
                  <SkipBack className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setIsPlaying((p) => !p)}
                  className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-sm"
                >
                  {isPlaying ? (
                    <>
                      <Pause className="w-3.5 h-3.5 fill-current" />
                      <span>Pause</span>
                    </>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>Play Animation</span>
                    </>
                  )}
                </button>
                <button
                  onClick={() => setCurrentStepIndex((p) => Math.min(totalSteps - 1, p + 1))}
                  disabled={currentStepIndex >= totalSteps - 1}
                  className="p-2 rounded-xl text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
                  title="Next Step"
                >
                  <SkipForward className="w-4 h-4" />
                </button>
              </div>

              {/* Speed & Repeat Case Trigger */}
              <div className="flex items-center gap-2">
                <button
                  onClick={handleAskForAnotherCase}
                  className="px-3 py-1.5 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 font-semibold text-xs hover:bg-purple-500/20 transition-colors"
                >
                  + Another Case
                </button>

                <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl text-xs font-mono">
                  {[0.5, 1, 2].map((s) => (
                    <button
                      key={s}
                      onClick={() => setSpeed(s)}
                      className={`px-2 py-0.5 rounded-lg ${
                        speed === s
                          ? 'bg-white dark:bg-zinc-700 text-purple-600 font-bold'
                          : 'text-zinc-400'
                      }`}
                    >
                      {s}x
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}
      </motion.div>
    </div>
  );
};
