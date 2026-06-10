package com.kindconnect.repository;

import com.kindconnect.model.SmartChatMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SmartChatRepository extends JpaRepository<SmartChatMessage, Long> {
}