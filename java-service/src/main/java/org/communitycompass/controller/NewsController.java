package org.communitycompass.controller;

import java.util.List;

import org.communitycompass.model.NewsItem;
import org.communitycompass.service.NewsService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** Weekly community updates / newsfeed (CC-15). Adapted from FirstStep. */
@RestController
@RequestMapping("/api/news")
public class NewsController {

    private final NewsService service;

    public NewsController(NewsService service) {
        this.service = service;
    }

    /** All updates, or just one category when {@code ?category=} is supplied. */
    @GetMapping
    public List<NewsItem> list(@RequestParam(required = false) String category) {
        return category == null ? service.getAll() : service.getByCategory(category);
    }

    @GetMapping("/{id}")
    public ResponseEntity<NewsItem> getOne(@PathVariable String id) {
        return service.getById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
