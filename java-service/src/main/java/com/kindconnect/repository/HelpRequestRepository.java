package com.kindconnect.repository;

import com.kindconnect.model.HelpRequest;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface HelpRequestRepository extends JpaRepository<HelpRequest, Long> {

    List<HelpRequest> findByUserId(Long userId);

    List<HelpRequest> findByRequestTypeIgnoreCase(String requestType);

    List<HelpRequest> findByStatusIgnoreCase(String status);
}