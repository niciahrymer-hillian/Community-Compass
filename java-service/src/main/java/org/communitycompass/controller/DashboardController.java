package org.communitycompass.controller;

import java.util.Map;

import org.communitycompass.service.NewsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Dashboard summary (kindConnect pattern). For the MVP this surfaces civic-guidance
 * metrics the Java service owns (newsfeed). Resident/risk metrics live in the
 * Python service; a later iteration can aggregate across both.
 */
@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    private final NewsService news;

    public DashboardController(NewsService news) {
        this.news = news;
    }

    @GetMapping("/summary")
    public Map<String, Object> summary() {
        return Map.of(
                "totalUpdates", news.getAll().size(),
                "urgentUpdates", news.urgentCount(),
                "categories", news.categories()
        );
    }
}
