package com.juliendubois.workshop;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class BaselineTest extends HttpFixture {
    @Test
    void catalogueAndEmptyCartAreAvailable() throws Exception {
        var products = request("GET", "/api/products", "");
        assertThat(products.statusCode()).isEqualTo(200);
        assertThat(json.readTree(products.body()).size()).isEqualTo(16);
        assertThat(cart().get("items").size()).isZero();
        assertThat(cart().get("totalCents").asInt()).isZero();
    }

    @Test
    void firstAddPersistsTheServerPrice() throws Exception {
        var response = add(1, 2);
        assertThat(response.statusCode()).isEqualTo(200);
        var body = json.readTree(response.body());
        assertThat(body.get("itemCount").asInt()).isEqualTo(2);
        assertThat(body.get("totalCents").asInt()).isEqualTo(2000);
        assertThat(storedQuantity(1)).isEqualTo(2);
    }

    @Test
    void invalidQuantitiesDoNotChangeTheCart() throws Exception {
        assertThat(add(1, 0).statusCode()).isEqualTo(400);
        assertThat(add(1, -1).statusCode()).isEqualTo(400);
        assertThat(add(1, 100).statusCode()).isEqualTo(400);
        assertThat(storedItems()).isZero();
    }

    @Test
    void unknownProductIsNotAdded() throws Exception {
        assertThat(add(999, 1).statusCode()).isEqualTo(404);
        assertThat(storedItems()).isZero();
    }
}
