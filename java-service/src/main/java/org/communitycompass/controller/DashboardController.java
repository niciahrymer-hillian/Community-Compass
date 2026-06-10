package org.communitycompass.controller;

import java.util.Map;
import java.util.stream.Stream;

import org.firststep.backend.model.NewsItem;
import org.firststep.backend.service.NewsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Dashboard summary (kindConnect pattern). Surfaces civic-guidance metrics from
 * the newsfeed, which is now FirstStep's actual NewsService. Resident/risk
 * metrics live in the Python service; a later iteration can aggregate both.
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
        var items = news.getAll();
        long urgent = items.stream()
                .filter(n -> "high".equalsIgnoreCase(n.urgency))
                .count();
        var categories = items.stream()
                .flatMap(n -> n.categoryTags == null ? Stream.empty() : n.categoryTags.stream())
                .distinct()
                .sorted()
                .toList();
        return Map.of(
                "totalUpdates", items.size(),
                "urgentUpdates", urgent,
                "categories", categories
        );
    }
}
