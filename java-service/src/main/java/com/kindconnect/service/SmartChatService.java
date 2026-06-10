package com.kindconnect.service;

import com.kindconnect.dto.ChatRequest;
import com.kindconnect.model.SmartChatMessage;
import com.kindconnect.repository.SmartChatRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class SmartChatService {

    private final SmartChatRepository smartChatRepository;

    public SmartChatService(SmartChatRepository smartChatRepository) {
        this.smartChatRepository = smartChatRepository;
    }

    public SmartChatMessage sendMessage(ChatRequest request) {
        String userMessage = request.getMessage();

        String category = chooseCategory(userMessage);
        String action = suggestAction(category);
        String response = generateResponse(category);

        SmartChatMessage chatMessage = new SmartChatMessage(
                request.getUserId(),
                userMessage,
                response,
                category,
                action,
                LocalDateTime.now().toString());

        return smartChatRepository.save(chatMessage);
    }

    public List<SmartChatMessage> getAllMessages() {
        return smartChatRepository.findAll();
    }

    public List<SmartChatMessage> getMessagesByUser(Long userId) {
        return smartChatRepository.findAll()
                .stream()
                .filter(message -> message.getUserId() != null
                        && message.getUserId().equals(userId))
                .toList();
    }

    private String chooseCategory(String message) {
        if (message == null) {
            return "GENERAL";
        }

        String lower = message.toLowerCase();

        if (lower.contains("food") || lower.contains("grocery")) {
            return "GROCERY_HELP";
        }

        if (lower.contains("ride") || lower.contains("transport")) {
            return "RIDE_HELP";
        }

        if (lower.contains("tech") || lower.contains("computer") || lower.contains("phone")) {
            return "TECH_HELP";
        }

        if (lower.contains("lonely") || lower.contains("talk") || lower.contains("call")) {
            return "FRIENDLY_CALL";
        }

        if (lower.contains("medicine") || lower.contains("appointment") || lower.contains("water")) {
            return "REMINDER";
        }

        if (lower.contains("sad") || lower.contains("stress") || lower.contains("mood")) {
            return "MOOD_CHECK";
        }

        return "GENERAL";
    }

    private String suggestAction(String category) {
        return switch (category) {
            case "GROCERY_HELP" -> "CREATE_GROCERY_HELP_REQUEST";
            case "RIDE_HELP" -> "CREATE_RIDE_HELP_REQUEST";
            case "TECH_HELP" -> "CREATE_TECH_HELP_REQUEST";
            case "FRIENDLY_CALL" -> "CREATE_FRIENDLY_CALL_REQUEST";
            case "REMINDER" -> "CREATE_REMINDER";
            case "MOOD_CHECK" -> "SAVE_MOOD_CHECK";
            default -> "VIEW_DASHBOARD";
        };
    }

    private String generateResponse(String category) {
        return switch (category) {
            case "GROCERY_HELP" -> "It sounds like you need grocery help. You can create a grocery help request.";
            case "RIDE_HELP" -> "It sounds like you need a ride. You can create a ride help request.";
            case "TECH_HELP" -> "It sounds like you need tech help. You can create a tech help request.";
            case "FRIENDLY_CALL" ->
                "It sounds like you may want someone to talk to. You can create a friendly call request.";
            case "REMINDER" ->
                "It sounds like you need a reminder. You can create a reminder for medicine, appointments, water, bills, or self-care.";
            case "MOOD_CHECK" ->
                "I am sorry you feel this way. You can save a mood check-in so the app can track how you feel.";
            default ->
                "I can help guide you to resources, reminders, mood check-ins, help requests, or volunteer support.";
        };
    }
}