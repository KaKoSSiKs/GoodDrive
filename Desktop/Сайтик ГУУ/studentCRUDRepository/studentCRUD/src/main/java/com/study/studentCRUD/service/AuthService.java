package com.study.studentCRUD.service;

import com.study.studentCRUD.LoginRequest;
import com.study.studentCRUD.LoginResponse;
import com.study.studentCRUD.RegisterRequest;
import com.study.studentCRUD.ResourceNotFoundException;
import com.study.studentCRUD.model.AppUser;
import com.study.studentCRUD.repository.AppUserRepository;
import com.study.studentCRUD.security.JwtTokenProvider;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final AppUserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(AppUserRepository userRepository, BCryptPasswordEncoder passwordEncoder, JwtTokenProvider jwtTokenProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    public void register(RegisterRequest request) {
        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new IllegalArgumentException("Email уже занят");
        }

        AppUser user = new AppUser();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setRole("USER");
        userRepository.save(user);
    }

    public LoginResponse login(LoginRequest request) {
        AppUser user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("Пользователь не найден"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            return new LoginResponse(null, "Неверный пароль");
        }

        String token = jwtTokenProvider.generateToken(user.getEmail(), user.getRole());
        return new LoginResponse(token, null);
    }
}