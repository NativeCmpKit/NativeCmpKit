# SPDX-License-Identifier: Apache-2.0
"""Finite related UI wiring, not a replacement native transport or compiler result.

One genuine iOS26+ owned application selects adaptive4 plus NEW drag/shader6;
pre26 adaptive4 remains independently required. Source admission and model XML
controls are not native execution, hardware profiling or issue acceptance.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import ios_adaptive_controls_native_focus as adaptive
import ios_adaptive_controls_runtime as adaptive_runtime
from ios_popover_anchor_plan import _ordinary_bytes, _unique_object

FOCUSES = ("ui-native-adaptive-pre26", "ui-native-adaptive-drag-shader-ios26plus")
# Legacy four/ten are immutable selections. These two disjoint requests are
# diagnostic isolation, not acceptance of any outcome from the failed UI650 ten.
SPLIT_FOCUSES = ("ui-native-related-nine-ios26plus", "ui-native-adaptive-customization-ios26plus")
PRE26_RECOVERY_FOCUSES = ("ui-native-adaptive-customization-pre26", "ui-native-adaptive-remaining-pre26")
PRE26_PENDING_FOCUSES = ("ui-native-adaptive-negative-steps-pre26", "ui-native-adaptive-toolbar-pre26")
ALL_FOCUSES = FOCUSES + SPLIT_FOCUSES + PRE26_RECOVERY_FOCUSES + PRE26_PENDING_FOCUSES
MODULE = "nativecmpkit-ui"
TASK_NAME = "iosSimulatorArm64ApplicationTest"
TASK = ":nativecmpkit-ui:" + TASK_NAME
SCOPE = ("One actually matching iOS26+ owned application: four adaptive public-control methods "
         "plus six NEW actual drag/shader/resource/construction methods. Separate genuine pre26 "
         "adaptive4 remains required, never N/A or simulated. No old8/other-OS accepted replay, "
         "physical hardware, Instruments, all-OS, consumer/API-ABI/security/release or issue closure claim.")
_METHOD = re.compile(r"@Test\s+fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)")
_DISABLED = re.compile(r"@(Ignore|Disabled|IgnoredTest)\b")
_SELECTIONS = {'ui-native-adaptive-drag-shader-ios26plus': {'focus_property': 'nativecmpkitUiRelatedFocus',
                                              'groups': [{'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.slider.AdaptiveSliderNativeMatrixTest',
                                                          'declared_methods': ['pre26PublicStepsTapDragAndAccessibilityMatrix',
                                                                               'ios26PublicStepsTapDragAndAccessibilityMatrix',
                                                                               'pre26PublicNegativeStepsAreRejected',
                                                                               'ios26PublicNegativeStepsAreRejected'],
                                                          'methods': ['ios26PublicStepsTapDragAndAccessibilityMatrix',
                                                                      'ios26PublicNegativeStepsAreRejected'],
                                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/slider/AdaptiveSliderNativeMatrixTest.kt'},
                                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.controls.AdaptiveControlCustomizationMatrixTest',
                                                          'declared_methods': ['pre26CustomColorsContentAndInteractionsSurviveDarkAndLargeText',
                                                                               'ios26CustomColorsContentAndInteractionsSurviveDarkAndLargeText'],
                                                          'methods': ['ios26CustomColorsContentAndInteractionsSurviveDarkAndLargeText'],
                                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlCustomizationMatrixTest.kt'},
                                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.toolbar.AdaptiveToolbarFallbackNativeTest',
                                                          'declared_methods': ['pre26EmptyAndPopulatedItemsRenderMaterialSlotsAndCallerPlacement',
                                                                               'ios26EmptyItemsRenderMaterialSlotsAndCallerPlacement'],
                                                          'methods': ['ios26EmptyItemsRenderMaterialSlotsAndCallerPlacement'],
                                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toolbar/AdaptiveToolbarFallbackNativeTest.kt'},
                                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.utils.DampedDragLifecycleRegressionTest',
                                                          'declared_methods': ['cancellationFromActualStartAndStopCallbacksCannotRecreateFeedbackAndNextGestureRecovers',
                                                                               'removingAnActiveActualModifierLeavesNoReleaseWorkInTheCallerScopeAndRangeReplacementRecovers',
                                                                               'thousandSustainedUpdatesTraceActualJobTreesAcrossFramesAndRepressWithoutCancellingSiblingWork'],
                                                          'methods': ['cancellationFromActualStartAndStopCallbacksCannotRecreateFeedbackAndNextGestureRecovers',
                                                                      'removingAnActiveActualModifierLeavesNoReleaseWorkInTheCallerScopeAndRangeReplacementRecovers',
                                                                      'thousandSustainedUpdatesTraceActualJobTreesAcrossFramesAndRepressWithoutCancellingSiblingWork'],
                                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/DampedDragLifecycleRegressionTest.kt'},
                                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.utils.InteractiveHighlightResourceLifecycleTest',
                                                          'declared_methods': ['disposingAPressedRetainedModifierClosesItsRealBuilderStopsPixelsAndNeverRestartsItsJobs',
                                                                               'removingAnActualPressedHighlightClosesItsBuilderAndNewCompositionUsesANewOwnedResource'],
                                                          'methods': ['disposingAPressedRetainedModifierClosesItsRealBuilderStopsPixelsAndNeverRestartsItsJobs',
                                                                      'removingAnActualPressedHighlightClosesItsBuilderAndNewCompositionUsesANewOwnedResource'],
                                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/InteractiveHighlightResourceLifecycleTest.kt'},
                                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.button.LiquidButtonConstructionTraceTest',
                                                          'declared_methods': ['hundredActualPublicButtonsKeepOptionalShaderConstructionAtZeroThroughInputDisableAndRecreation'],
                                                          'methods': ['hundredActualPublicButtonsKeepOptionalShaderConstructionAtZeroThroughInputDisableAndRecreation'],
                                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/button/LiquidButtonConstructionTraceTest.kt'}],
                                              'init_script': 'scripts/ci/ios_ui_adaptive_drag_shader_native.init.gradle.kts',
                                              'runtime_focus': 'ui-native-adaptive-ios26plus',
                                              'test_sources': ['nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlNativeHost.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/slider/AdaptiveSliderNativeMatrixTest.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlCustomizationMatrixTest.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toolbar/AdaptiveToolbarFallbackNativeTest.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHost.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/DampedDragLifecycleRegressionTest.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/InteractiveHighlightResourceLifecycleTest.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/button/LiquidButtonConstructionTraceTest.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/UiDragShaderTestHost.kt',
                                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/PointerCancellation.kt']},
 'ui-native-adaptive-pre26': {'focus_property': 'nativecmpkitAdaptiveControlsFocus',
                              'groups': [{'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.slider.AdaptiveSliderNativeMatrixTest',
                                          'declared_methods': ['pre26PublicStepsTapDragAndAccessibilityMatrix',
                                                               'ios26PublicStepsTapDragAndAccessibilityMatrix',
                                                               'pre26PublicNegativeStepsAreRejected',
                                                               'ios26PublicNegativeStepsAreRejected'],
                                          'methods': ['pre26PublicStepsTapDragAndAccessibilityMatrix',
                                                      'pre26PublicNegativeStepsAreRejected'],
                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/slider/AdaptiveSliderNativeMatrixTest.kt'},
                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.controls.AdaptiveControlCustomizationMatrixTest',
                                          'declared_methods': ['pre26CustomColorsContentAndInteractionsSurviveDarkAndLargeText',
                                                               'ios26CustomColorsContentAndInteractionsSurviveDarkAndLargeText'],
                                          'methods': ['pre26CustomColorsContentAndInteractionsSurviveDarkAndLargeText'],
                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlCustomizationMatrixTest.kt'},
                                         {'classname': 'io.github.apdelrahman1911.nativecmpkit.ui.toolbar.AdaptiveToolbarFallbackNativeTest',
                                          'declared_methods': ['pre26EmptyAndPopulatedItemsRenderMaterialSlotsAndCallerPlacement',
                                                               'ios26EmptyItemsRenderMaterialSlotsAndCallerPlacement'],
                                          'methods': ['pre26EmptyAndPopulatedItemsRenderMaterialSlotsAndCallerPlacement'],
                                          'source': 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toolbar/AdaptiveToolbarFallbackNativeTest.kt'}],
                              'init_script': 'scripts/ci/ios_adaptive_controls_native.init.gradle.kts',
                              'runtime_focus': 'ui-native-adaptive-pre26',
                              'test_sources': ['nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlNativeHost.kt',
                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/slider/AdaptiveSliderNativeMatrixTest.kt',
                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlCustomizationMatrixTest.kt',
                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toolbar/AdaptiveToolbarFallbackNativeTest.kt',
                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHost.kt',
                                               'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt']}}
SOURCE_SHA256 = {'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/button/LiquidButtonConstructionTraceTest.kt': 'dc8931c905b9d29fc14ef5dac53161789e0af080fefc74a67fec578dc11f9471',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlCustomizationMatrixTest.kt': 'c792203a97cc8bdea914856b5cd53195f7a623170820fbc3f91a4ef9fd55d61d',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlNativeHost.kt': '6103a635e38a0260d2dfe8e01c33ea6534c186119e93a97b8561693f1e97bac3',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt': '262319f38945fb86e292934f619695f1acb061cd12cb33527d0bbf9f0a4eacc8',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHost.kt': '2594edcf1060ae1bc54cf8b35cda81011306d6c182b0bebc183b492ea42fd698',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/PointerCancellation.kt': '5ad05e4614cf83c1402f2df8b8dbaa7424c1bb4931065e7acd5c4d39e66493a6',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/slider/AdaptiveSliderNativeMatrixTest.kt': 'c3287592a1f410df9db9d162b8899701f469f5b7405344353d551633abcc7b48',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toolbar/AdaptiveToolbarFallbackNativeTest.kt': 'ae4042dd54821a812a7a993cdfb69ceba8d87c648d938ce16009ef4cb6c4ea2e',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/DampedDragLifecycleRegressionTest.kt': 'e510be8cf46bb9df5a21489dbcfb324d2d4643cb6f98a91818c06accdfb15aae',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/InteractiveHighlightResourceLifecycleTest.kt': 'e4c10d40b659913a83e7ae6ff6eb50e4d981046f556bd01b33e8feb4d856f508',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/UiDragShaderTestHost.kt': '6b02f069769c8925b65e9896887415b32f45259eed680b9afefbf9dd0a1c744b'}
INIT_SHA256 = {'ui-native-adaptive-drag-shader-ios26plus': 'd1ca8aa762529030099ab2e68c67788ce718e7163659b4c4544c76442fda26fd',
 'ui-native-adaptive-pre26': 'c8ed4c647c4d44ccc72f05480d58bbf9a9e77077bd55a40560e998878f2726a4'}
# The earlier customization image is retained in the archived inverse. The
# runtime uses the renamed image of the reviewed screenshot/phase derivative.
CURRENT_CUSTOM_SOURCE_SHA256 = "b9a4cd85d69ae206989118a4bc1730701cf7813f12193d03832eb25785dca490"
_RELATED_TEN = _SELECTIONS[FOCUSES[1]]
_CUSTOM_SOURCE = adaptive.CUSTOM_SOURCE
_PRE26 = _SELECTIONS[FOCUSES[0]]
for _focus, _custom, _scope in (
    (PRE26_RECOVERY_FOCUSES[0], True, "The one unfinished pre-iOS 26 customization case in its own UIKit session."),
    (PRE26_RECOVERY_FOCUSES[1], False, "The three pre-iOS 26 slider and toolbar cases in a separate UIKit session."),
):
    _SELECTIONS[_focus] = {
        **_PRE26,
        "groups": [{**group, "methods": group["methods"] if (group["source"] == _CUSTOM_SOURCE) == _custom else []}
                   for group in _PRE26["groups"]],
        "scope": _scope,
    }
    INIT_SHA256[_focus] = INIT_SHA256[FOCUSES[0]]
for _focus, _method in zip(PRE26_PENDING_FOCUSES, (
    "pre26PublicNegativeStepsAreRejected", "pre26EmptyAndPopulatedItemsRenderMaterialSlotsAndCallerPlacement",
)):
    _SELECTIONS[_focus] = {
        **_PRE26,
        "groups": [{**group, "methods": [method for method in group["methods"] if method == _method]}
                   for group in _PRE26["groups"]],
        "scope": "One unfinished pre-iOS 26 case with independent native transport and test reporting.",
    }
    INIT_SHA256[_focus] = INIT_SHA256[FOCUSES[0]]
_SELECTIONS[SPLIT_FOCUSES[0]] = {
    **_RELATED_TEN,
    "groups": [group for group in _RELATED_TEN["groups"] if group["source"] != _CUSTOM_SOURCE],
    "test_sources": [name for name in _RELATED_TEN["test_sources"] if name != _CUSTOM_SOURCE],
    "task_name": "iosSimulatorArm64UiNineApplicationTest",
    "init_script": "scripts/ci/ios_ui_split_native.init.gradle.kts",
    "focus_property": "nativecmpkitUiSplitFocus",
    "admission_path": "build/ci-verification/ui-nine-native-source-admission.json",
    "receipt_subdirectory": "native-ui-nine-application",
    "transport_timeout_seconds": 1920,
    "native_task_timeout_seconds": 2400,
    "scope": "Only nine missing UI650 iOS26+ methods, excluding adaptive customization: public slider2/toolbar1 plus actual drag3/highlight2/button-construction1. One exact ten-source/common0 application and fresh task-specific XML/runtime/Worker/owned cleanup decide these nine alone. Adaptive customization1 has an independent application/task/receipt/budget; legacy related10 and genuine pre26four remain intact. No accepted native replay, missing-outcome waiver, compiler/link/native/issue/physical/consumer/API-ABI/security/release inference.",
}
_SELECTIONS[SPLIT_FOCUSES[1]] = {
    **_RELATED_TEN,
    "groups": [group for group in _RELATED_TEN["groups"] if group["source"] == _CUSTOM_SOURCE],
    "test_sources": [name for name in _RELATED_TEN["test_sources"] if name in (
        adaptive.BRANCH_SOURCE, _CUSTOM_SOURCE, adaptive.HOST_SOURCE, adaptive.IDENTITY_SOURCE)],
    "task_name": "iosSimulatorArm64AdaptiveCustomizationApplicationTest",
    "init_script": "scripts/ci/ios_ui_split_native.init.gradle.kts",
    "focus_property": "nativecmpkitUiSplitFocus",
    "admission_path": "build/ci-verification/adaptive-customization-native-source-admission.json",
    "receipt_subdirectory": "native-adaptive-customization-application",
    "transport_timeout_seconds": 600,
    "native_task_timeout_seconds": 2400,
    "scope": "Only the one missing UI650 genuine iOS26+ customization method, exact four-source/common0 application, unchanged actual assertions/waits plus first-row scalar caller phases and fresh screenshot finally-close. Independent600s cooperative console transport bound still fails on timeout; the dedicated2400s native task preserves original owned cleanup. No hang-cause diagnosis, synthetic success, inner-wait relaxation or acceptance of the separate nine/legacy10/pre26four; actual fresh XML/runtime/Worker/owned cleanup remain mandatory. No compiler/link/native/issue/physical/consumer/API-ABI/security/release inference.",
}
for _focus in SPLIT_FOCUSES:
    INIT_SHA256[_focus] = "98a0228646f62d82bfd72aea3b23f0e77031fd0d54bbdec174780a00acf3afdd"


def _selection(focus: str) -> dict:
    if type(focus) is not str or focus not in ALL_FOCUSES:
        raise ValueError("Select only the related iOS26+ ten or independent pre26 four")
    return _SELECTIONS[focus]


def focus_spec(focus: str) -> dict:
    return {"groups": tuple({**group, "methods": tuple(group["methods"]),
                              "declared_methods": tuple(group["declared_methods"])}
                             for group in _selection(focus)["groups"]),
            "module": MODULE, "scope": _selection(focus).get("scope", SCOPE)}


def sources(focus: str) -> tuple[str, ...]:
    return tuple(_selection(focus)["test_sources"])


def selectors(focus: str) -> tuple[str, ...]:
    return tuple(group["classname"] + "." + method
                 for group in focus_spec(focus)["groups"] for method in group["methods"])


def native_request(focus: str) -> list[str]:
    return [task(focus), *(argument for selector in selectors(focus) for argument in ("--tests", selector))]


def validate_request(task_names: list[str], focus: str) -> bool:
    if type(task_names) is not list or task_names != native_request(focus):
        raise ValueError("Related UI native execution requires only its exact ordered ten/four selectors")
    return True


def runtime_focus(focus: str) -> str:
    return _selection(focus)["runtime_focus"]


def init_script(focus: str) -> str:
    return _selection(focus)["init_script"]


def focus_property(focus: str) -> str:
    return _selection(focus)["focus_property"]


def task_name(focus: str) -> str:
    return _selection(focus).get("task_name", TASK_NAME)


def task(focus: str) -> str:
    return ":" + MODULE + ":" + task_name(focus)


def receipt_subdirectory(focus: str) -> str:
    return _selection(focus).get("receipt_subdirectory", "native-ui-application")


def timeout_accounting(focus: str) -> dict[str, int]:
    selection = _selection(focus)
    return {"transport_timeout_seconds": selection.get("transport_timeout_seconds", 1920),
            "native_task_timeout_seconds": selection.get("native_task_timeout_seconds", 2400)}


def source_sha256(focus: str) -> dict[str, str]:
    return {name: CURRENT_CUSTOM_SOURCE_SHA256 if name == _CUSTOM_SOURCE else SOURCE_SHA256[name]
            for name in sources(focus)}


def identities(focus: str) -> list[dict]:
    return [{"classname": task_name(focus) + "." + group["classname"],
             "name": method + "[iosSimulatorArm64]"}
            for group in focus_spec(focus)["groups"] for method in group["methods"]]


def validate_sources(root: Path, focus: str, test_sources: list[str] | None = None) -> bool:
    wanted = sources(focus)
    if test_sources is not None and (type(test_sources) is not list or test_sources != sorted(wanted)):
        raise ValueError("Related UI requires its exact ordinary eleven/six source list, not a superset")
    text = {name: _ordinary_bytes(root, name)[0].decode("utf-8") for name in wanted}
    # Reuse the unchanged actual-UIDevice branch checker; do not replay its old controls.
    adaptive.validate_sources(root, None if focus in SPLIT_FOCUSES else list(wanted))
    for group in focus_spec(focus)["groups"]:
        source = text[group["source"]]
        package, classname = group["classname"].rsplit(".", 1)
        if (_METHOD.findall(source) != list(group["declared_methods"]) or _DISABLED.search(source) or
                not re.search(r"(?m)^package " + re.escape(package) + r"\s*$", source) or
                not re.search(r"\bclass\s+" + re.escape(classname) + r"\s*\{", source)):
            raise ValueError("Related UI must retain every exact enabled authored declaration")
        if group["source"] not in adaptive.SOURCES:
            for method in group["methods"]:
                if re.search(r"@Test\s+fun\s+" + re.escape(method) +
                             r"\s*\(\s*\)\s*\{\s*requireUiDragShaderApplication\(\)", source) is None:
                    raise ValueError("Each real drag/shader method must require the owned Main application")
    declaring = {group["source"] for group in focus_spec(focus)["groups"]}
    if any(re.search(r"@(Test|Ignore|Disabled|IgnoredTest)\b", text[name]) for name in set(wanted) - declaring):
        raise ValueError("Related UI ownership/cancellation/resource helpers must be zero-test ordinary inputs")
    drag_host = adaptive.BASE + "utils/UiDragShaderTestHost.kt"
    if drag_host in text and "onApplicationMain { requireOwnedApplicationWindow(); Unit }" not in text[drag_host]:
        raise ValueError("Drag/shader admission must require the real owned application window on Main")
    for name in wanted:
        raw = text[name].encode()
        if hashlib.sha256(raw).hexdigest() != source_sha256(focus)[name]:
            raise ValueError("Related UI authored source differs from its unchanged reviewed input: " + name)
    if hashlib.sha256(_ordinary_bytes(root, init_script(focus))[0]).hexdigest() != INIT_SHA256[focus]:
        raise ValueError("Related UI native-only init differs from its exact reviewed source admission")
    return True


def _contract(focus: str) -> dict:
    return {"schema_version": 1, "focus": focus, "runtime_focus": runtime_focus(focus),
            "module": MODULE, "task": task(focus), "init_script": init_script(focus),
            "focus_property": focus_property(focus), "init_sha256": INIT_SHA256[focus],
            "selected_methods": list(selectors(focus)), "effective_sources": list(sources(focus)),
            "common_sources": [], "source_sha256": source_sha256(focus),
            "compiler_executions_attested": 0, "apple_links_attested": 0, "native_tests_executed": 0,
            **({"receipt_subdirectory": receipt_subdirectory(focus), **timeout_accounting(focus)}
               if focus in SPLIT_FOCUSES else {})}


def source_contract(root: Path, focus: str) -> dict:
    validate_sources(root, focus)
    return _contract(focus)


def validate_plan(test_plan: dict) -> bool:
    if type(test_plan) is not dict:
        raise ValueError("An exact finite related UI library plan is required")
    focus = test_plan.get("explicit_test_focus")
    wanted = _contract(focus)
    expected = test_plan.get("expected")
    if (test_plan.get("suite") != "ios" or test_plan.get("explicit_module_subset") != [MODULE] or
            test_plan.get("complete_suite_requested") is not False or type(expected) is not list or len(expected) != 1):
        raise ValueError("Related UI requires one explicit finite iOS nativecmpkit-ui application module")
    item = expected[0]
    if (type(item) is not dict or item.get("module") != MODULE or item.get("project") != ":nativecmpkit-ui" or
            item.get("task") != task(focus) or item.get("report_directory") != "nativecmpkit-ui/build/test-results/" + task_name(focus) or
            item.get("native_test_host") != "genuine-uikit-application" or item.get("test_source_sets") != ["iosTest"] or
            item.get("test_source_files") != sorted(sources(focus)) or
            item.get("test_filter") != ",".join(selectors(focus)) or item.get("required_testcases") != identities(focus) or
            item.get("ui_related_source_contract") != wanted or
            type(item["ui_related_source_contract"].get("schema_version")) is not int or
            any(type(item["ui_related_source_contract"].get(key)) is not int
                for key in ("compiler_executions_attested", "apple_links_attested", "native_tests_executed")) or
            (focus in SPLIT_FOCUSES and any(type(item["ui_related_source_contract"].get(key)) is not int
                for key in timeout_accounting(focus)))):
        raise ValueError("Related UI source/task/module/focus/hash admission must equal its exact native plan")
    return True


def validate_context(context: dict, focus: str, *, udid: str) -> bool:
    if type(context) is not dict or context.get("adaptive_runtime_focus") != runtime_focus(focus):
        raise ValueError("Related UI requires its fresh mapped adaptive inventory capture marker")
    return adaptive_runtime.validate_context(context, runtime_focus(focus), udid=udid)


def admission_path(focus: str) -> str:
    selection = _selection(focus)
    if focus in SPLIT_FOCUSES:
        return selection["admission_path"]
    return ("build/ci-verification/adaptive-controls-native-source-admission.json" if focus == FOCUSES[0]
            else "build/ci-verification/ui-related-native-source-admission.json")


def _admission(focus: str) -> dict:
    result = {"task": task(focus), "focus": focus, "selected_methods": list(selectors(focus)),
              "effective_sources": list(sources(focus)),
              "source_sha256": source_sha256(focus),
              "excluded_unrelated_test_sources": True, "production_source_sets_changed": False,
              "compiler_executions_attested": 0, "apple_links_attested": 0, "native_tests_executed": 0,
              "scope": "Source/selection admission only; original fresh native XML/runtime/cleanup decide results"}
    if focus != FOCUSES[0]:
        result["common_sources"] = []
    if focus in SPLIT_FOCUSES:
        result.update(receipt_subdirectory=receipt_subdirectory(focus), **timeout_accounting(focus))
    return result


def validate_admission(root: Path, started_ns: int, ended_ns: int, focus: str) -> bool:
    if type(started_ns) is not int or type(ended_ns) is not int or started_ns <= 0 or ended_ns < started_ns:
        return False
    try:
        expected = _admission(focus)
        raw, info = _ordinary_bytes(root, admission_path(focus))
        if not started_ns - 2_000_000_000 <= info.st_mtime_ns <= ended_ns + 2_000_000_000:
            return False
        source_contract(root, focus)
        document = json.loads(raw, object_pairs_hook=_unique_object,
                              parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite source admission")))
        return (type(document) is dict and document == expected and
                all(type(document.get(key)) is int for key in
                    ("compiler_executions_attested", "apple_links_attested", "native_tests_executed")) and
                type(document.get("excluded_unrelated_test_sources")) is bool and
                type(document.get("production_source_sets_changed")) is bool and
                (focus not in SPLIT_FOCUSES or all(type(document.get(key)) is int
                    for key in timeout_accounting(focus))))
    except (OSError, ValueError, UnicodeError, TypeError, RecursionError):
        return False


def _cases_shape(cases) -> bool:
    return type(cases) is list and all(type(case) is dict and
        all(type(case.get(key)) is str for key in ("classname", "name", "status")) for case in cases)


def outcomes(cases: list[dict], system: str, focus: str, *,
             cases_by_report: list[list[dict]] | None = None) -> tuple[list[dict], list[str]]:
    """Model acceptance policy only; actual owning XML/Worker/runtime/cleanup decide results."""
    expected = identities(focus)
    wanted = Counter((item["classname"], item["name"]) for item in expected)
    host_ok = type(system) is str and system.lower() in {"darwin", "macos", "mac os x"}
    errors = [] if host_ok else ["Related UI requires actual Apple-host application execution"]
    valid = _cases_shape(cases)
    actual = Counter((case["classname"], case["name"]) for case in cases) if valid else Counter()
    reports_ok = (type(cases_by_report) is list and all(_cases_shape(report) and report
                  for report in cases_by_report))
    if reports_ok:
        report_classes = [frozenset(case["classname"] for case in report) for report in cases_by_report]
        reports_ok = (Counter(report_classes) == Counter(frozenset((classname,)) for classname in {name for name, _ in wanted}) and
                      Counter((case["classname"], case["name"], case["status"])
                              for report in cases_by_report for case in report) ==
                      Counter((case["classname"], case["name"], case["status"]) for case in cases)) if valid else False
    exact = valid and actual == wanted and reports_ok
    if not exact:
        errors.append(f"Related UI XML must contain exactly {len(expected)} selected methods and one fresh report per class")
    source_by_class = {task_name(focus) + "." + group["classname"]: group["source"]
                       for group in focus_spec(focus)["groups"]}
    scenarios = []
    for item in expected:
        matching = [case for case in cases if (case["classname"], case["name"]) ==
                    (item["classname"], item["name"])] if valid else []
        passed = exact and host_ok and len(matching) == 1 and matching[0]["status"] == "passed"
        if not passed:
            errors.append("Related UI native method must pass exactly once: " + item["name"])
        scenarios.append({**item, "source": source_by_class[item["classname"]], "task": task_name(focus),
                          "target": "iosSimulatorArm64", "actual_os_branch_required": adaptive_runtime.branch(runtime_focus(focus)),
                          "required_on_host": True,
                          "disposition": "required-executed" if passed else "required-not-passed"})
    return scenarios, errors
