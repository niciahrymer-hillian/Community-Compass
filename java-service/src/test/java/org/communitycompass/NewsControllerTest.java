package org.communitycompass;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Verifies FirstStep's newsfeed (org.firststep.backend) is wired into the app and
 * loads news.json, plus our dashboard summary. Full @SpringBootTest so the
 * NewsService @EventListener(ApplicationReadyEvent) fires and loads the data.
 */
@SpringBootTest
@AutoConfigureMockMvc
class NewsControllerTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void listsFirstStepNews() throws Exception {
        mvc.perform(get("/api/news"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(8))
                .andExpect(jsonPath("$[0].headline").exists())
                .andExpect(jsonPath("$[0].why_it_matters").exists());
    }

    @Test
    void dashboardSummaryHasMetrics() throws Exception {
        mvc.perform(get("/api/dashboard/summary"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalUpdates").value(8))
                .andExpect(jsonPath("$.urgentUpdates").exists());
    }
}
