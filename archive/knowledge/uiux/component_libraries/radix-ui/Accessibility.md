# Accessibility

Source: https://www.radix-ui.com/primitives/docs/overview/accessibility

---

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[ThemesThemes](/)[PrimitivesPrimitives](/primitives)[IconsIcons](/icons)[ColorsColors](/colors)

[Documentation](/primitives/docs)[Case studies](/primitives/case-studies)[Blog](/blog)

Search

`/`

#### Overview

[Introduction](/primitives/docs/overview/introduction)[Getting started](/primitives/docs/overview/getting-started)[Accessibility](/primitives/docs/overview/accessibility)[Releases](/primitives/docs/overview/releases)

#### Guides

[Styling](/primitives/docs/guides/styling)[Animation](/primitives/docs/guides/animation)[Composition](/primitives/docs/guides/composition)[Server-side rendering](/primitives/docs/guides/server-side-rendering)

#### Components

[Accordion](/primitives/docs/components/accordion)[Alert Dialog](/primitives/docs/components/alert-dialog)[Aspect Ratio](/primitives/docs/components/aspect-ratio)[Avatar](/primitives/docs/components/avatar)[Checkbox](/primitives/docs/components/checkbox)[Collapsible](/primitives/docs/components/collapsible)[Context Menu](/primitives/docs/components/context-menu)[Dialog](/primitives/docs/components/dialog)[Dropdown Menu](/primitives/docs/components/dropdown-menu)[Form

Preview](/primitives/docs/components/form)[Hover Card](/primitives/docs/components/hover-card)[Label](/primitives/docs/components/label)[Menubar](/primitives/docs/components/menubar)[Navigation Menu](/primitives/docs/components/navigation-menu)[One-Time Password Field

Preview](/primitives/docs/components/one-time-password-field)[Password Toggle Field

Preview](/primitives/docs/components/password-toggle-field)[Popover](/primitives/docs/components/popover)[Progress](/primitives/docs/components/progress)[Radio Group](/primitives/docs/components/radio-group)[Scroll Area](/primitives/docs/components/scroll-area)[Select](/primitives/docs/components/select)[Separator](/primitives/docs/components/separator)[Slider](/primitives/docs/components/slider)[Switch](/primitives/docs/components/switch)[Tabs](/primitives/docs/components/tabs)[Toast](/primitives/docs/components/toast)[Toggle](/primitives/docs/components/toggle)[Toggle Group](/primitives/docs/components/toggle-group)[Toolbar](/primitives/docs/components/toolbar)[Tooltip](/primitives/docs/components/tooltip)

#### Utilities

[Accessible Icon](/primitives/docs/utilities/accessible-icon)[Direction Provider](/primitives/docs/utilities/direction-provider)[Portal](/primitives/docs/utilities/portal)[Slot](/primitives/docs/utilities/slot)[Visually Hidden](/primitives/docs/utilities/visually-hidden)

Overview

# Accessibility

Radix Primitives follow the WAI-ARIA authoring practices guidelines and are
tested in a wide selection of modern browsers and commonly used assistive
technologies.

We take care of many of the difficult implementation details related to accessibility, including `aria` and `role` attributes, focus management, and keyboard navigation. That means that users should be able to use our components as-is in most contexts and rely on functionality to follow the expected accessibility design patterns.

## [WAI-ARIA](#wai-aria)

[WAI-ARIA](https://www.w3.org/TR/wai-aria-1.2/), published and maintained by the W3C, specifies the semantics for many common UI patterns that show up in Radix Primitives. This is designed to provide meaning for controls that aren't built using elements provided by the browser. For example, if you use a `div` instead of a `button` element to create a button, there are attributes you need to add to the `div` in order to convey that it's a button for screen readers or voice recognition tools.

In addition to semantics, there are behaviors that are expected from different types of components. A `button` element is going to respond to certain interactions in ways that a `div` will not, so it's up to the developer to reimplement those interactions with JavaScript. The [WAI-ARIA authoring practices](https://www.w3.org/TR/wai-aria-practices-1.2/) provide additional guidance for implementing behaviors for various controls that come with Radix Primitives.

## [Accessible Labels](#accessible-labels)

With many built-in form controls, the native HTML `label` element is designed to provide semantic meaning and context for corresponding `input` elements. For non-form control elements, or for custom controls like those provided by Radix Primitives, [WAI-ARIA provides a specification](https://www.w3.org/TR/wai-aria-1.2/#namecalculation) for how to provide accessible names and descriptions to those controls.

Where possible, Radix Primitives include abstractions to make labelling our controls simple. The [`Label`](/primitives/docs/components/label) primitive is designed to work with many of our controls. Ultimately it's up to you to provide those labels so that users have the proper context when navigating your application.

## [Keyboard Navigation](#keyboard-navigation)

Many complex components, like [`Tabs`](/primitives/docs/components/tabs) and [`Dialog`](/primitives/docs/components/dialog), come with expectations from users on how to interact with their content using a keyboard or other non-mouse input modalities. Radix Primitives provide basic keyboard support in accordance with the [WAI-ARIA authoring practices](https://www.w3.org/TR/wai-aria-practices-1.2/).

## [Focus Management](#focus-management)

Proper keyboard navigation and good labelling often go hand-in-hand with managing focus. When a user interacts with an element and something changes as a result, it's often helpful to move focus with the interaction so that the next tab stop is logical depending on the new context of the app. And for screen reader users, moving focus often results in an announcement to convey this new context, which relies on proper labelling.

In many Radix Primitives, we move focus based on the interactions a user normally takes in a given component. For example, in [`AlertDialog`](/primitives/docs/components/alert-dialog), when the modal is opened, focus is programmatically moved to a `Cancel` button element to anticipate a response to the prompt.

Previous[Getting started](/primitives/docs/overview/getting-started)

Next[Releases](/primitives/docs/overview/releases)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/overview/accessibility.mdx "Edit this page on GitHub.")