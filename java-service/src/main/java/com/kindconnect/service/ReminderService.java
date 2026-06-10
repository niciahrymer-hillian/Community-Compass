package com.kindconnect.service;

import com.kindconnect.model.Reminder;
import com.kindconnect.repository.ReminderRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ReminderService {

    private final ReminderRepository reminderRepository;

    public ReminderService(ReminderRepository reminderRepository) {
        this.reminderRepository = reminderRepository;
    }

    public List<Reminder> getAllReminders() {
        return reminderRepository.findAll();
    }

    public List<Reminder> getRemindersByUser(Long userId) {
        return reminderRepository.findByUserId(userId);
    }

    public Reminder addReminder(Reminder reminder) {
        reminder.setCompleted(false);
        return reminderRepository.save(reminder);
    }

    @Transactional
    public Reminder markComplete(Long id) {
        Reminder reminder = reminderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Reminder not found"));

        reminder.setCompleted(true);
        return reminderRepository.save(reminder);
    }

    public void deleteReminder(Long id) {
        reminderRepository.deleteById(id);
    }
}