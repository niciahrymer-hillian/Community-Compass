package org.communitycompass;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point for the Community Compass Java service.
 *
 * <p>This service owns the civic-guidance side of the platform: the weekly
 * community newsfeed (FirstStep's actual {@code org.firststep.backend} code) and
 * dashboard summary metrics (kindConnect). It runs alongside the Python FastAPI
 * service.
 *
 * <p>scanBasePackages includes {@code org.firststep} so the FirstStep teammates'
 * controllers/services are component-scanned unchanged from their own package.
 */
@SpringBootApplication(scanBasePackages = {"org.communitycompass", "org.firststep"})
public class CommunityCompassApplication {
    public static void main(String[] args) {
        SpringApplication.run(CommunityCompassApplication.class, args);
    }
}
