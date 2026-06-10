package com.kindconnect.model;

import jakarta.persistence.*;

@Entity
public class SmartChatMessage {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long userId;

    @Column(length = 1000)
    private String userMessage;

    @Column(length = 1000)
    private String botResponse;

    private String category;
    private String suggestedAction;
    private String createdAt;

    public SmartChatMessage() {
    }

    public SmartChatMessage(Long userId, String userMessage, String botResponse,
            String category, String suggestedAction, String createdAt) {
        this.userId = userId;
        this.userMessage = userMessage;
        this.botResponse = botResponse;
        this.category = category;
        this.suggestedAction = suggestedAction;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public Long getUserId() {
        return userId;
    }

    public String getUserMessage() {
        return userMessage;
    }

    public String getBotResponse() {
        return botResponse;
    }

    public String getCategory() {
        return category;
    }

    public String getSuggestedAction() {
        return suggestedAction;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setUserMessage(String userMessage) {
        this.userMessage = userMessage;
    }

    public void setBotResponse(String botResponse) {
        this.botResponse = botResponse;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public void setSuggestedAction(String suggestedAction) {
        this.suggestedAction = suggestedAction;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }
}