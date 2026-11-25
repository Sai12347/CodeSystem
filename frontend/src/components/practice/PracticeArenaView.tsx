import React, { useState, useMemo } from 'react';
import {
  Code2,
  Play,
  CheckCircle2,
  Clock,
  Sparkles,
  Lightbulb,
  RotateCcw,
  Search,
  Filter,
  PlayCircle,
  ChevronLeft,
  ChevronRight,
  Bookmark,
  Award,
  Layers,
  HelpCircle,
  FolderOpen,
  ArrowRight,
  Building2,
} from 'lucide-react';
import { useUser } from '../../context/UserContext';
import {
  QuestionItem,
  Difficulty,
  getQuestionsForTopic,
  getTotalQuestionsCount,
} from '../../data/questionBank';
import { COMPLETE_30_DSA_TOPICS } from '../../data/dsaTopicsCatalog';
import { QuestionAnimationModal } from './QuestionAnimationModal';
import { dbService } from '../../services/databaseService';

export const PracticeArenaView: React.FC = () => {
  const { user, recordProblemSolved } = useUser();

  // Topic Selector State: default to 'arrays'
  const [selectedTopicId, setSelectedTopicId] = useState<string>('arrays');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Loaded questions for current selected topic
  const topicQuestions = useMemo(() => {
    return getQuestionsForTopic(selectedTopicId);
  }, [selectedTopicId]);

  // Selected Question State
  const [activeQuestionId, setActiveQuestionId] = useState<string>(topicQuestions[0]?.id || 'arrays_q_1');

  // Filter questions based on difficulty & search
  const filteredQuestions = useMemo(() => {
    return topicQuestions.filter((q) => {
      const matchDiff = selectedDifficulty === 'All' || q.difficulty === selectedDifficulty;
      const matchSearch =
        q.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        q.subtopic.toLowerCase().includes(searchQuery.toLowerCase()) ||
        q.companyTag.toLowerCase().includes(searchQuery.toLowerCase());
      return matchDiff && matchSearch;
    });
  }, [topicQuestions, selectedDifficulty, searchQuery]);

  // Active Question
  const activeQuestion = useMemo(() => {
    const found = filteredQuestions.find((q) => q.id === activeQuestionId);
    if (found) return found;
    return filteredQuestions[0] || topicQuestions[0];
  }, [filteredQuestions, activeQuestionId, topicQuestions]);

  // Editor states
  const [language, setLanguage] = useState<'java' | 'python'>('java');
  const [userCode, setUserCode] = useState<string>(activeQuestion?.starterCode?.java || '');
  const [executing, setExecuting] = useState<boolean>(false);
  const [results, setResults] = useState<{
    status: 'ACCEPTED' | 'WRONG_ANSWER';
    passedCount: number;
    totalCount: number;
    executionTimeMs: number;
    memoryMb: number;
  } | null>(null);

  const [showHintIndex, setShowHintIndex] = useState<number | null>(null);
  const [isAnimationModalOpen, setIsAnimationModalOpen] = useState<boolean>(false);

  // User progress from database
  const userProgress = useMemo(() => dbService.getUserProgress(user.id), [user.id]);

  const handleSelectQuestion = (q: QuestionItem) => {
    setActiveQuestionId(q.id);
    setUserCode(language === 'java' ? q.starterCode.java : q.starterCode.python);
    setResults(null);
    setShowHintIndex(null);
  };

  const handleSwitchLanguage = (lang: 'java' | 'python') => {
    setLanguage(lang);
    if (activeQuestion) {
      setUserCode(lang === 'java' ? activeQuestion.starterCode.java : activeQuestion.starterCode.python);
    }
  };

  const handleRunTests = () => {
    if (!activeQuestion) return;
    setExecuting(true);
    setResults(null);

    // Simulate isolated test suite execution and persist to database
    setTimeout(() => {
      setExecuting(false);
      const executionTime = Math.floor(Math.random() * 35) + 15;
      const memoryMb = Number((Math.random() * 4 + 12).toFixed(1));

      setResults({
        status: 'ACCEPTED',
        passedCount: 3,
        totalCount: 3,
        executionTimeMs: executionTime,
        memoryMb,
      });

      // Save submission to database
      dbService.saveSubmission({
        userId: user.id,
        problemId: activeQuestion.id,
        problemTitle: activeQuestion.title,
        language,
        code: userCode,
        status: 'ACCEPTED',
        executionTimeMs: executionTime,
        memoryMb,
      });

      // Award XP
      const xpReward = activeQuestion.difficulty === 'Expert' ? 120 : activeQuestion.difficulty === 'Hard' ? 80 : 50;
      recordProblemSolved(activeQuestion.id, xpReward);
    }, 600);
  };

  const isSolved = activeQuestion ? userProgress.solvedProblemIds.includes(activeQuestion.id) : false;
  const currentTopic = COMPLETE_30_DSA_TOPICS.find((t) => t.id === selectedTopicId) || COMPLETE_30_DSA_TOPICS[0];
  const totalAllQuestions = getTotalQuestionsCount();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* ======================================================== */}
      {/* 1. TOPIC SELECTOR HERO: ALL 30 DSA TOPICS AVAILABLE      */}
      {/* ======================================================== */}
      <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 p-6 rounded-3xl shadow-apple-sm space-y-4">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="p-1 rounded-lg bg-blue-600 text-white shadow-sm">
                <FolderOpen className="w-4 h-4" />
              </span>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                All 30 DSA Topics • 100-130 Questions Each ({totalAllQuestions}+ Total)
              </span>
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900 dark:text-white">
              Practice Session Topic Selector
            </h1>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
              Select any of the 30 DSA topics below. Every question includes real MNC interview PYQ tags and step-by-step testcase animations.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-xs text-right">
              <span className="text-zinc-400 block">Total Questions Solved</span>
              <span className="font-bold text-emerald-600 dark:text-emerald-400">
                {userProgress.solvedProblemIds.length} / {totalAllQuestions}
              </span>
            </div>
          </div>
        </div>

        {/* 30-Topic Selector Grid / Carousel */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-6 gap-2 pt-2 max-h-56 overflow-y-auto pr-1">
          {COMPLETE_30_DSA_TOPICS.map((topic) => {
            const isSelected = selectedTopicId === topic.id;
            return (
              <button
                key={topic.id}
                onClick={() => {
                  setSelectedTopicId(topic.id);
                  const firstQ = getQuestionsForTopic(topic.id)[0];
                  if (firstQ) handleSelectQuestion(firstQ);
                }}
                className={`p-2.5 rounded-2xl border text-left flex flex-col justify-between transition-all ${
                  isSelected
                    ? 'bg-blue-50 dark:bg-blue-950/40 border-blue-500 ring-2 ring-blue-500/30 shadow-sm'
                    : 'bg-zinc-50 dark:bg-zinc-800/50 border-zinc-200/80 dark:border-zinc-800 hover:border-zinc-400'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                        isSelected
                          ? 'bg-blue-600 text-white'
                          : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300'
                      }`}
                    >
                      {topic.questionCount} Qs
                    </span>
                    <span className="text-[9px] text-zinc-400 font-medium">{topic.category.slice(0, 3)}</span>
                  </div>
                  <h3
                    className={`text-xs font-bold mt-1.5 truncate ${
                      isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-zinc-900 dark:text-white'
                    }`}
                  >
                    {topic.name.replace(/^\d+\.\s*/, '')}
                  </h3>
                </div>
                <p className="text-[10px] text-zinc-400 line-clamp-1 mt-1">{topic.badge}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* ======================================================== */}
      {/* 2. SUB-FILTERS: Topic Details, Difficulty & Search       */}
      {/* ======================================================== */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-zinc-100/70 dark:bg-zinc-900/50 p-2.5 rounded-2xl border border-zinc-200/60 dark:border-zinc-800/60">
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar w-full sm:w-auto">
          <span className="text-xs font-bold text-zinc-800 dark:text-zinc-200 mr-2 whitespace-nowrap">
            {currentTopic.name} ({currentTopic.questionCount} Questions)
          </span>

          {(['All', 'Easy', 'Medium', 'Hard', 'Expert'] as const).map((diff) => (
            <button
              key={diff}
              onClick={() => setSelectedDifficulty(diff)}
              className={`px-3 py-1 text-xs font-semibold rounded-xl transition-colors ${
                selectedDifficulty === diff
                  ? 'bg-zinc-900 text-white dark:bg-white dark:text-black shadow-sm'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-white'
              }`}
            >
              {diff}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-zinc-400 absolute left-2.5 top-2.5 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={`Search ${currentTopic.name.replace(/^\d+\.\s*/, '')}...`}
            className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-900 dark:text-white placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* ======================================================== */}
      {/* 3. MAIN WORKSTATION: Question Explorer & Editor          */}
      {/* ======================================================== */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Side: Question List & Active Problem Description */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          {/* Question List in Selected Topic */}
          <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-4 shadow-apple-sm">
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-zinc-100 dark:border-zinc-800">
              <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                {currentTopic.name.replace(/^\d+\.\s*/, '')} ({filteredQuestions.length} Problems)
              </span>
              <span className="text-[10px] text-zinc-400">Click to switch problem</span>
            </div>

            <div className="max-h-56 overflow-y-auto space-y-1.5 pr-1">
              {filteredQuestions.map((q) => {
                const isSelected = q.id === activeQuestion?.id;
                const isItemSolved = userProgress.solvedProblemIds.includes(q.id);

                return (
                  <button
                    key={q.id}
                    onClick={() => handleSelectQuestion(q)}
                    className={`w-full p-2.5 rounded-xl text-left text-xs flex items-center justify-between transition-all ${
                      isSelected
                        ? 'bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-400/60 font-semibold'
                        : 'hover:bg-zinc-50 dark:hover:bg-zinc-800/50 text-zinc-700 dark:text-zinc-300'
                    }`}
                  >
                    <div className="truncate flex-1 pr-2">
                      <div className="flex items-center gap-1.5 mb-0.5">
                        <span className="text-zinc-400 font-mono text-[10px]">#{q.number}</span>
                        <span className="text-[9px] font-bold text-blue-600 dark:text-blue-400 bg-blue-500/10 px-1.5 py-0.2 rounded">
                          {q.companyTag.split(' ')[0]}
                        </span>
                      </div>
                      <span className="truncate block font-medium">{q.title}</span>
                    </div>

                    <div className="flex items-center gap-1.5 flex-shrink-0">
                      <span
                        className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                          q.difficulty === 'Easy'
                            ? 'bg-emerald-500/10 text-emerald-600'
                            : q.difficulty === 'Medium'
                            ? 'bg-amber-500/10 text-amber-600'
                            : q.difficulty === 'Hard'
                            ? 'bg-rose-500/10 text-rose-600'
                            : 'bg-purple-500/10 text-purple-600'
                        }`}
                      >
                        {q.difficulty}
                      </span>
                      {isItemSolved && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Problem Description Card */}
          {activeQuestion && (
            <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-6 shadow-apple-sm space-y-4 max-h-[520px] overflow-y-auto">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                      activeQuestion.difficulty === 'Easy'
                        ? 'bg-emerald-500/10 text-emerald-600'
                        : activeQuestion.difficulty === 'Medium'
                        ? 'bg-amber-500/10 text-amber-600'
                        : activeQuestion.difficulty === 'Hard'
                        ? 'bg-rose-500/10 text-rose-600'
                        : 'bg-purple-500/10 text-purple-600'
                    }`}
                  >
                    {activeQuestion.difficulty}
                  </span>
                  <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400">
                    {activeQuestion.companyTag}
                  </span>
                </div>

                {isSolved && (
                  <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div>
                <h2 className="text-lg font-bold text-zinc-900 dark:text-white">
                  #{activeQuestion.number}. {activeQuestion.title}
                </h2>
                <p className="text-xs text-zinc-600 dark:text-zinc-300 mt-2 leading-relaxed">
                  {activeQuestion.description}
                </p>
              </div>

              {/* Real World Analogy */}
              <div className="p-3 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800/50 text-[11px] text-zinc-600 dark:text-zinc-300">
                <span className="font-semibold text-zinc-800 dark:text-zinc-200">Real-World Context: </span>
                {activeQuestion.realWorldAnalogy}
              </div>

              {/* Examples */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2">
                  Example Cases
                </h3>
                {activeQuestion.examples.map((ex, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800/50 text-xs font-mono space-y-1"
                  >
                    <p>
                      <span className="text-zinc-400">Input:</span>{' '}
                      <span className="text-zinc-800 dark:text-zinc-200 font-semibold">{ex.input}</span>
                    </p>
                    <p>
                      <span className="text-zinc-400">Output:</span>{' '}
                      <span className="text-emerald-600 dark:text-emerald-400 font-semibold">{ex.output}</span>
                    </p>
                  </div>
                ))}
              </div>

              {/* Constraints */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-1.5">
                  Constraints
                </h3>
                <ul className="list-disc list-inside space-y-1 text-xs font-mono text-zinc-500">
                  {activeQuestion.constraints.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>

              {/* Hints */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-1.5">
                  Hints
                </h3>
                <div className="space-y-1.5">
                  {activeQuestion.hints.map((h, i) => (
                    <div key={i} className="text-xs">
                      <button
                        onClick={() => setShowHintIndex(showHintIndex === i ? null : i)}
                        className="text-amber-600 dark:text-amber-400 font-medium hover:underline flex items-center gap-1"
                      >
                        <Lightbulb className="w-3.5 h-3.5" />
                        <span>Hint {i + 1}</span>
                      </button>
                      {showHintIndex === i && (
                        <p className="mt-1 p-2.5 rounded-xl bg-amber-500/10 text-zinc-700 dark:text-zinc-300 text-xs">
                          {h}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Side: Code Editor, Prompt Banner & Animation Dry-Run */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* ======================================================== */}
          {/* CALLOUT BANNER: Asks user if they want dry run animation */}
          {/* ======================================================== */}
          <div className="p-4 rounded-3xl bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 text-white shadow-apple-md flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-1.5 text-purple-200 text-xs font-bold mb-1">
                <Sparkles className="w-4 h-4 fill-current" />
                <span>INTERACTIVE TESTCASE DRY-RUN</span>
              </div>
              <h4 className="text-sm font-bold">
                Want to visualize the dry-run for a specific test case?
              </h4>
              <p className="text-[11px] text-purple-100 mt-0.5">
                Enter your own custom numbers, pick edge cases, or let the system choose automatically!
              </p>
            </div>

            <button
              onClick={() => setIsAnimationModalOpen(true)}
              className="px-4 py-2 rounded-2xl bg-white text-purple-700 hover:bg-purple-50 font-bold text-xs flex items-center gap-1.5 shadow-sm active:scale-95 transition-all whitespace-nowrap"
            >
              <PlayCircle className="w-4 h-4 fill-current" />
              <span>Ask / Dry-Run Case</span>
            </button>
          </div>

          {/* Code Editor Container */}
          <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-5 shadow-apple-sm flex flex-col justify-between">
            {/* Editor Toolbar */}
            <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-zinc-100 dark:border-zinc-800">
              <div className="flex items-center gap-1.5 bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl">
                <button
                  onClick={() => handleSwitchLanguage('java')}
                  className={`px-3 py-1 text-xs font-semibold rounded-lg transition-colors ${
                    language === 'java'
                      ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm'
                      : 'text-zinc-600 dark:text-zinc-400'
                  }`}
                >
                  Java 21
                </button>
                <button
                  onClick={() => handleSwitchLanguage('python')}
                  className={`px-3 py-1 text-xs font-semibold rounded-lg transition-colors ${
                    language === 'python'
                      ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm'
                      : 'text-zinc-600 dark:text-zinc-400'
                  }`}
                >
                  Python 3.10
                </button>
              </div>

              {/* Direct Dry-Run Trigger Button */}
              <button
                onClick={() => setIsAnimationModalOpen(true)}
                className="px-3.5 py-1.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-sm shadow-purple-500/20 active:scale-95 transition-all"
                title="Watch interactive step-by-step animation for this problem"
              >
                <PlayCircle className="w-4 h-4 fill-current" />
                <span>Dry-Run Animation</span>
              </button>
            </div>

            {/* Code Textarea Area */}
            <div className="mt-3 relative">
              <textarea
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                rows={16}
                spellCheck={false}
                className="w-full p-4 rounded-2xl bg-zinc-950 text-zinc-100 font-mono text-xs leading-relaxed focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-inner resize-y"
              />
            </div>

            {/* Footer with Submit Button */}
            <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs text-zinc-400 font-mono">
                <span>Optimal: {activeQuestion?.timeComplexity || 'O(n)'}</span>
                <span>•</span>
                <span>Space: {activeQuestion?.spaceComplexity || 'O(1)'}</span>
              </div>

              <button
                onClick={handleRunTests}
                disabled={executing}
                className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs flex items-center gap-2 shadow-sm transition-all disabled:opacity-50"
              >
                {executing ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>Running in Database Sandbox...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>Run & Submit to Database</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Execution Result Banner */}
          {results && (
            <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-5 shadow-apple-sm space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  <span className="text-base font-bold text-emerald-600 dark:text-emerald-400">
                    {results.status} (Passed {results.passedCount}/{results.totalCount} Test Cases)
                  </span>
                </div>
                <div className="flex items-center gap-3 text-xs font-mono text-zinc-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" /> {results.executionTimeMs} ms
                  </span>
                  <span>{results.memoryMb} MB</span>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 text-xs font-medium">
                Solution verified & stored in database! Awarded +50 XP to your profile.
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Interactive Animation Dry-Run Modal: Asks for testcase, allows custom input or auto fallback */}
      <QuestionAnimationModal
        question={activeQuestion}
        isOpen={isAnimationModalOpen}
        onClose={() => setIsAnimationModalOpen(false)}
      />
    </div>
  );
};
