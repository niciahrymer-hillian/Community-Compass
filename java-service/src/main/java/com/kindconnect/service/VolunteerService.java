package com.kindconnect.service;

import com.kindconnect.model.Volunteer;
import com.kindconnect.repository.VolunteerRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class VolunteerService {

    private final VolunteerRepository volunteerRepository;

    public VolunteerService(VolunteerRepository volunteerRepository) {
        this.volunteerRepository = volunteerRepository;
    }

    public List<Volunteer> getAllVolunteers() {
        return volunteerRepository.findAll();
    }

    public Volunteer createVolunteer(Volunteer volunteer) {
        if (volunteer.getAvailable() == null) {
            volunteer.setAvailable(true);
        }

        return volunteerRepository.save(volunteer);
    }

    public List<Volunteer> getAvailableVolunteers() {
        return volunteerRepository.findByAvailableTrue();
    }

    public List<Volunteer> getAvailableVolunteersBySkill(String skillType) {
        return volunteerRepository.findBySkillTypeIgnoreCaseAndAvailableTrue(skillType);
    }
}