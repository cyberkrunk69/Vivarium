# WAI-ARIA Roles

Source: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles

---

# WAI-ARIA Roles

ARIA roles provide semantic meaning to content, allowing screen readers and other tools to present and support interaction with an object in a way that is consistent with user expectations of that type of object. ARIA roles can be used to describe elements that don't natively exist in HTML or exist but don't yet have full browser support.

By default, many semantic elements in HTML have a role; for example, `<input type="radio">` has the "radio" role. Non-semantic elements in HTML do not have a role; `<div>` and `<span>` without added semantics return `null`. The `role` attribute can provide semantics.

ARIA roles are added to HTML elements using `role="role type"`, where *role type* is the name of a role in the ARIA specification. Some roles require the inclusion of associated ARIA states or properties; others are only valid in association with other roles.

For example, `<ul role="tabpanel">` will be announced as a 'tab panel' by screen readers. However, if the tab panel doesn't have nested tabs, the element with the tabpanel role is not in fact a tab panel and accessibility has actually been negatively impacted.

The [ARIA states and properties](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes) associated with each role are included in the role's pages, with each attribute also having a dedicated page.

## [ARIA role types](#aria_role_types)

There are 6 categories of ARIA roles:

### [1. Document structure roles](#1._document_structure_roles)

Document Structure roles are used to provide a structural description for a section of content. Most of these roles should no longer be used as browsers now support semantic HTML elements with the same meaning. The roles without HTML equivalents, such as presentation, toolbar and tooltip roles, provide information on the document structure to assistive technologies such as screen readers as equivalent native HTML tags are not available.

- [`toolbar`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/toolbar_role)
- [`tooltip`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tooltip_role)
- [`feed`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/feed_role)
- [`math`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/math_role)
- [`presentation`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/presentation_role) / [`none`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/none_role)
- [`note`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/note_role)

For most document structure roles, semantic HTML equivalent elements are available and supported. Avoid using:

- [`application`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/application_role)
- [`article`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/article_role) (use [`<article>`](/en-US/docs/Web/HTML/Reference/Elements/article))
- [`cell`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/cell_role) (use [`<td>`](/en-US/docs/Web/HTML/Reference/Elements/td))
- [`columnheader`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/columnheader_role) (use `<th scope="col">`)
- [`definition`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/definition_role) (use [`<dfn>`](/en-US/docs/Web/HTML/Reference/Elements/dfn))
- [`directory`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/directory_role)
- [`document`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/document_role)
- [`figure`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/figure_role) (use [`<figure>`](/en-US/docs/Web/HTML/Reference/Elements/figure) instead)
- [`group`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/group_role)
- [`heading`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/heading_role) (use [h1](/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements) through [h6](/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements))
- [`img`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/img_role) (use [`<img>`](/en-US/docs/Web/HTML/Reference/Elements/img) or [`<picture>`](/en-US/docs/Web/HTML/Reference/Elements/picture) instead)
- [`list`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/list_role) (use either [`<ul>`](/en-US/docs/Web/HTML/Reference/Elements/ul) or [`<ol>`](/en-US/docs/Web/HTML/Reference/Elements/ol) instead)
- [`listitem`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/listitem_role) (use [`<li>`](/en-US/docs/Web/HTML/Reference/Elements/li) instead)
- [`meter`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/meter_role) (use [`<meter>`](/en-US/docs/Web/HTML/Reference/Elements/meter) instead)
- [`row`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/row_role) (use the [`<tr>`](/en-US/docs/Web/HTML/Reference/Elements/tr) with [`<table>`](/en-US/docs/Web/HTML/Reference/Elements/table))
- [`rowgroup`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/rowgroup_role) (use [`<thead>`](/en-US/docs/Web/HTML/Reference/Elements/thead), [`<tfoot>`](/en-US/docs/Web/HTML/Reference/Elements/tfoot) and [`<tbody>`](/en-US/docs/Web/HTML/Reference/Elements/tbody))
- [`rowheader`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/rowheader_role) (use `<th scope="row">`)
- [`separator`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/separator_role) (use [`<hr>`](/en-US/docs/Web/HTML/Reference/Elements/hr) if it doesn't have focus)
- [`table`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role) (use [`<table>`](/en-US/docs/Web/HTML/Reference/Elements/table))
- [`term`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/term_role) (use [`<dfn>`](/en-US/docs/Web/HTML/Reference/Elements/dfn))

These are included for completeness, but in most cases are rarely, if ever, useful:

- [`associationlist`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`associationlistitemkey`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`associationlistitemvalue`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`blockquote`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`caption`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`code`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`deletion`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`emphasis`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`insertion`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`paragraph`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`strong`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`subscript`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`superscript`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
- [`time`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)

### [2. Widget roles](#2._widget_roles)

Widget roles are used to define common interactive patterns. Like document structure roles, some widget roles have the same semantics as well-supported native HTML elements, and therefore should be avoided. The key difference is that widget roles typically require JavaScript for interaction, while document structure roles often do not.

- [`scrollbar`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/scrollbar_role)
- [`searchbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/searchbox_role)
- [`separator`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/separator_role) (when focusable)
- [`slider`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/slider_role)
- [`spinbutton`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/spinbutton_role)
- [`switch`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/switch_role)
- [`tab`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tab_role)
- [`tabpanel`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tabpanel_role)
- [`treeitem`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treeitem_role)

Avoid using [`button`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/button_role), [`checkbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/checkbox_role), [`gridcell`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/gridcell_role), [`link`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/link_role), [`menuitem`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menuitem_role), [`menuitemcheckbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menuitemcheckbox_role), [`menuitemradio`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menuitemradio_role), [`option`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/option_role), [`progressbar`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/progressbar_role), [`radio`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/radio_role), and [`textbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/textbox_role), which we've included for completeness. For most, semantic equivalents with accessible interactivity are available and supported. See the individual role documentation for more information.

#### Composite widget roles

- [`combobox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/combobox_role)
- [`menu`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menu_role)
- [`menubar`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menubar_role)
- [`tablist`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tablist_role)
- [`tree`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tree_role)
- [`treegrid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role)

Avoid using [`grid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role), [`listbox`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/listbox_role), and [`radiogroup`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/radio_role), which we've included for completeness. See the individual role documentation for more information.

Note that there is also a widget role (`role="widget"`), which is an abstract role and not in the widget role category.

### [3. Landmark roles](#3._landmark_roles)

Landmark roles provide a way to identify the organization and structure of a web page. By classifying and labeling sections of a page, structural information conveyed visually through layout is represented programmatically. Screen readers use landmark roles to provide keyboard navigation to important sections of a page. Use these sparingly. Too many landmark roles create "noise" in screen readers, making it difficult to understand the overall layout of the page.

- [`banner`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/banner_role) (document [`<header>`](/en-US/docs/Web/HTML/Reference/Elements/header))
- [`complementary`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/complementary_role) ([`<aside>`](/en-US/docs/Web/HTML/Reference/Elements/aside))
- [`contentinfo`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/contentinfo_role) (document [`<footer>`](/en-US/docs/Web/HTML/Reference/Elements/footer))
- [`form`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/form_role) ([`<form>`](/en-US/docs/Web/HTML/Reference/Elements/form))
- [`main`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/main_role) ([`<main>`](/en-US/docs/Web/HTML/Reference/Elements/main))
- [`navigation`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/navigation_role) ([`<nav>`](/en-US/docs/Web/HTML/Reference/Elements/nav))
- [`region`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/region_role) ([`<section>`](/en-US/docs/Web/HTML/Reference/Elements/section))
- [`search`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/search_role) ([`<search>`](/en-US/docs/Web/HTML/Reference/Elements/search))

### [4. Live region roles](#4._live_region_roles)

Live Region roles are used to define elements with content that will be dynamically changed. Sighted users can see dynamic changes when they are visually noticeable. These roles help low vision and blind users know if content has been updated. Assistive technologies, like screen readers, can be made to announce dynamic content changes:

- [`alert`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/alert_role)
- [`log`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/log_role)
- [`marquee`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/marquee_role)
- [`status`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role)
- [`timer`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/timer_role)

### [5. Window roles](#5._window_roles)

Window roles define sub-windows to the main document window, within the same window, such as pop up modal dialogs:

- [`alertdialog`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/alertdialog_role)
- [`dialog`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/dialog_role)

### [6. Abstract roles](#6._abstract_roles)

Abstract roles are only intended for use by browsers to help organize and streamline a document. They should not be used by developers writing HTML markup. Doing so will not result in any meaningful information being conveyed to assistive technologies or to users.

Avoid using [`command`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/command_role), [`composite`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/composite_role), [`input`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/input_role), [`landmark`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/landmark_role), [`range`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/range_role), [`roletype`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/roletype_role), [`section`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/section_role), [`sectionhead`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/sectionhead_role), [`select`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/select_role), [`structure`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structure_role), [`widget`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/widget_role), and [`window`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/window_role).

**Note:**
Don't use abstract roles in your sites and applications. They are for use by browsers. They are included for reference only.

**Warning:**
"Abstract roles are used for the ontology. Authors **MUST NOT** use abstract roles in content." - The WAI-ARIA specification

## [Roles defined on MDN](#roles_defined_on_mdn)

The following are the reference pages covering the WAI-ARIA roles discussed on MDN.

[ARIA: alert role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/alert_role)
:   The `alert` role is for important, and usually time-sensitive, information. The `alert` is a type of [`status`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role) processed as an atomic live region.

[ARIA: alertdialog role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/alertdialog_role)
:   The **alertdialog** role is to be used on modal alert dialogs that interrupt a user's workflow to communicate an important message and require a response.

[ARIA: application role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/application_role)
:   The `application` role indicates to assistive technologies that an element *and all of its children* should be treated similar to a desktop application, and no traditional HTML interpretation techniques should be used. This role should only be used to define very dynamic and desktop-like web applications. Most mobile and desktop web apps *are not* considered applications for this purpose.

[ARIA: article role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/article_role)
:   The `article` role indicates a section of a page that could easily stand on its own on a page, in a document, or on a website. It is usually set on related content items such as comments, forum posts, newspaper articles or other items grouped together on one page.

[ARIA: banner role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/banner_role)
:   The `banner` role is for defining a global site header, which usually includes a logo, company name, search feature, and possibly the global navigation or a slogan. It is generally located at the top of the page.

[ARIA: button role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/button_role)
:   The `button` role is for clickable elements that trigger a response when activated by the user. Adding `role="button"` tells the screen reader the element is a button, but provides no button functionality. Use `button` or `input` with `type="button"` instead.

[ARIA: cell role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/cell_role)
:   The `cell` value of the ARIA *role* attribute identifies an element as being a cell in a tabular container that does not contain column or row header information. To be supported, the cell must be nested in an element with the role of `row`.

[ARIA: checkbox role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/checkbox_role)
:   The `checkbox` role is for checkable interactive controls. Elements containing `role="checkbox"` must also include the [`aria-checked`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-checked) attribute to expose the checkbox's state to assistive technology.

[ARIA: columnheader role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/columnheader_role)
:   The `columnheader` value of the ARIA role attribute identifies an element as being a cell in a row contains header information for a column, similar to the native `th` element with column scope.

[ARIA: combobox role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/combobox_role)
:   The `combobox` role identifies an element as either an `input` or a `button` that controls another element, such as a `listbox` or `grid`, that can dynamically pop up to help the user set the value. A combobox can be either editable (allowing text input) or select-only (only allowing selection from the popup).

[ARIA: command role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/command_role)
:   The `command` role defines a widget that performs an action but does not receive input data.

[ARIA: comment role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/comment_role)
:   The `comment` role semantically denotes a comment/reaction to some content on the page, or to a previous comment.

[ARIA: complementary role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/complementary_role)
:   The `complementary` [landmark role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles#3._landmark_roles) is used to designate a supporting section that relates to the main content, yet can stand alone when separated. These sections are frequently presented as sidebars or call-out boxes. If possible, use the [HTML <aside> element](/en-US/docs/Web/HTML/Reference/Elements/aside) instead.

[ARIA: composite role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/composite_role)
:   The `composite` [abstract role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles#6._abstract_roles) indicates a widget that may contain navigable descendants or owned children.

[ARIA: contentinfo role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/contentinfo_role)
:   The `contentinfo` role defines a footer, containing identifying information such as copyright information, navigation links, and privacy statements, found on every document within a site. This section is commonly called a footer.

[ARIA: definition role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/definition_role)
:   The `definition` ARIA role indicates the element is a definition of a term or concept.

[ARIA: dialog role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/dialog_role)
:   The `dialog` role is used to mark up an HTML based application dialog or window that separates content or UI from the rest of the web application or page. Dialogs are generally placed on top of the rest of the page content using an overlay. Dialogs can be either non-modal (it's still possible to interact with content outside of the dialog) or modal (only the content in the dialog can be interacted with).

[ARIA: directory role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/directory_role)
:   The `directory` role was for a list of references to members of a group, such as a static table of contents.

[ARIA: document role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/document_role)
:   The `document` role is for focusable content within complex composite [widgets](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/widget_role) or [applications](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/application_role) for which assistive technologies can switch reading context back to a reading mode.

[ARIA: document structural roles](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structural_roles)
:   ARIA document-structure roles are used to provide a structural description for a section of content.

[ARIA: feed role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/feed_role)
:   A `feed` is a dynamic scrollable `list` of `articles` in which articles are added to or removed from either end of the list as the user scrolls. A `feed` enables screen readers to use the browse mode reading cursor to both read and scroll through a stream of rich content that may continue scrolling infinitely by loading more content as the user reads.

[ARIA: figure role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/figure_role)
:   The ARIA `figure` role can be used to identify a figure inside page content where appropriate semantics do not already exist. A figure is generally considered to be one or more images, code snippets, or other content that puts across information in a different way to a regular flow of text.

[ARIA: form role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/form_role)
:   The `form` role can be used to identify a group of elements on a page that provide equivalent functionality to an HTML form. The form is not exposed as a landmark region unless it has an [accessible name](/en-US/docs/Glossary/Accessible_name).

[ARIA: generic role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/generic_role)
:   The `generic` role creates a nameless container element which has no semantic meaning on its own.

[ARIA: grid role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role)
:   The grid role is for a widget that contains one or more rows of cells. The position of each cell is significant and can be focused using keyboard input.

[ARIA: gridcell role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/gridcell_role)
:   The `gridcell` role is used to make a cell in a [grid](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role) or [treegrid](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role). It is intended to mimic the functionality of the HTML `td` element for table-style grouping of information.

[ARIA: group role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/group_role)
:   The `group` role identifies a set of user interface objects that is not intended to be included in a page summary or table of contents by assistive technologies.

[ARIA: heading role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/heading_role)
:   The `heading` role defines this element as a heading to a page or section, with the [`aria-level`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-level) attribute providing for more structure.

[ARIA: img role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/img_role)
:   The ARIA `img` role can be used to identify multiple elements inside page content that should be considered as a single image. These elements could be images, code snippets, text, emojis, or other content that can be combined to deliver information in a visual manner.

[ARIA: input role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/input_role)
:   The `input` abstract role is a generic type of widget that allows user input.

[ARIA: landmark role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/landmark_role)
:   A landmark is an important subsection of a page. The `landmark` role is an abstract superclass for the aria role values for sections of content that are important enough that users will likely want to be able to navigate directly to them.

[ARIA: link role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/link_role)
:   A `link` widget provides an interactive reference to a resource. The target resource can be either external or local; i.e., either outside or within the current page or application.

[ARIA: list role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/list_role)
:   The ARIA `list` role can be used to identify a list of items. It is normally used in conjunction with the `listitem` role, which is used to identify a list item contained inside the list.

[ARIA: listbox role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/listbox_role)
:   The `listbox` role is used for lists from which a user may select one or more items which are static and, unlike HTML `select` elements, may contain images.

[ARIA: listitem role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/listitem_role)
:   The ARIA `listitem` role can be used to identify an item inside a list of items. It is normally used in conjunction with the [`list`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/list_role) role, which is used to identify a list container.

[ARIA: log role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/log_role)
:   The `log` role is used to identify an element that creates a [live region](/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions) where new information is added in a meaningful order and old information may disappear.

[ARIA: main role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/main_role)
:   The `main` landmark role is used to indicate the primary content of a document. The main content area consists of content that is directly related to or expands upon the central topic of a document, or the main function of an application.

[ARIA: mark role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/mark_role)
:   The `mark` role denotes content which is marked or highlighted for reference or notation purposes, due to the content's relevance in the enclosing context.

[ARIA: marquee role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/marquee_role)
:   A `marquee` is a type of [live region](/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions) containing non-essential information which changes frequently.

[ARIA: math role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/math_role)
:   The `math` role indicates that the content represents a mathematical expression.

[ARIA: menu role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menu_role)
:   The `menu` role is a type of composite widget that offers a list of choices to the user.

[ARIA: menubar role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menubar_role)
:   A `menubar` is a presentation of `menu` that usually remains visible and is usually presented horizontally.

[ARIA: menuitem role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menuitem_role)
:   The `menuitem` role indicates the element is an option in a set of choices contained by a `menu` or `menubar`.

[ARIA: menuitemcheckbox role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menuitemcheckbox_role)
:   A `menuitemcheckbox` is a `menuitem` with a checkable state whose possible values are `true`, `false`, or `mixed`.

[ARIA: menuitemradio role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menuitemradio_role)
:   A `menuitemradio` is checkable menuitem in a set of elements with the same role, only one of which can be checked at a time.

[ARIA: meter role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/meter_role)
:   The `meter` role is used to identify an element being used as a meter.

[ARIA: navigation role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/navigation_role)
:   The `navigation` role is used to identify major groups of links used for navigating through a website or page content.

[ARIA: none role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/none_role)
:   The `none` role is a synonym for the [`presentation`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/presentation_role) role; they both remove an element's implicit ARIA semantics from being exposed to the accessibility tree.

[ARIA: note role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/note_role)
:   A `note` role suggests a section whose content is parenthetic or ancillary to the main content.

[ARIA: option role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/option_role)
:   The `option` role is used for selectable items in a `listbox`.

[ARIA: presentation role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/presentation_role)
:   The `presentation` role and its synonym `none` remove an element's implicit ARIA semantics from being exposed to the accessibility tree.

[ARIA: progressbar role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/progressbar_role)
:   The `progressbar` role defines an element that displays the progress status for tasks that take a long time.

[ARIA: radio role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/radio_role)
:   The `radio` role is one of a group of checkable radio buttons, in a `radiogroup`, where no more than a single radio button can be checked at a time.

[ARIA: radiogroup role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/radiogroup_role)
:   The `radiogroup` role is a group of `radio` buttons.

[ARIA: range role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/range_role)
:   The `range` abstract role is a generic type of structure role representing a range of values.

[ARIA: region role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/region_role)
:   The **`region`** role is used to identify document areas the author deems significant. It is a generic landmark available to aid in navigation when none of the other landmark roles are appropriate.

[ARIA: roletype role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/roletype_role)
:   The **`roletype`** role, an [abstract role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles#6._abstract_roles), is the base role from which all other ARIA roles inherit.

[ARIA: row role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/row_role)
:   An element with `role="row"` is a row of cells within a tabular structure. A row contains one or more cells, grid cells or column headers, and possibly a row header, within a [`grid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role), [`table`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role) or [`treegrid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role), and optionally within a [`rowgroup`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/rowgroup_role).

[ARIA: rowgroup role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/rowgroup_role)
:   An element with `role="rowgroup"` is a group of [rows](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/row_role) within a tabular structure. A `rowgroup` contains one or more rows of [cells](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/cell_role), [grid cells](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/gridcell_role), [column headers](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/columnheader_role), or [row headers](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/rowheader_role) within a [`grid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role), [`table`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role) or [`treegrid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role).

[ARIA: rowheader role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/rowheader_role)
:   An element with `role="rowheader"` is a [cell](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/cell_role) containing header information for a [row](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/row_role) within a tabular structure of a [`grid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/grid_role), [`table`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role) or [`treegrid`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role).

[ARIA: scrollbar role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/scrollbar_role)
:   A `scrollbar` is a graphical object that controls the scrolling of content within a viewing area.

[ARIA: search role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/search_role)
:   The `search` role is used to identify the search functionality; the section of the page used to search the page, site, or collection of sites.

[ARIA: searchbox role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/searchbox_role)
:   The `searchbox` role indicates an element is a type of `textbox` intended for specifying search criteria.

[ARIA: section role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/section_role)
:   The **`section` role**, an abstract role, is a superclass role for renderable structural containment components.

[ARIA: sectionhead role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/sectionhead_role)
:   The **`sectionhead` role**, an abstract role, is superclass role for labels or summaries of the topic of its related section.

[ARIA: select role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/select_role)
:   The **`select` role**, an abstract role, is superclass role for form widgets that allows the user to make selections from a set of choices.

[ARIA: separator role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/separator_role)
:   The `separator` role indicates the element is a divider that separates and distinguishes sections of content or groups of menuitems. The implicit ARIA role of the native thematic break `hr` element is `separator`.

[ARIA: slider role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/slider_role)
:   The `slider` role defines an input where the user selects a value from within a given range.

[ARIA: spinbutton role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/spinbutton_role)
:   The `spinbutton` role defines a type of range that expects the user to select a value from among discrete choices.

[ARIA: status role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role)
:   The `status` role defines a [live region](/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions) containing advisory information for the user that is not important enough to be an [`alert`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/alert_role).

[ARIA: structure role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/structure_role)
:   The `structure` role is for document structural elements.

[ARIA: suggestion role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/suggestion_role)
:   The `suggestion` role semantically denotes a single proposed change to an editable document. This should be used on an element that wraps an element with an `insertion` role, and one with a `deletion` role.

[ARIA: switch role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/switch_role)
:   The ARIA **`switch`** role is functionally identical to the [checkbox](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/checkbox_role) role, except that instead of representing "checked" and "unchecked" states, which are fairly generic in meaning, the `switch` role represents the states "on" and "off."

[ARIA: tab role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tab_role)
:   The ARIA `tab` role indicates an interactive element inside a `tablist` that, when activated, displays its associated `tabpanel`.

[ARIA: table role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/table_role)
:   The `table` value of the ARIA `role` attribute identifies the element containing the role as having a non-interactive table structure containing data arranged in rows and columns, similar to the native `table` HTML element.

[ARIA: tablist role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tablist_role)
:   The `tablist` role identifies the element that serves as the container for a set of `tabs`. The tab content are referred to as `tabpanel` elements.

[ARIA: tabpanel role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tabpanel_role)
:   The ARIA `tabpanel` is a container for the resources of layered content associated with a `tab`.

[ARIA: term role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/term_role)
:   The `term` role can be used for a word or phrase with an optional corresponding [`definition`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/definition_role).

[ARIA: textbox role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/textbox_role)
:   The `textbox` role is used to identify an element that allows the input of free-form text. Whenever possible, rather than using this role, use an `input` element with [type="text"](/en-US/docs/Web/HTML/Reference/Elements/input/text), for single-line input, or a `textarea` element for multi-line input.

[ARIA: timer role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/timer_role)
:   The **`timer`** role indicates to assistive technologies that an element is a numerical counter listing the amount of elapsed time from a starting point or the remaining time until an end point. Assistive technologies will not announce updates to a timer as it has an implicit [`aria-live`](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live) value of `off`.

[ARIA: toolbar role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/toolbar_role)
:   The `toolbar` role defines the containing element as a collection of commonly used function buttons or controls represented in a compact visual form.

[ARIA: tooltip role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tooltip_role)
:   A `tooltip` is a contextual text bubble that displays a description for an element that appears on pointer hover or keyboard focus.

[ARIA: tree role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/tree_role)
:   A `tree` is a widget that allows the user to select one or more items from a hierarchically organized collection.

[ARIA: treegrid role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treegrid_role)
:   The `treegrid` role identifies an element as being grid whose rows can be expanded and collapsed in the same manner as for a `tree`.

[ARIA: treeitem role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/treeitem_role)
:   A `treeitem` is an item in a `tree`.

[ARIA: widget role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/widget_role)
:   The **`widget`** role, an [abstract role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles#6._abstract_roles), is an interactive component of a graphical user interface (GUI).

[ARIA: window role](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/window_role)
:   The `window` role defines a browser or app window.

## [See also](#see_also)

- [Using ARIA: Roles, States, and Properties](/en-US/docs/Web/Accessibility/ARIA/Guides/Techniques)
- [ARIA states and properties](/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Aug 14, 2025 by [MDN contributors](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/accessibility/aria/reference/roles/index.md?plain=1 "Folder: en-us/web/accessibility/aria/reference/roles (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAccessibility%2FARIA%2FReference%2FRoles&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Faccessibility%2Faria%2Freference%2Froles%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAccessibility%2FARIA%2FReference%2FRoles%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Faccessibility%2Faria%2Freference%2Froles%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F4a39dedf2c57c6947339a63a8de0e18a7abe8e2c%0A*+Document+last+modified%3A+2025-08-14T02%3A34%3A04.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")