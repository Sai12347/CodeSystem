import React from 'react';
import { useUser } from '../../context/UserContext';
import {
  Flame,
  Award,
  BookOpen,
  Code2,
  Clock,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  PlayCircle,
  TrendingUp,
} from 'lucide-react';
import { ActiveTab } from '../common/Navbar';
import { AlgorithmId } from '../../types/algorithm';
import { useVisualizer } from '../../context/VisualizerContext';

interface DashboardViewProps {
  onNavigate: (tab: ActiveTab) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate }) => {
  const { user, achievements, dailyChallenge, completeDailyChallenge } = useUser();
  const { selectAlgorithm } = useVisualizer();

  const handleLaunchAlgo = (id: AlgorithmId) => {
    selectAlgorithm(id);
    onNavigate('visualizer');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-zinc-900 via-zinc-900 to-blue-950 text-white p-8 sm:p-10 shadow-apple-lg border border-zinc-800">
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-400/30">
                Level {user.level} Thinker
              </span>
              <span className="text-xs text-zinc-400">
                {user.xp} / {user.xpToNextLevel} XP to Level {user.level + 1}
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              Welcome back, {user.name}! 👋
            </h1>
            <p className="mt-2 text-zinc-300 text-sm max-w-xl leading-relaxed">
              You are on a <span className="text-amber-400 font-bold">{user.streakDays}-day streak</span>!
              Today’s recommended challenge is ready. Dive into algorithms, predict step behaviors, and strengthen your problem-solving intuition.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
            <button
              onClick={() => onNavigate('visualizer')}
              className="px-5 py-3 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm flex items-center justify-center gap-2 shadow-lg shadow-blue-600/30 transition-all active:scale-95"
            >
              <PlayCircle className="w-4 h-4 fill-current" />
              <span>Resume Visualizer</span>
            </button>
            <button
              onClick={() => onNavigate('practice')}
              className="px-5 py-3 rounded-2xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm flex items-center justify-center gap-2 backdrop-blur-sm border border-white/10 transition-all"
            >
              <Code2 className="w-4 h-4" />
              <span>Practice Arena</span>
            </button>
          </div>
        </div>

        {/* Level XP Progress Bar */}
        <div className="mt-8 pt-6 border-t border-white/10">
          <div className="flex justify-between text-xs text-zinc-400 mb-2">
            <span>Overall DSA Curriculum Completion</span>
            <span className="font-semibold text-white">{user.completionPercentage}%</span>
          </div>
          <div className="w-full h-2.5 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-cyan-400 rounded-full transition-all duration-500"
              style={{ width: `${user.completionPercentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* 4 Core Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Streak */}
        <div className="p-5 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-500 flex items-center justify-center flex-shrink-0">
            <Flame className="w-6 h-6 fill-current animate-pulse" />
          </div>
          <div>
            <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">Learning Streak</span>
            <p className="text-2xl font-bold text-zinc-900 dark:text-white mt-0.5">{user.streakDays} Days</p>
          </div>
        </div>

        {/* Problems Solved */}
        <div className="p-5 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center flex-shrink-0">
            <Code2 className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">Problems Solved</span>
            <p className="text-2xl font-bold text-zinc-900 dark:text-white mt-0.5">{user.problemsSolved}</p>
          </div>
        </div>

        {/* Total Hours */}
        <div className="p-5 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center flex-shrink-0">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">Learning Time</span>
            <p className="text-2xl font-bold text-zinc-900 dark:text-white mt-0.5">
              {(user.totalLearningMinutes / 60).toFixed(1)} hrs
            </p>
          </div>
        </div>

        {/* Total XP */}
        <div className="p-5 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-6 h-6 fill-current" />
          </div>
          <div>
            <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">Total Earned XP</span>
            <p className="text-2xl font-bold text-zinc-900 dark:text-white mt-0.5">{user.xp} XP</p>
          </div>
        </div>
      </div>

      {/* Daily Challenge & Recommended Next Topics */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Daily Challenge Card */}
        <div className="lg:col-span-5 p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 uppercase tracking-wider">
                Daily Challenge
              </span>
              <span className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
                +{dailyChallenge.rewardXp} XP Reward
              </span>
            </div>

            <h3 className="text-lg font-bold text-zinc-900 dark:text-white mt-3">
              {dailyChallenge.title}
            </h3>
            <p className="text-xs text-zinc-600 dark:text-zinc-400 mt-2 leading-relaxed">
              {dailyChallenge.question}
            </p>
          </div>

          <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
            {dailyChallenge.isCompleted ? (
              <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" /> Challenge Completed!
              </span>
            ) : (
              <button
                onClick={() => {
                  handleLaunchAlgo('binary-search');
                  completeDailyChallenge();
                }}
                className="w-full py-2.5 px-4 rounded-xl bg-amber-500 hover:bg-amber-600 text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition-colors"
              >
                <span>Launch Challenge</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Recommended Topics */}
        <div className="lg:col-span-7 p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-zinc-900 dark:text-white">
                Recently Studied & Recommended
              </h3>
              <button
                onClick={() => onNavigate('learn')}
                className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
              >
                <span>View Full Syllabus</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            <div className="space-y-3">
              {[
                {
                  id: 'binary-search' as AlgorithmId,
                  title: 'Binary Search',
                  cat: 'Beginner',
                  desc: 'Divide-and-conquer on sorted arrays in O(log n)',
                  time: 'O(log n)',
                },
                {
                  id: 'bubble-sort' as AlgorithmId,
                  title: 'Bubble Sort',
                  cat: 'Beginner',
                  desc: 'Adjacent comparison & bubbling largest element',
                  time: 'O(n²)',
                },
                {
                  id: 'two-pointers' as AlgorithmId,
                  title: 'Two Pointers (Sorted)',
                  cat: 'Intermediate',
                  desc: 'Shrinking boundaries inwards in linear O(n) time',
                  time: 'O(n)',
                },
              ].map((topic) => (
                <div
                  key={topic.id}
                  className="flex items-center justify-between p-3.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/60 dark:border-zinc-800/60 hover:border-blue-400 transition-colors cursor-pointer group"
                  onClick={() => handleLaunchAlgo(topic.id)}
                >
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-xs">
                      <PlayCircle className="w-5 h-5 group-hover:scale-110 transition-transform" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-zinc-900 dark:text-white">
                        {topic.title}
                      </h4>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">{topic.desc}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="font-mono text-xs text-blue-600 dark:text-blue-400 font-semibold">
                      {topic.time}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Achievement Badges Showcase */}
      <div className="p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-zinc-900 dark:text-white">
              Achievement Badges
            </h3>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Unlocked through real interactive practice and milestones
            </p>
          </div>
          <button
            onClick={() => onNavigate('progress')}
            className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline"
          >
            All Badges
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          {achievements.map((badge) => {
            const isUnlocked = badge.unlockedAt !== null;
            return (
              <div
                key={badge.id}
                className={`p-4 rounded-2xl border text-center flex flex-col items-center justify-between transition-all ${
                  isUnlocked
                    ? 'bg-zinc-50 dark:bg-zinc-800/60 border-zinc-200 dark:border-zinc-700 shadow-sm'
                    : 'bg-zinc-50/50 dark:bg-zinc-900/40 border-zinc-200/40 dark:border-zinc-800/40 opacity-50'
                }`}
              >
                <div
                  className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-2 ${
                    isUnlocked
                      ? 'bg-amber-500/10 text-amber-500'
                      : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400'
                  }`}
                >
                  <Award className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-zinc-900 dark:text-white truncate max-w-[130px]">
                    {badge.title}
                  </h4>
                  <p className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-0.5 line-clamp-2">
                    {badge.description}
                  </p>
                </div>
                <div className="mt-2 text-[10px] font-semibold text-emerald-600 dark:text-emerald-400">
                  {isUnlocked ? 'Unlocked' : `${badge.progressPercent}%`}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
