package com.study.studentCRUD.repository;

import com.study.studentCRUD.model.Course;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CourseRepository extends JpaRepository<Course, Long> {
}