package com.kindconnect.model;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Table(name = "help_request")
public class HelpRequest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long userId;

    private String requestType;

    private String title;

    @Column(length = 1000)
    private String description;

    private String status;

    private LocalDate date;

    private LocalTime time;

    private Long volunteerId;

    public HelpRequest() {
    }

    public HelpRequest(Long userId, String requestType, String title, String description, String status, LocalDate date,
            LocalTime time, Long volunteerId) {
        this.userId = userId;
        this.requestType = requestType;
        this.title = title;
        this.description = description;
        this.status = status;
        this.date = date;
        this.time = time;
        this.volunteerId = volunteerId;
    }

    public Long getId() {
        return id;
    }

    public Long getUserId() {
        return userId;
    }

    public String getRequestType() {
        return requestType;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getStatus() {
        return status;
    }

    public LocalDate getDate() {
        return date;
    }

    public LocalTime getTime() {
        return time;
    }

    public Long getVolunteerId() {
        return volunteerId;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setRequestType(String requestType) {
        this.requestType = requestType;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public void setTime(LocalTime time) {
        this.time = time;
    }

    public void setVolunteerId(Long volunteerId) {
        this.volunteerId = volunteerId;
    }
}
