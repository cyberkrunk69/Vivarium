# ARIA states and properties (attributes)

Source: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes

---

# ARIA states and properties (attributes)

This page lists reference pages covering all the WAI-ARIA attributes discussed on MDN.

ARIA attributes enable modifying an element's states and properties as defined in the accessibility tree.

**Note:**
ARIA only modifies the accessibility tree, modifying how assistive technology presents the content to your users. ARIA doesn't change anything about an element's function or behavior. When not using semantic HTML elements for their intended purpose and default functionality, you must use JavaScript to manage behavior, focus, and ARIA states.

## [ARIA attribute types](#aria_attribute_types)

There are 4 categories of ARIA states and properties:

### [Widget attributes](#widget_attributes)

- [`aria-autocomplete`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-autocomplete)
- [`aria-checked`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-checked)
- [`aria-disabled`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-disabled)
- [`aria-errormessage`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-errormessage)
- [`aria-expanded`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded)
- [`aria-haspopup`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-haspopup)
- [`aria-hidden`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden)
- [`aria-invalid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid)
- [`aria-label`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label)
- [`aria-level`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-level)
- [`aria-modal`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-modal)
- [`aria-multiline`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-multiline)
- [`aria-multiselectable`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-multiselectable)
- [`aria-orientation`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-orientation)
- [`aria-placeholder`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-placeholder)
- [`aria-pressed`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-pressed)
- [`aria-readonly`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-readonly)
- [`aria-required`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-required)
- [`aria-selected`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-selected)
- [`aria-sort`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-sort)
- [`aria-valuemax`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuemax)
- [`aria-valuemin`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuemin)
- [`aria-valuenow`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuenow)
- [`aria-valuetext`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuetext)

### [Live region attributes](#live_region_attributes)

- [`aria-busy`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy)
- [`aria-live`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live)
- [`aria-relevant`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-relevant)
- [`aria-atomic`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-atomic)

### [Drag-and-Drop attributes](#drag-and-drop_attributes)

- [`aria-dropeffect`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-dropeffect)
- [`aria-grabbed`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-grabbed)

### [Relationship attributes](#relationship_attributes)

- [`aria-activedescendant`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-activedescendant)
- [`aria-colcount`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colcount)
- [`aria-colindex`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colindex)
- [`aria-colspan`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colspan)
- [`aria-controls`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-controls)
- [`aria-describedby`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-describedby)
- [`aria-description`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-description)
- [`aria-details`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-details)
- [`aria-errormessage`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-errormessage)
- [`aria-flowto`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-flowto)
- [`aria-labelledby`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-labelledby)
- [`aria-owns`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-owns)
- [`aria-posinset`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-posinset)
- [`aria-rowcount`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowcount)
- [`aria-rowindex`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowindex)
- [`aria-rowspan`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowspan)
- [`aria-setsize`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-setsize)

## [Global ARIA attributes](#global_aria_attributes)

Some states and properties apply to all HTML elements regardless of whether an ARIA role is applied. These are defined as "Global" attributes. Global states and properties are supported by all roles and base markup elements.

Many of the above attributes are global, meaning they can be included on any element unless specifically disallowed:

- [`aria-atomic`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-atomic)
- [`aria-busy`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy)
- [`aria-controls`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-controls)
- [`aria-current`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current)
- [`aria-describedby`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-describedby)
- [`aria-description`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-description)
- [`aria-details`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-details)
- [`aria-disabled`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-disabled)
- [`aria-dropeffect`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-dropeffect)
- [`aria-errormessage`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-errormessage)
- [`aria-flowto`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-flowto)
- [`aria-grabbed`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-grabbed)
- [`aria-haspopup`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-haspopup)
- [`aria-hidden`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden)
- [`aria-invalid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid)
- [`aria-keyshortcuts`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-keyshortcuts)
- [`aria-label`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label)
- [`aria-labelledby`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-labelledby)
- [`aria-live`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live)
- [`aria-owns`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-owns)
- [`aria-relevant`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-relevant)
- [`aria-roledescription`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-roledescription)

By "specifically disallowed," all the above attributes are global except for the `aria-label` and `aria-labelledby` properties, which are not allowed on elements with role [`presentation`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/presentation_role) nor its synonym [`none`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/none_role) role.

## [Index of states and properties](#index_of_states_and_properties)

The following are the reference pages covering the WAI-ARIA states and properties described on MDN.

[ARIA: aria-activedescendant attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-activedescendant)
:   The `aria-activedescendant` attribute identifies the currently active element when focus is on a [`composite`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/composite_role) widget, [`combobox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/combobox_role), [`textbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/textbox_role), [`group`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/group_role), or [`application`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/application_role).

[ARIA: aria-atomic attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-atomic)
:   In ARIA live regions, the global `aria-atomic` attribute indicates whether assistive technologies such as a screen reader will present all, or only parts of, the changed region based on the change notifications defined by the [`aria-relevant`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-relevant) attribute.

[ARIA: aria-autocomplete attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-autocomplete)
:   The `aria-autocomplete` attribute indicates whether inputting text could trigger display of one or more predictions of the user's intended value for a [`combobox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/combobox_role), [`searchbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/searchbox_role), or [`textbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/textbox_role) and specifies how predictions will be presented if they are made.

[ARIA: aria-braillelabel attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-braillelabel)
:   The global `aria-braillelabel` property defines a string value that labels the current element, which is intended to be converted into Braille.

[ARIA: aria-brailleroledescription attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-brailleroledescription)
:   The global `aria-brailleroledescription` attribute defines a human-readable, author-localized abbreviated description for the role of an element intended to be converted into Braille.

[ARIA: aria-busy attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy)
:   The `aria-busy` attribute is a global ARIA state that indicates whether an element is currently being modified.
    It helps assistive technologies understand that changes to the content are not yet complete, and that they may want to wait before informing users of the update.
    While `aria-busy` is commonly used in [ARIA live regions](/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions) to delay announcements until updates are complete, it can also be used outside of live regionsâfor example, in widgets or feedsâto signal ongoing changes or loading.

[ARIA: aria-checked attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-checked)
:   The `aria-checked` attribute indicates the current "checked" state of checkboxes, radio buttons, and other widgets.

[ARIA: aria-colcount attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colcount)
:   The `aria-colcount` attribute defines the total number of columns in a [`table`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role), [`grid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role), or [`treegrid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role) when not all columns are present in the [DOM](/en-US/docs/Glossary/DOM).

[ARIA: aria-colindex attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colindex)
:   The `aria-colindex` attribute defines an element's column index or position with respect to the total number of columns within a `table`, `grid`, or `treegrid`.

[ARIA: aria-colindextext attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colindextext)
:   The `aria-colindextext` attribute defines a human-readable text alternative of the numeric [`aria-colindex`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colindex).

[ARIA: aria-colspan attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-colspan)
:   The `aria-colspan` attribute defines the number of columns spanned by a cell or gridcell within a [`table`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role), [`grid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role), or [`treegrid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role).

[ARIA: aria-controls attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-controls)
:   The global `aria-controls` property identifies the element (or elements) whose contents or presence are controlled by the element on which this attribute is set.

[ARIA: aria-current attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current)
:   A non-null `aria-current` state on an element indicates that this element represents the current item within a container or set of related elements.

[ARIA: aria-describedby attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-describedby)
:   The global `aria-describedby` attribute identifies the element (or elements) that describes the element on which the attribute is set.

[ARIA: aria-description attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-description)
:   The global `aria-description` attribute defines a string value that describes or annotates the current element.

[ARIA: aria-details attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-details)
:   The global `aria-details` attribute identifies the element (or elements) that provide additional information related to the object.

[ARIA: aria-disabled attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-disabled)
:   The `aria-disabled` state indicates that the element is perceivable but disabled, so it is not editable or otherwise operable.

[ARIA: aria-dropeffect attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-dropeffect)
:   The global `aria-dropeffect` attribute indicates what functions may be performed when a dragged object is released on the drop target.

[ARIA: aria-errormessage attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-errormessage)
:   The `aria-errormessage` attribute on an object identifies the element(s) that provides an error message for that object.

[ARIA: aria-expanded attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded)
:   The `aria-expanded` attribute is set on an element to indicate if a control is expanded or collapsed, and whether or not the controlled elements are displayed or hidden.

[ARIA: aria-flowto attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-flowto)
:   The global `aria-flowto` attribute identifies the next element (or elements) in an alternate reading order of content. This allows assistive technology to override the general default of reading in document source order at the user's discretion.

[ARIA: aria-grabbed attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-grabbed)
:   The `aria-grabbed` state indicates an element's "grabbed" state in a drag-and-drop operation.

[ARIA: aria-haspopup attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-haspopup)
:   The `aria-haspopup` attribute indicates the availability and type of interactive popup element that can be triggered by the element on which the attribute is set.

[ARIA: aria-hidden attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden)
:   The `aria-hidden` state indicates whether the element is exposed to an accessibility API.

[ARIA: aria-invalid attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid)
:   The `aria-invalid` state indicates the entered value does not conform to the format expected by the application.

[ARIA: aria-keyshortcuts attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-keyshortcuts)
:   The global `aria-keyshortcuts` attribute indicates keyboard shortcuts that an author has implemented to activate or give focus to an element.

[ARIA: aria-label attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label)
:   The `aria-label` attribute defines a string value that can be used to name an element, as long as the element's role does not [prohibit naming](#associated_roles).

[ARIA: aria-labelledby attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-labelledby)
:   The `aria-labelledby` attribute identifies the element (or elements) that labels the element it is applied to.

[ARIA: aria-level attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-level)
:   The `aria-level` attribute defines the hierarchical level of an element within a structure.

[ARIA: aria-live attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live)
:   The global `aria-live` attribute indicates that an element will be updated, and describes the types of updates the user agents, assistive technologies, and user can expect from the live region.

[ARIA: aria-modal attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-modal)
:   The `aria-modal` attribute indicates whether an element is modal when displayed.

[ARIA: aria-multiline attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-multiline)
:   The `aria-multiline` attribute indicates whether a `textbox` accepts multiple lines of input or only a single line.

[ARIA: aria-multiselectable attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-multiselectable)
:   The `aria-multiselectable` attribute indicates that the user may select more than one item from the current selectable descendants.

[ARIA: aria-orientation attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-orientation)
:   The `aria-orientation` attribute indicates whether the element's orientation is horizontal, vertical, or unknown/ambiguous.

[ARIA: aria-owns attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-owns)
:   The `aria-owns` attribute identifies an element (or elements) in order to define a visual, functional, or contextual relationship between a parent and its child elements when the DOM hierarchy cannot be used to represent the relationship.

[ARIA: aria-placeholder attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-placeholder)
:   The `aria-placeholder` attribute defines a short hint (a word or short phrase) intended to help the user with data entry when a form control has no value. The hint can be a sample value or a brief description of the expected format.

[ARIA: aria-posinset attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-posinset)
:   The `aria-posinset` attribute defines an element's number or position in the current set of listitems or treeitems when not all items are present in the DOM.

[ARIA: aria-pressed attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-pressed)
:   The `aria-pressed` attribute indicates the current "pressed" state of a toggle button.

[ARIA: aria-readonly attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-readonly)
:   The `aria-readonly` attribute indicates that the element is not editable, but is otherwise operable.

[ARIA: aria-relevant attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-relevant)
:   Used in ARIA live regions, the global `aria-relevant` attribute indicates what notifications the user agent will trigger when the [accessibility tree](/en-US/docs/Glossary/Accessibility_tree) within a live region is modified.

[ARIA: aria-required attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-required)
:   The `aria-required` attribute indicates that user input is required on the element before a form may be submitted.

[ARIA: aria-roledescription attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-roledescription)
:   The `aria-roledescription` attribute defines a human-readable, author-localized description for the role of an element.

[ARIA: aria-rowcount attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowcount)
:   The `aria-rowcount` attribute defines the total number of rows in a table, grid, or treegrid.

[ARIA: aria-rowindex attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowindex)
:   The `aria-rowindex` attribute defines an element's position with respect to the total number of rows within a table, grid, or treegrid.

[ARIA: aria-rowindextext attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowindextext)
:   The `aria-rowindextext` attribute defines a human-readable text alternative of `aria-rowindex`.

[ARIA: aria-rowspan attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowspan)
:   The `aria-rowspan` attribute defines the number of rows spanned by a cell or gridcell within a table, grid, or treegrid.

[ARIA: aria-selected attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-selected)
:   The `aria-selected` attribute indicates the current "selected" state of various widgets.

[ARIA: aria-setsize attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-setsize)
:   The `aria-setsize` attribute defines the number of items in the current set of listitems or treeitems when not all items in the set are present in the DOM.

[ARIA: aria-sort attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-sort)
:   The `aria-sort` attribute indicates if items in a table or grid are sorted in ascending or descending order.

[ARIA: aria-valuemax attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuemax)
:   The `aria-valuemax` attribute defines the maximum allowed value for a range widget.

[ARIA: aria-valuemin attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuemin)
:   The `aria-valuemin` attribute defines the minimum allowed value for a range widget.

[ARIA: aria-valuenow attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuenow)
:   The `aria-valuenow` attribute defines the current value for a `range` widget.

[ARIA: aria-valuetext attribute](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuetext)
:   The `aria-valuetext` attribute defines the human-readable text alternative of `aria-valuenow` for a range widget.

## [See also](#see_also)

- [Using ARIA: roles, states, and properties](/en-US/docs/Web/Accessibility/ARIA/Guides/Techniques)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Mar 6, 2025 by [MDN contributors](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/accessibility/aria/reference/attributes/index.md?plain=1 "Folder: en-us/web/accessibility/aria/reference/attributes (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAccessibility%2FARIA%2FReference%2FAttributes&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Faccessibility%2Faria%2Freference%2Fattributes%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAccessibility%2FARIA%2FReference%2FAttributes%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Faccessibility%2Faria%2Freference%2Fattributes%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Ff65f7f6e4fda2cb1bd0e7db17777e2cb20be7d27%0A*+Document+last+modified%3A+2025-03-06T10%3A57%3A29.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")