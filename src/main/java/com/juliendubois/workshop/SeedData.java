package com.juliendubois.workshop;

import jakarta.persistence.EntityManager;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class SeedData {
    private final EntityManager em;

    SeedData(EntityManager em) { this.em = em; }

    @Transactional
    public void reset(int cartItems) {
        em.createQuery("delete from CartItem").executeUpdate();
        em.createQuery("delete from Product").executeUpdate();
        em.clear();
        String[] names = {"Notebook", "Coffee mug", "Pen set", "Desk pad",
                "Laptop sleeve", "Cable organiser", "Reading lamp", "Book stand",
                "Pencil case", "Travel cup", "Bookmark", "Sketchbook",
                "Mouse pad", "Phone stand", "Sticky notes", "Card holder"};
        for (int id = 1; id <= names.length; id++) {
            var product = new Product(id, names[id - 1], id == 1 ? 1000 : 1000 + id * 100);
            em.persist(product);
            if (id <= cartItems) {
                var item = new CartItem(product);
                item.setQuantity(1);
                em.persist(item);
            }
        }
        em.flush();
        em.clear();
    }
}
