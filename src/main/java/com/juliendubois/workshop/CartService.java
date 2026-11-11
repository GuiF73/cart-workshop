package com.juliendubois.workshop;

import java.util.List;
import jakarta.persistence.EntityManager;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
public class CartService {
    private final CartRepository repository;
    private final EntityManager em;

    CartService(CartRepository repository, EntityManager em) {
        this.repository = repository;
        this.em = em;
    }

    public record ItemView(long productId, String name, int priceCents, int quantity, int lineTotalCents) {}
    public record CartView(List<ItemView> items, int itemCount, int totalCents) {}
    public record ProductView(long id, String name, int priceCents) {}

    @Transactional(readOnly = true)
    public List<ProductView> products() {
        return em.createQuery("select p from Product p order by p.id", Product.class).getResultList()
                .stream().map(p -> new ProductView(p.getId(), p.getName(), p.getPriceCents())).toList();
    }

    @Transactional(readOnly = true)
    public CartView cart() {
        var items = repository.findCart().stream().map(item -> {
            var product = item.getProduct();
            return new ItemView(product.getId(), product.getName(), product.getPriceCents(),
                    item.getQuantity(), product.getPriceCents() * item.getQuantity());
        }).toList();
        return new CartView(items, items.stream().mapToInt(ItemView::quantity).sum(),
                items.stream().mapToInt(ItemView::lineTotalCents).sum());
    }

    @Transactional
    public CartView add(Long productId, Integer quantity) {
        if (productId == null || quantity == null || quantity < 1 || quantity > 99) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Quantity must be between 1 and 99");
        }
        var product = em.find(Product.class, productId);
        if (product == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found");
        }
        var item = repository.findById(productId).orElseGet(() -> new CartItem(product));
        int nextQuantity = item.getQuantity() + quantity;
        if (nextQuantity > 99) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Cart quantity cannot exceed 99");
        }
        item.setQuantity(quantity);
        repository.saveAndFlush(item);
        return cart();
    }
}
