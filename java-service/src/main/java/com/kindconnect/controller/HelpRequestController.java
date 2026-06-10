package com.kindconnect.controller;

import com.kindconnect.model.HelpRequest;
import com.kindconnect.service.HelpRequestService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/help-requests")
@CrossOrigin(origins = "*")
public class HelpRequestController {

    private final HelpRequestService helpRequestService;

    public HelpRequestController(HelpRequestService helpRequestService) {
        this.helpRequestService = helpRequestService;
    }

    @GetMapping
    public List<HelpRequest> getAllHelpRequests() {
        return helpRequestService.getAllHelpRequests();
    }

    @PostMapping
    public HelpRequest createHelpRequest(@RequestBody HelpRequest helpRequest) {
        return helpRequestService.createHelpRequest(helpRequest);
    }

    @GetMapping("/user/{userId}")
    public List<HelpRequest> getHelpRequestsByUser(@PathVariable Long userId) {
        return helpRequestService.getHelpRequestsByUser(userId);
    }

    @GetMapping("/type/{requestType}")
    public List<HelpRequest> getHelpRequestsByType(@PathVariable String requestType) {
        return helpRequestService.getHelpRequestsByType(requestType);
    }

    @GetMapping("/open")
    public List<HelpRequest> getOpenHelpRequests() {
        return helpRequestService.getOpenHelpRequests();
    }

    @PutMapping("/{requestId}/assign/{volunteerId}")
    public HelpRequest assignVolunteer(
            @PathVariable Long requestId,
            @PathVariable Long volunteerId) {
        return helpRequestService.assignVolunteer(requestId, volunteerId);
    }

    @PutMapping("/{requestId}/complete")
    public HelpRequest completeHelpRequest(@PathVariable Long requestId) {
        return helpRequestService.completeHelpRequest(requestId);
    }
}