# WebAIM's WCAG 2 Checklist

Source: https://webaim.org/standards/wcag/checklist

---

# WebAIM's WCAG 2 Checklist

You are here: [Home](/) > [Articles](/articles/) > [WCAG](/standards/wcag) > WCAG 2 Checklist

WebAIM Accessibility Testing Services

The experts at WebAIM can audit your web site and provide a detailed report to help you remediate accessibility and WCAG compliance issues.

[Learn more about WebAIM Evaluation Services](/services/evaluation)

Important!

The following is **NOT** the Web Content Accessibility Guidelines (WCAG) 2. It is a checklist that presents our recommendations for implementing the most common accessibility principles and techniques for those seeking WCAG conformance. The language used here significantly simplifies and condenses [the official WCAG 2.2 specification](//www.w3.org/TR/WCAG22/) and supporting materials to make it easier to implement and verify for web pages. The checklist contains links to the official success criteria.

[A PDF version of this checklist](/standards/wcag/WCAG2Checklist.pdf) is also available

## Tools

Show success criteria from WCAG version...
2.0  
2.1  
2.2  

Show level...
A  
AA  
AAA  

## Perceivable Web content is made available to the senses - sight, hearing, and/or touch

### Guideline 1.1 Provide text alternatives for any non-text content

#### [1.1.1 Non-text Content](//www.w3.org/TR/WCAG22/#non-text-content) A 2.0

- Images, image buttons, and image map hot spots have appropriate, equivalent [alternative text](/techniques/alttext/).
- Images that do not convey content, are decorative, or contain content that is already conveyed in text are given empty alternative text (`alt=""`) or implemented as CSS backgrounds. All linked images have descriptive alternative text.
- Equivalent alternatives to complex images are provided in context or on a separate linked page.
- Form buttons have a descriptive value.
- Inputs have associated [accessible names](/articles/label-name/).
- Embedded multimedia is identified via accessible text.
- Frames and iframes are appropriately [titled](/techniques/frames/).

### Guideline 1.2 Provide alternatives for time-based media.

NOTE: If the audio or video is designated as an alternative to web content (e.g., an audio or sign language version of a web page), then the web content itself serves as the alternative.

#### [1.2.1 Audio-only and Video-only (Prerecorded)](//www.w3.org/TR/WCAG22/#audio-only-and-video-only-prerecorded) A 2.0

- A [descriptive transcript](/techniques/captions/#transcripts) of relevant content is provided for non-live audio-only (audio podcasts, MP3 files, etc.).
- A descriptive transcript or [audio description](/techniques/captions/#ad) of relevant content is provided for non-live video-only, unless the video is decorative.

#### [1.2.2 Captions (Prerecorded)](//www.w3.org/TR/WCAG22/#captions-prerecorded) A 2.0

- [Synchronized captions](/techniques/captions/) are provided for non-live video (YouTube videos, etc.).

#### [1.2.3 Audio Description or Media Alternative (Prerecorded)](//www.w3.org/TR/WCAG22/#audio-description-or-media-alternative-prerecorded) A 2.0

- A descriptive transcript **or** audio description is provided for non-live video.   
  NOTE: Only required if there is relevant visual content that is not presented in the audio.

#### [1.2.4 Captions (Live)](//www.w3.org/TR/WCAG22/#captions-live) AA 2.0

- Synchronized captions are provided for live media that contains audio (audio-only broadcasts, web casts, video conferences, etc.)

#### [1.2.5 Audio Description (Prerecorded)](//www.w3.org/TR/WCAG22/#audio-description-prerecorded) AA 2.0

- Audio descriptions are provided for non-live video.  
  NOTE: Only required if there is relevant visual content that is not presented in the audio.
- While not required at Level AA, for optimal accessibility WebAIM recommends descriptive transcripts in addition to audio descriptions.

#### [1.2.6 Sign Language (Prerecorded)](//www.w3.org/TR/WCAG22/#sign-language-prerecorded) AAA 2.0

- A sign language video is provided for media that contains audio.

#### [1.2.7 Extended Audio Description (Prerecorded)](//www.w3.org/TR/WCAG22/#extended-audio-description-prerecorded) AAA 2.0

- When audio description cannot be added to video due to insufficient pauses in the audio, an alternative version of the video with pauses that allow audio descriptions is provided.

#### [1.2.8 Media Alternative (Prerecorded)](//www.w3.org/TR/WCAG22/#media-alternative-prerecorded) AAA 2.0

- A descriptive transcript is provided for pre-recorded media that has a video track. For optimal accessibility, WebAIM strongly recommends transcripts for all multimedia.

#### [1.2.9 Audio-only (Live)](//www.w3.org/TR/WCAG22/#audio-only-live) AAA 2.0

- A descriptive text transcript (e.g., the script of the live audio) is provided for live content that has audio.

### Guideline 1.3 Create content that can be presented in different ways (for example simpler layout) without losing information or structure.

#### [1.3.1 Info and Relationships](//www.w3.org/TR/WCAG22/#info-and-relationships) A 2.0

- [Semantic markup](/techniques/semanticstructure/) is appropriately used to designate headings, regions/landmarks, lists, emphasized or special text, etc.
- [Tables](/techniques/tables/data) are used for tabular data and data cells are associated with their headers. Data table captions, if present, are associated to data tables.
- [Text labels](/techniques/forms/controls) are associated with form inputs. Related form controls are grouped with fieldset/legend. ARIA labelling may be used when standard HTML is insufficient.

#### [1.3.2 Meaningful Sequence](//www.w3.org/TR/WCAG22/#meaningful-sequence) A 2.0

- The [reading and navigation order](/techniques/screenreader/#linearization) (determined by code order) is logical and intuitive.

#### [1.3.3 Sensory Characteristics](//www.w3.org/TR/WCAG22/#sensory-characteristics) A 2.0

- Instructions do not rely upon shape, size, or visual location (e.g., "Click the square icon to continue" or "Instructions are in the right-hand column").
- Instructions do not rely upon sound (e.g., "A beeping sound indicates you may continue.").

#### [1.3.4 Orientation](//www.w3.org/TR/WCAG22/#orientation) AA 2.1

- Orientation of web content is not restricted to only portrait or landscape, unless a specific orientation is necessary.

#### [1.3.5 Identify Input Purpose](//www.w3.org/TR/WCAG22/#identify-input-purpose) AA 2.1

- Input fields that collect [certain types of user information](//www.w3.org/TR/WCAG22/#input-purposes) have an appropriate `autocomplete` attribute defined.

#### [1.3.6 Identify Purpose](//www.w3.org/TR/WCAG22/#identify-purpose) AAA 2.1

- Regions/landmarks are used to identify page regions.
- ARIA is used, where appropriate, to enhance HTML semantics to better identify the purpose of interface components.

### Guideline 1.4 Make it easier for users to see and hear content including separating foreground from background.

#### [1.4.1 Use of Color](//www.w3.org/TR/WCAG22/#use-of-color) A 2.0

- Color is not used as the sole method of conveying content or distinguishing visual elements.
- Color alone is not used to distinguish [links](/techniques/hypertext/) from surrounding text unless the [contrast ratio](/resources/linkcontrastchecker/) between the link and the surrounding text is at least 3:1 *and* an additional distinction (e.g., it becomes underlined) is provided when the link is hovered over and receives keyboard focus.

#### [1.4.2 Audio Control](//www.w3.org/TR/WCAG22/#audio-control) A 2.0

- A mechanism is provided to stop, pause, mute, or adjust volume for audio that automatically plays on a page for more than 3 seconds.

#### [1.4.3 Contrast (Minimum)](//www.w3.org/TR/WCAG22/#contrast-minimum) AA 2.0

- Text and images of text have a contrast ratio of at least 4.5:1.
- Large text - at least 18 point (typically 24px) or 14 point (typically 18.66px) and bold - has a contrast ratio of at least 3:1.

#### [1.4.4 Resize text](//www.w3.org/TR/WCAG22/#resize-text) AA 2.0

- The page is readable and functional when the page is zoomed to 200%. NOTE: [1.4.10 (below)](#sc1.4.10) introduces additional requirements for zoomed content.

#### [1.4.5 Images of Text](//www.w3.org/TR/WCAG22/#images-of-text) AA 2.0

- If the same visual presentation can be made using text alone, an image is not used to present that text.

#### [1.4.6 Contrast (Enhanced)](//www.w3.org/TR/WCAG22/#contrast-enhanced) AAA 2.0

- Text and images of text have a contrast ratio of at least 7:1.
- Large text - at least 18 point (typically 24px) or 14 point (typically 18.66px) and bold - has a contrast ratio of at least 4.5:1.

#### [1.4.7 Low or No Background Audio](//www.w3.org/TR/WCAG22/#low-or-no-background-audio) AAA 2.0

- Audio with speech has no or very low background noise so the speech is easily distinguished.

#### [1.4.8 Visual Presentation](//www.w3.org/TR/WCAG22/#visual-presentation) AAA 2.0

- Blocks of text over one sentence in length:
  - Are no more than 80 characters wide.
  - Are NOT fully justified (aligned to both the left and the right margins).
  - Have adequate line spacing (at least 1/2 the height of the text) and paragraph spacing (1.5 times line spacing).
  - Have defined or inherited foreground and background colors.
  - Do NOT require horizontal scrolling when the text size is doubled.

#### [1.4.9 Images of Text (No Exception)](//www.w3.org/TR/WCAG22/#images-of-text-no-exception) AAA 2.0

- Text is used within an image only for decoration (the image does not convey content) OR when the information cannot be presented with text alone.

#### [1.4.10 Reflow](//www.w3.org/TR/WCAG22/#reflow) AA 2.1

- No loss of content or functionality occurs, and horizontal scrolling is avoided when content is presented at a width of 320 pixels.
  - This requires responsive design for most web sites. This is best tested by setting the browser window to 1280 pixels wide and then zooming the page content to 400%.
- Content that requires horizontal scrolling, such as data tables, complex images (such as maps and charts), toolbars, etc. are exempted.

#### [1.4.11 Non-text Contrast](//www.w3.org/TR/WCAG22/#non-text-contrast) AA 2.1

- A contrast ratio of at least 3:1 is present for differentiating graphical objects (such as icons and components of charts or graphs) and author-customized interface components (such as buttons, form controls, and focus indicators/outlines).
- At least 3:1 contrast is maintained in the various states (focus, hover, active, etc.) of author-customized interactive components.

#### [1.4.12 Text Spacing](//www.w3.org/TR/WCAG22/#text-spacing) AA 2.1

- No loss of content or functionality occurs when the user adapts paragraph spacing to 2 times the font size, text line height/spacing to 1.5 times the font size, word spacing to .16 times the font size, and letter spacing to .12 times the font size.
- This is best supported by avoiding pixel height definitions for elements that contain text.

#### [1.4.13 Content on Hover or Focus](//www.w3.org/TR/WCAG22/#content-on-hover-or-focus) AA 2.1

- When additional content is presented on hover or keyboard focus:
  - The newly revealed content can be dismissed (generally via the Esc key) without moving the pointer or keyboard focus, unless the content presents an input error or does not obscure or interfere with other page content.
  - The pointer can be moved to the new content without the content disappearing.
  - The new content must remain visible until the pointer or keyboard focus is moved away from the triggering control, the new content is dismissed, or the new content is no longer relevant.

## Operable Interface forms, controls, and navigation are operable.

### Guideline 2.1 Make all functionality available from a keyboard.

#### [2.1.1 Keyboard](//www.w3.org/TR/WCAG22/#keyboard) A 2.0

- All page functionality is available using the [keyboard](/techniques/keyboard/), unless the functionality cannot be accomplished in any known way using a keyboard (e.g., free hand drawing).
- Page-specified shortcut keys and accesskeys (accesskey should typically be avoided) do not conflict with existing browser and screen reader shortcuts.

#### [2.1.2 No Keyboard Trap](//www.w3.org/TR/WCAG22/#no-keyboard-trap) A 2.0

- [Keyboard](/techniques/keyboard/) focus is never locked or trapped at one particular page element. The user can navigate to and from all navigable page elements using only a keyboard.

#### [2.1.3 Keyboard (No Exception)](//www.w3.org/TR/WCAG22/#keyboard-no-exception) AAA 2.0

- All page functionality is available using the keyboard.

#### [2.1.4 Character Key Shortcuts](//www.w3.org/TR/WCAG22/#character-key-shortcuts) A 2.1

- If a keyboard shortcut uses printable character keys, then the user must be able to disable the key command, change the defined key to a non-printable key (Ctrl, Alt, etc.), or only activate the shortcut when an associated interface component or button is focused.

### Guideline 2.2 Provide users enough time to read and use content.

#### [2.2.1 Timing Adjustable](//www.w3.org/TR/WCAG22/#timing-adjustable) A 2.0

- If a page or application has a time limit, the user is given options to turn off, adjust, or extend that time limit. This is not a requirement for real-time events (e.g., an auction), where the time limit is absolutely required, or if the time limit is longer than 20 hours.

#### [2.2.2 Pause, Stop, Hide](//www.w3.org/TR/WCAG22/#pause-stop-hide) A 2.0

- Automatically moving, blinking, or scrolling content (such as carousels, marquees, or animations) that lasts longer than 5 seconds can be paused, stopped, or hidden by the user.
- Automatically updating content (e.g., a dynamically-updating news ticker, chat messages, etc.) can be paused, stopped, or hidden by the user or the user can manually control the timing of the updates.

#### [2.2.3 No Timing](//www.w3.org/TR/WCAG22/#no-timing) AAA 2.0

- The content and functionality have no time limits or constraints.

#### [2.2.4 Interruptions](//www.w3.org/TR/WCAG22/#interruptions) AAA 2.0

- Interruptions (alerts, page updates, etc.) can be postponed or suppressed by the user.

#### [2.2.5 Re-authenticating](//www.w3.org/TR/WCAG22/#re-authenticating) AAA 2.0

- If an authentication session expires, the user can re-authenticate and continue the activity without losing any data from the current page.

#### [2.2.6 Timeouts](//www.w3.org/TR/WCAG22/#timeouts) AAA 2.1

- Users must be warned of any timeout that could result in data loss, unless the data is preserved for longer than 20 hours of user inactivity.

### Guideline 2.3 Do not design content in a way that is known to cause seizures.

#### [2.3.1 Three Flashes or Below Threshold](//www.w3.org/TR/WCAG22/#three-flashes-or-below-threshold) A 2.0

- No page content [flashes](/articles/seizure/) more than 3 times per second unless that flashing content is sufficiently small and the flashes are of low contrast and do not contain too much red. ([See general flash and red flash thresholds](//www.w3.org/TR/WCAG22/#dfn-general-flash-and-red-flash-thresholds))

#### [2.3.2 Three Flashes](//www.w3.org/TR/WCAG22/#three-flashes) AAA 2.0

- No page content flashes more than 3 times per second.

#### [2.3.3 Animation from Interactions](//www.w3.org/TR/WCAG22/#animation-from-interactions) AAA 2.1

- Users can disable non-essential animation and movement that is triggered by user interaction.

### Guideline 2.4 Provide ways to help users navigate, find content, and determine where they are.

#### [2.4.1 Bypass Blocks](//www.w3.org/TR/WCAG22/#bypass-blocks) A 2.0

- A link is provided to [skip navigation](/techniques/skipnav/) and other page elements that are repeated across web pages.
- While proper use of headings or regions/landmarks is sufficient to meet this success criterion, because keyboard navigation by headings or regions is not supported in most browsers, WebAIM recommends a "skip" link in addition to headings and regions.

#### [2.4.2 Page Titled](//www.w3.org/TR/WCAG22/#page-titled) A 2.0

- The web page has a descriptive and informative [page title](/techniques/pagetitle/).

#### [2.4.3 Focus Order](//www.w3.org/TR/WCAG22/#focus-order) A 2.0

- The navigation order of links, form controls, etc. is logical and intuitive.

#### [2.4.4 Link Purpose (In Context)](//www.w3.org/TR/WCAG22/#link-purpose-in-context) A 2.0

- The purpose of each link (or image button or image map hotspot) can be determined from the link text alone, or from the link text and its context (e.g., surrounding text, list item, previous heading, or table headers).
- Links with the same text that go to different locations are readily distinguishable.

#### [2.4.5 Multiple Ways](//www.w3.org/TR/WCAG22/#multiple-ways) AA 2.0

- [Multiple ways](/techniques/sitetools/) are available to find other web pages on the site - at least two of: a list of related pages, table of contents, site map, site search, or list of all available web pages.

#### [2.4.6 Headings and Labels](//www.w3.org/TR/WCAG22/#headings-and-labels) AA 2.0

- Page headings and labels for form and interactive controls are informative. Avoid duplicating heading and label text unless the structure provides adequate differentiation between them.

#### [2.4.7 Focus Visible](//www.w3.org/TR/WCAG22/#focus-visible) AA 2.0

- There is a visible indicator for page elements when they receive keyboard focus.

#### [2.4.8 Location](//www.w3.org/TR/WCAG22/#location) AAA 2.0

- If a web page is part of a sequence of pages or within a complex site structure, an indication of the current page location is provided, for example, through breadcrumbs or specifying the current step in a sequence (e.g., "Step 2 of 5 - Shipping Address").

#### [2.4.9 Link Purpose (Link Only)](//www.w3.org/TR/WCAG22/#link-purpose-link-only) AAA 2.0

- The purpose of each link (or image button or image map hotspot) can be determined from the link text alone.
- There are no links with the same text that go to different locations.

#### [2.4.10 Section Headings](//www.w3.org/TR/WCAG22/#section-headings) AAA 2.0

- Beyond providing an overall document structure, individual sections of content are designated using headings, where appropriate.

#### [2.4.11 Focus Not Obscured (Minimum)](//www.w3.org/TR/WCAG22/#focus-not-obscured-minimum) AA 2.2

- When elements have keyboard focus, they are not entirely covered or hidden by page content.

#### [2.4.12 Focus Not Obscured (Enhanced)](//www.w3.org/TR/WCAG22/#focus-not-obscured-enhanced) AAA 2.2

- When elements have keyboard focus, they are entirely visible.

#### [2.4.13 Focus Appearance](//www.w3.org/TR/WCAG22/#focus-appearance) AAA 2.2

- If a custom focus indicator or background color is in place, the focus indicator pixels must:
  - have at least 3:1 contrast between focused/unfocused states
  - be at least as large as the area of a 2 pixel thick perimeter surrounding the element. The formula `(width × 4) + (height × 4) = focus indicator area` can be used for rectangular components.

### Guideline 2.5 Make it easier for users to operate functionality through various inputs beyond keyboard.

#### [2.5.1 Pointer Gestures](//www.w3.org/TR/WCAG22/#pointer-gestures) A 2.1

- If multipoint or path-based gestures (such as pinching, swiping, or dragging across the screen) are not essential to the functionality, then the functionality can also be performed with a single point activation (such as activating a button).

#### [2.5.2 Pointer Cancellation](//www.w3.org/TR/WCAG22/#pointer-cancellation) A 2.1

- To help avoid inadvertent activation of controls, avoid non-essential down-event (e.g., `onmousedown`) activation when clicking, tapping, or long pressing the screen. For complex interactions (such as drag and drop), `onmousedown` can be used if an associated `onmouseup` (or similar) event can be aborted or reversed.

#### [2.5.3 Label in Name](//www.w3.org/TR/WCAG22/#label-in-name) A 2.1

- If an interface component (link, button, etc.) presents text (or images of text), the accessible name (label, alternative text, aria-label, etc.) for that component must include the visible text.

#### [2.5.4 Motion Actuation](//www.w3.org/TR/WCAG22/#motion-actuation) A 2.1

- Functionality that is triggered by moving the device (such as shaking or panning a mobile device) or by user movement (such as waving to a camera) can be disabled and equivalent functionality is provided via standard controls like buttons.

#### [2.5.5 Target Size](//www.w3.org/TR/WCAG22/#target-size) AAA 2.1

- Clickable targets are at least 44 by 44 pixels in size unless an alternative target of that size is provided, the target is inline (such as a link within a sentence), the target is not author-modified (such as a default checkbox), or the small target size is essential to the functionality.

#### [2.5.6 Concurrent Input Mechanisms](//www.w3.org/TR/WCAG22/#concurrent-input-mechanisms) AAA 2.1

- Content does not require a specific input type, such as touch-only or keyboard-only, but must support alternative inputs (such as using a keyboard on a mobile device).

#### [2.5.7 Dragging Movements](//www.w3.org/TR/WCAG22/#dragging-movements) AA 2.2

- Functionality that uses pointer dragging can also be achieved using a single pointer without dragging (unless dragging is essential).

#### [2.5.8 Target Size (Minimum)](//www.w3.org/TR/WCAG22/#target-size-minimum) AA 2.2

- Pointer input target sizes are at least 24 by 24 pixels unless:
  - A 24 pixel diameter circle centered on the target element does not intersect with any other target or a 24 pixel circle centered on an adjacent target.
  - The functionality can be achieved in some other conformant manner.
  - The target is in a sentence or list.
  - The target size can't be modified or is essential to the functionality.

## Understandable Information and the operation of user interface must be understandable.

### Guideline 3.1 Make text content readable and understandable.

#### [3.1.1 Language of Page](//www.w3.org/TR/WCAG22/#language-of-page) A 2.0

- The language of the page is identified using the `lang` attribute (e.g., `<html lang="en">`).

#### [3.1.2 Language of Parts](//www.w3.org/TR/WCAG22/#language-of-parts) AA 2.0

- The language of page content that is in a different language is identified using the `lang` attribute (e.g., `<blockquote lang="es">`).

#### [3.1.3 Unusual Words](//www.w3.org/TR/WCAG22/#unusual-words) AAA 2.0

- [Words](/techniques/writing/) that may be ambiguous, unfamiliar, or used in a very specific way are defined through adjacent text, a definition list, a glossary, or other suitable method.

#### [3.1.4 Abbreviations](//www.w3.org/TR/WCAG22/#abbreviations) AAA 2.0

- The meaning of an unfamiliar abbreviation is provided by expanding it the first time it is used, using the `<abbr>` element, or linking to a definition or glossary.

#### [3.1.5 Reading Level](//www.w3.org/TR/WCAG22/#reading-level) AAA 2.0

- A more understandable alternative is provided for content that is more advanced than can be reasonably read by a person with roughly 9 years of primary education.

#### [3.1.6 Pronunciation](//www.w3.org/TR/WCAG22/#pronunciation) AAA 2.0

- If the pronunciation of a word is vital to understanding that word, its pronunciation is provided immediately following the word or via a link or glossary.

### Guideline 3.2 Make Web pages appear and operate in predictable ways.

#### [3.2.1 On Focus](//www.w3.org/TR/WCAG22/#on-focus) A 2.0

- When a page element receives focus, it does not result in a substantial change to the page, the spawning of a pop-up window, an additional change of keyboard focus, or any other change that could confuse or disorient the user.

#### [3.2.2 On Input](//www.w3.org/TR/WCAG22/#on-input) A 2.0

- When a user inputs information or interacts with a control, it does not result in a substantial change to the page, the spawning of a pop-up window, an additional change of keyboard focus, or any other change that could confuse or disorient the user unless the user is informed of the change ahead of time.

#### [3.2.3 Consistent Navigation](//www.w3.org/TR/WCAG22/#consistent-navigation) AA 2.0

- Navigation links that are repeated on web pages do not change order when navigating through the site.

#### [3.2.4 Consistent Identification](//www.w3.org/TR/WCAG22/#consistent-identification) AA 2.0

- Elements that have the same functionality across multiple web pages are consistently identified. For example, a search box at the top of the site should always be labeled the same way.

#### [3.2.5 Change on Request](//www.w3.org/TR/WCAG22/#change-on-request) AAA 2.0

- Substantial changes to the page, the spawning of pop-up windows, uncontrolled changes of keyboard focus, or any other change that could confuse or disorient the user must be initiated by the user. Alternatively, the user is provided an option to disable such changes.

#### [3.2.6 Consistent Help](//www.w3.org/TR/WCAG22/#consistent-help) A 2.2

- Contact and self-help details or functionality are presented consistently when present on multiple web pages.

### Guideline 3.3 Help users avoid and correct mistakes.

#### [3.3.1 Error Identification](//www.w3.org/TR/WCAG22/#error-identification) A 2.0

- Required inputs or inputs that require a specific format, value, or length provide this information within the element's label.
- [Form validation](/techniques/formvalidation/) errors are efficient, intuitive, and accessible. The error is clearly identified, quick access to the problematic element is provided, and the user can easily fix the error and resubmit the form.

#### [3.3.2 Labels or Instructions](//www.w3.org/TR/WCAG22/#labels-or-instructions) A 2.0

- Inputs are identified by labels or instructions that help users know what information to enter.

#### [3.3.3 Error Suggestion](//www.w3.org/TR/WCAG22/#error-suggestion) AA 2.0

- If an input error is detected (via client-side or server-side validation), suggestions are provided for fixing the input in a timely and accessible manner.

#### [3.3.4 Error Prevention (Legal, Financial, Data)](//www.w3.org/TR/WCAG22/#error-prevention-legal-financial-data) AA 2.0

- Submissions, changes, and deletions of legal, financial, or test data can be reversed, verified, or confirmed.

#### [3.3.5 Help](//www.w3.org/TR/WCAG22/#help) AAA 2.0

- Instructions and cues are provided in context to help in form completion and submission.

#### [3.3.6 Error Prevention (All)](//www.w3.org/TR/WCAG22/#error-prevention-all) AAA 2.0

- If the user can submit information, the submission is reversible, verified, or confirmed.

#### [3.3.7 Redundant Entry](//www.w3.org/TR/WCAG22/#redundant-entry) A 2.2

- Information that a user must re-enter to complete a single-session process must be auto-populated or available for the user to select, unless re-entering the information is essential to the functionality, the information poses security issues, or the previously-entered information is no longer valid.

#### [3.3.8 Accessible Authentication (Minimum)](//www.w3.org/TR/WCAG22/#accessible-authentication-minimum) AA 2.2

- A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless the cognitive function test can be bypassed in some way, can be completed with assistance by some other mechanism, uses object recognition (such as "click on the photo of a flower"), or uses identification of non-text content provided by the user (such as a user-provided image).

#### [3.3.9 Accessible Authentication (Enhanced)](//www.w3.org/TR/WCAG22/#accessible-authentication-enhanced) AAA 2.2

- A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless the cognitive function test can be bypassed in some way or can be completed with assistance by some other mechanism.

## Robust Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies.

### Guideline 4.1 Maximize compatibility with current and future user agents, including assistive technologies.

#### [4.1.1 Parsing (Obsolete and removed)](//www.w3.org/TR/WCAG22/#parsing) A 2.0

NOTE: This success criterion is no longer useful and as of 2023 has been removed from WCAG. It previously required that significant HTML validation/parsing errors be avoided.

#### [4.1.2 Name, Role, Value](//www.w3.org/TR/WCAG22/#name-role-value) A 2.0

- Markup is used in a way that facilitates accessibility. This includes following the HTML specifications and using forms, input labels, frame titles, etc. appropriately.
- ARIA is used appropriately to enhance accessibility when HTML is not sufficient.

#### [4.1.3 Status Messages](//www.w3.org/TR/WCAG22/#status-messages) AA 2.1

- If an important status message is presented and focus is not set to that message, the message must be announced to screen reader users, typically via an ARIA alert or live region.

This checklist is provided as a resource to help implement [Web Content Accessibility Guidelines (WCAG) 2.2](//www.w3.org/TR/WCAG22/) (W3C Recommendation), which is [Copyright](//www.w3.org/Consortium/Legal/ipr-notice#Copyright) © 2017-2023 [W3C](//www.w3.org/)®.