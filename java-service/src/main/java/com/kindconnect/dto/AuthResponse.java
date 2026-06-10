package com.kindconnect.dto;

public class AuthResponse {

    private boolean success;
    private String message;
    private Long userId;
    private String name;
    private String email;
    private String userType;

    public AuthResponse() {
        this(false, null, null, null, null, null);
    }

    public AuthResponse(String message) {
        this(false, message, null, null, null, null);
    }

    public AuthResponse(boolean success, String message, Long userId, String name, String email, String userType) {
        this.success = success;
        this.message = message;
        this.userId = userId;
        this.name = name;
        this.email = email;
        this.userType = userType;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }

    public Long getUserId() {
        return userId;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public String getUserType() {
        return userType;
    }
}