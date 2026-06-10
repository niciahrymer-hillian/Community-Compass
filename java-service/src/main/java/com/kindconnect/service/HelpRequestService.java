package com.kindconnect.service;

import com.kindconnect.model.HelpRequest;
import com.kindconnect.repository.HelpRequestRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HelpRequestService {

    private final HelpRequestRepository helpRequestRepository;

    public HelpRequestService(HelpRequestRepository helpRequestRepository) {
        this.helpRequestRepository = helpRequestRepository;
    }

    public List<HelpRequest> getAllHelpRequests() {
        return helpRequestRepository.findAll();
    }

    public HelpRequest createHelpRequest(HelpRequest helpRequest) {
        if (helpRequest.getStatus() == null || helpRequest.getStatus().isBlank()) {
            helpRequest.setStatus("OPEN");
        }

        return helpRequestRepository.save(helpRequest);
    }

    public List<HelpRequest> getHelpRequestsByUser(Long userId) {
        return helpRequestRepository.findByUserId(userId);
    }

    public List<HelpRequest> getHelpRequestsByType(String requestType) {
        return helpRequestRepository.findByRequestTypeIgnoreCase(requestType);
    }

    public List<HelpRequest> getOpenHelpRequests() {
        return helpRequestRepository.findByStatusIgnoreCase("OPEN");
    }

    public HelpRequest assignVolunteer(Long requestId, Long volunteerId) {
        HelpRequest helpRequest = helpRequestRepository.findById(requestId)
                .orElseThrow(() -> new RuntimeException("Help request not found"));

        helpRequest.setVolunteerId(volunteerId);
        helpRequest.setStatus("ASSIGNED");

        return helpRequestRepository.save(helpRequest);
    }

    public HelpRequest completeHelpRequest(Long requestId) {
        HelpRequest helpRequest = helpRequestRepository.findById(requestId)
                .orElseThrow(() -> new RuntimeException("Help request not found"));

        helpRequest.setStatus("COMPLETED");

        return helpRequestRepository.save(helpRequest);
    }
}