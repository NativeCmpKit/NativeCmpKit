/*
 * Copyright (c) 2026 NativeCmpKit contributors.
 * SPDX-License-Identifier: Apache-2.0
 */
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javafx.application.Platform;
import javafx.concurrent.Worker;
import javafx.scene.Scene;
import javafx.scene.layout.HBox;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public final class JavaFxHttp2CancellationProbe {
    private record Fixture(Stage stage, WebEngine first, WebEngine second) {}

    public static void main(String[] args) throws Exception {
        JavaFxPublicCancellationProbe.require(args.length == 2, "Expected the owned port and witness directory");
        JavaFxPublicCancellationProbe.require(System.getProperty("com.sun.webkit.useHTTP2Loader") == null,
            "Private loader route override refused");
        int port = Integer.parseInt(args[0]);
        JavaFxPublicCancellationProbe.require(port > 0 && port <= 65535, "Invalid owned port");
        String origin = "https://127.0.0.1:" + port;
        Path evidence = Path.of(args[1]);
        var startup = new CountDownLatch(1);
        Platform.startup(startup::countDown);
        try {
            JavaFxPublicCancellationProbe.require(startup.await(5, TimeUnit.SECONDS), "JavaFX startup deadline");
            Platform.setImplicitExit(false);
            Fixture fixture = JavaFxPublicCancellationProbe.fx(() -> {
                var first = new WebView();
                var second = new WebView();
                var stage = new Stage();
                stage.setScene(new Scene(new HBox(first, second), 800, 400));
                stage.show();
                return new Fixture(stage, first.getEngine(), second.getEngine());
            });
            try {
                WebEngine first = fixture.first(), second = fixture.second();
                JavaFxPublicCancellationProbe.fx(() -> { first.load(origin + "/cancel"); return null; });
                JavaFxPublicCancellationProbe.waitFor(() -> Files.isRegularFile(evidence.resolve("cancel-pending")),
                    "first request reached the negotiated HTTP/2 peer");
                JavaFxPublicCancellationProbe.fx(() -> { second.load(origin + "/survive"); return null; });
                JavaFxPublicCancellationProbe.waitFor(() -> Files.isRegularFile(evidence.resolve("both-pending")),
                    "both requests reached one HTTP/2 connection");
                JavaFxPublicCancellationProbe.require(JavaFxPublicCancellationProbe.fx(() ->
                    first.getLoadWorker().isRunning() && second.getLoadWorker().isRunning()
                ), "Both public workers must be pending before cancellation");
                JavaFxPublicCancellationProbe.require(JavaFxPublicCancellationProbe.fx(() -> first.getLoadWorker().cancel()),
                    "Public cancellation refused the pending HTTP/2 stream");
                JavaFxPublicCancellationProbe.waitFor(() -> JavaFxPublicCancellationProbe.fx(() ->
                    first.getLoadWorker().getState() == Worker.State.CANCELLED &&
                    second.getLoadWorker().getState() == Worker.State.SUCCEEDED &&
                    "NativeCmpKitH2Survived".equals(second.getTitle())
                ), "the cancelled worker and sibling native document");
                JavaFxPublicCancellationProbe.fx(() -> { first.load(origin + "/recover"); return null; });
                JavaFxPublicCancellationProbe.waitFor(() -> JavaFxPublicCancellationProbe.fx(() ->
                    first.getLoadWorker().getState() == Worker.State.SUCCEEDED && "NativeCmpKitH2Recovery".equals(first.getTitle())
                ), "same-engine recovery on the negotiated connection");
                Files.createFile(evidence.resolve("client-complete"));
                JavaFxPublicCancellationProbe.waitFor(() -> Files.isRegularFile(evidence.resolve("peer.json")),
                    "the real peer accepted all stream outcomes before teardown");
            } finally {
                JavaFxPublicCancellationProbe.fx(() -> { fixture.stage().close(); return null; });
            }
        } finally {
            Platform.exit();
        }
    }
}
