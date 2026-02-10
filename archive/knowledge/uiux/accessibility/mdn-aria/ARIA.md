# ARIA

Source: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA

---

# ARIA

Accessible Rich Internet Applications **(ARIA)** is a set of [roles](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles) and [attributes](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes) that define ways to make web content and web applications (especially those developed with JavaScript) more accessible to people with disabilities.

ARIA supplements HTML so that interactions and widgets commonly used in applications can be passed to assistive technologies when there is not otherwise a mechanism. For example, ARIA enables accessible JavaScript widgets, form hints and error messages, live content updates, and more.

## [Before using ARIA](#before_using_aria)

**Warning:**
Many of these widgets are fully supported in modern browsers. **Developers should prefer using the correct semantic HTML element over using ARIA**, if such an element exists. For instance, native elements have built-in [keyboard accessibility](/en-US/docs/Web/Accessibility/Guides/Keyboard-navigable_JavaScript_widgets), roles and states. However, if you choose to use ARIA, you are responsible for mimicking the equivalent browser behavior in script.

[The first rule of ARIA](https://w3c.github.io/using-aria/#rule1) use is "If you can use a native HTML element or attribute with the semantics and behavior you require already built in, instead of re-purposing an element and adding an ARIA role, state or property to make it accessible, then do so."

**Note:**
There is a saying "No ARIA is better than bad ARIA." In [WebAim's survey of over one million home pages](https://webaim.org/projects/million/#aria), they found that Home pages with ARIA present averaged 41% more detected errors than those without ARIA. While ARIA is designed to make web pages more accessible, if used incorrectly, it can do more harm than good.

Here's the markup for a progress bar widget:

html

```
<div
  id="percent-loaded"
  role="progressbar"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"></div>
```

This progress bar is built using a [`<div>`](/en-US/docs/Web/HTML/Reference/Elements/div), which has no meaning. We include ARIA roles and properties to add meaning. In this example, the [`role="progressbar"`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/progressbar_role) attribute informs the browser that this element is actually a JavaScript-powered progress bar widget. The [`aria-valuemin`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuemin) and [`aria-valuemax`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuemax) attributes specify the minimum and maximum values for the progress bar, and the [`aria-valuenow`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuenow) describes the current state of it and therefore must be kept updated with JavaScript.

Along with placing them directly in the markup, ARIA attributes can be added to the element and updated dynamically using JavaScript code like this:

js

```
// Find the progress bar <div> in the DOM.
const progressBar = document.getElementById("percent-loaded");

// Set its ARIA roles and states,
// so that assistive technologies know what kind of widget it is.
progressBar.setAttribute("role", "progressbar");
progressBar.setAttribute("aria-valuemin", 0);
progressBar.setAttribute("aria-valuemax", 100);

// Create a function that can be called at any time to update
// the value of the progress bar.
function updateProgress(percentComplete) {
  progressBar.setAttribute("aria-valuenow", percentComplete);
}
```

All content that is available to non-assistive technology users must be made available to assistive technologies. Similarly, no features should be included targeting assistive technology users that aren't also accessible to those not using assistive technologies. The above progressbar needs to be styled to make it look like a progressbar.

It would have been much simpler to use the native [`<progress>`](/en-US/docs/Web/HTML/Reference/Elements/progress) element instead:

html

```
<progress id="percent-loaded" value="75" max="100">75 %</progress>
```

**Note:**
The `min` attribute is not allowed for the [`<progress>`](/en-US/docs/Web/HTML/Reference/Elements/progress) element; its minimum value is always `0`.

**Note:**
HTML landmark elements ([`<main>`](/en-US/docs/Web/HTML/Reference/Elements/main), [`<header>`](/en-US/docs/Web/HTML/Reference/Elements/header), [`<nav>`](/en-US/docs/Web/HTML/Reference/Elements/nav), etc.) have built-in implicit ARIA roles, so there is no need to duplicate them.

## [Support](#support)

Like any other web technology, there are varying degrees of support for ARIA. Support is based on the operating system and browser being used, as well as the kind of assistive technology interfacing with it. In addition, the version of the operating system, browser, and assistive technology are contributing factors. Older software versions may not support certain ARIA roles, have only partial support, or misreport its functionality.

It is also important to acknowledge that some people who rely on assistive technology are reluctant to upgrade their software, for fear of losing the ability to interact with their computer and browser. Because of this, it is important to [use semantic HTML elements](/en-US/docs/Learn_web_development/Core/Accessibility/HTML) whenever possible, as semantic HTML has far better support for assistive technology.

It is also important to test your authored ARIA with actual assistive technology. This is because browser emulators and simulators are not really effective for testing full support. Similarly, proxy assistive technology solutions are not sufficient to fully guarantee functionality.

## [Reference](#reference)

The [ARIA reference](/en-US/docs/Web/Accessibility/ARIA/Reference) is a comprehensive list of ARIA attributes and roles that are documented on MDN.

[ARIA roles](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles)
:   ARIA roles can be used to describe elements that don't natively exist in HTML or those which exist but don't yet have wide browser support.

[ARIA states and properties (attributes)](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes)
:   ARIA attributes enable modifying an element's states and properties as defined in the accessibility tree.

## [Guides](#guides)

The [ARIA guides](/en-US/docs/Web/Accessibility/ARIA/Guides) are resources that help you improve the accessibility of web page features such as tables, forms, and keyboard-navigation.

## [Standardization efforts](#standardization_efforts)

[WAI-ARIA specification](https://w3c.github.io/aria/)
:   The W3C specification itself.

[WAI-ARIA authoring practices](https://www.w3.org/WAI/ARIA/apg/)
:   The official best practices documents how best to ARIA-ify common widgets and interactions. An excellent resource.

## [ARIA for scripted widgets](#aria_for_scripted_widgets)

[Writing keyboard-navigable JavaScript widgets](/en-US/docs/Web/Accessibility/Guides/Keyboard-navigable_JavaScript_widgets)
:   Built-in elements like [`<input>`](/en-US/docs/Web/HTML/Reference/Elements/input), [`<button>`](/en-US/docs/Web/HTML/Reference/Elements/button), etc. have built-in keyboard accessibility. If you 'fake' these with [`<div>`](/en-US/docs/Web/HTML/Reference/Elements/div)s and ARIA, you must ensure your widgets are keyboard accessible.

[Live regions](/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions)
:   Live regions provide suggestions to screen readers about how to handle changes to the contents of a page.

## [Videos](#videos)

The following talks are a great way to understand ARIA:

[ARIA, Accessibility APIs and coding like you give a damn! â LÃ©onie Watson](https://www.youtube.com/watch?v=qdB8SRhqvFc)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Oct 2, 2025 by [MDN contributors](/en-US/docs/Web/Accessibility/ARIA/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/accessibility/aria/index.md?plain=1 "Folder: en-us/web/accessibility/aria (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAccessibility%2FARIA&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Faccessibility%2Faria%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAccessibility%2FARIA%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Faccessibility%2Faria%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Fcab1109a0c225299a9fb2b3402bcd4a1931b8ab7%0A*+Document+last+modified%3A+2025-10-02T16%3A39%3A46.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")