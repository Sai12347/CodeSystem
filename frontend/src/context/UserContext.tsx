import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, AchievementBadge, DailyChallenge } from '../types/user';
import { dbService, DbUser } from '../services/databaseService';

interface UserContextType {
  user: DbUser;
  isLoggedIn: boolean;
  achievements: AchievementBadge[];
  dailyChallenge: DailyChallenge;
  allRegisteredUsers: DbUser[];
  awardXp: (amount: number, reason: string) => void;
  recordTopicCompletion: (topicId: string) => void;
  recordProblemSolved: (problemId: string, xpEarned: number) => void;
  completeDailyChallenge: () => void;
  login: (usernameOrEmail: string, pass: string) => void;
  register: (params: { username: string; email: string; password: string; name: string; avatarUrl?: string }) => void;
  logout: () => void;
  switchUser: (userId: string) => void;
}

const initialBadges: AchievementBadge[] = [
  {
    id: 'badge_first_spark',
    title: 'First Spark',
    description: 'Visualized your first algorithm',
    icon: 'Sparkles',
    category: 'MASTERY',
    unlockedAt: '2026-01-11',
    progressPercent: 100,
  },
  {
    id: 'badge_week_streak',
    title: 'Relentless Flow',
    description: 'Maintained a 7-day learning streak',
    icon: 'Flame',
    category: 'STREAK',
    unlockedAt: '2026-01-17',
    progressPercent: 100,
  },
  {
    id: 'badge_binary_master',
    title: 'Logarithmic Thinker',
    description: 'Completed all Binary Search interactive challenges',
    icon: 'Target',
    category: 'MASTERY',
    unlockedAt: '2026-01-18',
    progressPercent: 100,
  },
  {
    id: 'badge_sorter',
    title: 'Sorting Sensei',
    description: 'Dry-run 5 different sorting algorithms',
    icon: 'Layers',
    category: 'PRACTICE',
    unlockedAt: null,
    progressPercent: 60,
  },
  {
    id: 'badge_predictor',
    title: 'Oracle Mind',
    description: 'Get 10 predictions correct in Predict Mode',
    icon: 'HelpCircle',
    category: 'SPEED',
    unlockedAt: null,
    progressPercent: 70,
  },
];

const initialDailyChallenge: DailyChallenge = {
  id: 'dc_today',
  date: new Date().toISOString().split('T')[0],
  title: 'Binary Search Edge Condition',
  algorithmId: 'binary-search',
  difficulty: 'Easy',
  rewardXp: 50,
  isCompleted: false,
  question: 'Observe what happens when target is larger than all elements in the array.',
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<DbUser>(() => {
    const existing = dbService.getCurrentUser();
    if (existing) return existing;
    return dbService.getAllUsers()[0];
  });

  const [allRegisteredUsers, setAllRegisteredUsers] = useState<DbUser[]>(() => dbService.getAllUsers());
  const [achievements] = useState<AchievementBadge[]>(initialBadges);
  const [dailyChallenge, setDailyChallenge] = useState<DailyChallenge>(initialDailyChallenge);

  const syncUserFromDb = () => {
    const u = dbService.getCurrentUser();
    if (u) {
      setCurrentUser({ ...u });
    }
    setAllRegisteredUsers(dbService.getAllUsers());
  };

  const login = (usernameOrEmail: string, pass: string) => {
    const loggedIn = dbService.login(usernameOrEmail, pass);
    setCurrentUser({ ...loggedIn });
    setAllRegisteredUsers(dbService.getAllUsers());
  };

  const register = (params: { username: string; email: string; password: string; name: string; avatarUrl?: string }) => {
    const registered = dbService.register(params);
    setCurrentUser({ ...registered });
    setAllRegisteredUsers(dbService.getAllUsers());
  };

  const logout = () => {
    dbService.logout();
    // Default to a guest user or first user
    const users = dbService.getAllUsers();
    if (users.length > 0) {
      dbService.setCurrentUser(users[0].id);
      setCurrentUser({ ...users[0] });
    }
    setAllRegisteredUsers(dbService.getAllUsers());
  };

  const switchUser = (userId: string) => {
    const switched = dbService.setCurrentUser(userId);
    setCurrentUser({ ...switched });
    setAllRegisteredUsers(dbService.getAllUsers());
  };

  const awardXp = (amount: number, reason: string) => {
    const u = { ...currentUser };
    u.xp += amount;
    const nextLevel = Math.floor(u.xp / 500) + 1;
    u.level = nextLevel;
    u.xpToNextLevel = nextLevel * 500;
    dbService.updateUser(u);
    setCurrentUser(u);
    setAllRegisteredUsers(dbService.getAllUsers());
  };

  const recordTopicCompletion = (topicId: string) => {
    awardXp(100, `Completed topic: ${topicId}`);
    const u = { ...currentUser };
    u.completionPercentage = Math.min(100, u.completionPercentage + 3);
    u.totalLearningMinutes += 25;
    dbService.updateUser(u);
    setCurrentUser(u);
  };

  const recordProblemSolved = (problemId: string, xpEarned: number) => {
    dbService.recordProblemSolved(currentUser.id, problemId, xpEarned);
    syncUserFromDb();
  };

  const completeDailyChallenge = () => {
    if (!dailyChallenge.isCompleted) {
      setDailyChallenge((prev) => ({ ...prev, isCompleted: true }));
      awardXp(dailyChallenge.rewardXp, 'Completed Daily Challenge');
    }
  };

  return (
    <UserContext.Provider
      value={{
        user: currentUser,
        isLoggedIn: !!currentUser,
        achievements,
        dailyChallenge,
        allRegisteredUsers,
        awardXp,
        recordTopicCompletion,
        recordProblemSolved,
        completeDailyChallenge,
        login,
        register,
        logout,
        switchUser,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be used within UserProvider');
  return context;
};
