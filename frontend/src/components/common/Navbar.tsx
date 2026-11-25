import React, { useState } from 'react';
import {
  Sparkles,
  Flame,
  Award,
  BookOpen,
  PlayCircle,
  Code2,
  Bot,
  BarChart3,
  User,
  Command,
  UserPlus,
  LogIn,
  LogOut,
  Building2,
  ChevronDown,
} from 'lucide-react';
import { useUser } from '../../context/UserContext';
import { ThemeToggle } from './ThemeToggle';
import { KeyboardShortcutsModal } from './KeyboardShortcutsModal';
import { AuthModal } from './AuthModal';

export type ActiveTab = 'dashboard' | 'learn' | 'visualizer' | 'practice' | 'companies' | 'ai-tutor' | 'progress' | 'profile';

interface NavbarProps {
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, onTabChange }) => {
  const { user, logout } = useUser();
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authDefaultMode, setAuthDefaultMode] = useState<'login' | 'register' | 'switch'>('register');
  const [showUserMenu, setShowUserMenu] = useState(false);

  const navItems = [
    { id: 'dashboard' as ActiveTab, label: 'Dashboard', icon: BarChart3 },
    { id: 'learn' as ActiveTab, label: 'Learn DSA', icon: BookOpen },
    { id: 'visualizer' as ActiveTab, label: 'Visualizer', icon: PlayCircle },
    { id: 'practice' as ActiveTab, label: 'Practice', icon: Code2 },
    { id: 'companies' as ActiveTab, label: 'Companies (100+ PYQs)', icon: Building2 },
    { id: 'ai-tutor' as ActiveTab, label: 'AI Tutor', icon: Bot },
    { id: 'progress' as ActiveTab, label: 'Progress', icon: Award },
    { id: 'profile' as ActiveTab, label: 'Profile', icon: User },
  ];

  const handleOpenFreshLogin = () => {
    setAuthDefaultMode('register');
    setShowAuthModal(true);
    setShowUserMenu(false);
  };

  const handleOpenSignIn = () => {
    setAuthDefaultMode('login');
    setShowAuthModal(true);
    setShowUserMenu(false);
  };

  const handleOpenSwitch = () => {
    setAuthDefaultMode('switch');
    setShowAuthModal(true);
    setShowUserMenu(false);
  };

  return (
    <>
      <header className="sticky top-0 z-40 w-full backdrop-blur-apple bg-white/70 dark:bg-black/70 border-b border-zinc-200/80 dark:border-zinc-800/80 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
          {/* Logo & Brand */}
          <div className="flex items-center gap-6">
            <button
              onClick={() => onTabChange('dashboard')}
              className="flex items-center gap-2.5 focus:outline-none group text-left"
            >
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-blue-500/20 group-hover:scale-105 transition-transform">
                <Sparkles className="w-5 h-5 fill-current" />
              </div>
              <div>
                <span className="text-lg font-bold tracking-tight text-zinc-900 dark:text-white">AlgoPlay</span>
                <span className="hidden sm:inline-block ml-1.5 px-1.5 py-0.5 text-[10px] font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-md">
                  PRO
                </span>
              </div>
            </button>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center gap-1" aria-label="Main Navigation">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => onTabChange(item.id)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full transition-all ${
                      isActive
                        ? 'bg-zinc-900 text-white dark:bg-white dark:text-black shadow-sm'
                        : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* User Gamification Stats & Controls */}
          <div className="flex items-center gap-2.5">
            {/* Daily Streak */}
            <div
              className="flex items-center gap-1.5 px-2.5 py-1 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-full text-xs font-semibold"
              title={`${user.streakDays} Day Learning Streak!`}
            >
              <Flame className="w-3.5 h-3.5 fill-current animate-pulse text-amber-500" />
              <span>{user.streakDays}d</span>
            </div>

            {/* XP and Level Pill */}
            <div
              className="hidden sm:flex items-center gap-2 px-3 py-1 bg-zinc-100 dark:bg-zinc-800 rounded-full text-xs font-medium border border-zinc-200 dark:border-zinc-700"
              title={`${user.xp} XP / Level ${user.level}`}
            >
              <span className="font-semibold text-blue-600 dark:text-blue-400">Lv.{user.level}</span>
              <span className="text-zinc-400 dark:text-zinc-500">•</span>
              <span className="text-zinc-700 dark:text-zinc-300">{user.xp} XP</span>
            </div>

            {/* Fresh Login Shortcut Button */}
            <button
              onClick={handleOpenFreshLogin}
              className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-blue-500/10 text-blue-600 dark:text-blue-400 hover:bg-blue-500/20 rounded-full text-xs font-semibold transition-colors"
              title="Create a fresh user profile in database"
            >
              <UserPlus className="w-3.5 h-3.5" />
              <span>Fresh Login</span>
            </button>

            {/* Keyboard Shortcuts Button */}
            <button
              onClick={() => setShowShortcuts(true)}
              aria-label="Keyboard shortcuts"
              title="Keyboard shortcuts"
              className="hidden md:flex p-2 text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-full transition-colors"
            >
              <Command className="w-4 h-4" />
            </button>

            {/* Theme Toggle */}
            <ThemeToggle />

            {/* User Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu((prev) => !prev)}
                className="flex items-center gap-1.5 p-1 rounded-full ring-2 ring-zinc-200 dark:ring-zinc-800 hover:ring-blue-500 transition-all focus:outline-none"
                aria-label="User account menu"
              >
                <img
                  src={user.avatarUrl}
                  alt={user.name}
                  className="w-8 h-8 rounded-full object-cover"
                />
                <ChevronDown className="w-3 h-3 text-zinc-400 mr-1 hidden sm:inline" />
              </button>

              {/* Dropdown Menu */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-xl p-2 z-50 text-xs">
                  <div className="p-2 border-b border-zinc-100 dark:border-zinc-800 mb-1">
                    <p className="font-bold text-zinc-900 dark:text-white truncate">{user.name}</p>
                    <p className="text-[10px] text-zinc-400 truncate">@{user.username}</p>
                    <p className="text-[10px] text-blue-500 font-medium mt-0.5">Database Synced</p>
                  </div>

                  <button
                    onClick={handleOpenFreshLogin}
                    className="w-full text-left p-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center gap-2 text-zinc-700 dark:text-zinc-200 font-medium"
                  >
                    <UserPlus className="w-3.5 h-3.5 text-blue-500" />
                    <span>Login as Fresh User</span>
                  </button>

                  <button
                    onClick={handleOpenSignIn}
                    className="w-full text-left p-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center gap-2 text-zinc-700 dark:text-zinc-200 font-medium"
                  >
                    <LogIn className="w-3.5 h-3.5 text-emerald-500" />
                    <span>Sign In Existing Account</span>
                  </button>

                  <button
                    onClick={handleOpenSwitch}
                    className="w-full text-left p-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center gap-2 text-zinc-700 dark:text-zinc-200 font-medium"
                  >
                    <Award className="w-3.5 h-3.5 text-amber-500" />
                    <span>Switch Profiles</span>
                  </button>

                  <div className="border-t border-zinc-100 dark:border-zinc-800 my-1" />

                  <button
                    onClick={() => {
                      logout();
                      setShowUserMenu(false);
                    }}
                    className="w-full text-left p-2 rounded-xl hover:bg-rose-50 dark:hover:bg-rose-950/40 text-rose-600 dark:text-rose-400 flex items-center gap-2 font-medium"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    <span>Sign Out</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Sub-Navigation Bar */}
        <div className="lg:hidden flex items-center gap-1 px-4 py-2 overflow-x-auto no-scrollbar border-t border-zinc-100 dark:border-zinc-900">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`flex items-center gap-1 px-3 py-1 text-xs font-medium whitespace-nowrap rounded-full transition-all ${
                  isActive
                    ? 'bg-zinc-900 text-white dark:bg-white dark:text-black'
                    : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </header>

      <KeyboardShortcutsModal isOpen={showShortcuts} onClose={() => setShowShortcuts(false)} />
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        defaultMode={authDefaultMode}
      />
    </>
  );
};
