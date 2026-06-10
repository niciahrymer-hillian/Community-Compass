package com.kindconnect.dto;

public class AgentChatRequest {
    private Long userId;
    private String message;

    public Long getUserId() {
        return userId;
    }

    public String getMessage() {
        return message;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}