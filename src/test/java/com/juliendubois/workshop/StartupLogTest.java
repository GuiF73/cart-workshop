package com.juliendubois.workshop;

import java.time.Duration;
import io.github.jdubois.bootui.autoconfigure.BootUiProperties;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import org.springframework.context.support.GenericApplicationContext;
import org.springframework.mock.env.MockEnvironment;
import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(OutputCaptureExtension.class)
class StartupLogTest {
    @Test
    void printsHomeAndBootUiLinks(CapturedOutput output) {
        logReady(new MockEnvironment().withProperty("local.server.port", "18765"),
                new BootUiProperties());

        assertThat(output.getOut()).contains("Shopping cart is ready!",
                "Home:   http://127.0.0.1:18765/",
                "BootUI: http://127.0.0.1:18765/bootui/");
    }

    @Test
    void usesBoundPortAndConfiguredPaths(CapturedOutput output) {
        var properties = new BootUiProperties();
        properties.setPath("/diagnostics");
        logReady(new MockEnvironment()
                .withProperty("local.server.port", "54321")
                .withProperty("server.port", "0")
                .withProperty("server.address", "127.0.0.1")
                .withProperty("server.ssl.enabled", "true")
                .withProperty("server.servlet.context-path", "/shop"), properties);

        assertThat(output.getOut()).contains(
                "Home:   https://127.0.0.1:54321/shop/",
                "BootUI: https://127.0.0.1:54321/shop/diagnostics/")
                .doesNotContain(":0/");
    }

    @Test
    void doesNotAdvertiseAbsentBootUi(CapturedOutput output) {
        logReady(new MockEnvironment().withProperty("local.server.port", "54321"), null);

        assertThat(output.getOut()).contains("Home:   http://127.0.0.1:54321/",
                "BootUI: disabled").doesNotContain("/bootui/");
    }

    @Test
    void doesNotAdvertiseDisabledBootUi(CapturedOutput output) {
        var properties = new BootUiProperties();
        properties.setEnabled(BootUiProperties.Mode.OFF);
        logReady(new MockEnvironment().withProperty("local.server.port", "54321"), properties);

        assertThat(output.getOut()).contains("BootUI: disabled").doesNotContain("/bootui/");
    }

    private void logReady(MockEnvironment environment, BootUiProperties bootUi) {
        try (var context = new GenericApplicationContext()) {
            context.setEnvironment(environment);
            if (bootUi != null) {
                context.getBeanFactory().registerSingleton("bootUiProperties", bootUi);
            }
            context.refresh();
            new ShoppingCartApplication().logReady(new ApplicationReadyEvent(
                    new SpringApplication(ShoppingCartApplication.class), new String[0],
                    context, Duration.ZERO));
        }
    }
}
