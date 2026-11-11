package com.juliendubois.workshop;

import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CartController {
    private final CartService service;
    private final SeedData seed;
    private final String revision;

    CartController(CartService service, SeedData seed, @Value("${workshop.revision}") String revision) {
        this.service = service;
        this.seed = seed;
        this.revision = revision;
    }

    public record AddItem(Long productId, Integer quantity) {}
    public record Identity(String application, String revision, long processId) {}

    @GetMapping("/api/products")
    public List<CartService.ProductView> products() { return service.products(); }

    @GetMapping("/api/cart")
    public CartService.CartView cart() { return service.cart(); }

    @PostMapping("/api/cart/items")
    public CartService.CartView add(@RequestBody AddItem request) {
        return service.add(request.productId(), request.quantity());
    }

    @GetMapping("/api/workshop")
    public Identity identity() {
        return new Identity("shopping-cart", revision, ProcessHandle.current().pid());
    }

    @PostMapping("/api/workshop/reset")
    public CartService.CartView reset(@RequestParam(defaultValue = "0") int items) {
        if (items != 0 && items != 8 && items != 16) {
            throw new org.springframework.web.server.ResponseStatusException(
                    org.springframework.http.HttpStatus.BAD_REQUEST, "Use 0, 8 or 16 sample items");
        }
        seed.reset(items);
        return service.cart();
    }
}
