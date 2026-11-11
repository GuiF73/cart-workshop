package com.juliendubois.workshop;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class CartItem {
    @Id
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Product product;
    private int quantity;

    protected CartItem() {}

    CartItem(Product product) {
        this.id = product.getId();
        this.product = product;
    }

    public Long getId() { return id; }
    public Product getProduct() { return product; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
}
