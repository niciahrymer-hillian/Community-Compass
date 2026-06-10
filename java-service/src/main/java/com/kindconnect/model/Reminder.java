package com.kindconnect.model;

import jakarta.persistence.*;

@Entity
public class Reminder {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long userId;

    private String title;
    private String type; // Medicine, Appointment, Water, Bill, Self-care
    private String date;
    private String time;
    private boolean completed;

    public Reminder() {
    }

    public Reminder(Long userId, String title, String type, String date, String time) {
        this.userId = userId;
        this.title = title;
        this.type = type;
        this.date = date;
        this.time = time;
        this.completed = false;
    }

    public Long getId() {
        return id;
    }

    public Long getUserId() {
        return userId;
    }

    public String getTitle() {
        return title;
    }

    public String getType() {
        return type;
    }

    public String getDate() {
        return date;
    }

    public String getTime() {
        return time;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }
}