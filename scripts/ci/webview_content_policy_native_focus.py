# SPDX-License-Identifier: Apache-2.0
"""Five exact WebView source/selector/XML profiles, never compiler/native acceptance.

The author's four classes/fourteen bodies and all older native inputs stay authored.
Android adds one zero-test lossless JUnit Filter for NEW4 plus only affected saver1.
"""
from __future__ import annotations

import hashlib
import re

from ios_popover_anchor_plan import _ordinary_bytes
from webview_content_policy_source_pins import CONTRACT_INPUT_SHA256

SOURCE = "scripts/ci/webview_content_policy_native_focus.py"
SPEC_RELATIVE = "scripts/ci/fixtures/webview-content-policy-routing-source-inverse.json"
MODULE = "nativecmpkit-webview"
DESKTOP_FOCUS = "webview-content-policy-linux"
ANDROID_FOCUS = "webview-content-policy-android"
ANDROID_RESTORE_FOCUS = "webview-content-policy-android-restore"
ANDROID_FOCUSES = (ANDROID_FOCUS, ANDROID_RESTORE_FOCUS)
JS_FOCUS = "webview-content-policy-js"
WASM_FOCUS = "webview-content-policy-wasm"
IOS_FOCUS = "ios-webview-content-policy"
IOS_RESTORE_FOCUS = "ios-webview-content-policy-restore"
IOS_FOCUSES = (IOS_FOCUS, IOS_RESTORE_FOCUS)
FOCUSES = (DESKTOP_FOCUS, ANDROID_FOCUS, JS_FOCUS, WASM_FOCUS, *IOS_FOCUSES, ANDROID_RESTORE_FOCUS)
CONTRACT_FIELD = "webview_content_policy_source_contract"
ANDROID_FILTER_CLASS = "io.github.apdelrahman1911.nativecmpkit.ui.web.AndroidContentPolicyVerificationFilter"
ANDROID_FILTER_SOURCE = "nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidContentPolicyVerificationFilter.kt"
ANDROID_AFFECTED_CLASS = "io.github.apdelrahman1911.nativecmpkit.ui.web.AndroidWebViewLifetimeDeviceTest"
ANDROID_AFFECTED_METHOD = "retainedStateReleasesRepeatedRealActivitiesAndViewsAndRestoresSerializedNativeState"
ANDROID_AFFECTED_SOURCE = "nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidWebViewLifetimeDeviceTest.kt"
ANDROID_NETWORK_SOURCES = (
    "nativecmpkit-webview/src/androidDeviceTest/AndroidManifest.xml",
    "nativecmpkit-webview/src/androidDeviceTest/res/xml/nativecmpkit_webview_test_network_security.xml",
)
ANDROID_SAVER_SOURCE = "nativecmpkit-webview/src/androidMain/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/WebView.android.kt"
IOS_HOST_CONTROL = "nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeWebViewApplicationHostTest.kt"
IOS_FIXTURE = "scripts/ci/webview_content_policy_fixture.py"
IOS_HELPER = "nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/IosContentPolicyFixture.kt"
_METHOD = re.compile(r"@Test\s+fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)")
_DISABLED = re.compile(r"@(Ignore|Disabled|IgnoredTest)\b")

SPECS = {'webview-content-policy-linux': {'profile': 'webview-content-policy-linux',
                                  'focus': 'webview-content-policy-linux',
                                  'slot': 'desktop-linux-x64',
                                  'suite': 'desktop',
                                  'task': ':nativecmpkit-webview:desktopTest',
                                  'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.web.DesktopWebViewContentPolicyAcceptanceTest',
                                  'source': 'nativecmpkit-webview/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/DesktopWebViewContentPolicyAcceptanceTest.kt',
                                  'methods': ('savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory',
                                              'documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved',
                                              'unsupportedHeadersAndBaseUrlRefuseBeforeNetworkForBothEntryPoints'),
                                  'helpers': ('nativecmpkit-webview/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/DesktopContentPolicyWindow.kt',
                                              'nativecmpkit-webview/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/OwnedWebViewContentPolicyHttpFixture.kt'),
                                  'report_directory': 'nativecmpkit-webview/build/test-results/desktopTest'},
 'webview-content-policy-android': {'profile': 'webview-content-policy-android',
                                    'focus': 'webview-content-policy-android',
                                    'slot': 'android-device-api35',
                                    'suite': 'android-device',
                                    'task': ':nativecmpkit-webview:connectedAndroidDeviceTest',
                                    'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.web.AndroidWebViewContentPolicyAcceptanceTest',
                                    'source': 'nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidWebViewContentPolicyAcceptanceTest.kt',
                                    'methods': ('savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory',
                                                'documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved',
                                                'initialHeadersRedirectsAndSubresourcesMatchStateAndNavigatorPolicy',
                                                'relativeResourcesPreserveSupportedUnicodeEncoding'),
                                    'helpers': ('nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/OwnedWebViewContentPolicyHttpFixture.kt',
                                                'nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidWebViewLifetimeDeviceTest.kt'),
                                    'report_directory': 'nativecmpkit-webview/build/outputs/androidTest-results/connected/androidMain'},
 'webview-content-policy-js': {'profile': 'webview-content-policy-js',
                               'focus': 'webview-content-policy-js',
                               'slot': 'browser-js',
                               'suite': 'js',
                               'task': ':nativecmpkit-webview:jsBrowserTest',
                               'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.web.BrowserWebViewContentPolicyAcceptanceTest',
                               'source': 'nativecmpkit-webview/src/webTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/BrowserWebViewContentPolicyAcceptanceTest.kt',
                               'methods': ('savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory',
                                           'documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved',
                                           'unsupportedHeadersAndBaseUrlRefuseBeforeNetworkForBothEntryPoints'),
                               'helpers': ('nativecmpkit-webview/src/webTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/BrowserContentPolicyFixture.kt',
                                           'nativecmpkit-webview/karma.config.d/nativecmpkit-content-policy-fixture.js'),
                               'report_directory': 'nativecmpkit-webview/build/test-results/jsBrowserTest'},
 'webview-content-policy-wasm': {'profile': 'webview-content-policy-wasm',
                                 'focus': 'webview-content-policy-wasm',
                                 'slot': 'browser-wasm',
                                 'suite': 'wasm',
                                 'task': ':nativecmpkit-webview:wasmJsBrowserTest',
                                 'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.web.BrowserWebViewContentPolicyAcceptanceTest',
                                 'source': 'nativecmpkit-webview/src/webTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/BrowserWebViewContentPolicyAcceptanceTest.kt',
                                 'methods': ('savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory',
                                             'documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved',
                                             'unsupportedHeadersAndBaseUrlRefuseBeforeNetworkForBothEntryPoints'),
                                 'helpers': ('nativecmpkit-webview/src/webTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/BrowserContentPolicyFixture.kt',
                                             'nativecmpkit-webview/karma.config.d/nativecmpkit-content-policy-fixture.js'),
                                 'report_directory': 'nativecmpkit-webview/build/test-results/wasmJsBrowserTest'},
 'ios-webview-content-policy': {'profile': 'ios-webview-content-policy',
                                'focus': 'ios-webview-content-policy',
                                'slot': 'ios-iphone',
                                'suite': 'ios',
                                'task': ':nativecmpkit-webview:iosSimulatorArm64ApplicationTest',
                                'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.web.IosWebViewContentPolicyAcceptanceTest',
                                'source': 'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/IosWebViewContentPolicyAcceptanceTest.kt',
                                'methods': ('savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory',
                                            'documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved',
                                            'initialHeadersRedirectsAndSubresourcesMatchStateAndNavigatorPolicy',
                                            'relativeResourcesPreserveSupportedUnicodeEncoding'),
                                'helpers': ('nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/IosContentPolicyFixture.kt',
                                            'scripts/ci/webview_content_policy_fixture.py',
                                            'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeWebViewApplicationHost.kt',
                                            'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeObjectIdentity.kt'),
                                'report_directory': 'nativecmpkit-webview/build/test-results/iosSimulatorArm64ApplicationTest'}}

SOURCE_SHA256 = {'nativecmpkit-webview/karma.config.d/nativecmpkit-content-policy-fixture.js': 'c78874d7622fa8a507d68735305a989a5fc21b0a072098532473e6c586212d81',
 'nativecmpkit-webview/src/androidDeviceTest/AndroidManifest.xml': 'fdf8777e220cdc5f9e6ce133027821e3a908f1e144db0698ba1a89bcadc1e562',
 'nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidContentPolicyVerificationFilter.kt': 'e461bcc12a49dbe3b4a72c6b762ce0ca0fb1b4135accaecf2b07db5d2fa5e706',
 'nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidWebViewContentPolicyAcceptanceTest.kt': '5c6f334c2ad3145accf540f5985b4a89f6630101677447bf4ff1f6565ae06f23',
 'nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/AndroidWebViewLifetimeDeviceTest.kt': '8b6d5b4f49d534391d5ba92cbd836bc26562caa034d040a4604884d79967de7b',
 'nativecmpkit-webview/src/androidDeviceTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/OwnedWebViewContentPolicyHttpFixture.kt': 'be3c9d172f7ce95bf070af874170db2ed262793ff483e457a91f1be3a78bb92e',
 'nativecmpkit-webview/src/androidDeviceTest/res/xml/nativecmpkit_webview_test_network_security.xml': 'd41572dbbaf67ec740c28ed69a8c5fce4223329c4c96d726f1df9a08f95de71d',
 'nativecmpkit-webview/src/androidMain/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/WebView.android.kt': '2a33704f075e1cbef2b8a2fe538d945b8e52aa7a3536cfdf0329781aaf688c5f',
 'nativecmpkit-webview/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/DesktopContentPolicyWindow.kt': 'f12040dc853bbbee03b0e1ef7c589329482e97affd675cd6afa4f261cf9c4716',
 'nativecmpkit-webview/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/DesktopWebViewContentPolicyAcceptanceTest.kt': '0efd10133e800ba6724ed89f66f2a1c54e20e4195fec896caedbc7e3aeac2450',
 'nativecmpkit-webview/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/OwnedWebViewContentPolicyHttpFixture.kt': 'be3c9d172f7ce95bf070af874170db2ed262793ff483e457a91f1be3a78bb92e',
 'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/IosContentPolicyFixture.kt': 'dd372e8d89e672a31aa14c8fe714894b111d149626c16918467ede1280f2a703',
 'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/IosWebViewContentPolicyAcceptanceTest.kt': '94d41e5b77d32cadff53dd812a687833d5cc871346d39a7931268557782cabbe',
 'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeObjectIdentity.kt': 'cc9b988cc03586fa535bfa8f3be66e0581252611fdfb6db12fa2606b48d09ee6',
 'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeWebViewApplicationHost.kt': '4177b7ed6f2d0040ffe72545eea6f7a02ff002bc22cbba46026d937bceb06d50',
 'nativecmpkit-webview/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/internal/NativeWebViewApplicationHostTest.kt': '24bdf9d5b96aaf13597e08f25be408d60b76311d3c30ad1726129e3205adc8c1',
 'nativecmpkit-webview/src/webTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/BrowserContentPolicyFixture.kt': '513d9a85877761382e7af458b1bc3eccaadb3d8f921e6472789b9dbbaae55293',
 'nativecmpkit-webview/src/webTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/web/BrowserWebViewContentPolicyAcceptanceTest.kt': '2acc1ff9fe88d113b6881ae80211f2046dd567ba5331b855ad3ab9f51e064b1b',
 'scripts/ci/webview_content_policy_fixture.py': '77b73b9bca3a479ce8c16f7a4c8e596520514a3e4057ce30efc18953d10f5fe9'}


def spec(focus: str) -> dict:
    if type(focus) is not str or focus not in FOCUSES:
        raise ValueError("An exact content-policy focus is required")
    if focus == IOS_RESTORE_FOCUS:
        owner = SPECS[IOS_FOCUS]
        return {**owner, "focus": focus, "methods": owner["methods"][:1]}
    if focus == ANDROID_RESTORE_FOCUS:
        owner = SPECS[ANDROID_FOCUS]
        return {**owner, "focus": focus, "methods": owner["methods"][:2]}
    return SPECS[focus]


def allowed(suite: str, modules: tuple[str, ...] | None, focus: str) -> bool:
    return (type(focus) is str and focus in FOCUSES and suite == spec(focus)["suite"] and modules == (MODULE,))


def groups(focus: str) -> tuple[dict, ...]:
    row = spec(focus)
    group = {"classname": row["classname"], "source": row["source"], "methods": row["methods"]}
    if focus == IOS_RESTORE_FOCUS:
        group["declared_methods"] = SPECS[IOS_FOCUS]["methods"]
    selected = (group,)
    if focus == ANDROID_FOCUS:
        selected += ({"classname": ANDROID_AFFECTED_CLASS, "source": ANDROID_AFFECTED_SOURCE,
                      "methods": (ANDROID_AFFECTED_METHOD,)},)
    return selected


def identities(focus: str) -> list[dict]:
    row = spec(focus)
    prefix = "iosSimulatorArm64ApplicationTest." if focus in IOS_FOCUSES else ""
    suffix = "[iosSimulatorArm64]" if focus in IOS_FOCUSES else "[desktop]" if focus == DESKTOP_FOCUS else ""
    return [{"classname": prefix + group["classname"], "name": method + suffix}
            for group in groups(focus) for method in group["methods"]]


def selector(focus: str) -> str:
    row = spec(focus)
    if focus == ANDROID_FOCUS:
        return ANDROID_FILTER_CLASS
    if focus == ANDROID_RESTORE_FOCUS:
        return ",".join(row["classname"] + "#" + method for method in row["methods"])
    if focus in IOS_FOCUSES:
        return ",".join(row["classname"] + "." + method for method in row["methods"])
    return row["classname"]


def sources(focus: str) -> tuple[str, ...]:
    row = spec(focus)
    selected = {row["source"], *row["helpers"]}
    if focus in ANDROID_FOCUSES:
        selected.update((*ANDROID_NETWORK_SOURCES, ANDROID_SAVER_SOURCE, ANDROID_FILTER_SOURCE))
    if focus in IOS_FOCUSES:
        selected.add(IOS_HOST_CONTROL)
    return tuple(sorted(selected))


def validate_sources(root, focus: str) -> bool:
    row = spec(focus)
    payload = {name: _ordinary_bytes(root, name)[0] for name in sources(focus)}
    for name, raw in payload.items():
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256[name]:
            raise ValueError("Exact content-policy native/helper/source image changed: " + name)
    source = payload[row["source"]].decode("utf-8")
    package, classname = row["classname"].rsplit(".", 1)
    owner = {IOS_RESTORE_FOCUS: IOS_FOCUS, ANDROID_RESTORE_FOCUS: ANDROID_FOCUS}.get(focus, focus)
    declarations = SPECS[owner]["methods"]
    if (_METHOD.findall(source) != list(declarations) or _DISABLED.search(source) or
            not re.search(r"(?m)^package\s+" + re.escape(package) + r"\s*$", source) or
            not re.search(r"\bclass\s+" + re.escape(classname) + r"\s*\{", source)):
        raise ValueError("Exact enabled content-policy native declarations are required")
    if focus in ANDROID_FOCUSES:
        helper = payload[ANDROID_FILTER_SOURCE].decode("utf-8")
        if (_METHOD.search(helper) or _DISABLED.search(helper) or
                "class AndroidContentPolicyVerificationFilter : Filter()" not in helper):
            raise ValueError("One exact public no-arg zero-test JUnit Filter is required")
    return True


def _contract(focus: str) -> dict:
    row = spec(focus)
    pins = {name: SOURCE_SHA256[name] for name in sources(focus)} | CONTRACT_INPUT_SHA256
    return {"schema_version": 1, "focus": focus, "module": MODULE, "suite": row["suite"],
            "task": row["task"], "selected_testcases": identities(focus), "source_hashes": pins,
            "new_methods": len(row["methods"]), "affected_existing_methods": int(focus == ANDROID_FOCUS),
            "compiler_executions_attested": 0, "native_executions_attested": 0}


def source_contract(root, focus: str) -> dict:
    validate_sources(root, focus)
    wanted = _contract(focus)
    for name, digest in wanted["source_hashes"].items():
        if hashlib.sha256(_ordinary_bytes(root, name)[0]).hexdigest() != digest:
            raise ValueError("Current content-policy owner/native manifest identity changed: " + name)
    return wanted


def configure_item(root, item: dict, focus: str) -> None:
    row = spec(focus)
    contract = source_contract(root, focus)
    item.update(test_filter=selector(focus), required_testcases=identities(focus), required_original_xml=1)
    item[CONTRACT_FIELD] = contract
    # Normal Kotlin source-set inheritance is retained, not narrowed or rewritten.
    item["test_source_files"] = sorted(set(item["test_source_files"]) | set(contract["source_hashes"]))
    if focus in ANDROID_FOCUSES:
        item.update(test_filter_argument="filter" if focus == ANDROID_FOCUS else "class", verification_api_level=35,
                    native_fixture_paths=[*ANDROID_NETWORK_SOURCES, row["helpers"][0],
                                          ANDROID_AFFECTED_SOURCE, ANDROID_FILTER_SOURCE])
    elif focus in (JS_FOCUS, WASM_FOCUS):
        item["browser_http_fixture"] = row["helpers"][1]


def validate_plan(test_plan: dict) -> bool:
    focus = test_plan.get("explicit_test_focus")
    row = spec(focus)
    expected = test_plan.get("expected")
    if (type(expected) is not list or len(expected) != 1 or test_plan.get("suite") != row["suite"] or
            test_plan.get("explicit_module_subset") != [MODULE] or test_plan.get("complete_suite_requested") is not False):
        raise ValueError("Content policy requires one exact finite suite and nativecmpkit-webview module")
    item = expected[0]; contract = item.get(CONTRACT_FIELD)
    wanted = _contract(focus)
    if (item.get("module") != MODULE or item.get("project") != ":nativecmpkit-webview" or
            item.get("task") != row["task"] or item.get("report_directory") != row["report_directory"] or
            item.get("test_filter") != selector(focus) or item.get("required_testcases") != identities(focus) or
            type(item.get("required_original_xml")) is not int or item["required_original_xml"] != 1 or
            contract != wanted or type(contract.get("schema_version")) is not int or
            any(type(contract.get(key)) is not int for key in
                ("new_methods", "affected_existing_methods", "compiler_executions_attested", "native_executions_attested")) or
            not set(wanted["source_hashes"]) <= set(item.get("test_source_files", []))):
        raise ValueError("Content policy requires exact task, class, methods, sources and original XML identity")
    if focus in ANDROID_FOCUSES:
        if (item.get("test_filter_argument") != ("filter" if focus == ANDROID_FOCUS else "class") or item.get("test_exclusion_annotation") is not None or
                type(item.get("verification_api_level")) is not int or item["verification_api_level"] != 35 or
                item.get("agp_declared_xml_directory") != "nativecmpkit-webview/build/intermediates/android_test_results/androidMain/connectedAndroidDeviceTest" or
                item.get("utp_results_directory") != row["report_directory"] or
                item.get("native_fixture_paths") != [*ANDROID_NETWORK_SOURCES, row["helpers"][0],
                                                    ANDROID_AFFECTED_SOURCE, ANDROID_FILTER_SOURCE]):
            raise ValueError("Android content policy requires exact lossless filter and API35 native5 report")
    elif focus in IOS_FOCUSES:
        if (item.get("native_test_host") != "genuine-uikit-application" or
                item.get("test_filter_argument") is not None or item.get("test_exclusion_annotation") is not None):
            raise ValueError("iOS content policy requires the actual owned UIKit application")
    elif (item.get("native_test_host") is not None or item.get("test_filter_argument") is not None or
          item.get("test_exclusion_annotation") is not None):
        raise ValueError("Content-policy host cannot be replaced by a foreign native application")
    if focus in (JS_FOCUS, WASM_FOCUS) and item.get("browser_http_fixture") != row["helpers"][1]:
        raise ValueError("Browser content policy requires its own unchanged Karma fixture")
    return True


def validate_host(focus: str, system: str, machine: str) -> None:
    spec(focus)
    if focus == DESKTOP_FOCUS and (system != "Linux" or machine.lower() not in ("x86_64", "amd64", "x64")):
        raise ValueError("Desktop content policy is registered only for Linux x64")


def case_inventory(focus: str, cases: list[dict]) -> bool:
    row = spec(focus)
    if type(cases) is not list or len(cases) != len(identities(focus)) or any(type(case) is not dict for case in cases):
        return False
    if focus in (JS_FOCUS, WASM_FOCUS):
        task = row["task"].rsplit(":", 1)[1]
        target = "js" if focus == JS_FOCUS else "wasmJs"
        methods = []
        for case in cases:
            name = case.get("name")
            if type(name) is not str or case.get("classname") != task + "." + row["classname"]:
                return False
            method, separator, suffix = name.partition("[")
            if not separator or not re.fullmatch(re.escape(target) + r", browser, [^\[\]\r\n]+\]", suffix):
                return False
            methods.append(method)
        return len(set(methods)) == len(row["methods"]) and set(methods) == set(row["methods"])
    if any(type(case.get("classname")) is not str or type(case.get("name")) is not str for case in cases):
        return False
    return {(case.get("classname"), case.get("name")) for case in cases} == {
        (case["classname"], case["name"]) for case in identities(focus)}


def scope(focus: str) -> str:
    row = spec(focus)
    return (f"Only NEW{len(row['methods'])}" + (" plus exactly the affected existing Android saver native-history/Reload method" if focus == ANDROID_FOCUS else "") +
            "; actual target-native DOM/document/wire/history observations and one fresh exact original task XML remain mandatory. "
            "iOS separately requires nonce/process/install/source-bound localhost fixture, real Worker/protocol/runtime/binary agreement and independent cleanup. "
            "All other accepted native bodies remain authored and unselected. No unchanged replay, full ios/all admission, issue closure, API-ABI, consumer, dependency, security or release/publication certification.")
