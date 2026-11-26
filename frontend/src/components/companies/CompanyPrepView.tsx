import React, { useState, useMemo } from 'react';
import {
  Building2,
  Search,
  Filter,
  PlayCircle,
  Award,
  CheckCircle2,
  TrendingUp,
  Clock,
  Sparkles,
  ArrowRight,
  ExternalLink,
  Briefcase,
  Layers,
  Code2,
  Play,
  RotateCcw,
  Lightbulb,
  ChevronLeft,
  ChevronRight,
  ArrowLeft,
  FileCode,
} from 'lucide-react';
import {
  TOP_MNCS,
  CompanyName,
  CompanyMeta,
  CompanyQuestionItem,
  getQuestionsForCompany,
} from '../../data/companyCatalog';
import { QuestionAnimationModal } from '../practice/QuestionAnimationModal';
import { useUser } from '../../context/UserContext';
import { dbService } from '../../services/databaseService';
import { JudgeResponse, judgeService } from '../../services/judgeService';
import { JudgeResultsPanel } from '../practice/JudgeResultsPanel';

export const CompanyPrepView: React.FC = () => {
  const { user, recordProblemSolved } = useUser();

  // Selected Company & Filters
  const [selectedCompany, setSelectedCompany] = useState<CompanyName>('Google');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Active View Mode: 'CATALOG' or 'PRACTICE_IDE'
  const [viewMode, setViewMode] = useState<'CATALOG' | 'PRACTICE_IDE'>('CATALOG');

  // Active question being practiced
  const [activeQuestionId, setActiveQuestionId] = useState<string>('google_pyq_1');

  // Animation modal state
  const [activeAnimQuestion, setActiveAnimQuestion] = useState<any | null>(null);
  const [isAnimModalOpen, setIsAnimModalOpen] = useState<boolean>(false);

  // Coding Editor states
  const [language, setLanguage] = useState<'java' | 'python'>('java');
  const [userCode, setUserCode] = useState<string>('');
  const [executing, setExecuting] = useState<boolean>(false);
  const [showHintIndex, setShowHintIndex] = useState<number | null>(null);
  const [executionNotice, setExecutionNotice] = useState<string | null>(null);
  const [judgeResult, setJudgeResult] = useState<JudgeResponse | null>(null);
  const [xpAwarded, setXpAwarded] = useState<number | null>(null);

  // User database progress
  const userProgress = useMemo(() => dbService.getUserProgress(user.id), [user.id]);

  const companyMeta: CompanyMeta = useMemo(() => {
    return TOP_MNCS.find((c) => c.name === selectedCompany) || TOP_MNCS[0];
  }, [selectedCompany]);

  const allCompanyQuestions = useMemo(() => {
    return getQuestionsForCompany(selectedCompany);
  }, [selectedCompany]);

  // Filter questions
  const filteredQuestions = useMemo(() => {
    return allCompanyQuestions.filter((q) => {
      const matchDiff = selectedDifficulty === 'All' || q.difficulty === selectedDifficulty;
      const matchSearch =
        q.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        q.topic.toLowerCase().includes(searchQuery.toLowerCase()) ||
        q.subtopic.toLowerCase().includes(searchQuery.toLowerCase());
      return matchDiff && matchSearch;
    });
  }, [allCompanyQuestions, selectedDifficulty, searchQuery]);

  const activeQuestion = useMemo(() => {
    const found = allCompanyQuestions.find((q) => q.id === activeQuestionId);
    if (found) return found;
    return filteredQuestions[0] || allCompanyQuestions[0];
  }, [allCompanyQuestions, activeQuestionId, filteredQuestions]);

  const solvedCompanyCount = useMemo(() => {
    return allCompanyQuestions.filter((q) => userProgress.solvedProblemIds.includes(q.id)).length;
  }, [allCompanyQuestions, userProgress]);

  // Open direct coding practice for any company question
  const handleOpenPracticeForQuestion = (q: CompanyQuestionItem) => {
    setActiveQuestionId(q.id);
    setUserCode(language === 'java' ? q.starterCode.java : q.starterCode.python);
    setExecutionNotice(null);
    setJudgeResult(null);
    setXpAwarded(null);
    setShowHintIndex(null);
    setViewMode('PRACTICE_IDE');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Open animation dry-run modal
  const handleOpenAnimation = (q: CompanyQuestionItem) => {
    const adaptedQuestion: any = {
      ...q,
      hints: [
        `This is a generated company-tagged practice prompt.`,
        `Focus on optimal asymptotic bounds: ${q.timeComplexity}.`,
      ],
      animationSteps: [],
    };
    setActiveAnimQuestion(adaptedQuestion);
    setIsAnimModalOpen(true);
  };

  const handleSwitchLanguage = (lang: 'java' | 'python') => {
    setLanguage(lang);
    if (activeQuestion) {
      setUserCode(lang === 'java' ? activeQuestion.starterCode.java : activeQuestion.starterCode.python);
    }
  };

  const handleRunAndSubmit = async () => {
    if (!activeQuestion) return;
    setExecuting(true);
    setExecutionNotice(null);
    setJudgeResult(null);
    setXpAwarded(null);
    try {
      const result = await judgeService.submitSolution(activeQuestion.slug, language, userCode);
      setJudgeResult(result);
      dbService.saveSubmission({
        userId: user.id,
        problemId: activeQuestion.id,
        problemTitle: activeQuestion.title,
        language,
        code: userCode,
        status: result.status,
        executionTimeMs: result.executionTimeMs,
        memoryMb: null,
      });
      if (result.status === 'ACCEPTED') {
        const alreadySolved = userProgress.solvedProblemIds.includes(activeQuestion.id);
        const reward = activeQuestion.difficulty === 'Hard' ? 80 : 50;
        recordProblemSolved(activeQuestion.id, reward);
        if (!alreadySolved) setXpAwarded(reward);
      }
    } catch (error) {
      setExecutionNotice(error instanceof Error ? error.message : 'The judge request failed. Please try again.');
    } finally {
      setExecuting(false);
    }
  };

  // Navigate to next or previous question
  const currentIndex = filteredQuestions.findIndex((q) => q.id === activeQuestion.id);
  const handlePrevQuestion = () => {
    if (currentIndex > 0) {
      handleOpenPracticeForQuestion(filteredQuestions[currentIndex - 1]);
    }
  };
  const handleNextQuestion = () => {
    if (currentIndex < filteredQuestions.length - 1) {
      handleOpenPracticeForQuestion(filteredQuestions[currentIndex + 1]);
    }
  };

  const isSolved = activeQuestion ? userProgress.solvedProblemIds.includes(activeQuestion.id) : false;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* ======================================================== */}
      {/* 1. TOP MNC CAROUSEL / SELECTOR                          */}
      {/* ======================================================== */}
      <div>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="p-1 rounded-lg bg-blue-600 text-white shadow-sm">
                <Building2 className="w-4 h-4" />
              </span>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                Curated problems grouped by company tags
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">
              Company-Tagged Practice
            </h1>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 max-w-2xl">
              Browse curated problems by company tags. Tags are for organizing practice and do not claim a question was asked at a specific interview.
            </p>
          </div>

          {viewMode === 'PRACTICE_IDE' && (
            <button
              onClick={() => setViewMode('CATALOG')}
              className="px-4 py-2 rounded-2xl bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Question Catalog</span>
            </button>
          )}
        </div>

        {/* Company Selection Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 mt-5">
          {TOP_MNCS.map((c) => {
            const isSelected = selectedCompany === c.name;
            return (
              <button
                key={c.name}
                onClick={() => {
                  setSelectedCompany(c.name);
                  setSelectedDifficulty('All');
                  const firstQ = getQuestionsForCompany(c.name)[0];
                  if (firstQ) {
                    setActiveQuestionId(firstQ.id);
                    setUserCode(language === 'java' ? firstQ.starterCode.java : firstQ.starterCode.python);
                  }
                }}
                className={`p-3.5 rounded-2xl border text-left flex items-center gap-3 transition-all ${
                  isSelected
                    ? 'bg-blue-50 dark:bg-blue-950/40 border-blue-500 ring-2 ring-blue-500/30 shadow-sm'
                    : 'bg-white dark:bg-zinc-900 border-zinc-200/80 dark:border-zinc-800 hover:border-zinc-400'
                }`}
              >
                <div className="text-2xl p-2 rounded-xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                  {c.logo}
                </div>
                <div className="truncate">
                  <h3 className="text-xs font-bold text-zinc-900 dark:text-white truncate">
                    {c.name}
                  </h3>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="text-[10px] font-semibold text-blue-600 dark:text-blue-400">
                      {getQuestionsForCompany(c.name).length} Qs
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* ======================================================== */}
      {/* 2. MODE A: ACTIVE CODING WORKSPACE FOR SELECTED QUESTION */}
      {/* ======================================================== */}
      {viewMode === 'PRACTICE_IDE' && activeQuestion && (
        <div className="space-y-4">
          {/* Practice Workspace Top Navigation Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setViewMode('CATALOG')}
                className="p-2 rounded-xl text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                title="Back to Catalog"
              >
                <ArrowLeft className="w-4 h-4" />
              </button>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-blue-600 dark:text-blue-400">
                    Question #{activeQuestion.number}
                  </span>
                  <span
                    className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
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
                </div>
                <h2 className="text-base font-bold text-zinc-900 dark:text-white mt-0.5">
                  {activeQuestion.title}
                </h2>
              </div>
            </div>

            {/* Pagination Controls */}
            <div className="flex items-center gap-2">
              <button
                onClick={handlePrevQuestion}
                disabled={currentIndex <= 0}
                className="p-2 rounded-xl border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
                title="Previous Question"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-xs font-mono text-zinc-400">
                {currentIndex + 1} / {filteredQuestions.length}
              </span>
              <button
                onClick={handleNextQuestion}
                disabled={currentIndex >= filteredQuestions.length - 1}
                className="p-2 rounded-xl border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
                title="Next Question"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Split Workspace: Left = Problem Specs; Right = Code Editor & Test Runner */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Pane: Spec & Examples */}
            <div className="lg:col-span-5 bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-6 shadow-apple-sm space-y-4 max-h-[640px] overflow-y-auto">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-zinc-500">
                  Topic: {activeQuestion.topic} ({activeQuestion.subtopic})
                </span>
                {isSolved && (
                  <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2">
                  Problem Statement
                </h3>
                <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                  {activeQuestion.description}
                </p>
              </div>

              {/* Examples */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2">
                  Sample Test Cases
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
            </div>

            {/* Right Pane: Code Editor & Execution */}
            <div className="lg:col-span-7 flex flex-col gap-4">
              {/* Callout to trigger Dry-Run Animation */}
              <div className="p-4 rounded-3xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-apple-md flex items-center justify-between gap-3">
                <div>
                  <h4 className="text-xs font-bold flex items-center gap-1.5 text-purple-100">
                    <Sparkles className="w-3.5 h-3.5 fill-current" />
                    <span>INTERACTIVE TESTCASE DRY-RUN ANIMATION</span>
                  </h4>
                  <p className="text-[11px] text-purple-100 mt-0.5">
                    Step through logic before submitting. Run custom or automatic cases!
                  </p>
                </div>
                <button
                  onClick={() => handleOpenAnimation(activeQuestion)}
                  className="px-3.5 py-1.5 rounded-xl bg-white text-purple-700 font-bold text-xs flex items-center gap-1.5 shadow-sm active:scale-95 transition-all whitespace-nowrap"
                >
                  <PlayCircle className="w-3.5 h-3.5 fill-current" />
                  <span>Dry-Run Animation</span>
                </button>
              </div>

              {/* Code Editor Container */}
              <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-5 shadow-apple-sm flex flex-col justify-between">
                {/* Editor Header Toolbar */}
                <div className="flex items-center justify-between pb-3 border-b border-zinc-100 dark:border-zinc-800">
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

                  <button
                    onClick={() =>
                      setUserCode(
                        language === 'java'
                          ? activeQuestion.starterCode.java
                          : activeQuestion.starterCode.python
                      )
                    }
                    title="Reset to company starter template"
                    className="p-1.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Editor Area */}
                <div className="mt-3 relative">
                  <textarea
                    value={userCode}
                    onChange={(e) => setUserCode(e.target.value)}
                    rows={16}
                    spellCheck={false}
                    className="w-full p-4 rounded-2xl bg-zinc-950 text-zinc-100 font-mono text-xs leading-relaxed focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-inner resize-y"
                  />
                </div>

                {/* Submit Toolbar */}
                <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs text-zinc-400 font-mono">
                    <span>Target: {activeQuestion.timeComplexity}</span>
                    <span>•</span>
                    <span>Space: {activeQuestion.spaceComplexity}</span>
                  </div>

                  <button
                    onClick={handleRunAndSubmit}
                    className="px-5 py-2.5 rounded-xl bg-zinc-600 hover:bg-zinc-700 text-white font-semibold text-xs flex items-center gap-2 shadow-sm transition-all"
                  >
                    {executing ? 'Judging…' : 'Submit Solution'}
                  </button>
                </div>
              </div>

              {executionNotice && (
                <div className="p-4 rounded-2xl border border-amber-300 bg-amber-50 dark:bg-amber-950/30 dark:border-amber-800 text-xs text-amber-800 dark:text-amber-200" role="status">
                  {executionNotice}
                </div>
              )}
              <JudgeResultsPanel result={judgeResult} errorMessage={null} xpAwarded={xpAwarded} />
            </div>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* 3. MODE B: COMPANY CATALOG VIEW WITH DIRECT SOLVE BUTTON */}
      {/* ======================================================== */}
      {viewMode === 'CATALOG' && (
        <>
          {/* Active Company Hero Banner */}
              <div className="p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="text-4xl p-3 rounded-2xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center shadow-inner">
                {companyMeta.logo}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-xl font-bold text-zinc-900 dark:text-white">
                    {companyMeta.name} Curated Problems
                  </h2>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 max-w-xl">
                  Problems tagged with this company in the curated practice bank.
                </p>
              </div>
            </div>

            {/* Company Solved Stat */}
            <div className="flex items-center gap-3">
              <div className="px-4 py-2.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700 text-right">
                <span className="text-[11px] text-zinc-400 block">Your {companyMeta.name} Progress</span>
                <span className="text-sm font-bold text-emerald-600 dark:text-emerald-400">
                  {solvedCompanyCount} / {allCompanyQuestions.length} Solved
                </span>
              </div>
            </div>
          </div>

          {/* Problem Search */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-zinc-100/70 dark:bg-zinc-900/50 p-2.5 rounded-2xl border border-zinc-200/60 dark:border-zinc-800/60">
            {/* Search */}
            <div className="relative sm:w-64">
              <Search className="w-3.5 h-3.5 text-zinc-400 absolute left-2.5 top-2.5 pointer-events-none" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={`Search ${companyMeta.name} problems...`}
                className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-900 dark:text-white placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Question List Table */}
          <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-5 shadow-apple-sm space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-zinc-100 dark:border-zinc-800 text-xs font-bold text-zinc-500">
              <span>
                {companyMeta.name} Questions ({filteredQuestions.length} Found) — Click Solve on Any Question
              </span>
              <div className="flex items-center gap-2">
                {(['All', 'Easy', 'Medium', 'Hard'] as const).map((d) => (
                  <button
                    key={d}
                    onClick={() => setSelectedDifficulty(d)}
                    className={`px-2 py-0.5 rounded text-[11px] font-semibold transition-colors ${
                      selectedDifficulty === d
                        ? 'bg-blue-600 text-white'
                        : 'text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200'
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>

            <div className="divide-y divide-zinc-100 dark:divide-zinc-800/60 max-h-[620px] overflow-y-auto pr-1">
              {filteredQuestions.map((q) => {
                const isItemSolved = userProgress.solvedProblemIds.includes(q.id);

                return (
                  <div
                    key={q.id}
                    className="py-3.5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 hover:bg-zinc-50/60 dark:hover:bg-zinc-800/30 p-2.5 rounded-2xl transition-colors group"
                  >
                    <div className="flex items-start gap-3 flex-1">
                      <div className="mt-1">
                        <CheckCircle2
                          className={`w-4 h-4 ${
                            isItemSolved ? 'text-emerald-500 fill-emerald-500/10' : 'text-zinc-300 dark:text-zinc-700'
                          }`}
                        />
                      </div>

                      <div>
                        <div className="flex flex-wrap items-center gap-1.5 mb-1">
                          <span className="text-[10px] font-mono font-bold text-zinc-400">#{q.number}</span>
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
                        </div>

                        <h4
                          onClick={() => handleOpenPracticeForQuestion(q)}
                          className="text-xs sm:text-sm font-bold text-zinc-900 dark:text-white leading-snug cursor-pointer group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors"
                        >
                          {q.title}
                        </h4>

                        <p className="text-xs text-zinc-600 dark:text-zinc-300 mt-1.5 leading-relaxed max-w-3xl">
                          {q.description}
                        </p>

                        <div className="flex items-center gap-3 text-[11px] text-zinc-400 mt-1">
                          <span>Topic: {q.topic} ({q.subtopic})</span>
                          <span>•</span>
                          <span className="font-mono text-zinc-500">{q.timeComplexity}</span>
                        </div>
                      </div>
                    </div>

                    {/* Right Actions: Dry-Run Animation and Practice Button */}
                    <div className="flex items-center gap-2.5 w-full sm:w-auto justify-between sm:justify-end">
                      {/* Dry-Run Animation Button */}
                      <button
                        onClick={() => handleOpenAnimation(q)}
                        className="px-3 py-1.5 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-600 dark:text-purple-400 font-semibold text-xs flex items-center gap-1.5 transition-colors"
                        title="Watch dry run animation with custom or auto test case"
                      >
                        <PlayCircle className="w-3.5 h-3.5" />
                        <span className="hidden sm:inline">Dry-Run</span>
                      </button>

                      {/* MAIN ACTION: Solve / Practice Any Question! */}
                      <button
                        onClick={() => handleOpenPracticeForQuestion(q)}
                        className="px-4 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-sm active:scale-95 transition-all"
                        title="Open interactive coding editor to practice this question"
                      >
                        <Code2 className="w-3.5 h-3.5" />
                        <span>Practice / Solve</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}

      {/* Interactive Animation Modal for Company Questions */}
      <QuestionAnimationModal
        question={activeAnimQuestion}
        isOpen={isAnimModalOpen}
        onClose={() => setIsAnimModalOpen(false)}
      />
    </div>
  );
};
