package com.kindconnect.model;

import jakarta.persistence.*;

@Entity
@Table(name = "volunteer")
public class Volunteer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String email;
    private String phone;
    private String skillType;
    private Boolean available;

    public Volunteer() {
    }

    public Volunteer(String name, String email, String phone, String skillType, Boolean available) {
        this.name = name;
        this.email = email;
        this.phone = phone;
        this.skillType = skillType;
        this.available = available;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public String getPhone() {
        return phone;
    }

    public String getSkillType() {
        return skillType;
    }

    public Boolean getAvailable() {
        return available;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public void setSkillType(String skillType) {
        this.skillType = skillType;
    }

    public void setAvailable(Boolean available) {
        this.available = available;
    }
}