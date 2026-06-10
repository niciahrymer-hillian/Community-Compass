package org.communitycompass;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

import org.communitycompass.controller.DashboardController;
import org.communitycompass.controller.NewsController;
import org.communitycompass.service.NewsService;
import org.springframework.context.annotation.Import;

/** Controller tests (CC-15). NewsService is real (in-memory), no DB needed. */
@WebMvcTest({NewsController.class, DashboardController.class})
@Import(NewsService.class)
class NewsControllerTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void listsAllNews() throws Exception {
        mvc.perform(get("/api/news"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(6))
                .andExpect(jsonPath("$[0].whyItMatters").exists());
    }

    @Test
    void filtersByCategory() throws Exception {
        mvc.perform(get("/api/news").param("category", "housing"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].category").value("housing"));
    }

    @Test
    void unknownIdReturns404() throws Exception {
        mvc.perform(get("/api/news/does-not-exist"))
                .andExpect(status().isNotFound());
    }

    @Test
    void dashboardSummaryHasMetrics() throws Exception {
        mvc.perform(get("/api/dashboard/summary"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalUpdates").value(6))
                .andExpect(jsonPath("$.urgentUpdates").exists());
    }
}
