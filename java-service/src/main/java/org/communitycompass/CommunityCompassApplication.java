package org.communitycompass;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point for the Community Compass Java service.
 *
 * <p>This service owns the civic-guidance side of the platform: the weekly
 * community newsfeed (adapted from FirstStep) and dashboard summary metrics
 * (kindConnect). It runs alongside the Python FastAPI service.
 */
@SpringBootApplication
public class CommunityCompassApplication {
    public static void main(String[] args) {
        SpringApplication.run(CommunityCompassApplication.class, args);
    }
}
