package com.juliendubois.workshop;

import org.junit.jupiter.api.Test;
import tools.jackson.databind.JsonNode;
import static org.assertj.core.api.Assertions.assertThat;

class CartContractTest extends HttpFixture {
    @Test
    void repeatedAddsAccumulateAndPersistTheServerCalculatedTotal() throws Exception {
        var firstResponse = add(1, 1);
        assertThat(firstResponse.statusCode()).isEqualTo(200);
        var firstCart = json.readTree(firstResponse.body());
        assertThat(firstCart.get("items").get(0).get("quantity").asInt()).isEqualTo(1);
        assertThat(firstCart.get("items").get(0).get("priceCents").asInt()).isEqualTo(1000);
        assertThat(firstCart.get("totalCents").asInt()).isEqualTo(1000);

        var secondResponse = add(1, 1);
        assertThat(secondResponse.statusCode()).isEqualTo(200);
        var secondCart = json.readTree(secondResponse.body());
        assertThat(secondCart.get("items").get(0).get("quantity").asInt()).isEqualTo(2);
        assertThat(secondCart.get("items").get(0).get("lineTotalCents").asInt()).isEqualTo(2000);
        assertThat(secondCart.get("itemCount").asInt()).isEqualTo(2);
        assertThat(secondCart.get("totalCents").asInt()).isEqualTo(2000);

        assertThat(cart()).isEqualTo(secondCart);
        assertThat(storedQuantity(1)).isEqualTo(2);
    }

    @Test
    void addingMultipleUnitsIncrementsAnExistingQuantity() throws Exception {
        assertThat(add(1, 3).statusCode()).isEqualTo(200);

        var response = add(1, 2);

        assertThat(response.statusCode()).isEqualTo(200);
        var result = json.readTree(response.body());
        assertThat(result.get("items").get(0).get("quantity").asInt()).isEqualTo(5);
        assertThat(result.get("items").get(0).get("lineTotalCents").asInt()).isEqualTo(5000);
        assertThat(result.get("totalCents").asInt()).isEqualTo(5000);
        assertThat(storedQuantity(1)).isEqualTo(5);
    }

    @Test
    void addingANewProductPreservesExistingItemsAndUsesServerPrices() throws Exception {
        assertThat(add(1, 2).statusCode()).isEqualTo(200);

        var response = add(2, 1);

        assertThat(response.statusCode()).isEqualTo(200);
        var result = json.readTree(response.body());
        assertThat(result.get("items").size()).isEqualTo(2);
        assertThat(result.get("items").get(0).get("productId").asLong()).isEqualTo(1);
        assertThat(result.get("items").get(0).get("quantity").asInt()).isEqualTo(2);
        assertThat(result.get("items").get(0).get("priceCents").asInt()).isEqualTo(1000);
        assertThat(result.get("items").get(0).get("lineTotalCents").asInt()).isEqualTo(2000);
        assertThat(result.get("items").get(1).get("productId").asLong()).isEqualTo(2);
        assertThat(result.get("items").get(1).get("quantity").asInt()).isEqualTo(1);
        assertThat(result.get("items").get(1).get("priceCents").asInt()).isEqualTo(1200);
        assertThat(result.get("items").get(1).get("lineTotalCents").asInt()).isEqualTo(1200);
        assertThat(result.get("itemCount").asInt()).isEqualTo(3);
        assertThat(result.get("totalCents").asInt()).isEqualTo(3200);
        assertThat(storedQuantity(1)).isEqualTo(2);
        assertThat(storedQuantity(2)).isEqualTo(1);
    }

    @Test
    void acceptsQuantityLimitsAndRejectsAnAccumulatedQuantityOver99WithoutChangingState() throws Exception {
        var maximumResponse = add(1, 99);
        assertThat(maximumResponse.statusCode()).isEqualTo(200);
        var maximumCart = json.readTree(maximumResponse.body());
        assertThat(maximumCart.get("items").get(0).get("quantity").asInt()).isEqualTo(99);
        assertThat(maximumCart.get("items").get(0).get("lineTotalCents").asInt()).isEqualTo(99000);
        assertThat(maximumCart.get("totalCents").asInt()).isEqualTo(99000);

        var otherItemResponse = add(2, 1);
        assertThat(otherItemResponse.statusCode()).isEqualTo(200);
        var beforeRejectedAdd = cart();
        assertThat(beforeRejectedAdd.get("totalCents").asInt()).isEqualTo(100200);

        assertThat(add(1, 1).statusCode()).isEqualTo(400);

        assertThat(cart()).isEqualTo(beforeRejectedAdd);
        assertThat(storedQuantity(1)).isEqualTo(99);
        assertThat(storedQuantity(2)).isEqualTo(1);
    }

    @Test
    void rejectsQuantitiesOutsideOneTo99WithoutChangingState() throws Exception {
        var beforeRejectedAdds = cart();

        for (int quantity : new int[]{0, 100}) {
            assertThat(add(1, quantity).statusCode()).isEqualTo(400);
            assertThat(cart()).isEqualTo(beforeRejectedAdds);
            assertThat(storedItems()).isZero();
        }

        assertThat(add(1, 1).statusCode()).isEqualTo(200);
        var beforeRejectedExistingAdd = cart();

        assertThat(add(1, 100).statusCode()).isEqualTo(400);

        assertThat(cart()).isEqualTo(beforeRejectedExistingAdd);
        assertThat(storedQuantity(1)).isEqualTo(1);
    }
}
