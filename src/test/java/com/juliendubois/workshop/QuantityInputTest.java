package com.juliendubois.workshop;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class QuantityInputTest extends HttpFixture {
    @Test
    void fractionalQuantityCannotCreateAnItem() throws Exception {
        var response = request("POST", "/api/cart/items",
                "{\"productId\":1,\"quantity\":1.5}");

        assertThat(response.statusCode()).isEqualTo(400);
        assertThat(cart().get("items").size()).isZero();
        assertThat(storedItems()).isZero();
    }

    @Test
    void fractionalQuantityCannotChangeAnExistingCart() throws Exception {
        assertThat(add(1, 2).statusCode()).isEqualTo(200);
        var before = cart();

        var response = request("POST", "/api/cart/items",
                "{\"productId\":1,\"quantity\":1.5}");

        assertThat(response.statusCode()).isEqualTo(400);
        assertThat(cart()).isEqualTo(before);
        assertThat(storedQuantity(1)).isEqualTo(2);
    }
}
