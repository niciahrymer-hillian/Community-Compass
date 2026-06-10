package org.communitycompass.service;

import java.util.List;
import java.util.Optional;

import org.communitycompass.model.NewsItem;
import org.springframework.stereotype.Service;

/**
 * Serves weekly community updates (CC-15). FirstStep loaded these from a
 * news.json file; for the MVP we seed a synthetic Delaware set in-memory so the
 * service is self-contained and demoable. Swap in a DB or RSS pull later.
 */
@Service
public class NewsService {

    private final List<NewsItem> items = List.of(
            new NewsItem("n1",
                    "Delaware opens Section 8 waitlist for 2 weeks",
                    "DSHA is accepting Housing Choice Voucher applications through the end of the month.",
                    "housing", "high", "2026-06-08", "2026-06-22",
                    "Delaware State Housing Authority",
                    "If you need rental help, apply now — the waitlist usually closes fast."),
            new NewsItem("n2",
                    "Summer SNAP benefits for families with kids",
                    "Eligible families receive extra food benefits over the summer months.",
                    "food", "medium", "2026-06-05", "2026-08-31",
                    "Delaware Health & Social Services",
                    "Extra grocery money is available if you have school-age children at home."),
            new NewsItem("n3",
                    "Free job-training cohort starts in July",
                    "Delaware JobLink is enrolling for a paid workforce-readiness program.",
                    "employment", "medium", "2026-06-03", "2026-06-28",
                    "Delaware JobLink",
                    "You can get paid while learning skills that lead to steady work."),
            new NewsItem("n4",
                    "Mobile health clinic schedule for June",
                    "Westside Family Healthcare's mobile clinic adds new neighborhood stops.",
                    "health", "low", "2026-06-01", null,
                    "Westside Family Healthcare",
                    "Low-cost checkups are coming closer to where you live this month."),
            new NewsItem("n5",
                    "Utility shut-off protection ends soon",
                    "The seasonal moratorium on electricity disconnections is ending.",
                    "benefits", "high", "2026-06-07", "2026-06-15",
                    "Delaware Public Service Commission",
                    "Set up a payment plan now to avoid losing power once protections lift."),
            new NewsItem("n6",
                    "Free GED testing vouchers available",
                    "Delaware Adult Education is covering GED test fees for new enrollees.",
                    "education", "low", "2026-05-30", "2026-07-31",
                    "Delaware Adult Education",
                    "You can finish your GED without paying the usual test fees.")
    );

    public List<NewsItem> getAll() {
        return items;
    }

    public List<NewsItem> getByCategory(String category) {
        return items.stream()
                .filter(n -> n.category().equalsIgnoreCase(category))
                .toList();
    }

    public Optional<NewsItem> getById(String id) {
        return items.stream().filter(n -> n.id().equals(id)).findFirst();
    }

    public long urgentCount() {
        return items.stream().filter(n -> "high".equalsIgnoreCase(n.urgency())).count();
    }

    public List<String> categories() {
        return items.stream().map(NewsItem::category).distinct().sorted().toList();
    }
}
