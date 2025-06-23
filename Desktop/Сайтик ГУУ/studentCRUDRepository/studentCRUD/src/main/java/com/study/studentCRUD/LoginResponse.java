package com.study.studentCRUD;

public class LoginResponse {
    private String token;
    private String error;

    public LoginResponse(String token, String error) {
        this.token = token;
        this.error = error;
    }

    public String getToken() { return token; }
    public String getError() { return error; }
}