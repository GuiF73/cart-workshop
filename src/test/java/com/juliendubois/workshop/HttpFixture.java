package com.juliendubois.workshop;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import org.hibernate.SessionFactory;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.transaction.support.TransactionTemplate;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        properties = {"bootui.enabled=false", "server.address=127.0.0.1"})
abstract class HttpFixture {
    @LocalServerPort int port;
    @Autowired SeedData seed;
    @Autowired EntityManager em;
    @Autowired EntityManagerFactory emf;
    @Autowired TransactionTemplate tx;
    final HttpClient client = HttpClient.newHttpClient();
    final ObjectMapper json = new ObjectMapper();

    @BeforeEach
    void reset() { seed.reset(0); }

    HttpResponse<String> request(String method, String path, String body) throws Exception {
        return client.send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port + path))
                .header("Content-Type", "application/json")
                .method(method, HttpRequest.BodyPublishers.ofString(body)).build(),
                HttpResponse.BodyHandlers.ofString());
    }

    HttpResponse<String> add(long productId, int quantity) throws Exception {
        return request("POST", "/api/cart/items",
                "{\"productId\":" + productId + ",\"quantity\":" + quantity + "}");
    }

    JsonNode cart() throws Exception {
        var response = request("GET", "/api/cart", "");
        assertThat(response.statusCode()).isEqualTo(200);
        return json.readTree(response.body());
    }

    int storedQuantity(long id) {
        return tx.execute(status -> {
            em.clear();
            return em.find(CartItem.class, id).getQuantity();
        });
    }

    long storedItems() {
        return tx.execute(status -> {
            em.clear();
            return em.createQuery("select count(i) from CartItem i", Long.class).getSingleResult();
        });
    }

    org.hibernate.stat.Statistics statistics() {
        return emf.unwrap(SessionFactory.class).getStatistics();
    }
}
