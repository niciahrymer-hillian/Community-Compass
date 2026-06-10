package com.kindconnect.controller;

import com.kindconnect.model.Resource;
import com.kindconnect.service.ResourceService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import org.communitycompass.CommunityCompassApplication;

import java.util.List;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

// Full @SpringBootTest (not @WebMvcTest) because the app now wires JPA/H2; the
// ResourceService is still mocked so this stays a focused controller test.
// classes=… because the app entry point lives in org.communitycompass.
@SpringBootTest(classes = CommunityCompassApplication.class)
@AutoConfigureMockMvc
class ResourceControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ResourceService resourceService;

    @Test
    void getResourcesByCategory_returnsJsonResponse() throws Exception {
        Resource resource = new Resource("Local Food Bank", "Food", "Offers groceries", "Newark, DE", "302-000-0002");
        when(resourceService.getResourcesByCategory("Food")).thenReturn(List.of(resource));

        mockMvc.perform(get("/api/resources/category/Food"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Local Food Bank"))
                .andExpect(jsonPath("$[0].category").value("Food"));
    }
}
