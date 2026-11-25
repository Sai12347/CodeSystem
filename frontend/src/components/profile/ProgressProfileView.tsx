import React from 'react';
import { useUser } from '../../context/UserContext';
import { Award, Flame, Target, BookOpen, Clock, Calendar, CheckCircle2 } from 'lucide-react';

export const ProgressProfileView: React.FC = () => {
  const { user, achievements } = useUser();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Profile Overview Card */}
      <div className="p-8 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm flex flex-col md:flex-row items-center md:items-start justify-between gap-6">
        <div className="flex flex-col sm:flex-row items-center gap-5 text-center sm:text-left">
          <img
            src={user.avatarUrl}
            alt={user.name}
            className="w-20 h-20 rounded-3xl object-cover ring-4 ring-blue-500/20 shadow-md"
          />
          <div>
            <div className="flex items-center justify-center sm:justify-start gap-2">
              <h1 className="text-2xl font-bold text-zinc-900 dark:text-white">{user.name}</h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400">
                Level {user.level}
              </span>
            </div>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">@{user.username} • {user.email}</p>
            <p className="text-xs text-zinc-400 mt-1">Member since {user.joinedAt}</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-center">
          <div className="p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800/50 min-w-[90px]">
            <Flame className="w-5 h-5 text-amber-500 mx-auto mb-1" />
            <span className="text-lg font-bold text-zinc-900 dark:text-white">{user.streakDays}</span>
            <p className="text-[10px] text-zinc-400">Day Streak</p>
          </div>
          <div className="p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800/50 min-w-[90px]">
            <Target className="w-5 h-5 text-blue-600 mx-auto mb-1" />
            <span className="text-lg font-bold text-zinc-900 dark:text-white">{user.problemsSolved}</span>
            <p className="text-[10px] text-zinc-400">Solved</p>
          </div>
          <div className="p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800/50 min-w-[90px]">
            <Award className="w-5 h-5 text-purple-600 mx-auto mb-1" />
            <span className="text-lg font-bold text-zinc-900 dark:text-white">{user.xp}</span>
            <p className="text-[10px] text-zinc-400">Total XP</p>
          </div>
        </div>
      </div>

      {/* Weekly Activity Grid */}
      <div className="p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm">
        <h2 className="text-base font-bold text-zinc-900 dark:text-white mb-2">
          Weekly Consistency Calendar
        </h2>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-4">
          Continuous active practice unlocks high-retention mastery.
        </p>

        <div className="grid grid-cols-7 gap-2 text-center text-xs">
          {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, i) => (
            <div key={day} className="p-3 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800/50">
              <span className="text-[11px] text-zinc-400 font-medium">{day}</span>
              <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto my-1.5 font-bold text-xs">
                ✓
              </div>
              <span className="text-[10px] text-zinc-500">45m</span>
            </div>
          ))}
        </div>
      </div>

      {/* All Achievements & Badges */}
      <div className="p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm">
        <h2 className="text-base font-bold text-zinc-900 dark:text-white mb-2">
          Milestone Achievements
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {achievements.map((b) => {
            const isUnlocked = b.unlockedAt !== null;
            return (
              <div
                key={b.id}
                className={`p-4 rounded-2xl border flex items-center gap-4 transition-all ${
                  isUnlocked
                    ? 'bg-zinc-50 dark:bg-zinc-800/60 border-zinc-200 dark:border-zinc-700'
                    : 'bg-zinc-50/40 dark:bg-zinc-900/30 border-zinc-200/40 dark:border-zinc-800/40 opacity-60'
                }`}
              >
                <div
                  className={`w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 ${
                    isUnlocked ? 'bg-amber-500/10 text-amber-500' : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400'
                  }`}
                >
                  <Award className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <h4 className="text-sm font-bold text-zinc-900 dark:text-white">{b.title}</h4>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{b.description}</p>
                  <div className="mt-2 flex items-center justify-between text-[11px]">
                    <span className="text-zinc-400 font-mono">
                      {isUnlocked ? `Unlocked ${b.unlockedAt}` : 'In progress'}
                    </span>
                    <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                      {isUnlocked ? '100%' : `${b.progressPercent}%`}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
