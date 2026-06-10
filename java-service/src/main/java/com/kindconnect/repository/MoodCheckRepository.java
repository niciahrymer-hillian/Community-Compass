package com.kindconnect.repository;

import com.kindconnect.model.MoodCheck;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MoodCheckRepository extends JpaRepository<MoodCheck, Long> {
}
