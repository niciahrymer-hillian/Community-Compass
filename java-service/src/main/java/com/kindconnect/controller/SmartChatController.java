package com.kindconnect.controller;

import com.kindconnect.dto.ChatRequest;
import com.kindconnect.model.SmartChatMessage;
import com.kindconnect.service.SmartChatService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*")
public class SmartChatController {

    private final SmartChatService smartChatService;

    public SmartChatController(SmartChatService smartChatService) {
        this.smartChatService = smartChatService;
    }

    @PostMapping
    public SmartChatMessage sendMessage(@RequestBody ChatRequest request) {
        return smartChatService.sendMessage(request);
    }

    @GetMapping
    public List<SmartChatMessage> getAllMessages() {
        return smartChatService.getAllMessages();
    }

    @GetMapping("/user/{userId}")
    public List<SmartChatMessage> getMessagesByUser(@PathVariable("userId") Long userId) {
        return smartChatService.getMessagesByUser(userId);
    }
}