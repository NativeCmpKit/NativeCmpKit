package io.github.apdelrahman1911.nativecmpkit.ui.datepicker

import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.v2.runComposeUiTest
import kotlinx.coroutines.test.TestResult
import kotlin.test.Test

/** Returns the actual browser Promise; no runBlocking or unawaited assertions. */
@OptIn(ExperimentalTestApi::class)
class CompactDateTransactionAcceptanceTest {
    @Test fun capturedConfirmRevalidatesTheLatestRules(): TestResult = runComposeUiTest {
        rejectCapturedConfirmAfterRulesTighten()
    }
    @Test fun replacementOwnerYearRangeAndRuleStartAnIndependentTransaction(): TestResult = runComposeUiTest {
        replaceOwnerAndYearRangeWithoutTransplantingScratchState()
    }
    @Test fun nullInputClearCancelReopenAndConfirmRemainTransactional(): TestResult = runComposeUiTest {
        clearActualInputThenCancelReopenAndCommitNull()
    }
    @Test fun noSelectableDateRejectsCommitAndCancelReopenRecovers(): TestResult = runComposeUiTest {
        rejectAllDaysThenCancelAndReopenWithRecoveredRules()
    }
}
