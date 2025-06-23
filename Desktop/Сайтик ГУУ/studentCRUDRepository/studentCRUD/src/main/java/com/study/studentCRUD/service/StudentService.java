package com.study.studentCRUD.service;

import com.study.studentCRUD.ResourceNotFoundException;
import com.study.studentCRUD.controller.StudentRequest;
import com.study.studentCRUD.model.Course;
import com.study.studentCRUD.model.Student;
import com.study.studentCRUD.repository.CourseRepository;
import com.study.studentCRUD.repository.StudentRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StudentService {

    private final StudentRepository studentRepository;
    private final CourseRepository courseRepository;

    public StudentService(StudentRepository studentRepository, CourseRepository courseRepository) {
        this.studentRepository = studentRepository;
        this.courseRepository = courseRepository;
    }

    public List<Student> getAllStudents() {
        List<Student> students = studentRepository.findAll();
        System.out.println("Students fetched: " + students.size());
        return students;
    }

    public Student createStudent(StudentRequest request) {
        Course course = courseRepository.findById(request.getCourseId())
                .orElseThrow(() -> new ResourceNotFoundException("Курс с ID " + request.getCourseId() + " не найден"));
        Student student = new Student();
        student.setName(request.getName());
        student.setCourse(course);
        student.setEmail(request.getEmail());
        return studentRepository.save(student);
    }

    public Student updateStudent(Long id, StudentRequest request) {
        Student student = studentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Студент не найден"));
        Course course = courseRepository.findById(request.getCourseId())
                .orElseThrow(() -> new ResourceNotFoundException("Курс с ID " + request.getCourseId() + " не найден"));
        student.setName(request.getName());
        student.setCourse(course);
        return studentRepository.save(student);
    }

    public void deleteStudent(Long id) {
        if (!studentRepository.existsById(id)) {
            throw new ResourceNotFoundException("Студент не найден");
        }
        studentRepository.deleteById(id);
    }
}