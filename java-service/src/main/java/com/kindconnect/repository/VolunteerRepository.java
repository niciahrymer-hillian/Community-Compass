package com.kindconnect.repository;

import com.kindconnect.model.Volunteer;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface VolunteerRepository extends JpaRepository<Volunteer, Long> {

    List<Volunteer> findByAvailableTrue();

    List<Volunteer> findBySkillTypeIgnoreCaseAndAvailableTrue(String skillType);
}