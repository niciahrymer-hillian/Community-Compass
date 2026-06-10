package org.firststep.backend.service;

import java.util.Collections;
import java.util.List;

import org.firststep.backend.model.NewsItem;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class NewsService {

    private final ObjectMapper mapper = new ObjectMapper();

    private List<NewsItem> newsItems =
            Collections.emptyList();

    @EventListener(ApplicationReadyEvent.class)
    public void init() {

        try {

            // FirstStep read app/data/news.json from disk; in Community Compass we
            // load the same file from the classpath so it ships inside the jar.
            JsonNode root =
                    mapper.readTree(
                            new ClassPathResource("data/news.json").getInputStream());

            newsItems =
                    mapper.convertValue(
                            root.get("records"),
                            new TypeReference<List<NewsItem>>() {});

            System.out.println(
                    "Loaded news items ("
                    + newsItems.size()
                    + " records)");

        } catch (Exception e) {

            System.err.println(
                    "Failed to load news.json: "
                    + e.getMessage());
        }
    }

    public List<NewsItem> getAll() {
        return newsItems;
    }
}
