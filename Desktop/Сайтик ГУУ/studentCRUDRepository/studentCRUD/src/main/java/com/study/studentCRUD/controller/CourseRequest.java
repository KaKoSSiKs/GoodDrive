package com.study.studentCRUD.controller;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class CourseRequest {

    @NotBlank(message = "Название курса не может быть пустым")
    @Size(max = 255, message = "Название курса не может превышать 255 символов")
    private String title;

    @Size(max = 255, message = "Описание курса не может превышать 255 символов")
    private String description;

    // Геттеры и сеттеры
    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}