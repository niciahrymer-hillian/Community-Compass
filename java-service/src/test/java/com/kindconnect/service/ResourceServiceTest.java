package com.kindconnect.service;

import com.kindconnect.model.Resource;
import com.kindconnect.repository.ResourceRepository;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class ResourceServiceTest {

    private final ResourceRepository resourceRepository = Mockito.mock(ResourceRepository.class);
    private final ResourceService resourceService = new ResourceService(resourceRepository);

    @Test
    void getAllResources_returnsAllResources() {
        List<Resource> resources = List.of(
                new Resource("Community Food Center", "Food", "Provides food", "Wilmington, DE", "302-000-0001"));

        Mockito.when(resourceRepository.findAll()).thenReturn(resources);

        assertThat(resourceService.getAllResources()).isSameAs(resources);
        Mockito.verify(resourceRepository).findAll();
    }

    @Test
    void getResourcesByCategory_usesRepositoryIgnoreCase() {
        Resource food = new Resource("Local Food Bank", "Food", "Offers groceries", "Newark, DE", "302-000-0002");

        Mockito.when(resourceRepository.findByCategoryIgnoreCase("Food")).thenReturn(List.of(food));

        assertThat(resourceService.getResourcesByCategory("Food")).containsExactly(food);
        Mockito.verify(resourceRepository).findByCategoryIgnoreCase("Food");
    }

    @Test
    void addResource_savesAndReturnsResource() {
        Resource resource = new Resource("Community Food Center", "Food", "Provides food", "Wilmington, DE",
                "302-000-0001");

        Mockito.when(resourceRepository.save(resource)).thenReturn(resource);

        assertThat(resourceService.addResource(resource)).isSameAs(resource);
        Mockito.verify(resourceRepository).save(resource);
    }
}
