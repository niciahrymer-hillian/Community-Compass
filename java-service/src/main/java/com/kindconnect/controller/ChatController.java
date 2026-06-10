package com.kindconnect.controller;

import com.kindconnect.dto.AgentChatRequest;
import com.kindconnect.dto.AgentChatResponse;
import com.kindconnect.service.OllamaService;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = "*")
public class ChatController {

    private final OllamaService ollamaService;

    public ChatController(OllamaService ollamaService) {
        this.ollamaService = ollamaService;
    }

    @PostMapping("/chat")
    public AgentChatResponse chat(@RequestBody AgentChatRequest request) {
        String reply = ollamaService.askOllama(request.getMessage());
        return new AgentChatResponse(reply);
    }
}