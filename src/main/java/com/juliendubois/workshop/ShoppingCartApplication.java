package com.juliendubois.workshop;

import io.github.jdubois.bootui.autoconfigure.BootUiProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.annotation.Bean;
import org.springframework.context.event.EventListener;
import org.springframework.web.util.UriComponentsBuilder;

@SpringBootApplication
public class ShoppingCartApplication {
    private static final Logger log = LoggerFactory.getLogger(ShoppingCartApplication.class);

    public static void main(String[] args) {
        SpringApplication.run(ShoppingCartApplication.class, args);
    }

    @EventListener(ApplicationReadyEvent.class)
    void logReady(ApplicationReadyEvent event) {
        var context = event.getApplicationContext();
        var env = context.getEnvironment();
        var baseUrl = UriComponentsBuilder.newInstance()
                .scheme(env.getProperty("server.ssl.enabled", Boolean.class, false) ? "https" : "http")
                .host(env.getProperty("server.address", "127.0.0.1"))
                .port(env.getRequiredProperty("local.server.port", Integer.class))
                .path(env.getProperty("server.servlet.context-path", ""))
                .build().toUriString();
        var bootUi = context.getBeanProvider(BootUiProperties.class).getIfAvailable();
        log.info("""

                ----------------------------------------------------------
                  Shopping cart is ready!
                  Home:   {}/
                  BootUI: {}
                ----------------------------------------------------------""",
                baseUrl, bootUi == null || bootUi.getEnabled() == BootUiProperties.Mode.OFF
                        ? "disabled" : baseUrl + bootUi.getPath() + "/");
    }

    @Bean
    CommandLineRunner seed(SeedData seed) {
        return args -> seed.reset(0);
    }
}
