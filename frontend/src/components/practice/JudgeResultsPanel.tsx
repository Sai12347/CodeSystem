import React from 'react';
import {
  CheckCircle2,
  XCircle,
  Clock,
  AlertTriangle,
  Lock,
  Terminal,
  ShieldCheck,
} from 'lucide-react';
import { JudgeResponse } from '../../services/judgeService';

interface JudgeResultsPanelProps {
  result: JudgeResponse | null;
  errorMessage: string | null;
  xpAwarded?: number | null;
}

export const JudgeResultsPanel: React.FC<JudgeResultsPanelProps> = ({
  result,
  errorMessage,
  xpAwarded,
}) => {
  if (errorMessage) {
    return (
      <div className="bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/70 rounded-3xl p-5 shadow-apple-sm space-y-2">
        <div className="flex items-center gap-2 text-rose-700 dark:text-rose-300 font-bold text-sm">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>Judge Execution Unavailable</span>
        </div>
        <p className="text-xs text-rose-600 dark:text-rose-300/90 leading-relaxed">
          {errorMessage}
        </p>
      </div>
    );
  }

  if (!result) return null;

  const isAccepted = result.status === 'ACCEPTED';
  const statusStyles: Record<string, string> = {
    ACCEPTED: 'text-emerald-600 dark:text-emerald-400',
    WRONG_ANSWER: 'text-rose-600 dark:text-rose-400',
    TIME_LIMIT_EXCEEDED: 'text-amber-600 dark:text-amber-400',
    RUNTIME_ERROR: 'text-orange-600 dark:text-orange-400',
    COMPILATION_ERROR: 'text-rose-600 dark:text-rose-400',
  };

  const visibleResults = result.results.filter((r) => !r.hidden);
  const hiddenResults = result.results.filter((r) => r.hidden);

  return (
    <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-5 shadow-apple-sm space-y-4">
      {/* Header Summary */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          {isAccepted ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0" />
          ) : (
            <XCircle className="w-5 h-5 text-rose-500 flex-shrink-0" />
          )}
          <div>
            <div className={`text-sm font-extrabold tracking-tight ${statusStyles[result.status] || 'text-zinc-900 dark:text-white'}`}>
              {result.status.replace(/_/g, ' ')}
              <span className="ml-2 text-xs font-semibold text-zinc-500 dark:text-zinc-400">
                ({result.passedCount}/{result.totalCount} {result.mode === 'run' ? 'Sample' : 'Total'} Tests Passed)
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2 mt-1 text-[11px] font-mono">
              <span className="px-2 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300">
                Visible: {result.visiblePassed}/{result.visibleTotal}
              </span>
              {result.hiddenTotal > 0 && (
                <span className="px-2 py-0.5 rounded-md bg-purple-500/10 text-purple-700 dark:text-purple-300 flex items-center gap-1">
                  <Lock className="w-3 h-3" />
                  Hidden: {result.hiddenPassed}/{result.hiddenTotal}
                </span>
              )}
              <span className="text-zinc-400 flex items-center gap-1">
                <Clock className="w-3 h-3" /> {result.executionTimeMs.toFixed(1)} ms
              </span>
            </div>
          </div>
        </div>

        {isAccepted && result.mode === 'submit' && xpAwarded ? (
          <div className="px-3 py-1 rounded-xl bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 text-xs font-bold flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4" />
            <span>+{xpAwarded} XP Awarded</span>
          </div>
        ) : null}
      </div>

      {/* Compilation Error Block */}
      {result.compileError && (
        <div className="p-3.5 rounded-2xl bg-rose-950/90 text-rose-100 border border-rose-800 text-xs font-mono whitespace-pre-wrap overflow-x-auto max-h-56">
          <div className="flex items-center gap-1.5 text-rose-300 font-bold mb-1.5">
            <Terminal className="w-3.5 h-3.5" />
            <span>Compiler / Syntax Diagnostics</span>
          </div>
          {result.compileError}
        </div>
      )}

      {/* Top-level error when no per-test rows */}
      {!result.compileError && result.error && result.results.length === 0 && (
        <div className="p-3 rounded-2xl bg-rose-500/10 text-rose-700 dark:text-rose-300 text-xs font-mono">
          {result.error}
        </div>
      )}

      {/* Visible Test Cases Breakdown */}
      {visibleResults.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-[11px] font-bold uppercase tracking-wider text-zinc-400">
            Visible Sample Tests
          </h4>
          <div className="space-y-2">
            {visibleResults.map((tc, idx) => (
              <div
                key={tc.id}
                className={`p-3 rounded-2xl border text-xs font-mono space-y-1.5 ${
                  tc.passed
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200/70 dark:border-emerald-900/50'
                    : 'bg-rose-50/60 dark:bg-rose-950/20 border-rose-200/80 dark:border-rose-900/50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold flex items-center gap-1.5 text-zinc-800 dark:text-zinc-200">
                    {tc.passed ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    ) : (
                      <XCircle className="w-3.5 h-3.5 text-rose-500" />
                    )}
                    Sample #{idx + 1} ({tc.status.replace(/_/g, ' ')})
                  </span>
                  <span className="text-[10px] text-zinc-400">{tc.timeMs.toFixed(1)} ms</span>
                </div>

                {tc.input && (
                  <div className="text-[11px] break-all">
                    <span className="text-zinc-400">Input: </span>
                    <span className="text-zinc-800 dark:text-zinc-200">{tc.input}</span>
                  </div>
                )}
                {tc.expected !== null && (
                  <div className="text-[11px] break-all">
                    <span className="text-zinc-400">Expected: </span>
                    <span className="text-emerald-700 dark:text-emerald-400 font-semibold">{tc.expected}</span>
                  </div>
                )}
                <div className="text-[11px] break-all">
                  <span className="text-zinc-400">Your output: </span>
                  <span className={`font-semibold ${tc.passed ? 'text-emerald-700 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                    {tc.actual ?? (tc.status === 'TIME_LIMIT_EXCEEDED' ? 'No output (time limit exceeded)' : 'No output returned')}
                  </span>
                </div>
                {tc.stdout && (
                  <div className="text-[11px] text-zinc-500 dark:text-zinc-400 whitespace-pre-wrap">
                    <span className="text-zinc-400">Stdout: </span>
                    {tc.stdout}
                  </div>
                )}
                {tc.error && (
                  <div className="text-[11px] text-rose-600 dark:text-rose-400 whitespace-pre-wrap">
                    {tc.error}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Hidden Test Cases Summary Grid (Inputs/Outputs Never Exposed) */}
      {hiddenResults.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h4 className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 flex items-center gap-1.5">
              <Lock className="w-3 h-3" />
              <span>Hidden Test Suite ({result.hiddenPassed}/{result.hiddenTotal} Passed)</span>
            </h4>
            <span className="text-[10px] text-zinc-400">Inputs & outputs locked</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
            {hiddenResults.map((tc, idx) => (
              <div
                key={tc.id}
                className={`px-2.5 py-2 rounded-xl border text-[11px] font-mono flex items-center justify-between ${
                  tc.passed
                    ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-700 dark:text-emerald-300'
                    : 'bg-rose-500/10 border-rose-500/20 text-rose-700 dark:text-rose-300'
                }`}
                title={tc.error || tc.status}
              >
                <span className="flex items-center gap-1 font-semibold">
                  {tc.passed ? (
                    <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                  ) : (
                    <XCircle className="w-3 h-3 text-rose-500" />
                  )}
                  H#{idx + 1}
                </span>
                <span className="text-[10px] opacity-80">
                  {tc.passed
                    ? `${tc.timeMs.toFixed(0)}ms`
                    : tc.status === 'TIME_LIMIT_EXCEEDED'
                    ? 'TLE'
                    : tc.status === 'RUNTIME_ERROR'
                    ? 'RE'
                    : 'WA'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
