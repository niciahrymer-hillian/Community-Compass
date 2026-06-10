package com.kindconnect.model;

import jakarta.persistence.*;

@Entity
public class MoodCheck {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long userId;

    private String mood; // Happy, Sad, Lonely, Stressed, Tired

    @Column(length = 1000)
    private String note;

    private String date;

    public MoodCheck() {
    }

    public MoodCheck(Long userId, String mood, String note, String date) {
        this.userId = userId;
        this.mood = mood;
        this.note = note;
        this.date = date;
    }

    public Long getId() {
        return id;
    }

    public Long getUserId() {
        return userId;
    }

    public String getMood() {
        return mood;
    }

    public String getNote() {
        return note;
    }

    public String getDate() {
        return date;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setMood(String mood) {
        this.mood = mood;
    }

    public void setNote(String note) {
        this.note = note;
    }

    public void setDate(String date) {
        this.date = date;
    }
}
