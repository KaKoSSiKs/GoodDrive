package com.study.studentCRUD.controller;

import com.study.studentCRUD.ResourceNotFoundException;
import com.study.studentCRUD.model.AppUser;
import com.study.studentCRUD.repository.AppUserRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/profile")
public class ProfileController {

    private final AppUserRepository userRepository;

    public ProfileController(AppUserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping("/me")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<UserResponse> getProfile(Authentication authentication) {
        String email = authentication.getName();
        AppUser user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("Пользователь не найден"));
        return ResponseEntity.ok(new UserResponse(user.getEmail(), user.getRole()));
    }
}

