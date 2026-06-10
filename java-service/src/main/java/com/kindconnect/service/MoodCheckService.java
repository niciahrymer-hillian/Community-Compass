package com.kindconnect.service;

import com.kindconnect.model.MoodCheck;
import com.kindconnect.repository.MoodCheckRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MoodCheckService {

    private final MoodCheckRepository moodCheckRepository;

    public MoodCheckService(MoodCheckRepository moodCheckRepository) {
        this.moodCheckRepository = moodCheckRepository;
    }

    public List<MoodCheck> getAllMoodChecks() {
        return moodCheckRepository.findAll();
    }

    public List<MoodCheck> getMoodChecksByUser(Long userId) {
        return moodCheckRepository.findAll()
                .stream()
                .filter(moodCheck -> moodCheck.getUserId() != null
                        && moodCheck.getUserId().equals(userId))
                .toList();
    }

    public MoodCheck saveMoodCheck(MoodCheck moodCheck) {
        return moodCheckRepository.save(moodCheck);
    }

    public void deleteMoodCheck(Long id) {
        moodCheckRepository.deleteById(id);
    }
}