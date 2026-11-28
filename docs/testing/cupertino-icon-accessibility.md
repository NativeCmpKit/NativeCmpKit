# Cupertino icon accessibility verification

`CupertinoIcon` clears the semantics of the inner font-backed glyph and retains
the caller's outer modifier. The icon is decorative when `contentDescription`
is null. A labeled icon exposes its description and image role. An enclosing
button keeps its click action and button role. Pass a null icon description when
adjacent text already labels the button.

The hosted Desktop suite can run `:nativecmpkit-cupertino-icons:desktopTest`.
`CupertinoIconSemanticsTest` covers standalone decorative and labeled icons, an
explicitly labeled button with a decorative icon, and a labeled icon-only button.
The icon-only case inspects merged and unmerged Compose semantics at font scales
0.85, 1.0 and 2.0 and activates the button once at each scale. These assertions
exercise Compose semantics. Layout at enlarged glyph sizes and platform screen
reader announcements require separate checks.

Use default and enlarged system font scales. Inspect the Android TalkBack, iOS
VoiceOver, desktop screen-reader and browser accessibility output for each
scenario.

| Control | Required observation |
| --- | --- |
| Standalone decorative icon | The accessibility tree exposes no private-use glyph text or fallback announcement. |
| Standalone labeled icon | The image label occurs once without an extra glyph announcement. |
| Text button with a decorative icon | The text label is announced and activating the button works. |
| Icon-only labeled button | One meaningful label and the button action remain, and activating the button works. |

Record the target, OS or browser, font scale, focus order, exact announcement
and activation result. Compare the merged and unmerged Compose trees where
available, and retain the browser accessibility tree separately.
[Issue #97](https://github.com/NativeCmpKit/NativeCmpKit/issues/97)
