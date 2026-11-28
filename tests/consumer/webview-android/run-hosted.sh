#!/usr/bin/env bash
set -euo pipefail

candidate_repo=$1
version=$2
output=$3
consumer="$RUNNER_TEMP/nativecmpkit-webview-android"
test ! -e "$consumer"
cp -R tests/consumer/webview-android "$consumer"
mkdir -p "$output"
export ANDROID_AVD_HOME="$RUNNER_TEMP/nativecmpkit-webview-avd"
export ANDROID_USER_HOME="$RUNNER_TEMP/nativecmpkit-webview-android-user"
export PATH="$ANDROID_HOME/platform-tools:$PATH"
mkdir "$ANDROID_AVD_HOME" "$ANDROID_USER_HOME"
avd="nativecmpkit-webview-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}"
device=emulator-5574
android_api=23
sdk_tools="$ANDROID_HOME/cmdline-tools/latest/bin"
test -x "$sdk_tools/avdmanager"
printf 'no\n' | "$sdk_tools/avdmanager" create avd --name "$avd" --package 'system-images;android-23;google_apis;x86_64'

command -v setfacl > /dev/null || sudo apt-get install -y acl
test -c /dev/kvm
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
test -r /dev/kvm && test -w /dev/kvm
test -z "$(adb devices | awk 'NR>1 && NF { print $1 }')"
"$ANDROID_HOME/emulator/emulator" -avd "$avd" -port 5574 -cores 2 -memory 2048 \
  -no-window -no-audio -no-boot-anim -no-snapshot -gpu swiftshader_indirect > "$output/emulator.log" 2>&1 &
emulator_pid=$!
cleanup() {
    if kill -0 "$emulator_pid" 2>/dev/null; then
        timeout 10 adb -s "$device" emu kill 2>/dev/null || true
        for ((attempt=0; attempt<10; attempt++)); do
            if ! kill -0 "$emulator_pid" 2>/dev/null; then break; fi
            sleep 1
        done
        if kill -0 "$emulator_pid" 2>/dev/null; then kill "$emulator_pid" 2>/dev/null || true; fi
        wait "$emulator_pid" || true
    fi
}
trap cleanup EXIT
export ANDROID_SERIAL="$device"
timeout 120 adb wait-for-device
for ((attempt=0; attempt<60; attempt++)); do
    if [[ "$(timeout 5 adb shell getprop sys.boot_completed | tr -d '\r')" == 1 ]]; then break; fi
    sleep 2
done
test "$(timeout 5 adb shell getprop sys.boot_completed | tr -d '\r')" = 1
test "$(timeout 5 adb shell getprop ro.build.version.sdk | tr -d '\r')" = "$android_api"
test "$(adb devices | awk 'NR>1 && NF {print $1,$2}')" = "$device device"
timeout 10 adb shell input keyevent 82
timeout 10 adb shell dumpsys webviewupdate > "$output/webview-provider.txt" || true

status=0
./gradlew -p "$consumer" verifyPublishedWebViewBinding connectedDebugAndroidTest \
  -PnativecmpkitRepository="$candidate_repo" -PnativecmpkitVersion="$version" \
  --max-workers=1 --no-parallel --no-configuration-cache --no-build-cache || status=$?
printf '%s\n' "$status" > "$output/gradle-exit.txt"
shopt -s globstar nullglob
reports=("$consumer"/build/outputs/androidTest-results/**/TEST-*.xml)
if [[ ${#reports[@]} == 1 ]]; then cp "${reports[0]}" "$output/TEST-PublishedAndroidWebView.xml"; fi
test "$status" -eq 0

python3 -B - "$consumer/build/outputs/androidTest-results" "$output" "$device" "$version" <<'PYTHON'
from pathlib import Path
import hashlib
import json
import os
import sys
from xml.etree.ElementTree import parse

reports, output, serial, version = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
files = sorted(reports.rglob('TEST-*.xml'))
cases = [case for path in files for case in parse(path).getroot().iter('testcase')]
expected = 'io.github.apdelrahman1911.nativecmpkit.consumer.androidwebview.PublishedAndroidWebViewTest'
if len(files) != 1 or len(cases) != 1 or cases[0].get('classname') != expected or cases[0].get('name') != 'loadsOwnedHtmlAndDisposesPublishedWebView':
    raise SystemExit('Missing exact packaged Android WebView testcase')
if any(child.tag in ('skipped', 'failure', 'error') for child in cases[0]):
    raise SystemExit('Packaged Android WebView testcase did not pass')
target = output / 'TEST-PublishedAndroidWebView.xml'
receipt = {'revision': os.environ['GITHUB_SHA'], 'version': version, 'serial': serial, 'android_api': 23,
           'testcase': cases[0].get('name'), 'executed': 1, 'passed': 1,
           'junit_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
(output / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
PYTHON
