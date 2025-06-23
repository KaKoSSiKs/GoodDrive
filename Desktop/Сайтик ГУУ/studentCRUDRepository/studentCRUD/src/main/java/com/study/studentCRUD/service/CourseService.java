package com.study.studentCRUD.service;

import com.study.studentCRUD.ResourceNotFoundException;
import com.study.studentCRUD.controller.CourseRequest;
import com.study.studentCRUD.model.Course;
import com.study.studentCRUD.repository.CourseRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CourseService {

    private final CourseRepository courseRepository;

    public CourseService(CourseRepository courseRepository) {
        this.courseRepository = courseRepository;
    }

    public List<Course> getAllCourses() {
        List<Course> courses = courseRepository.findAll();
        System.out.println("Courses fetched: " + courses.size());
        return courses;
    }

    public Course createCourse(CourseRequest request) {
        Course course = new Course();
        course.setTitle(request.getTitle());
        course.setDescription(request.getDescription());
        return courseRepository.save(course);
    }

    public Course updateCourse(Long id, CourseRequest request) {
        Course course = courseRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Курс не найден"));
        course.setTitle(request.getTitle());
        course.setDescription(request.getDescription());
        return courseRepository.save(course);
    }

    public void deleteCourse(Long id) {
        if (!courseRepository.existsById(id)) {
            throw new ResourceNotFoundException("Курс не найден");
        }
        courseRepository.deleteById(id);
    }
}