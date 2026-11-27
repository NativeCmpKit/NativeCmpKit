#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""NEW finite source controls. Passing these never substitutes for target compilation/native execution."""
from pathlib import Path
import ast
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "io.github.apdelrahman1911.nativecmpkit.ui.web."
PREFIX = "nativecmpkit-webview/src/{set}/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/"
CORE_METHODS = (
    "savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory",
    "documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved",
)
MOBILE_METHODS = CORE_METHODS + (
    "initialHeadersRedirectsAndSubresourcesMatchStateAndNavigatorPolicy",
    "relativeResourcesPreserveSupportedUnicodeEncoding",
)
OTHER_METHODS = CORE_METHODS + ("unsupportedHeadersAndBaseUrlRefuseBeforeNetworkForBothEntryPoints",)
CLASSES = {
    "IosWebViewContentPolicyAcceptanceTest": ("iosTest", MOBILE_METHODS),
    "AndroidWebViewContentPolicyAcceptanceTest": ("androidDeviceTest", MOBILE_METHODS),
    "DesktopWebViewContentPolicyAcceptanceTest": ("desktopTest", OTHER_METHODS),
    "BrowserWebViewContentPolicyAcceptanceTest": ("webTest", OTHER_METHODS),
}
ANDROID_SOURCE = "nativecmpkit-webview/src/androidMain/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/WebView.android.kt"
# The d968257f preimage with only its Kotlin namespace migrated.
ANDROID_PREIMAGE_SHA256 = "130c46efe44e30a7f88b4c8d3b7a03f92169ee646a63f6468405db3ae82551e1"
ANDROID_PREIMAGE = "                this.pageTitle = it[pageTitleKey] as String?\n                this.lastLoadedUrl = it[lastLoadedUrlKey] as String?\n"
ANDROID_POSTIMAGE = "                // Native history is not a displayed document. Actual native callbacks\n                // repopulate metadata; never paint an old title/URL over a new blank view.\n"
# Complete renamed images from 18e1978d, including the reviewed WebView fixes already in its parent.
UNCHANGED_INPUTS = {
    "nativecmpkit-webview/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit/ui/web/WebViewContracts.kt": "4476eb5ee9bf590b121e29c8a95e2e3cd31d6e96260c999953da19b6c67460ca",
    "nativecmpkit-webview/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit/ui/web/WebView.kt": "f690e412f95a3b9a08eec97b7d6f751cd8f6da20befbc1c31e6bfc5c8b5e951e",
    "nativecmpkit-webview/src/iosMain/kotlin/io.github.apdelrahman1911.nativecmpkit/ui/web/WebView.ios.kt": "940585ae412eaeebeedf55ba927ad5e9a6422d9a2b8695608f2dceaadb4bcbef",
    "nativecmpkit-webview/src/desktopMain/kotlin/io.github.apdelrahman1911.nativecmpkit/ui/web/WebView.desktop.kt": "26b914d5f62aceae320d9ca8df91018e70aca2f8ea3e451f2bc03e2313b85953",
    "nativecmpkit-webview/src/webMain/kotlin/io.github.apdelrahman1911.nativecmpkit/ui/web/WebView.web.kt": "7f84bda8a1f50b96b4a8c498f4e377d009664036fcfa203707b73180064b95b8",
    "scripts/ci/ios_webview_request_fixture.py": "caa5842043e012622d8ab05ffdfc61e4382238c5760a3b18db81639908dd4649",
    "nativecmpkit-webview/build.gradle.kts": "e49deed63c5482e257a08909c3b296c21ac341403596a1d5ca14c6b2b8ed64a7",
    "nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeWebViewApplicationHost.kt": "4177b7ed6f2d0040ffe72545eea6f7a02ff002bc22cbba46026d937bceb06d50",
    "nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeWebViewApplicationHostTest.kt": "24bdf9d5b96aaf13597e08f25be408d60b76311d3c30ad1726129e3205adc8c1",
    "nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeObjectIdentity.kt": "cc9b988cc03586fa535bfa8f3be66e0581252611fdfb6db12fa2606b48d09ee6",
    "nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidWebViewLifetimeDeviceTest.kt": "8b6d5b4f49d534391d5ba92cbd836bc26562caa034d040a4604884d79967de7b",
}


def source(klass):
    return (ROOT / (PREFIX.format(set=CLASSES[klass][0]) + klass + ".kt")).read_text()


def proposal():
    return json.loads((ROOT / "docs/testing/nativecmpkit-webview-content-policy-focuses.json").read_text())


class WebViewContentPolicySourceTest(unittest.TestCase):
    def test_android_saver_restoration_does_not_paint_saved_metadata_before_native_document(self):
        path = ROOT / "nativecmpkit-webview/src/androidMain/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/WebView.android.kt"
        source = path.read_text()
        saver = source.split("actual val WebStateSaver: Saver<WebViewState, Any> = run {", 1)[1]
        restore = saver.split("restore = {", 1)[1]
        self.assertIn("WebViewState(WebContent.NavigatorOnly)", restore)
        self.assertIn("this.viewState = it[stateBundle] as Bundle?", restore)
        self.assertNotRegex(restore, r"this\.(?:pageTitle|lastLoadedUrl)\s*=\s*it\[",
            "The public saver restores stale title/final URL before any real remounted document witness")


class WebViewContentPolicyNewSourceTest(unittest.TestCase):
    """Source/inventory/ownership controls only; never claim target API/DOM compilation."""
    def test_exact_four_enabled_class_inventory_is_fourteen_authored_seventeen_target_cases(self):
        count = 0
        for klass, (_, methods) in CLASSES.items():
            text = source(klass)
            self.assertIn("package " + PACKAGE.rstrip("."), text)
            self.assertIn("class " + klass, text)
            self.assertEqual(list(methods), re.findall(r"@Test\s+fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)", text))
            self.assertNotRegex(text, r"@(Ignore|Disabled|IgnoredTest)\b")
            count += len(methods)
        plan = proposal()
        self.assertEqual((4, 14, 17), (len(CLASSES), count, sum(row["required_native_cases"] for row in plan["profiles"])))

    def test_proposal_has_exact_five_single_host_tasks_and_no_all_host_alias(self):
        expected = (
            ("webview-content-policy-linux", "desktop-linux-x64", "desktop", ":nativecmpkit-webview:desktopTest", "DesktopWebViewContentPolicyAcceptanceTest"),
            ("webview-content-policy-android", "android-device-api35", "android-device", ":nativecmpkit-webview:connectedAndroidDeviceTest", "AndroidWebViewContentPolicyAcceptanceTest"),
            ("webview-content-policy-js", "browser-js", "js", ":nativecmpkit-webview:jsBrowserTest", "BrowserWebViewContentPolicyAcceptanceTest"),
            ("webview-content-policy-wasm", "browser-wasm", "wasm", ":nativecmpkit-webview:wasmJsBrowserTest", "BrowserWebViewContentPolicyAcceptanceTest"),
            ("ios-webview-content-policy", "ios-iphone", "ios", ":nativecmpkit-webview:iosSimulatorArm64ApplicationTest", "IosWebViewContentPolicyAcceptanceTest"),
        )
        plan = proposal()
        self.assertEqual("finite-source-proposal-not-runner-registration", plan["kind"])
        self.assertEqual([66, 73], plan["issues"])
        self.assertEqual("nativecmpkit-webview", plan["module"])
        self.assertEqual(len(expected), len(plan["profiles"]))
        for row, (focus, slot, suite, task, klass) in zip(plan["profiles"], expected, strict=True):
            self.assertEqual((focus, focus, slot, suite, task, PACKAGE + klass),
                             tuple(row[key] for key in ("profile", "focus", "slot", "suite", "task", "classname")))
            self.assertEqual(list(CLASSES[klass][1]), row["methods"])
            self.assertEqual(PREFIX.format(set=CLASSES[klass][0]) + klass + ".kt", row["source"])
            self.assertEqual(len(row["methods"]), row["required_native_cases"])
            self.assertTrue(all((ROOT / path).is_file() for path in row["helpers"]))
        self.assertEqual(0, plan["compiler_executions_by_this_patch"])
        self.assertEqual(0, plan["native_executions_by_this_patch"])

    def test_android_production_diff_is_only_exact_metadata_restore_inverse(self):
        text = (ROOT / ANDROID_SOURCE).read_text()
        self.assertEqual(1, text.count(ANDROID_POSTIMAGE))
        # Peel the later visible-commit title gate before comparing the older saver change.
        changes = (
            ("""        state.viewState?.let {
            // A restored history title can arrive before any document is rendered.
            state.awaitingRestoredDocument = true
            if (view.restoreState(it) == null) state.awaitingRestoredDocument = false
        }
""", "        state.viewState?.let { view.restoreState(it) }\n"),
            ("                state.awaitingRestoredDocument = false\n", ""),
            ("""    override fun onPageCommitVisible(view: WebView, url: String) {
        super.onPageCommitVisible(view, url)
        if (state.webView !== view || !state.awaitingRestoredDocument) return
        state.awaitingRestoredDocument = false
        // The provider may have delivered the new title before the visible commit.
        state.pageTitle = view.title
    }

""", ""),
            ("if (state.webView === view && !state.awaitingRestoredDocument) state.pageTitle = title",
             "if (state.webView === view) state.pageTitle = title"),
            ("\n    internal var awaitingRestoredDocument = false\n", ""),
        )
        original = text
        for current, previous in changes:
            self.assertEqual(1, original.count(current))
            original = original.replace(current, previous, 1)
        reconstructed = original.replace(ANDROID_POSTIMAGE, ANDROID_PREIMAGE, 1).encode()
        self.assertEqual(ANDROID_PREIMAGE_SHA256, hashlib.sha256(reconstructed).hexdigest())
        for value in ('val pageTitleKey = "pagetitle"', 'val lastLoadedUrlKey = "lastloaded"', 'val stateBundle = "bundle"',
                      "view.saveState(saved)", "pageTitleKey to it.pageTitle", "lastLoadedUrlKey to it.lastLoadedUrl",
                      "this.viewState = it[stateBundle] as Bundle?"):
            self.assertIn(value, text)

    def test_owning_common_native_and_accepted_fixture_helper_bytes_remain_unchanged(self):
        for path, digest in UNCHANGED_INPUTS.items():
            self.assertEqual(digest, hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), path)

    def test_authored_native_tests_never_inject_callbacks_loading_title_url_errors_or_saver_results(self):
        forbidden = (r"\.(?:pageTitle|lastLoadedUrl|loadingState|errorsForCurrentRequest)\s*=(?!=)",
                     r"\.(?:onPageFinished|onReceivedError|didFinishNavigation|didFailProvisionalNavigation)\s*\(",
                     r"\b(?:WebResourceResponse|shouldInterceptRequest|WKURLSchemeHandler|NSURLProtocol)\b",
                     r"@(Ignore|Disabled|IgnoredTest)\b")
        for klass in CLASSES:
            text = source(klass)
            evaluator_owner = (ROOT / (PREFIX.format(set="desktopTest") + "DesktopContentPolicyWindow.kt")).read_text() if klass == "DesktopWebViewContentPolicyAcceptanceTest" else text
            for expression in forbidden:
                self.assertNotRegex(text + evaluator_owner, expression, klass)
            self.assertIn("WebStateSaver.restore", text)
            self.assertIn("WebStateSaver", text)
            self.assertIn("evaluateJavascriptResult", evaluator_owner)
            self.assertIn("document.title", text)
            self.assertIn("document.getElementById('policy-form').submit()", text)

    def test_non_android_restore_rows_remount_real_owners_and_keep_explicit_non_saveable_opt_out(self):
        for klass in ("IosWebViewContentPolicyAcceptanceTest", "DesktopWebViewContentPolicyAcceptanceTest", "BrowserWebViewContentPolicyAcceptanceTest"):
            text = source(klass)
            self.assertIn('listOf("url", "html", "navigator", "redirect", "null")', text)
            self.assertIn("assertNotSame(state, restored)", text)
            self.assertIn("assertNull(restored.pageTitle)", text)
            self.assertIn('if (row == "redirect") "final" else row', text)
            self.assertIn("assertBlank", text)
            self.assertIn('"html-recovery"', text)
            self.assertIn('"null-recovery"', text)
            self.assertIn('val sensitive = policyState(WebContent.NavigatorOnly)', text)
            self.assertIn('val fresh = policyState(WebContent.NavigatorOnly)', text)
            self.assertNotRegex(text, r"(?:restorableWebUrl|token)\s*\.\s*(?:contains|startsWith|endsWith)")

    def test_android_restoration_uses_real_parcel_bundle_and_dom_metadata_before_bounded_reload(self):
        text = source("AndroidWebViewContentPolicyAcceptanceTest")
        self.assertIn('listOf("html", "navigator", "redirect", "null")', text)
        for value in ("Parcel.obtain()", "parcel.writeValue(saved)", "parcel.readValue(WebViewState::class.java.classLoader)",
                      "parcel.recycle()", "copyBackForwardList().currentItem?.url", "fixture.navigator.reload()",
                      "assertMetadataMatchesRealDocument(current, fixture.navigator)",
                      "assertMetadataMatchesRealDocument(saved, fixture.navigator)", "document.location.href",
                      'page in minimum..(minimum + 1)', 'getValue("get") in minimum..(minimum + 1)'):
            self.assertIn(value, text)
        self.assertIn('exact(server, "url", "get" to 0)', text)
        self.assertIn('assertEquals(native.canGoBack(), navigator.canGoBack)', text)

    def test_mobile_main_header_counts_include_three_real_relative_gets_and_actual_redirect_parity(self):
        for klass in ("IosWebViewContentPolicyAcceptanceTest", "AndroidWebViewContentPolicyAcceptanceTest"):
            text = source(klass)
            for value in ('listOf("state", "navigator")', 'listOf("initial", "same", "cross")',
                          '"get" to if (route == "initial") 4 else 1', '"main_initial" to 1', '"main_authorization" to 1',
                          'document.getElementById(\'policy-link\').click()', 'observations["state-$route"]', 'observations["navigator-$route"]',
                          '"script_initial" to 0', '"script_authorization" to 0', '"style_initial" to 0', '"image_authorization" to 0'):
                self.assertIn(value, text)
            self.assertIn('assertTrue(value in 0..1)', text)

    def test_mobile_relative_resource_evidence_is_real_dom_computed_style_decoded_image_unicode_and_aliases(self):
        for klass in ("IosWebViewContentPolicyAcceptanceTest", "AndroidWebViewContentPolicyAcceptanceTest"):
            text = source(klass)
            for value in ('"utf8" to "utf-8", "utf8-alias" to "utf8"', "baseUrl =", "navigator.loadHtml",
                          "relative-resource-text", "getComputedStyle", "rgb(17, 34, 51)", "naturalWidth === 7", "naturalHeight === 9",
                          '"get" to 3, "page" to 0, "script" to 1, "style" to 1, "image" to 1'):
                self.assertIn(value, text)

    def test_desktop_browser_unsupported_both_entry_points_preserve_current_dom_with_zero_real_requests(self):
        for klass, encodings in (
            ("DesktopWebViewContentPolicyAcceptanceTest", 'listOf("utf-8", "utf8", "UTF-8", "UTF8")'),
            ("BrowserWebViewContentPolicyAcceptanceTest", 'listOf("utf-8", "utf8")'),
        ):
            text = source(klass)
            for value in ('listOf("state", "navigator")', '"additionalHttpHeaders"', '"baseUrl"', 'it.code == -2',
                          '"$entry-headers", "get" to 0', '"$entry-base", "get" to 0, "script" to 0, "style" to 0, "image" to 0',
                          encodings, 'assertSame(native, state.'):
                self.assertIn(value, text)
            self.assertIn("outerHTML", text)

    def test_jvm_transport_helpers_are_byte_identical_finite_owned_sockets_and_main_only_authentication(self):
        name = "OwnedWebViewContentPolicyHttpFixture.kt"
        desktop = (ROOT / (PREFIX.format(set="desktopTest") + name)).read_bytes()
        android = (ROOT / (PREFIX.format(set="androidDeviceTest") + name)).read_bytes()
        self.assertEqual(desktop, android)
        text = desktop.decode()
        self.assertNotIn("@Test", text)
        for value in ('InetAddress.getByName("127.0.0.1")', "repeat(2)", "ArrayBlockingQueue(16)",
                      "ThreadPoolExecutor(8, 8", "connections.incrementAndGet() <= 512", "raw.size() < 8192",
                      'size in 0..512', 'count.getValue("get") + count.getValue("post") < 12',
                      'asset == null && method == "headers" && stage.endsWith("-initial")', "403",
                      "sockets.toList().forEach(::closeSocket)", "workers.awaitTermination(4, TimeUnit.SECONDS)", "assertHealthy()"):
            self.assertIn(value, text)
        counter_block = text.split("val counters = listOf(", 1)[1].split("fun create(", 1)[0]
        self.assertEqual(20, len(re.findall(r'"([a-z_]+)"', counter_block)))

    def test_python_native_transport_binds_source_actual_process_and_private_environment_without_system_mutation(self):
        text = (ROOT / "scripts/ci/webview_content_policy_fixture.py").read_text()
        tree = ast.parse(text)
        imports = [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        imports += [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names]
        self.assertFalse(set(imports) & {"subprocess", "os", "ios_ui_application", "ios_webview_request_fixture", "library_tests"})
        for value in ("def bind_application(", "def launch_environment(", "def validate_receipt(", "self.methods not in (IOS_METHODS, IOS_RESTORE_METHODS)",
                      "self._process not in (None, pid)", '"SIMCTL_CHILD_" + name', "environment = dict(inherited)",
                      "complete_native_stages(document[\"methods\"], selected)", "process_sha256(native_pid)",
                      'listener.bind(("127.0.0.1", 0))', '"native_helper_sha256"', '"owned_workers_terminated"',
                      "independent(close_listener)", "independent(close_workers)"):
            self.assertIn(value, text)
        self.assertNotRegex(text, r"(?:os\.environ|sys\.environ)\s*(?:\[|\.update)")

    def test_browser_receipts_require_real_origin_source_trust_and_actual_public_owner_disconnect_cleanup(self):
        helper = (ROOT / (PREFIX.format(set="webTest") + "BrowserContentPolicyFixture.kt")).read_text()
        for value in ("message.source === native.contentWindow", "message.origin == origin", "message.isTrusted",
                      'window.location.hostname in listOf("localhost", "127.0.0.1")', "own.dispose()",
                      'window.removeEventListener("message", listener)', "native.remove()"):
            self.assertIn(value, helper)
        text = source("BrowserWebViewContentPolicyAcceptanceTest")
        self.assertIn("state.iframe == null && state.owner == null && native?.isConnected != true", text)
        self.assertIn("BrowserSandboxPolicy.Trusted", text)
        middleware = (ROOT / "nativecmpkit-webview/karma.config.d/nativecmpkit-content-policy-fixture.js").read_text()
        for value in ("Object.prototype.hasOwnProperty.call", "!owns(stages, method)", "!owns(session.rows, action)",
                      "owns(session.rows, extra)", "session.pending.size >= 16", "++session.connections > 512", "counts.get + counts.post >= 12",
                      "lease.response.destroy()", "Promise.all(pending.map(lease => lease.closed))", ", 2000)",
                      "window.location.origin)"):
            self.assertIn(value, middleware)
        self.assertNotRegex(middleware, r"(?:server|process)\.(?:close|kill|exit)\s*\(")

    def test_documentation_separates_original_criteria_source_red_transport_controls_and_pending_native_acceptance(self):
        text = (ROOT / "docs/testing/webview-content-policy.md").read_text()
        for value in ("source preparation", "14 methods", "17 executions", "stale-metadata source hazard",
                      "not a failure observed on a device", "transport ownership only", "protocol.observed_launch_pid",
                      "No OS process-death execution", "not yet registered", "at least 8 GiB free",
                      "including", "not an observed provider fact", "Unchanged"):
            if value == "Unchanged":
                self.assertIn("unchanged", text)
            else:
                self.assertIn(value, text)
        self.assertIn(proposal()["important_affected_existing_saver_seam"].split(PACKAGE, 1)[1], text)


if __name__ == "__main__":
    unittest.main()
