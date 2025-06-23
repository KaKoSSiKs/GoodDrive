package com.study.studentCRUD.repository;

import com.study.studentCRUD.model.Student;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StudentRepository extends JpaRepository<Student, Long> {
}