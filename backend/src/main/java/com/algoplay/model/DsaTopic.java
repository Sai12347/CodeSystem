package com.algoplay.model;

import jakarta.persistence.*;

@Entity
@Table(name = "dsa_topics")
public class DsaTopic {
    @Id
    @Column(length = 64)
    private String id;

    @Column(nullable = false, length = 128)
    private String title;

    @Column(nullable = false, length = 32)
    private String category; // BEGINNER, INTERMEDIATE, ADVANCED

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(columnDefinition = "TEXT")
    private String realWorldExample;

    private String timeComplexityBest;
    private String timeComplexityAverage;
    private String timeComplexityWorst;
    private String spaceComplexity;

    public DsaTopic() {}

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getRealWorldExample() { return realWorldExample; }
    public void setRealWorldExample(String realWorldExample) { this.realWorldExample = realWorldExample; }
    public String getTimeComplexityBest() { return timeComplexityBest; }
    public void setTimeComplexityBest(String best) { this.timeComplexityBest = best; }
    public String getTimeComplexityAverage() { return timeComplexityAverage; }
    public void setTimeComplexityAverage(String avg) { this.timeComplexityAverage = avg; }
    public String getTimeComplexityWorst() { return timeComplexityWorst; }
    public void setTimeComplexityWorst(String worst) { this.timeComplexityWorst = worst; }
    public String getSpaceComplexity() { return spaceComplexity; }
    public void setSpaceComplexity(String space) { this.spaceComplexity = space; }
}
