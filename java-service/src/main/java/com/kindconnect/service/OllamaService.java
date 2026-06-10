package com.kindconnect.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

@Service
public class OllamaService {

    @Value("${ollama.api.url}")
    private String ollamaApiUrl;

    @Value("${ollama.model}")
    private String ollamaModel;

    private final ObjectMapper objectMapper;

    public OllamaService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public String askOllama(String userMessage) {
        try {
            String prompt = """
                    You are KindConnect AI Agent.

                    KindConnect helps users with:
                    - food resources
                    - healthcare resources
                    - transportation help
                    - daily reminders
                    - mood check-ins
                    - friendly calls
                    - volunteer support
                    - tech help

                    Give a short, friendly, helpful answer.

                    User message:
                    %s
                    """.formatted(userMessage);

            Map<String, Object> body = Map.of(
                    "model", ollamaModel,
                    "prompt", prompt,
                    "stream", false);

            String requestBody = objectMapper.writeValueAsString(body);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(ollamaApiUrl))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                    .build();

            HttpClient client = HttpClient.newHttpClient();

            HttpResponse<String> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() < 200 || response.statusCode() >= 300) {
                return "Ollama error: " + response.body();
            }

            JsonNode root = objectMapper.readTree(response.body());
            return root.path("response").asText();

        } catch (Exception e) {
            return "Ollama is not running. Start Ollama first. Error: " + e.getMessage();
        }
    }
}
