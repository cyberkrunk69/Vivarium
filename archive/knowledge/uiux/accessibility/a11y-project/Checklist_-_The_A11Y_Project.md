# Checklist - The A11Y Project

Source: https://www.a11yproject.com/checklist/

---

Table of Contents

This checklist uses [The Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/) as a reference point. The WCAG is a shared standard for web content accessibility for individuals, organizations, and governments.

There are three levels of accessibility compliance in the WCAG, which reflect the priority of support:

![](/img/checklist/wcag-level-a-small.svg)

**A: Essential** If this isn't met, assistive technology may not be able to read, understand, or fully operate the page or view.

![](/img/checklist/wcag-level-aa-small.svg)

**AA: Ideal Support** Required for [multiple government and public body websites](https://www.w3.org/WAI/policies/). The A11Y Project strives for AA compliance.

![](/img/checklist/wcag-level-aaa-small.svg)

**AAA: Specialized Support** This is typically reserved for parts of websites and web apps that serve a specialized audience.

This checklist targets many, but not all level A and AA concerns. Note that the different levels of WCAG support do not necessarily indicate an increased level of difficulty to implement.

## Success criteria

Each item on this checklist has a corresponding WCAG “success criterion.” Success criterion are the specific, testable rules that power the WCAG, described by a reference number and short title. For example, the rule about text resizing is called [1.4.4 Resize text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html).

Some accessibility issues may have multiple success criterion apply to them. We have identified the one most relevant for each checklist item.

## Does this checklist guarantee my site is accessible?

No. However, addressing the issues called out in this checklist will help improve the experience for everyone who uses your site.

The issues this checklist prompts you to check for covers a wide range of disability conditions. There is no such thing as “perfect accessibility” or a site being “100% accessible.” You should be wary of companies and services that make such promises. If you need professional accessibility help, use [professional accessibility services](/resources/#professional-help).

---

## Content

Content is the most important part of your site.

Task: Use plain language and avoid figures of speech, idioms, and complicated metaphors.

 Use plain language and avoid figures of speech, idioms, and complicated metaphors.

[3.1.5 Reading Level](https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html)

Write content at [an 8th grade reading level](https://datayze.com/readability-analyzer.php).

[Share Link to checklist item: Use plain language and avoid figures of speech, idioms, and complicated metaphors.](#use-plain-language-and-avoid-figures-of-speech-idioms-and-complicated-metaphors)

Task: Make sure that `button`, `a`, and `label` element content is unique and descriptive.

 Make sure that `button`, `a`, and `label` element content is unique and descriptive.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Terms like “click here” and “read more” do not provide any context. Some people navigate using a list of all buttons or links on a page or view. When using this mode, the terms indicate what will happen if navigated to or activated.

[Share Link to checklist item: Make sure that `button`, `a`, and `label` element content is unique and descriptive.](#make-sure-that-button-a-and-label-element-content-is-unique-and-descriptive)

Task: Use left-aligned text for left-to-right (LTR) languages, and right-aligned text for right-to-left (RTL) languages.

 Use left-aligned text for left-to-right (LTR) languages, and right-aligned text for right-to-left (RTL) languages.

[1.4.8 Visual Presentation](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)

Centered-aligned or justified text is difficult to read.

[Share Link to checklist item: Use left-aligned text for left-to-right (LTR) languages, and right-aligned text for right-to-left (RTL) languages.](#use-left-aligned-text-for-left-to-right-ltr-languages-and-right-aligned-text-for-right-to-left-rtl-languages)

## Global code

Global code is code that affects your entire website or web app.

Task: Validate your HTML.

 Validate your HTML.

[4.1.1 Parsing](https://www.w3.org/WAI/WCAG22/Understanding/parsing.html)

[Valid HTML](https://validator.w3.org/nu/) helps to provide a consistent, expected experience across all browsers and assistive technology.

[Share Link to checklist item: Validate your HTML.](#validate-your-html)

Task: Use a `lang` attribute on the `html` element.

 Use a `lang` attribute on the `html` element.

[3.1.1 Language of Page](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)

This helps assistive technology such as screen readers to [pronounce content correctly](https://github.com/FreedomScientific/VFO-standards-support/issues/188).

[Share Link to checklist item: Use a `lang` attribute on the `html` element.](#use-a-lang-attribute-on-the-html-element)

Task: Provide a unique `title` for each page or view.

 Provide a unique `title` for each page or view.

[2.4.2 Page Titled](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html)

The `title` element, contained in the document's `head` element, is often the first piece of information announced by assistive technology. This helps tell people what page or view they are going to start navigating.

[Share Link to checklist item: Provide a unique `title` for each page or view.](#provide-a-unique-title-for-each-page-or-view)

Task: Ensure that viewport zoom is not disabled.

 Ensure that viewport zoom is not disabled.

[1.4.4 Resize text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)

Some people need to increase the size of text to a point where they can read it. Do not stop them from doing this, even for web apps with a native app-like experience. Even native apps should respect Operating System settings for resizing text.

[Share Link to checklist item: Ensure that viewport zoom is not disabled.](#ensure-that-viewport-zoom-is-not-disabled)

Task: Use landmark elements to indicate important content regions.

 Use landmark elements to indicate important content regions.

[4.1.2 Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html)

[Landmark regions](https://www.w3.org/TR/wai-aria-practices/examples/landmarks/HTML5.html) help communicate the layout and important areas of a page or view, and can allow quick access to these regions. For example, use the `nav` element to wrap a site's navigation, and the `main` element to contain the primary content of a page.

[Share Link to checklist item: Use landmark elements to indicate important content regions.](#use-landmark-elements-to-indicate-important-content-regions)

Task: Ensure a linear content flow.

 Ensure a linear content flow.

[2.4.3 Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)

Remove `tabindex` attribute values that aren't either `0` or `-1`. Elements that are inherently focusable, such as links or `button` elements, do not require a `tabindex`. Elements that are not inherently focusable should not have a `tabindex` applied to them outside of very specific use cases.

[Share Link to checklist item: Ensure a linear content flow.](#ensure-a-linear-content-flow)

Task: Avoid using the `autofocus` attribute.

 Avoid using the `autofocus` attribute.

[2.4.3 Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)

People who are blind or who have low vision may be disoriented when focus is moved without their permission. Additionally, `autofocus` can be problematic for people with motor control disabilities, as it may create extra work for them to navigate out from the autofocused area and to other locations on the page/view.

[Share Link to checklist item: Avoid using the `autofocus` attribute.](#avoid-using-the-autofocus-attribute)

Task: Allow extending session timeouts.

 Allow extending session timeouts.

[2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html)

If you cannot remove session timeouts altogether, then let the person using your site easily turn off, adjust, or extend their session well before it ends.

[Share Link to checklist item: Allow extending session timeouts.](#allow-extending-session-timeouts)

Task: Remove `title` attribute tooltips.

 Remove `title` attribute tooltips.

[4.1.2 Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html)

[The `title` attribute has numerous issues](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title#Accessibility_concerns), and should not be used if the information provided is important for all people to access. An acceptable use for the `title` attribute would be labeling an `iframe` element to indicate what content it contains.

[Share Link to checklist item: Remove `title` attribute tooltips.](#remove-title-attribute-tooltips)

## Keyboard

It is important that your interface and content can be operated, and navigated by use of a keyboard. Some people cannot use a mouse, or may be using other assistive technologies that may not allow for hovering or precise clicking.

Task: Make sure there is a visible focus style for interactive elements that are navigated to via keyboard input.

 Make sure there is a visible focus style for interactive elements that are navigated to via keyboard input.

[2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)

Can a person navigating with a keyboard, [switch](https://axesslab.com/switches/), voice control, or screen reader see where they currently are on the page?

[Share Link to checklist item: Make sure there is a visible focus style for interactive elements that are navigated to via keyboard input.](#make-sure-there-is-a-visible-focus-style-for-interactive-elements-that-are-navigated-to-via-keyboard-input)

Task: Check to see that keyboard focus order matches the visual layout.

 Check to see that keyboard focus order matches the visual layout.

[1.3.2 Meaningful Sequence](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html)

Can a person navigating with a keyboard or screen reader move around the page in a predictable way?

[Share Link to checklist item: Check to see that keyboard focus order matches the visual layout.](#check-to-see-that-keyboard-focus-order-matches-the-visual-layout)

Task: Remove invisible focusable elements.

 Remove invisible focusable elements.

[2.4.3 Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)

Remove the ability to focus on elements that are not presently meant to be discoverable. This includes things like inactive drop down menus, off screen navigations, or modals.

[Share Link to checklist item: Remove invisible focusable elements.](#remove-invisible-focusable-elements)

## Images

Images are a very common part of most websites. Help make sure they can be enjoyed by all.

Task: Make sure that all `img` elements have an `alt` attribute.

 Make sure that all `img` elements have an `alt` attribute.

[1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

`alt` attributes (alt text) give a description of an image for people who may not be able to view them. When an `alt` attribute isn't present on an image, a screen reader may announce the image's file name and path instead. This fails to communicate the image’s content.

[Share Link to checklist item: Make sure that all `img` elements have an `alt` attribute.](#make-sure-that-all-img-elements-have-an-alt-attribute)

Task: Make sure that decorative images use null `alt` (empty) attribute values.

 Make sure that decorative images use null `alt` (empty) attribute values.

[1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

Null `alt` attributes are also sometimes known as empty `alt` attributes. They are made by including no information between the opening and closing quotes of an `alt` attribute. Decorative images do not communicate information that is required to understand the website's overall meaning. Historically they were used for flourishes and [spacer gif](https://en.wikipedia.org/wiki/Spacer_GIF) images, but tend to be less relevant for modern websites and web apps.

[Share Link to checklist item: Make sure that decorative images use null `alt` (empty) attribute values.](#make-sure-that-decorative-images-use-null-alt-empty-attribute-values)

Task: Provide a text alternative for complex images such as charts, graphs, and maps.

 Provide a text alternative for complex images such as charts, graphs, and maps.

[1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

Is there a plain text which lists points on the map or sections of a flowchart? Describe all visible information. This includes graph axes, data points and labels, and the overall point the graphic is communicating.

[Share Link to checklist item: Provide a text alternative for complex images such as charts, graphs, and maps.](#provide-a-text-alternative-for-complex-images-such-as-charts-graphs-and-maps)

Task: For images containing text, make sure the alt description includes the image's text.

 For images containing text, make sure the alt description includes the image's text.

[1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

For example, the FedEx logo should have an alt value of “FedEx.”

[Share Link to checklist item: For images containing text, make sure the alt description includes the image's text.](#for-images-containing-text-make-sure-the-alt-description-includes-the-images-text)

## Headings

Heading elements (h1, h2, h3, etc.) help break up the content of the page into related “chunks” of information. They are incredibly important for helping people who use assistive technology to understand the meaning of a page or view.

Task: Use heading elements to introduce content.

 Use heading elements to introduce content.

[2.4.6 Headings or Labels](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)

Heading elements construct a document outline, and should not be used for purely visual design.

[Share Link to checklist item: Use heading elements to introduce content.](#use-heading-elements-to-introduce-content)

Task: Use only one `h1` element per page or view.

 Use only one `h1` element per page or view.

[2.4.6 Headings or Labels](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)

The `h1` element should be used to communicate the high-level purpose of the page or view. Do not use the `h1` element for a heading that does not change between pages or views (for example, the site's name).

[Share Link to checklist item: Use only one `h1` element per page or view.](#use-only-one-h1-element-per-page-or-view)

Task: Heading elements should be written in a logical sequence.

 Heading elements should be written in a logical sequence.

[2.4.6 Headings or Labels](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)

[The order of heading elements](https://webdesign.tutsplus.com/articles/the-importance-of-heading-levels-for-assistive-technology--cms-31753) should descend, based on the “depth” of the content. For example, a `h4` element should not appear on a page before the first `h3` element declaration. A tool such as [headingsMap](/resources/#headingsmap) can help you evaluate this.

[Share Link to checklist item: Heading elements should be written in a logical sequence.](#heading-elements-should-be-written-in-a-logical-sequence)

Task: Don't skip heading levels.

 Don't skip heading levels.

[2.4.6 Headings or Labels](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)

For example, don't jump from a `h2` to a `h4`, skipping a `h3` element. If heading levels are being skipped for a specific visual treatment, use CSS classes instead.

[Share Link to checklist item: Don't skip heading levels.](#dont-skip-heading-levels)

## Lists

Lists elements let people know a collection of items are related and if they are sequential, and how many items are present in the list grouping.

Task: Use list elements (`ol`, `ul`, and `dl` elements) for list content.

 Use list elements (`ol`, `ul`, and `dl` elements) for list content.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

This may include sections of related content, items visually displayed in a grid-like layout, or sibling a elements.

[Share Link to checklist item: Use list elements (`ol`, `ul`, and `dl` elements) for list content.](#use-list-elements-ol-ul-and-dl-elements-for-list-content)

## Controls

Controls are interactive elements such as links and buttons that let a person navigate to a destination or perform an action.

Task: Use the `a` element for links.

 Use the `a` element for links.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Links should always have a `href` attribute, even when used in Single Page Applications (SPAs). Without a `href` attribute, the link will not be properly exposed to assistive technology. An example of this would be a link that uses an `onclick` event, in place of a `href` attribute.

[Share Link to checklist item: Use the `a` element for links.](#use-the-a-element-for-links)

Task: Ensure that links are recognizable as links.

 Ensure that links are recognizable as links.

[1.4.1 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

Color alone is not sufficient to indicate the presence of a link. Underlines are a popular and commonly-understood way to communicate the presence of link content.

[Share Link to checklist item: Ensure that links are recognizable as links.](#ensure-that-links-are-recognizable-as-links)

Task: Ensure that controls have `:focus` states.

 Ensure that controls have `:focus` states.

[2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)

Visible focus styles help people determine which interactive element has keyboard focus. This lets them know that they can perform actions like activating a button or navigating to a link's destination.

[Share Link to checklist item: Ensure that controls have `:focus` states.](#ensure-that-controls-have-focus-states)

Task: Use the `button` element for buttons.

 Use the `button` element for buttons.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Buttons are used to submit data or perform an on-screen action which does not shift keyboard focus. You can add `type="button"` to a `button` element to prevent the browser from attempting to submit form information when activated.

[Share Link to checklist item: Use the `button` element for buttons.](#use-the-button-element-for-buttons)

Task: Provide a skip link and make sure that it is visible when focused.

 Provide a skip link and make sure that it is visible when focused.

[2.4.1 Bypass Blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html)

A [skip link](/posts/skip-nav-links/) can be used to provide quick access to the main content of a page or view. This allows a person to easily bypass globally repeated content such as a website's primary navigation, or persistent search widget.

[Share Link to checklist item: Provide a skip link and make sure that it is visible when focused.](#provide-a-skip-link-and-make-sure-that-it-is-visible-when-focused)

Task: Identify links that open in a new tab or window.

 Identify links that open in a new tab or window.

[G201: Giving users advanced warning when opening a new window](https://www.w3.org/WAI/WCAG22/Techniques/general/G201)

Ideally, avoid links that open in a new tab or window. If a link does, ensure the link's behavior will be communicated in a way that is apparent to all users. Doing this will help people understand what will happen before activating the link. While this technique is technically not required for compliance, it is an often-cited area of frustration for many different kinds of assistive technology users.

[Share Link to checklist item: Identify links that open in a new tab or window.](#identify-links-that-open-in-a-new-tab-or-window)

## Tables

Tables are a structured set of data that help people understand the relationships between different types of information.

Task: Use the `table` element to describe tabular data.

 Use the `table` element to describe tabular data.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Do you need to display data in rows and columns? Use the `table` element.

[Share Link to checklist item: Use the `table` element to describe tabular data.](#use-the-table-element-to-describe-tabular-data)

Task: Use the `th` element for table headers (with appropriate `scope` attributes).

 Use the `th` element for table headers (with appropriate `scope` attributes).

[4.1.1 Parsing](https://www.w3.org/WAI/WCAG22/Understanding/parsing.html)

Depending on [how complex your table is](https://www.w3.org/WAI/tutorials/tables/), you may also consider using `scope="col"` for column headers, and `scope="row"` for row headers. Many different kinds of assistive technology still use the `scope` attribute to help them understand and describe the structure of a table.

[Share Link to checklist item: Use the `th` element for table headers (with appropriate `scope` attributes).](#use-the-th-element-for-table-headers-with-appropriate-scope-attributes)

Task: Use the `caption` element to provide a title for the table.

 Use the `caption` element to provide a title for the table.

[2.4.6 Headings or Labels](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)

The table's `caption` should describe what kind of information the table contains.

[Share Link to checklist item: Use the `caption` element to provide a title for the table.](#use-the-caption-element-to-provide-a-title-for-the-table)

## Forms

Forms allow people to enter information into a site for processing and manipulation. This includes things like sending messages and placing orders.

Task: All inputs in a form are associated with a corresponding `label` element.

 All inputs in a form are associated with a corresponding `label` element.

[3.2.2 On Input](https://www.w3.org/WAI/WCAG22/Understanding/on-input.html)

Use a `for`/`id` pairing to guarantee the highest level of browser/assistive technology support.

[Share Link to checklist item: All inputs in a form are associated with a corresponding `label` element.](#all-inputs-in-a-form-are-associated-with-a-corresponding-label-element)

Task: Use `fieldset` and `legend` elements where appropriate.

 Use `fieldset` and `legend` elements where appropriate.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Does your form contain multiple sections of related inputs? Use `fieldset` to group them, and `legend` to provide a label for what this section is for.

[Share Link to checklist item: Use `fieldset` and `legend` elements where appropriate.](#use-fieldset-and-legend-elements-where-appropriate)

Task: Inputs use `autocomplete` where appropriate.

 Inputs use `autocomplete` where appropriate.

[1.3.5 Identify Input Purpose](https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html)

[Providing a mechanism](https://www.w3.org/TR/html52/sec-forms.html#sec-autofill) to help people more quickly, easily, and accurately fill in form fields that ask for common information (for example, name, address, phone number).

[Share Link to checklist item: Inputs use `autocomplete` where appropriate.](#inputs-use-autocomplete-where-appropriate)

Task: Make sure that form input errors are displayed in list above the form after submission.

 Make sure that form input errors are displayed in list above the form after submission.

[3.3.1 Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)

This provides a way for assistive technology users to quickly have a high-level understanding of what issues are present in the form. This is especially important for larger forms with many inputs. Make sure that each reported error also has a link to the corresponding field with invalid input.

[Share Link to checklist item: Make sure that form input errors are displayed in list above the form after submission.](#make-sure-that-form-input-errors-are-displayed-in-list-above-the-form-after-submission)

Task: Associate input error messaging with the input it corresponds to.

 Associate input error messaging with the input it corresponds to.

[3.3.1 Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)

Techniques such as [using `aria-describedby`](https://developer.paciellogroup.com/blog/2018/09/describing-aria-describedby/) allow people who use assistive technology to more easily understand the difference between the input and the error message associated with it.

[Share Link to checklist item: Associate input error messaging with the input it corresponds to.](#associate-input-error-messaging-with-the-input-it-corresponds-to)

Task: Make sure that error, warning, and success states are not visually communicated by just color.

 Make sure that error, warning, and success states are not visually communicated by just color.

[1.4.1 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

People who are color blind, who have other low vision conditions, or different cultural understandings for color may not see the state change, or understand what kind of feedback the state represents if color is the only indicator.

[Share Link to checklist item: Make sure that error, warning, and success states are not visually communicated by just color.](#make-sure-that-error-warning-and-success-states-are-not-visually-communicated-by-just-color)

## Media

Media includes content such as pre-recorded and live audio and video.

Task: Make sure that media does not autoplay.

 Make sure that media does not autoplay.

[1.4.2 Audio Control](https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html)

Unexpected video and audio can be distracting and disruptive, especially for certain kinds of cognitive disability such as ADHD. Certain kinds of autoplaying video and animation can be a trigger for vestibular and seizure disorders.

[Share Link to checklist item: Make sure that media does not autoplay.](#make-sure-that-media-does-not-autoplay)

Task: Ensure that media controls use appropriate markup.

 Ensure that media controls use appropriate markup.

[1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Examples include making sure an audio mute button has [a pressed toggle state](https://www.w3.org/WAI/PF/aria/states_and_properties#aria-pressed) when active, or that a volume slider uses `<input type="range">`.

[Share Link to checklist item: Ensure that media controls use appropriate markup.](#ensure-that-media-controls-use-appropriate-markup)

Task: Check to see that all media can be paused.

 Check to see that all media can be paused.

[2.1.1 Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)

Provide a global pause function on any media element. If the device has a keyboard, ensure that pressing the `Space` key can pause playback. Make sure you also don't interfere with the `Space` key's ability to scroll the page/view when not focusing on a form control.

[Share Link to checklist item: Check to see that all media can be paused.](#check-to-see-that-all-media-can-be-paused)

## Video

Video-specific checks.

Task: Confirm the presence of captions.

 Confirm the presence of captions.

[1.2.2 Captions](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html)

Captions allow a person who cannot hear the audio content of a video to still understand its content.

[Share Link to checklist item: Confirm the presence of captions.](#confirm-the-presence-of-captions)

Task: Remove seizure triggers.

 Remove seizure triggers.

[2.3.1 Three Flashes or Below Threshold](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html)

Certain kinds of strobing or flashing animations will trigger seizures.

[Share Link to checklist item: Remove seizure triggers.](#remove-seizure-triggers)

## Audio

Audio-specific checks.

Task: Confirm that transcripts are available.

 Confirm that transcripts are available.

[1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

Transcripts allow people who cannot hear to still understand the audio content. It also allows people to digest audio content at a pace that is comfortable to them.

[Share Link to checklist item: Confirm that transcripts are available.](#confirm-that-transcripts-are-available)

## Appearance

How your website app content looks in any given situation.

Task: Check your content in specialized browsing modes.

 Check your content in specialized browsing modes.

[1.4.1 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

Activate [modes such as Windows High Contrast or Inverted Colors](/posts/operating-system-and-browser-accessibility-display-modes/). Is your content still legible? Are your icons, borders, links, form fields, and other content still present? Can you distinguish foreground content from the background?

[Share Link to checklist item: Check your content in specialized browsing modes.](#check-your-content-in-specialized-browsing-modes)

Task: Increase text size to 200%.

 Increase text size to 200%.

[1.4.4 Resize text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)

Is the content still readable? Does increasing the text size cause content to overlap?

[Share Link to checklist item: Increase text size to 200%.](#increase-text-size-to-200percent)

Task: Double-check that good proximity between content is maintained.

 Double-check that good proximity between content is maintained.

[1.3.3 Sensory Characteristics](https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html)

Use [the straw test](https://scottvinkle.me/blogs/work/proximity-and-zoom) to ensure people who depend on screen zoom software can still easily discover all content.

[Share Link to checklist item: Double-check that good proximity between content is maintained.](#double-check-that-good-proximity-between-content-is-maintained)

Task: Make sure color isn't the only way information is conveyed.

 Make sure color isn't the only way information is conveyed.

[1.4.1 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

Can you still see where links are among body content if everything is grayscale?

[Share Link to checklist item: Make sure color isn't the only way information is conveyed.](#make-sure-color-isnt-the-only-way-information-is-conveyed)

Task: Make sure instructions are not visual or audio-only.

 Make sure instructions are not visual or audio-only.

[1.3.3 Sensory Characteristics](https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html)

Use a combination of characteristics to write cues, particularly the actual names of sections and elements, rather than just descriptions like location (“on the right”) or audio (“after the tone”).

[Share Link to checklist item: Make sure instructions are not visual or audio-only.](#make-sure-instructions-are-not-visual-or-audio-only)

Task: Use a simple, straightforward, and consistent layout.

 Use a simple, straightforward, and consistent layout.

[1.4.10 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

A complicated layout can be confusing to understand and use.

[Share Link to checklist item: Use a simple, straightforward, and consistent layout.](#use-a-simple-straightforward-and-consistent-layout)

## Animation

Content that moves, either on its own, or when triggered by a person activating a control.

Task: Ensure animations are subtle and do not flash too much.

 Ensure animations are subtle and do not flash too much.

[2.3.1 Three Flashes or Below Threshold](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html)

Certain kinds of strobing or flashing animations will trigger seizures. Others may be distracting and disruptive, especially for certain kinds of cognitive disability such as ADHD.

[Share Link to checklist item: Ensure animations are subtle and do not flash too much.](#ensure-animations-are-subtle-and-do-not-flash-too-much)

Task: Provide a mechanism to pause background video.

 Provide a mechanism to pause background video.

[2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)

Background video can be distracting, especially if content is placed over it.

[Share Link to checklist item: Provide a mechanism to pause background video.](#provide-a-mechanism-to-pause-background-video)

Task: Make sure all animation obeys the `prefers-reduced-motion` media query.

 Make sure all animation obeys the `prefers-reduced-motion` media query.

[2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)

Remove animations when the “reduce motion” setting is activated. If an animation is necessary to communicate meaning for a concept, slow its duration down.

[Share Link to checklist item: Make sure all animation obeys the `prefers-reduced-motion` media query.](#make-sure-all-animation-obeys-the-prefers-reduced-motion-media-query)

## Color contrast

[Color contrast](/posts/what-is-color-contrast/) is how legible colors are when placed next to, and on top of each other.

Task: Check the contrast for all normal-sized text.

 Check the contrast for all normal-sized text.

[1.4.3 Contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Level AA compliance requires a contrast ratio of 4.5:1.

[Share Link to checklist item: Check the contrast for all normal-sized text.](#check-the-contrast-for-all-normal-sized-text)

Task: Check the contrast for all large-sized text.

 Check the contrast for all large-sized text.

[1.4.3 Contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Level AA compliance requires a contrast ratio of 3:1.

[Share Link to checklist item: Check the contrast for all large-sized text.](#check-the-contrast-for-all-large-sized-text)

Task: Check the contrast for all icons.

 Check the contrast for all icons.

[1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

Level AA compliance requires a contrast ratio of 3.0:1.

[Share Link to checklist item: Check the contrast for all icons.](#check-the-contrast-for-all-icons)

Task: Check the contrast of borders for input elements (text input, radio buttons, checkboxes, etc.).

 Check the contrast of borders for input elements (text input, radio buttons, checkboxes, etc.).

[1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

Level AA compliance requires a contrast ratio of 3.0:1.

[Share Link to checklist item: Check the contrast of borders for input elements (text input, radio buttons, checkboxes, etc.).](#check-the-contrast-of-borders-for-input-elements-text-input-radio-buttons-checkboxes-etc)

Task: Check text that overlaps images or video.

 Check text that overlaps images or video.

[1.4.3 Contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Is text still legible?

[Share Link to checklist item: Check text that overlaps images or video.](#check-text-that-overlaps-images-or-video)

Task: Check custom `::selection` colors.

 Check custom `::selection` colors.

[1.4.3 Contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Is the color contrast you set in your [`::selection` CSS declaration](https://developer.mozilla.org/en-US/docs/Web/CSS/::selection) sufficient? Otherwise someone may not be able read it if they highlight it.

[Share Link to checklist item: Check custom `::selection` colors.](#check-custom-selection-colors)

## Mobile and touch

Things to check mobile experiences for.

Task: Check that the site can be rotated to any orientation.

 Check that the site can be rotated to any orientation.

[1.3.4 Orientation](https://www.w3.org/WAI/WCAG22/Understanding/orientation.html)

Does the site only allow portrait orientation?

[Share Link to checklist item: Check that the site can be rotated to any orientation.](#check-that-the-site-can-be-rotated-to-any-orientation)

Task: Remove horizontal scrolling.

 Remove horizontal scrolling.

[1.4.10 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

Requiring someone to scroll horizontally can be difficult for some, irritating for all.

[Share Link to checklist item: Remove horizontal scrolling.](#remove-horizontal-scrolling)

Task: Ensure that button and link icons can be activated with ease.

 Ensure that button and link icons can be activated with ease.

[2.5.5 Target Size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)

It's good to make sure things like hamburger menus, social icons, gallery viewers, and other touch controls are usable by a wide range of hand and stylus sizes.

[Share Link to checklist item: Ensure that button and link icons can be activated with ease.](#ensure-that-button-and-link-icons-can-be-activated-with-ease)

Task: Ensure sufficient space between interactive items in order to provide a scroll area.

 Ensure sufficient space between interactive items in order to provide a scroll area.

[2.4.1 Bypass Blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html)

Some people who experience motor control issues such as [hand tremors](https://axesslab.com/hand-tremors/) may have a very difficult time scrolling past interactive items which feature zero spacing.

[Share Link to checklist item: Ensure sufficient space between interactive items in order to provide a scroll area.](#ensure-sufficient-space-between-interactive-items-in-order-to-provide-a-scroll-area)

## Next steps

Remember to periodically check your site to ensure it is still accessible. The A11Y Project also strongly encourages you to verify your testing by [hiring a professional tester](/resources/#professional-testers).

## Further reading

TetraLogical has a good in-depth, yet still [high-level explanation of the WCAG](https://tetralogical.com/articles/wcag-primer/). Check it out if you want to learn more about its history and principles.