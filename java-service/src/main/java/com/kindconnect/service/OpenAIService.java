package com.kindconnect.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

@Service
public class OpenAIService {

    private final ObjectMapper objectMapper;

    public OpenAIService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public String askOpenAI(String userMessage) {
        String apiKey = System.getenv("OPENAI_API_KEY");

        if (apiKey == null || apiKey.isBlank()) {
            return "OpenAI API key is missing. Please set OPENAI_API_KEY in your terminal.";
        }

        try {
            String prompt = """
                    You are KindConnect Assistant.

                    KindConnect helps users with:
                    - food resources
                    - healthcare resources
                    - transportation help
                    - daily reminders
                    - mood check-ins
                    - friendly calls
                    - tech help
                    - volunteer support

                    Keep your answer simple, friendly, and helpful.
                    Do not make the answer too long.

                    User message:
                    %s
                    """.formatted(userMessage);

            Map<String, Object> body = Map.of(
                    "model", "gpt-4.1-mini",
                    "input", prompt);

            String requestBody = objectMapper.writeValueAsString(body);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.openai.com/v1/responses"))
                    .header("Content-Type", "application/json")
                    .header("Authorization", "Bearer " + apiKey)
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                    .build();

            HttpClient client = HttpClient.newHttpClient();

            HttpResponse<String> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() < 200 || response.statusCode() >= 300) {
                return "OpenAI error: " + response.body();
            }

            JsonNode root = objectMapper.readTree(response.body());

            String outputText = root.path("output_text").asText();

            if (outputText != null && !outputText.isBlank()) {
                return outputText;
            }

            return "OpenAI replied, but I could not read the response text.";

        } catch (Exception e) {
            return "OpenAI error: " + e.getMessage();
        }
    }
}