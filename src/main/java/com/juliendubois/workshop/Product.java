package com.juliendubois.workshop;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Product {
    @Id
    private Long id;
    private String name;
    private int priceCents;

    protected Product() {}

    Product(long id, String name, int priceCents) {
        this.id = id;
        this.name = name;
        this.priceCents = priceCents;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public int getPriceCents() { return priceCents; }
}
