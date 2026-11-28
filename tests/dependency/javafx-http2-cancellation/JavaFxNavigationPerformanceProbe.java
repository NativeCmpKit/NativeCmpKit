/*
 * Copyright (c) 2026 NativeCmpKit contributors.
 * SPDX-License-Identifier: Apache-2.0
 */
import java.lang.management.ManagementFactory;
import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javafx.application.Platform;
import javafx.concurrent.Worker;
import javafx.scene.Scene;
import javafx.scene.layout.StackPane;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public final class JavaFxNavigationPerformanceProbe {
    private record Fixture(Stage window, WebEngine engine) {}

    private static long load(WebEngine engine) throws Exception {
        try (var peer = new JavaFxPublicCancellationProbe.CompletePeer(false)) {
            long started = System.nanoTime();
            JavaFxPublicCancellationProbe.fx(() -> {
                engine.load(peer.url());
                return null;
            });
            peer.awaitAdmission();
            peer.awaitCompletion();
            JavaFxPublicCancellationProbe.waitFor(() -> JavaFxPublicCancellationProbe.fx(() ->
                engine.getLoadWorker().getState() == Worker.State.SUCCEEDED &&
                peer.title.equals(engine.getTitle()) && engine.getDocument() != null
            ), "repeatable real navigation performance case");
            return System.nanoTime() - started;
        }
    }

    public static void main(String[] args) throws Exception {
        JavaFxPublicCancellationProbe.require(args.length == 0, "Performance fixture takes no options");
        var os = ManagementFactory.getPlatformMXBean(com.sun.management.OperatingSystemMXBean.class);
        var startup = new CountDownLatch(1);
        long bootedAt = System.nanoTime();
        Platform.startup(startup::countDown);
        try {
            JavaFxPublicCancellationProbe.require(startup.await(5, TimeUnit.SECONDS), "JavaFX startup deadline");
            Platform.setImplicitExit(false);
            Fixture fixture = JavaFxPublicCancellationProbe.fx(() -> {
                var view = new WebView();
                var window = new Stage();
                window.setScene(new Scene(new StackPane(view), 720, 400));
                window.show();
                return new Fixture(window, view.getEngine());
            });
            try {
                long startupNanos = System.nanoTime() - bootedAt;
                for (int i = 0; i < 4; i++) load(fixture.engine());
                long cpuBefore = os.getProcessCpuTime();
                long[] samples = new long[20];
                for (int i = 0; i < samples.length; i++) samples[i] = load(fixture.engine());
                System.out.printf("{\"startupNanos\":%d,\"processCpuNanos\":%d,\"samplesNanos\":%s}%n",
                    startupNanos, os.getProcessCpuTime() - cpuBefore, Arrays.toString(samples));
            } finally {
                JavaFxPublicCancellationProbe.fx(() -> { fixture.window().close(); return null; });
            }
        } finally {
            Platform.exit();
        }
    }
}
