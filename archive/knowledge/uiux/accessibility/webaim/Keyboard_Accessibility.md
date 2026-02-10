# Keyboard Accessibility

Source: https://webaim.org/techniques/keyboard/

---

# Keyboard Accessibility

You are here: [Home](/) > [Articles](/articles/) > Keyboard Accessibility

WebAIM Accessibility Testing Services

The experts at WebAIM can audit your web site and provide a detailed report to help you remediate accessibility and WCAG compliance issues.

[Learn more about WebAIM Evaluation Services](/services/evaluation)

## Introduction

Important

Ensure that all content can be accessed with the keyboard alone.

Keyboard accessibility is one of the most important aspects of web accessibility. Many users with motor disabilities rely on a keyboard. Some people have tremors which don't allow for fine muscle control. Others have little or no use of their hands, or no hands at all. In addition to traditional keyboards, some users may use modified keyboards or other hardware that mimics the functionality of a keyboard. Blind users also typically use a keyboard for navigation. Users without disabilities may use a keyboard for navigation because of preference or efficiency.

## Potential Problems

There are many ways that a webpage can introduce difficulties for users who rely on a keyboard for navigation. Below are a few of the most common issues.

### Focus indicators

A keyboard user typically uses the Tab key to navigate through interactive elements on a web page—links, buttons, fields for inputting text, etc. When an item is tabbed to, it has keyboard "focus" and can be activated or manipulated with the keyboard. A sighted keyboard user must be provided with a **visual** indicator of the element that currently has keyboard focus. Focus indicators are provided automatically by web browsers. While their appearance varies based on the browser, the focus indicator is typically shown as a border or highlight (called an outline) around the focused element. These outlines can be hidden by applying `outline:0` or `outline:none` CSS to focusable elements.

Important

[Avoid `outline:0` or `outline:none`](/blog/plague-of-outline-0/) or other styles that remove or limit visibility of keyboard focus indicators.

In addition to the default outline, you can use CSS to make the focus indicator more visually apparent and keyboard-friendly by ensuring the focus indicator is highly visible with sufficient contrast, and by adding a background color or other visual focus style to links and other interactive controls. The outline can be styled to match your site design but should be readily detected when navigating with the Tab key.

### Navigation order

As a keyboard user navigates through the page, the order in which interactive items receive keyboard focus is important. The default keyboard navigation order must be logical and intuitive. This generally means that it follows the visual flow of the page—left to right, top to bottom. For most pages this means header first, then main navigation, then page navigation (if present), and finally the footer. This navigation order (and also the reading order for screen readers) is determined by the web page's source code. For best results:

- Structure your underlying source code so that the reading/navigation order is correct.
- Then, if necessary, use CSS to control the visual presentation of the elements on your page.
- Do not use `tabindex` values of 1 or greater to change the default keyboard navigation order.

### Items that should not receive keyboard focus

Links, buttons, and form controls are natively accessible to keyboard users, so should be used for interactivity whenever possible. Page elements that are not interactive to mouse or touch users should not be made keyboard focusable (such as by using `tabindex`). Making non-interactive elements keyboard navigable will cause confusion.

Note

Note: An `<a>` element is only keyboard accessible or presented to screen reader users as a link when it has a non-empty `href` attribute. `<a>` (without an `href` attribute) or `<a href="">` (no `href` attribute value) should not be used for links.

### Inaccessible custom widgets

If a native HTML element is not sufficient, then a custom-made control or widget might be necessary. All custom controls must still be accessible to keyboard users. You may need to use `tabindex="0"` to ensure an element can receive keyboard focus. [ARIA](/techniques/aria/) may also be necessary to ensure that the control or widget is presented correctly to screen reader users. The [ARIA Authoring Practices](https://www.w3.org/TR/wai-aria-practices-1.1/) outlines necessary keyboard interactions and ARIA coding necessary for many types of custom widgets. To be made highly accessible the following must occur:

- The interaction is presented in an intuitive and predictable way
- JavaScript event handlers work with a keyboard and a mouse.
- The interaction uses standardized keystrokes.

### Lengthy navigation

Sighted mouse users are able to visually scan a web page and directly click on any item. Keyboard users must press the Tab key or other navigation keys to navigate through the interactive elements that precede the item the user wants to activate. Tabbing through lengthy navigation may be particularly demanding for users with motor disabilities.

Long lists of links or other navigable items may pose a burden for keyboard-only users. The following best practices can facilitate efficient keyboard navigation:

- Provide a ["skip to main content"](/techniques/skipnav/) link on the page.
- Use a [proper heading structure](/techniques/semanticstructure/#headings).
- Provide [regions or ARIA landmarks](/techniques/semanticstructure/#regions) (`<main>`, `<nav>`, etc.)

## Keyboard Testing

Testing with a keyboard is an essential part of any accessibility evaluation.

The following table includes many of the most common online interactions, the standard keystrokes for the interaction, and additional information on things to consider during testing.

| Interaction | Keystrokes | Notes |
| --- | --- | --- |
| Navigate to interactive elements | - Tab - navigate forward - Shift + Tab - navigate backward | - Keyboard focus indicators must be present. - Navigation order should be logical and intuitive. |
| Link | - Enter - activate the link |  |
| Button | - Enter or Spacebar - activate the button | Ensure elements with ARIA `role="button"` can be activated with both key commands. |
| Checkbox | - Spacebar - check/uncheck a checkbox | Users can typically select zero, one, or multiple options from group of checkboxes. |
| Radio buttons | - Spacebar - select the focused option (if not selected) - ↑/↓ or ←/→ - navigate between options - Tab - leave the group of radio buttons | Users can select only one option from a group of radio buttons. |
| Select (dropdown) menu | - ↑/↓ - navigate between options - Spacebar - expand - Enter/Esc - select option and collapse | You can also filter or jump to options in the menu as you type letters. |
| Autocomplete | - Type to begin filtering - ↑/↓ - navigate to an option - Enter - select an option |  |
| Dialog | - Esc - close | - Modal dialogs should maintain keyboard focus. - Non-modal dialogs should close automatically when they lose focus. - When a dialog closes, focus should usually return to the element that opened the dialog. |
| Slider | - ↑/↓ or ←/→ - increase or decrease slider value - Home/End - beginning or end | - For double-headed sliders (to set a range), Tab/Shift + Tab should toggle between each end. - In some sliders PageUp/PageDown can move by a larger increment (e.g., by 10%). |
| Menu bar | - ↑/↓ - previous/next menu option - Enter - expand the menu (optional) and select an option. - ←/→ - expand/collapse submenu | - A menu bar dynamically changes content within an application. Links that utilize Tab/Enter are NOT menu bars. |
| Tab panel | - Tab - once to navigate into the group of tabs and once to navigate out of the group of tabs - ↑/↓ or ←/→ - choose and activate previous/next tab. | - This is for 'application' tabs that dynamically change content within the tab panel. If a menu looks like a group of tabs, but is actually a group of links to different pages, Tab and Enter are more appropriate. |
| 'Tree' menu | - ↑/↓ - navigate previous/next menu option - ←/→ - expand/collapse submenu, move up/down one level. |  |
| Scroll | - ↑/↓ - scroll vertically - ←/→ - scroll horizontally - Spacebar/Shift + Spacebar - scroll by page | The space bar will, by default, scroll the page, but only if an interactive control that allows space bar input is not focused. Horizontal scrolling within the page should be minimized. |

Note

The [ARIA authoring practices document](https://www.w3.org/TR/wai-aria-practices-1.1/) provides additional information for these and other common interactions. Be sure to test keyboard accessibility on mobile devices—users with disabilities often utilize an external keyboard with phones and tablets.

[Next](tabindex)