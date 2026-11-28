/*
 * Copyright (c) 2026 NativeCmpKit contributors.
 * SPDX-License-Identifier: Apache-2.0
 */
import java.lang.management.ManagementFactory;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javafx.application.Platform;
import javafx.concurrent.Worker;
import javafx.scene.Scene;
import javafx.scene.layout.StackPane;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public final class JavaFxCancellationLifecycleProbe {
    private static final int REPEATS = 16;
    private record Fixture(Stage stage, WebEngine engine) {}

    private static void navigationReplacesPendingExchange(WebEngine engine) throws Exception {
        try (var pending = new JavaFxPublicCancellationProbe.HeldPeer("zero-header")) {
            begin(engine, pending);
            try (var next = new JavaFxPublicCancellationProbe.CompletePeer(false)) {
                JavaFxPublicCancellationProbe.fx(() -> { engine.load(next.url()); return null; });
                pending.awaitRealEof();
                next.awaitAdmission();
                next.awaitCompletion();
                JavaFxPublicCancellationProbe.waitFor(() -> JavaFxPublicCancellationProbe.fx(() ->
                    engine.getLoadWorker().getState() == Worker.State.SUCCEEDED && next.title.equals(engine.getTitle())
                ), "replacement navigation succeeded");
            }
        }
    }

    private static void begin(WebEngine engine, JavaFxPublicCancellationProbe.HeldPeer peer) throws Exception {
        JavaFxPublicCancellationProbe.fx(() -> { engine.load(peer.url()); return null; });
        peer.awaitAdmission();
        JavaFxPublicCancellationProbe.waitFor(() -> JavaFxPublicCancellationProbe.fx(() ->
            engine.getLoadWorker().getState() == Worker.State.RUNNING && engine.getLoadWorker().isRunning()
        ), "pending lifecycle request");
    }

    private static long cancelExchange(WebEngine engine) throws Exception {
        try (var pending = new JavaFxPublicCancellationProbe.HeldPeer("zero-header")) {
            begin(engine, pending);
            long started = System.nanoTime();
            JavaFxPublicCancellationProbe.require(JavaFxPublicCancellationProbe.fx(() -> engine.getLoadWorker().cancel()),
                "Repeated pending cancellation refused");
            pending.awaitRealEof();
            JavaFxPublicCancellationProbe.require(JavaFxPublicCancellationProbe.fx(() ->
                engine.getLoadWorker().getState() == Worker.State.CANCELLED
            ), "Repeated exchange did not reach CANCELLED");
            return System.nanoTime() - started;
        }
    }

    private static void detachAfterCancelling(Stage stage, WebEngine engine) throws Exception {
        try (var pending = new JavaFxPublicCancellationProbe.HeldPeer("zero-header")) {
            begin(engine, pending);
            JavaFxPublicCancellationProbe.fx(() -> {
                JavaFxPublicCancellationProbe.require(engine.getLoadWorker().cancel(), "Detach cancellation refused");
                stage.setScene(null);
                stage.close();
                return null;
            });
            pending.awaitRealEof();
            JavaFxPublicCancellationProbe.require(JavaFxPublicCancellationProbe.fx(() -> !stage.isShowing()
                && stage.getScene() == null), "Detached WebView still owned by the stage");
        }
    }

    public static void main(String[] args) throws Exception {
        JavaFxPublicCancellationProbe.require(args.length == 0, "Lifecycle probe has no options");
        JavaFxPublicCancellationProbe.require(System.getProperty("com.sun.webkit.useHTTP2Loader") == null,
            "Private loader route override refused");
        var os = ManagementFactory.getPlatformMXBean(com.sun.management.UnixOperatingSystemMXBean.class);
        JavaFxPublicCancellationProbe.require(os != null, "Expected a hosted Unix descriptor counter");
        var startup = new CountDownLatch(1);
        Platform.startup(startup::countDown);
        try {
            JavaFxPublicCancellationProbe.require(startup.await(5, TimeUnit.SECONDS), "JavaFX lifecycle startup deadline");
            Platform.setImplicitExit(false);
            Fixture fixture = JavaFxPublicCancellationProbe.fx(() -> {
                var view = new WebView();
                var window = new Stage();
                window.setScene(new Scene(new StackPane(view), 720, 400));
                window.show();
                return new Fixture(window, view.getEngine());
            });
            try {
                WebEngine engine = fixture.engine();
                navigationReplacesPendingExchange(engine);
                for (int cycle = 0; cycle < 3; cycle++) cancelExchange(engine);
                long descriptorsBefore = os.getOpenFileDescriptorCount();
                long worstCancelNanos = 0;
                for (int cycle = 0; cycle < REPEATS; cycle++) {
                    worstCancelNanos = Math.max(worstCancelNanos, cancelExchange(engine));
                }
                JavaFxPublicCancellationProbe.waitFor(() -> os.getOpenFileDescriptorCount() <= descriptorsBefore + 4,
                    "file descriptors after repeated cancellation settle near the warm baseline");
                long descriptorsAfter = os.getOpenFileDescriptorCount();
                detachAfterCancelling(fixture.stage(), engine);
                System.out.printf("{\"replacementNavigation\":true,\"detachAfterCancel\":true,"
                    + "\"repeatPeerEofs\":%d,\"openDescriptorsBefore\":%d,\"openDescriptorsAfter\":%d,"
                    + "\"worstCancelNanos\":%d}%n", REPEATS, descriptorsBefore, descriptorsAfter, worstCancelNanos);
            } finally {
                JavaFxPublicCancellationProbe.fx(() -> { fixture.stage().close(); return null; });
            }
        } finally {
            Platform.exit();
        }
    }
}
