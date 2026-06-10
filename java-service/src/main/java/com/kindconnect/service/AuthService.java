package com.kindconnect.service;

import com.kindconnect.dto.AuthResponse;
import com.kindconnect.dto.LoginRequest;
import com.kindconnect.dto.RegisterRequest;
import com.kindconnect.model.User;
import com.kindconnect.repository.UserRepository;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            return new AuthResponse(
                    false,
                    "Email already exists",
                    null,
                    null,
                    null,
                    null);
        }

        String encodedPassword = passwordEncoder.encode(request.getPassword());

        User user = new User(
                request.getName(),
                request.getEmail(),
                encodedPassword,
                request.getUserType());

        User savedUser = userRepository.save(user);

        return new AuthResponse(
                true,
                "Registration successful",
                savedUser.getId(),
                savedUser.getName(),
                savedUser.getEmail(),
                savedUser.getUserType());
    }

    public AuthResponse login(LoginRequest request) {
        return userRepository.findByEmail(request.getEmail())
                .map(user -> {
                    if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
                        return new AuthResponse(false, "Invalid credentials", null, null, null, null);
                    }
                    return new AuthResponse(true, "Login successful", user.getId(), user.getName(), user.getEmail(),
                            user.getUserType());
                })
                .orElseGet(() -> new AuthResponse(false, "Invalid credentials", null, null, null, null));
    }
}
