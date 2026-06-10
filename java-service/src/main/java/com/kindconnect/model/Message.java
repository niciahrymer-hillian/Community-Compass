package com.kindconnect.model;

import jakarta.persistence.*;

@Entity
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long userId;
    private String title;

    @Column(length = 1000)
    private String content;

    private String type;
    private Boolean readMessage = false;

    public Message() {
    }

    public Message(Long userId, String title, String content, String type, Boolean readMessage) {
        this.userId = userId;
        this.title = title;
        this.content = content;
        this.type = type;
        this.readMessage = readMessage;
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

    public String getContent() {
        return content;
    }

    public String getType() {
        return type;
    }

    public Boolean getReadMessage() {
        return readMessage;
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

    public void setContent(String content) {
        this.content = content;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setReadMessage(Boolean readMessage) {
        this.readMessage = readMessage;
    }
}