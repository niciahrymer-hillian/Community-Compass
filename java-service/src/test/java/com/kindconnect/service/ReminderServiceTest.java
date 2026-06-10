package com.kindconnect.service;

import com.kindconnect.model.Reminder;
import com.kindconnect.repository.ReminderRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

class ReminderServiceTest {

    private ReminderRepository reminderRepository;
    private ReminderService reminderService;

    @BeforeEach
    void setUp() {
        reminderRepository = mock(ReminderRepository.class);
        reminderService = new ReminderService(reminderRepository);
    }

    @Test
    void getAllRemindersDelegatesToRepository() {
        reminderService.getAllReminders();

        verify(reminderRepository).findAll();
    }

    @Test
    void getRemindersByUserUsesRepositoryQuery() {
        Long userId = 42L;
        Reminder expected = new Reminder(userId, "Take medicine", "Medicine", "2026-06-03", "09:00");
        when(reminderRepository.findByUserId(userId)).thenReturn(List.of(expected));

        List<Reminder> results = reminderService.getRemindersByUser(userId);

        assertThat(results).containsExactly(expected);
        verify(reminderRepository).findByUserId(userId);
    }

    @Test
    void addReminderMarksReminderAsIncompleteBeforeSave() {
        Reminder reminder = new Reminder(1L, "Drink water", "Water", "2026-06-03", "10:00");
        when(reminderRepository.save(any(Reminder.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Reminder saved = reminderService.addReminder(reminder);

        assertThat(saved.isCompleted()).isFalse();
        verify(reminderRepository).save(saved);
    }

    @Test
    void markCompleteUpdatesStatusAndSavesReminder() {
        Long id = 123L;
        Reminder reminder = new Reminder(1L, "Pay bill", "Bill", "2026-06-03", "11:00");
        reminder.setId(id);
        when(reminderRepository.findById(id)).thenReturn(Optional.of(reminder));
        when(reminderRepository.save(any(Reminder.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Reminder result = reminderService.markComplete(id);

        assertThat(result.isCompleted()).isTrue();
        verify(reminderRepository).findById(id);
        verify(reminderRepository).save(reminder);
    }

    @Test
    void markCompleteThrowsWhenReminderMissing() {
        Long id = 999L;
        when(reminderRepository.findById(id)).thenReturn(Optional.empty());

        assertThrows(RuntimeException.class, () -> reminderService.markComplete(id));
    }
}
