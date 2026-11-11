package com.juliendubois.workshop;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface CartRepository extends JpaRepository<CartItem, Long> {
    @Query("select i from CartItem i order by i.id")
    List<CartItem> findCart();
}
