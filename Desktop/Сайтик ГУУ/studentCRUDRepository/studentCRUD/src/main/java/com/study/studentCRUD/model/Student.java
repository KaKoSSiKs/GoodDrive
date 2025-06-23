package com.study.studentCRUD.model;

import jakarta.persistence.*;

@Entity
@Table(name = "student")
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String email;

    @ManyToOne
    @JoinColumn(name = "course_id", nullable = false)
    private Course course;

    // Геттеры и сеттеры
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Course getCourse() { return course; }
    public void setCourse(Course course) { this.course = course; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}