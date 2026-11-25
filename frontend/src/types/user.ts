export interface UserProfile {
  id: string;
  username: string;
  email: string;
  name: string;
  avatarUrl: string;
  level: number;
  xp: number;
  xpToNextLevel: number;
  streakDays: number;
  problemsSolved: number;
  totalLearningMinutes: number;
  completionPercentage: number;
  joinedAt: string;
}

export interface AchievementBadge {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'STREAK' | 'MASTERY' | 'SPEED' | 'PRACTICE';
  unlockedAt: string | null;
  progressPercent: number;
}

export interface DailyChallenge {
  id: string;
  date: string;
  title: string;
  algorithmId: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  rewardXp: number;
  isCompleted: boolean;
  question: string;
}
