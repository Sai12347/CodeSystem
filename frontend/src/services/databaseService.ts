/**
 * CodeSystem Database Service
 * Provides full relational persistence across browser sessions,
 * mirroring MySQL schema (Users, Profiles, Problems, Submissions, Progress, Badges).
 */

export interface DbUser {
  id: string;
  username: string;
  email: string;
  passwordHash: string; // Base64 encoded hash
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

export interface DbSubmission {
  id: string;
  userId: string;
  problemId: string;
  problemTitle: string;
  language: 'java' | 'python';
  code: string;
  status: 'ACCEPTED' | 'WRONG_ANSWER' | 'TIME_LIMIT_EXCEEDED' | 'RUNTIME_ERROR' | 'COMPILATION_ERROR';
  executionTimeMs: number;
  memoryMb: number | null;
  submittedAt: string;
}

export interface DbUserProgress {
  userId: string;
  solvedProblemIds: string[];
  completedTopicIds: string[];
  bookmarkedProblemIds: string[];
  unlockedBadgeIds: string[];
  notes: Record<string, string>; // problemId -> notes
}

const STORAGE_KEYS = {
  USERS: 'codesystem_db_users',
  CURRENT_USER_ID: 'codesystem_db_current_user_id',
  SUBMISSIONS: 'codesystem_db_submissions',
  PROGRESS: 'codesystem_db_progress',
};

// Seed default demo user
const DEFAULT_DEMO_USER: DbUser = {
  id: 'usr_alex_rivera',
  username: 'alex_code',
  email: 'alex@example.com',
  passwordHash: btoa('password123'),
  name: 'Alex Rivera',
  avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
  level: 4,
  xp: 1350,
  xpToNextLevel: 2000,
  streakDays: 7,
  problemsSolved: 24,
  totalLearningMinutes: 380,
  completionPercentage: 35,
  joinedAt: '2026-01-10',
};

class DatabaseService {
  private users: Map<string, DbUser> = new Map();
  private submissions: DbSubmission[] = [];
  private progress: Map<string, DbUserProgress> = new Map();
  private currentUserId: string | null = null;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage() {
    try {
      // Load Users
      const rawUsers = localStorage.getItem(STORAGE_KEYS.USERS);
      if (rawUsers) {
        const parsed: DbUser[] = JSON.parse(rawUsers);
        parsed.forEach((u) => this.users.set(u.id, u));
      } else {
        this.users.set(DEFAULT_DEMO_USER.id, DEFAULT_DEMO_USER);
        this.saveUsers();
      }

      // Load Current User ID
      const currentId = localStorage.getItem(STORAGE_KEYS.CURRENT_USER_ID);
      if (currentId && this.users.has(currentId)) {
        this.currentUserId = currentId;
      } else {
        this.currentUserId = DEFAULT_DEMO_USER.id;
        localStorage.setItem(STORAGE_KEYS.CURRENT_USER_ID, DEFAULT_DEMO_USER.id);
      }

      // Load Submissions
      const rawSubs = localStorage.getItem(STORAGE_KEYS.SUBMISSIONS);
      if (rawSubs) {
        this.submissions = JSON.parse(rawSubs);
      }

      // Load Progress
      const rawProg = localStorage.getItem(STORAGE_KEYS.PROGRESS);
      if (rawProg) {
        const parsed: Record<string, DbUserProgress> = JSON.parse(rawProg);
        Object.entries(parsed).forEach(([uid, prog]) => this.progress.set(uid, prog));
      }
    } catch (e) {
      console.error('Failed to load CodeSystem database from localStorage:', e);
    }
  }

  private saveUsers() {
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(Array.from(this.users.values())));
  }

  private saveSubmissions() {
    localStorage.setItem(STORAGE_KEYS.SUBMISSIONS, JSON.stringify(this.submissions));
  }

  private saveProgress() {
    const obj: Record<string, DbUserProgress> = {};
    this.progress.forEach((v, k) => (obj[k] = v));
    localStorage.setItem(STORAGE_KEYS.PROGRESS, JSON.stringify(obj));
  }

  // User & Authentication Methods
  public getCurrentUser(): DbUser | null {
    if (!this.currentUserId) return null;
    return this.users.get(this.currentUserId) || null;
  }

  public setCurrentUser(userId: string): DbUser {
    const user = this.users.get(userId);
    if (!user) throw new Error('User not found in database.');
    this.currentUserId = userId;
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER_ID, userId);
    return user;
  }

  public register(params: {
    username: string;
    email: string;
    password: string;
    name: string;
    avatarUrl?: string;
  }): DbUser {
    // Check if username or email already exists
    for (const u of this.users.values()) {
      if (u.username.toLowerCase() === params.username.toLowerCase()) {
        throw new Error(`Username "${params.username}" is already taken.`);
      }
      if (u.email.toLowerCase() === params.email.toLowerCase()) {
        throw new Error(`Email "${params.email}" is already registered.`);
      }
    }

    const newUser: DbUser = {
      id: `usr_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      username: params.username.trim(),
      email: params.email.trim().toLowerCase(),
      passwordHash: btoa(params.password),
      name: params.name.trim() || params.username.trim(),
      avatarUrl:
        params.avatarUrl ||
        `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(params.username)}`,
      level: 1,
      xp: 0,
      xpToNextLevel: 500,
      streakDays: 1,
      problemsSolved: 0,
      totalLearningMinutes: 0,
      completionPercentage: 0,
      joinedAt: new Date().toISOString().split('T')[0],
    };

    this.users.set(newUser.id, newUser);
    this.saveUsers();

    // Initialize progress record
    const initProg: DbUserProgress = {
      userId: newUser.id,
      solvedProblemIds: [],
      completedTopicIds: [],
      bookmarkedProblemIds: [],
      unlockedBadgeIds: ['badge_first_spark'],
      notes: {},
    };
    this.progress.set(newUser.id, initProg);
    this.saveProgress();

    this.setCurrentUser(newUser.id);
    return newUser;
  }

  public login(usernameOrEmail: string, password: string): DbUser {
    const query = usernameOrEmail.trim().toLowerCase();
    const encodedPass = btoa(password);

    for (const u of this.users.values()) {
      if (
        (u.username.toLowerCase() === query || u.email.toLowerCase() === query) &&
        u.passwordHash === encodedPass
      ) {
        this.setCurrentUser(u.id);
        return u;
      }
    }

    throw new Error('Invalid username/email or password.');
  }

  public logout() {
    this.currentUserId = null;
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER_ID);
  }

  public getAllUsers(): DbUser[] {
    return Array.from(this.users.values());
  }

  public updateUser(updatedUser: DbUser) {
    this.users.set(updatedUser.id, updatedUser);
    this.saveUsers();
  }

  // Progress Methods
  public getUserProgress(userId: string): DbUserProgress {
    let p = this.progress.get(userId);
    if (!p) {
      p = {
        userId,
        solvedProblemIds: [],
        completedTopicIds: [],
        bookmarkedProblemIds: [],
        unlockedBadgeIds: [],
        notes: {},
      };
      this.progress.set(userId, p);
      this.saveProgress();
    }
    return p;
  }

  public recordProblemSolved(userId: string, problemId: string, xpEarned: number) {
    const prog = this.getUserProgress(userId);
    if (!prog.solvedProblemIds.includes(problemId)) {
      prog.solvedProblemIds.push(problemId);
      this.saveProgress();

      // Update user stats
      const user = this.users.get(userId);
      if (user) {
        user.problemsSolved += 1;
        user.xp += xpEarned;
        user.totalLearningMinutes += 15;
        const nextLevel = Math.floor(user.xp / 500) + 1;
        user.level = nextLevel;
        user.xpToNextLevel = nextLevel * 500;
        this.updateUser(user);
      }
    }
  }

  public saveSubmission(submission: Omit<DbSubmission, 'id' | 'submittedAt'>): DbSubmission {
    const fullSub: DbSubmission = {
      ...submission,
      id: `sub_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
      submittedAt: new Date().toISOString(),
    };
    this.submissions.unshift(fullSub);
    this.saveSubmissions();
    return fullSub;
  }

  public getSubmissionsForUser(userId: string): DbSubmission[] {
    return this.submissions.filter((s) => s.userId === userId);
  }
}

export const dbService = new DatabaseService();
