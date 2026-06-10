package com.kindconnect.controller;

import com.kindconnect.model.Reminder;
import com.kindconnect.service.ReminderService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reminders")
@CrossOrigin(origins = "*")
public class ReminderController {

    private final ReminderService reminderService;

    public ReminderController(ReminderService reminderService) {
        this.reminderService = reminderService;
    }

    @GetMapping
    public List<Reminder> getAllReminders() {
        return reminderService.getAllReminders();
    }

    @GetMapping("/user/{userId}")
    public List<Reminder> getRemindersByUser(@PathVariable("userId") Long userId) {
        return reminderService.getRemindersByUser(userId);
    }

    @PostMapping
    public Reminder addReminder(@RequestBody Reminder reminder) {
        return reminderService.addReminder(reminder);
    }

    @PutMapping("/{id}/complete")
    public Reminder markComplete(@PathVariable("id") Long id) {
        return reminderService.markComplete(id);
    }

    @DeleteMapping("/{id}")
    public void deleteReminder(@PathVariable("id") Long id) {
        reminderService.deleteReminder(id);
    }
}