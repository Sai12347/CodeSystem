package com.codesystem.model;

import jakarta.persistence.*;

@Entity
@Table(name = "user_profiles")
public class UserProfile {
    @Id
    private Long userId;

    private String name;
    private String avatarUrl;
    private int level = 1;
    private int xp = 0;
    private int streakDays = 0;
    private int problemsSolved = 0;
    private int totalLearningMinutes = 0;

    public UserProfile() {}

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getAvatarUrl() { return avatarUrl; }
    public void setAvatarUrl(String avatarUrl) { this.avatarUrl = avatarUrl; }
    public int getLevel() { return level; }
    public void setLevel(int level) { this.level = level; }
    public int getXp() { return xp; }
    public void setXp(int xp) { this.xp = xp; }
    public int getStreakDays() { return streakDays; }
    public void setStreakDays(int streakDays) { this.streakDays = streakDays; }
    public int getProblemsSolved() { return problemsSolved; }
    public void setProblemsSolved(int problemsSolved) { this.problemsSolved = problemsSolved; }
    public int getTotalLearningMinutes() { return totalLearningMinutes; }
    public void setTotalLearningMinutes(int totalLearningMinutes) { this.totalLearningMinutes = totalLearningMinutes; }
}
