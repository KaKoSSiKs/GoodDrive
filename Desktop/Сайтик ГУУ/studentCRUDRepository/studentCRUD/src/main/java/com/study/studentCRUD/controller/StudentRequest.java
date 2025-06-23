package com.study.studentCRUD.controller;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class StudentRequest {

    @NotBlank(message = "ФИО студента не может быть пустым")
    @Size(max = 255, message = "ФИО студента не может превышать 255 символов")
    private String name;

    @NotNull(message = "ID курса не может быть пустым")
    private Long courseId;

    @NotNull(message = "Email студента не может быть пустым")
    private String email;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public Long getCourseId() { return courseId; }
    public void setCourseId(Long courseId) { this.courseId = courseId; }
}
