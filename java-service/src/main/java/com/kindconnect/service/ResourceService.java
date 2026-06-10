package com.kindconnect.service;

import com.kindconnect.model.Resource;
import com.kindconnect.repository.ResourceRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ResourceService {

    private final ResourceRepository resourceRepository;

    public ResourceService(ResourceRepository resourceRepository) {
        this.resourceRepository = resourceRepository;
    }

    public List<Resource> getAllResources() {
        return resourceRepository.findAll();
    }

    public List<Resource> getResourcesByCategory(String category) {
        return resourceRepository.findByCategoryIgnoreCase(category);
    }

    public Resource addResource(Resource resource) {
        return resourceRepository.save(resource);
    }
}