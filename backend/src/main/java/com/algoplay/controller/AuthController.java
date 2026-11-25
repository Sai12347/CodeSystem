package com.algoplay.controller;

import com.algoplay.model.User;
import com.algoplay.model.UserProfile;
import com.algoplay.repository.UserProfileRepository;
import com.algoplay.repository.UserRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserRepository userRepository;
    private final UserProfileRepository userProfileRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthController(UserRepository userRepository, UserProfileRepository userProfileRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.userProfileRepository = userProfileRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public record RegisterRequest(String username, String email, String password, String name) {}
    public record LoginRequest(String username, String password) {}

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest request) {
        if (userRepository.existsByUsername(request.username())) {
            return ResponseEntity.badRequest().body(Map.of("error", "Username already taken"));
        }
        if (userRepository.existsByEmail(request.email())) {
            return ResponseEntity.badRequest().body(Map.of("error", "Email already in use"));
        }

        User user = new User();
        user.setUsername(request.username());
        user.setEmail(request.email());
        user.setPasswordHash(passwordEncoder.encode(request.password()));
        user = userRepository.save(user);

        UserProfile profile = new UserProfile();
        profile.setUserId(user.getId());
        profile.setName(request.name() != null ? request.name() : request.username());
        profile.setAvatarUrl("https://api.dicebear.com/7.x/bottts/svg?seed=" + user.getUsername());
        userProfileRepository.save(profile);

        return ResponseEntity.ok(Map.of(
            "message", "User created successfully",
            "userId", user.getId(),
            "username", user.getUsername()
        ));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        var userOpt = userRepository.findByUsername(request.username());
        if (userOpt.isEmpty() || !passwordEncoder.matches(request.password(), userOpt.get().getPasswordHash())) {
            return ResponseEntity.status(401).body(Map.of("error", "Invalid username or password"));
        }

        User user = userOpt.get();
        return ResponseEntity.ok(Map.of(
            "message", "Login successful",
            "userId", user.getId(),
            "username", user.getUsername(),
            "token", "algoplay_mock_jwt_token_" + user.getId()
        ));
    }
}
