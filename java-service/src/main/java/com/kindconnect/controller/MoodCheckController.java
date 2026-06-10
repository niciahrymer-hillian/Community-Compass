package com.kindconnect.controller;

import com.kindconnect.model.MoodCheck;
import com.kindconnect.service.MoodCheckService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/moods")
@CrossOrigin(origins = "*")
public class MoodCheckController {

    private final MoodCheckService moodCheckService;

    public MoodCheckController(MoodCheckService moodCheckService) {
        this.moodCheckService = moodCheckService;
    }

    @GetMapping
    public List<MoodCheck> getAllMoodChecks() {
        return moodCheckService.getAllMoodChecks();
    }

    @GetMapping("/user/{userId}")
    public List<MoodCheck> getMoodChecksByUser(@PathVariable("userId") Long userId) {
        return moodCheckService.getMoodChecksByUser(userId);
    }

    @PostMapping
    public MoodCheck saveMoodCheck(@RequestBody MoodCheck moodCheck) {
        return moodCheckService.saveMoodCheck(moodCheck);
    }

    @DeleteMapping("/{id}")
    public void deleteMoodCheck(@PathVariable("id") Long id) {
        moodCheckService.deleteMoodCheck(id);
    }
}