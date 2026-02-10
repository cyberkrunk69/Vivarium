# Releases

Source: https://www.radix-ui.com/primitives/docs/overview/releases

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

# Releases

Radix Primitives releases and their changelogs.

## [May 5, 2025](#may-5-2025)

This release introduces a brand new primitive in preview: [`PasswordToggleField`](/primitives/docs/components/password-toggle-field).

This new primitive provides components for rendering a password input alongside a button to toggle its visibility. Aside from its primary functionality, it also includes:

- Returning focus to the input when toggling with a pointer
- Maintaining focus when toggling with keyboard or virtual navigation
- Resetting visibility to hidden after form submission to prevent accidental storage
- Implicit accessible labeling for icon-based toggle buttons

This API is currently unstable, and we hope you'll help us test it out! Import the primitive using the `unstable_` prefix.

```
import { unstable_PasswordToggleField as PasswordToggleField } from "radix-ui";

export function PasswordField() {

return (

<PasswordToggleField.Root>

<PasswordToggleField.Input />

<PasswordToggleField.Toggle>

<PasswordToggleField.Icon
					visible={<EyeOpenIcon />}
					hidden={<EyeClosedIcon />}
				/>

</PasswordToggleField.Toggle>

</PasswordToggleField.Root>

);

}
```

### [Other updates](#other-updates)

- Add unstable `Provider`, `Trigger` and `BubbleInput` parts to Checkbox ([#3459](https://github.com/radix-ui/primitives/pull/3459))
- Update default input type to `text` and pass to the underlying input element ([#3510](https://github.com/radix-ui/primitives/pull/3510))

## [April 22, 2025](#april-22-2025)

- Update the dependency for `use-sync-external-store` to ensure entrypoint is valid – [#3491](https://github.com/radix-ui/primitives/pull/3491)

## [April 17, 2025](#april-17-2025)

This release introduces a brand new primitive in preview: [`OneTimePasswordField`](/primitives/docs/components/one-time-password-field).

This new group of components are designed to implement a common design pattern for one-time password fields displayed as separate input fields for each character. This UI is deceptively complex to implement in such a way that interactions follow user expectations. The new primitive handles all of this complexity for you, including:

- Keyboard navigation mimicking the behavior of a single input field
- Overriding values on paste
- Password manager autofill support
- Input validation for numeric and alphanumeric values
- Auto-submit on completion
- Focus management
- Hidden input to provide a single value to form data

As this is a preview release, **the API is currently unstable**. We hope you'll help us test it out and let us know how it goes.

Import the primitive using the `unstable_` prefix.

```
import { unstable_OneTimePasswordField as OneTimePasswordField } from "radix-ui";

export function Verify() {

return (

<OneTimePasswordField.Root>

<OneTimePasswordField.Input />

<OneTimePasswordField.Input />

<OneTimePasswordField.Input />

<OneTimePasswordField.Input />

<OneTimePasswordField.Input />

<OneTimePasswordField.Input />

<OneTimePasswordField.HiddenInput />

</OneTimePasswordField.Root>

);

}
```

### [Other updates](#other-updates-1)

- All form controls with internal bubble inputs now use the Radix `Primitive` component by default. This will allow us to expose these components in a future release so users can better control this behavior in the future.
- Minor improvements to `useControllableState` to enhance performance, reduce surface area for bugs, and log warnings when misused

## [April 8, 2025](#april-8-2025)

- Improved rendering performance for the Tooltip provider – [#2720](https://github.com/radix-ui/primitives/pull/2720)
- Ensure Tooltip is closed when `pointerdown` is fired on the trigger – [#3380](https://github.com/radix-ui/primitives/pull/3380)
- Add support for `crossOrigin` in Avatar images – [#3261](https://github.com/radix-ui/primitives/pull/3261)
- Fix Avatar flashing when an image is already cached – [#3008](https://github.com/radix-ui/primitives/pull/3008)
- Improve `displayName` for better debugging of slottable components – [#3441](https://github.com/radix-ui/primitives/pull/3441)

## [February 5, 2025](#february-5-2025)

- Updated dependencies to remove peer dependency warnings for `react` and `react-dom` – [#3350](https://github.com/radix-ui/primitives/pull/3350)
- Skip forwarding refs to `SlotClone` when the child is a `Fragment` – [#3229](https://github.com/radix-ui/primitives/pull/3229)

## [January 22, 2025](#january-22-2025)

- Added a `radix-ui` package that exposes the latest version of all Radix Primitives from a single place. This tree-shakable entrypoint makes it easier to bring in whatever components you need and keep them up-to-date without worrying about conflicting or duplicate dependencies.
- Updated `aria-hidden` and `react-remove-scroll` dependencies for the following components:
  - Alert Dialog
  - Context Menu
  - Dialog
  - Dropdown Menu
  - Hover Card
  - Menubar
  - Navigation Menu
  - Popover
  - Select
  - Toast
  - Tooltip

## [October 1, 2024](#october-1-2024)

# Alert Dialog

1.1.2

- Fix `allowPinchZoom` bug for trackpad users – [#3127](https://github.com/radix-ui/primitives/pull/3127)

# Avatar

1.1.1

- Check for `referrerPolicy` when checking the image loading status – [#2772](https://github.com/radix-ui/primitives/pull/2772)

# Checkbox

1.1.2

- Fix a bug where `defaultChecked` unexpectedly changed for uncontrolled checkboxes – [#2135](https://github.com/radix-ui/primitives/pull/2135)
- Forward the `form` prop to the bubble input element to fix non-parent form submissions – [#3161](https://github.com/radix-ui/primitives/pull/3161)

# Dialog

1.1.2

- Fix `allowPinchZoom` bug for trackpad users – [#3127](https://github.com/radix-ui/primitives/pull/3127)

# Radio Group

1.2.1

- Forward the `form` prop to the bubble input element to fix non-parent form submissions – [#3161](https://github.com/radix-ui/primitives/pull/3161)

# Scroll Area

1.2.0

- Fix `asChild` prop not working as expected on the `Viewport` – [#2945](https://github.com/radix-ui/primitives/pull/2945)
- Update internal styles to fix other issues with `Viewport` – [#2945](https://github.com/radix-ui/primitives/pull/2945)

# Select

2.1.2

- Fix error thrown when items are initially undefined – [#2623](https://github.com/radix-ui/primitives/pull/2623)
- Fix several bugs for touch devices – [#2939](https://github.com/radix-ui/primitives/pull/2939)
- Forward the `form` prop to the bubble input element to fix non-parent form submissions – [#3161](https://github.com/radix-ui/primitives/pull/3161)
- Fix position bug where popover may start off-screen for long items – [#3149](https://github.com/radix-ui/primitives/pull/3149)

# Slider

1.2.1

- Forward the root `form` prop to each thumb's bubble input element to fix non-parent form submissions – [#3161](https://github.com/radix-ui/primitives/pull/3161)

# Switch

1.1.1

- Forward the `form` prop to the bubble input element to fix non-parent form submissions – [#3161](https://github.com/radix-ui/primitives/pull/3161)

# Toast

1.2.2

- Fix incorrect focus when `hotkey` is an empty array – [#2491](https://github.com/radix-ui/primitives/pull/2491)

## [June 28, 2024](#june-28-2024)

# Checkbox

1.1.1

- Export `CheckedState` type

# Tooltip

1.1.2

- Export `TooltipProviderProps` type

## [June 21, 2024](#june-21-2024)

# Portal

1.1.1

- Add a missing internal utility to `package.json`. The corresponding packages that provide a Portal part also received a patch update. – [#2966](https://github.com/radix-ui/primitives/pull/2966)

## [June 19, 2024](#june-19-2024)

# All primitives

  

Released minor versions for all primitives with the following changes:

- Full React 19 compatability – [#2952](https://github.com/radix-ui/primitives/pull/2952)
- Full RSC compatibility – [#2923](https://github.com/radix-ui/primitives/pull/2923)
- Internal build tooling changes – [#2922](https://github.com/radix-ui/primitives/pull/2922) – [#2931](https://github.com/radix-ui/primitives/pull/2931)
- Update and pin `react-remove-scroll` dependency version to avoid double scrollbar bugs in edge cases – [#2776](https://github.com/radix-ui/primitives/pull/2776)
- Don’t scroll menu items in response to hover – [#2451](https://github.com/radix-ui/primitives/pull/2451)
- Make sure that components that close on Escape key press capture the corresponding keyboard event. This way you can call `stopPropagation` in `onEscapeKeyDown` if you need more control rendering Radix components within another component that closes on Escape key press.
- Make sure that components with roving focus do not interfere with browser or system hotkeys, such as back navigation – [#2739](https://github.com/radix-ui/primitives/pull/2739)
- Make sure that components that support `hideWhenDetached` prop do not allow interactions with hidden content – [#2743](https://github.com/radix-ui/primitives/pull/2743) – [#2745](https://github.com/radix-ui/primitives/pull/2745)

# Dialog

1.1.0

- Log an error when an accessible title via the `Dialog.Title` part is missing – [#2948](https://github.com/radix-ui/primitives/pull/2948)
- Log a warning when an accessible description via the `Dialog.Description` part is missing – [#2948](https://github.com/radix-ui/primitives/pull/2948)

# Label

2.1.0

- Make sure that the component doesn’t interfere when clicking on the spinner of a number input

# Navigation Menu

1.2.0

- Remove unsupported `disableOutsidePointerEvents` prop

# Portal

1.1.0

- Fix hydration error in SSR on the initial render – [#2923](https://github.com/radix-ui/primitives/pull/2923)

# Progress

1.2.0

- Explicitly allow `value={undefined}` to represent an indeterminate state, matching the current practical behaviour – [#2947](https://github.com/radix-ui/primitives/pull/2947)

# Select

2.1.0

- Add `nonce` prop to be able to pass CSP nonce to the inline styles – [#2728](https://github.com/radix-ui/primitives/pull/2728)

# Scroll Area

1.1.0

- Add `nonce` prop to be able to pass CSP nonce to the inline styles – [#2728](https://github.com/radix-ui/primitives/pull/2728)

## [September 25, 2023](#september-25-2023)

# Alert Dialog

1.0.5

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Avatar

1.0.4

- Prevent image flash – [#2340](https://github.com/radix-ui/primitives/pull/2340)

# Context Menu

2.1.5

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Dialog

1.0.5

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Dropdown Menu

2.0.6

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Hover Card

1.0.7

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Menubar

1.0.4

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Navigation Menu

1.1.4

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Popover

1.0.7

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)
- Fix `Popover` nested inside `Dialog` not opening – [#2182](https://github.com/radix-ui/primitives/pull/2182)

# Scroll Area

1.0.5

- Add `scroll-behavior: smooth` compatibility – [#2175](https://github.com/radix-ui/primitives/pull/2175)

# Select

2.0.0Major

- **[Breaking]** Add ability to reset to placeholder using `""` `value`. Note that this is only a breaking change if you were using an option with a `value` of `""`. – [#2174](https://github.com/radix-ui/primitives/pull/2174)
- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)

# Toast

1.1.5

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)

# Tooltip

1.0.7

- Fix pointer-events issue when clicking outside – [#2177](https://github.com/radix-ui/primitives/pull/2177)
- Fix `Portal` part types lying about accepting DOM props – [#2178](https://github.com/radix-ui/primitives/pull/2178)
- Fix issue with boundary padding calculations – [#2185](https://github.com/radix-ui/primitives/pull/2185)
- Add option to always re-position `Content` on the fly – [#2092](https://github.com/radix-ui/primitives/pull/2092)

## [May 26, 2023](#may-26-2023)

This release ensures all of our primitives are ESM compatible. We have also updated to the latest version of [Floating UI](https://floating-ui.com/) for all of our popper-positioned primitives.

# All primitives

- Improve ESM compatibility – [#2130](https://github.com/radix-ui/primitives/pull/2130)
- Fix possible upstream compiler errors (`@types/react` phantom dependency) – [#1896](https://github.com/radix-ui/primitives/pull/1896)

# Context Menu

2.1.4

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)

# Dialog

1.0.4

- Prevent non-modal dialog from re-opening when closing using trigger in Safari – [#2110](https://github.com/radix-ui/primitives/pull/2110)
- Ensure focus trapping is maintained when the focused item is deleted – [#2145](https://github.com/radix-ui/primitives/pull/2145)

# Dropdown Menu

2.0.5

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)

# Hover Card

1.0.6

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)

# Menubar

1.0.3

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)

# Navigation Menu

1.1.3

- Do not close when clicking items and meta key is down – [#2080](https://github.com/radix-ui/primitives/pull/2080)

# Popover

1.0.6

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)
- Prevent non-modal popover from re-opening when closing using trigger in Safari – [#2110](https://github.com/radix-ui/primitives/pull/2110)
- Ensure `--radix-popper-available-width` is calculated correctly when using `collisionBoundary` – [#2032](https://github.com/radix-ui/primitives/pull/2032)

# Select

1.2.2

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)
- Improve scroll buttons touch screen support – [#1771](https://github.com/radix-ui/primitives/pull/1771)

# Slider

1.1.2

- Clamp thumb position within range – [#1988](https://github.com/radix-ui/primitives/pull/1988)

# Slot

1.0.2

- Ensure `Slot` can be used in a React Server Component – [#2116](https://github.com/radix-ui/primitives/pull/2116)

# Tooltip

1.0.6

- Position content correctly when matching trigger size – [#1995](https://github.com/radix-ui/primitives/pull/1995)
- Improve large content hoverability – [#2155](https://github.com/radix-ui/primitives/pull/2155)

## [March 8, 2023](#march-8-2023)

This release introduces a brand new primitive in preview: [`Form`](/primitives/docs/components/form).

# Form

0.0.2Preview

- New primitive – [#1998](https://github.com/radix-ui/primitives/pull/1998)

## [February 24, 2023](#february-24-2023)

# Checkbox

1.0.2

- Reset checkbox state when form is reset – [#1733](https://github.com/radix-ui/primitives/pull/1733)

# ContextMenu

2.1.2

- Expose new CSS custom properties to enable size constraints – [#1942](https://github.com/radix-ui/primitives/pull/1942)
- Don't exit fullscreen mode when pressing escape to dismiss from submenu – [#1752](https://github.com/radix-ui/primitives/pull/1752)
- Relax `onCheckedChange` type on `ContextMenu.CheckboxItem` – [#1778](https://github.com/radix-ui/primitives/pull/1778)

# DropdownMenu

2.0.3

- Expose new CSS custom properties to enable size constraints – [#1942](https://github.com/radix-ui/primitives/pull/1942)
- Don't exit fullscreen mode when pressing escape to dismiss from submenu – [#1752](https://github.com/radix-ui/primitives/pull/1752)
- Relax `onCheckedChange` type on `DropdownMenu.CheckboxItem` – [#1778](https://github.com/radix-ui/primitives/pull/1778)

# HoverCard

1.0.4

- Expose new CSS custom properties to enable size constraints – [#1942](https://github.com/radix-ui/primitives/pull/1942)

# Menubar

1.0.1

- Expose new CSS custom properties to enable size constraints – [#1943](https://github.com/radix-ui/primitives/pull/1943)
- Don't exit fullscreen mode when pressing escape to dismiss from submenu – [#1752](https://github.com/radix-ui/primitives/pull/1752)
- Relax `onCheckedChange` type on `Menubar.CheckboxItem` – [#1778](https://github.com/radix-ui/primitives/pull/1778)

# Popover

1.0.4

- Expose new CSS custom properties to enable size constraints – [#1942](https://github.com/radix-ui/primitives/pull/1942)

# Tooltip

1.0.4

- Expose new CSS custom properties to enable size constraints – [#1942](https://github.com/radix-ui/primitives/pull/1942)

## [January 17, 2023](#january-17-2023)

This release introduces a brand new primitive: [`Menubar`](/primitives/docs/components/menubar). It also adds support for a highly requested feature for [`Select`](/primitives/docs/components/select): the ability to position the content in a similar way to `Popover` or `DropdownMenu`.

# Accordion

1.1.0

- Add horizontal orientation support with new `orientation` prop, as well as RTL support with `dir` – [#1850](https://github.com/radix-ui/primitives/pull/1850)

# Context Menu

2.1.1

- Fix consistency issue with RTL positioning – [#1890](https://github.com/radix-ui/primitives/pull/1890)

# Dropdown Menu

2.0.2

- Fix consistency issue with RTL positioning – [#1890](https://github.com/radix-ui/primitives/pull/1890)

# Hover Card

1.0.3

- Fix consistency issue with RTL positioning – [#1890](https://github.com/radix-ui/primitives/pull/1890)

# Menubar

1.0.0Major

- New primitive – [#1846](https://github.com/radix-ui/primitives/pull/1846)

# Popover

1.0.3

- Fix consistency issue with RTL positioning – [#1890](https://github.com/radix-ui/primitives/pull/1890)

# Select

1.2.0

- Add `position` prop to `Select.Content` to enable popper positioning – [#1853](https://github.com/radix-ui/primitives/pull/1853)

# Tooltip

1.0.3

- Fix consistency issue with RTL positioning – [#1890](https://github.com/radix-ui/primitives/pull/1890)

## [December 14, 2022](#december-14-2022)

# Context Menu

2.1.0

- Add `disabled` prop to `ContextMenu.Trigger` – [#1746](https://github.com/radix-ui/primitives/pull/1746)

## [November 15, 2022](#november-15-2022)

# Select

1.1.2

- Fix invalid `pointerId` in Cypress when running Firefox – [#1753](https://github.com/radix-ui/primitives/pull/1753)

## [October 17, 2022](#october-17-2022)

# Accordion

1.0.1

- Fix initial animation playback in Firefox and Safari – [#1710](https://github.com/radix-ui/primitives/pull/1710)

# Alert Dialog

1.0.2

- Fix issue with textarea elements not being scrollable in Firefox – [#1550](https://github.com/radix-ui/primitives/pull/1550)

# Collapsible

1.0.1

- Fix initial animation playback in Firefox and Safari – [#1710](https://github.com/radix-ui/primitives/pull/1710)

# Context Menu

2.0.1Major

- **[Breaking]** Add support for indeterminate state on `ContextMenu.CheckboxItem`. Note that this is only a breaking change if you are currently using the `CheckboxItem` part and your codebase is written in TypeScript. – [#1624](https://github.com/radix-ui/primitives/pull/1624)

# Dialog

1.0.2

- Fix issue with textarea elements not being scrollable in Firefox – [#1550](https://github.com/radix-ui/primitives/pull/1550)

# Dropdown Menu

2.0.1Major

- **[Breaking]** Add support for indeterminate state on `DropdownMenu.CheckboxItem`. Note that this is only a breaking change if you are currently using the `CheckboxItem` part and your codebase is written in TypeScript. – [#1624](https://github.com/radix-ui/primitives/pull/1624)
- Correctly pair `DropdownMenu.Trigger` open state with `aria-expanded` when closed – [#1644](https://github.com/radix-ui/primitives/pull/1644)
- Fix issue with eager selection of items when using `asChild` – [#1647](https://github.com/radix-ui/primitives/pull/1647)
- Fix issue with dismissing when the component is used in a separate popup window – [#1677](https://github.com/radix-ui/primitives/pull/1677)

# Hover Card

1.0.2

- Improve text selection experience – [#1692](https://github.com/radix-ui/primitives/pull/1692)

# Label

2.0.0Major

- **[Breaking]** Remove `useLabelContext` and support for fully custom controls. For native labelling to work, ensure your custom controls are based on native elements such as `button` or `input`. – [#1686](https://github.com/radix-ui/primitives/pull/1686)
- Improve native behavior by using the native `label` element – [#1686](https://github.com/radix-ui/primitives/pull/1686)

# Navigation Menu

1.1.1

- Prevent menu from re-opening with the pointer after being dismissed with escape – [#1579](https://github.com/radix-ui/primitives/pull/1579)
- Add `delayDuration` and `skipDelayDuration` props to `NavigationMenu.Root`. Note that by default, triggers now have a brief delay before opening in order to improve UX, this can be modified using the props provided. – [#1716](https://github.com/radix-ui/primitives/pull/1716)

# Radio Group

1.1.0

- Add `disabled` prop to `RadioGroup.Root` – [#1530](https://github.com/radix-ui/primitives/pull/1530)
- Fix issue where `RadioGroup.Root` was focusable when all items were disabled – [#1530](https://github.com/radix-ui/primitives/pull/1530)

# Select

1.1.1

- Add `disabled` prop to `Select.Root` – [#1699](https://github.com/radix-ui/primitives/pull/1699)
- Add `required` prop to `Select.Root` – [#1598](https://github.com/radix-ui/primitives/pull/1598)

# Slider

1.1.0

- Add ability to visually invert the slider using the new `inverted` prop on `Slider.Root` – [#1695](https://github.com/radix-ui/primitives/pull/1695)
- Add `onValueCommit` prop to `Slider.Root` to better handle discrete value changes – [#1696](https://github.com/radix-ui/primitives/pull/1696)

# Slot

1.0.1

- Stop eagerly creating callback props – [#1713](https://github.com/radix-ui/primitives/pull/1713)

# Toast

1.1.1

- Fix regression with screen readers announcing as "group" rather than "status" – [#1556](https://github.com/radix-ui/primitives/pull/1556)
- Fix regression with `ref` assignments on child elements returning `null` – [#1668](https://github.com/radix-ui/primitives/pull/1668)
- Add `onPause` and `onResume` props to `Toast.Root` – [#1669](https://github.com/radix-ui/primitives/pull/1669)
- Fix timer reset issue which would cause toasts to dismiss early in some cases – [#1682](https://github.com/radix-ui/primitives/pull/1682)

# Toolbar

1.0.1

- Prevent `Toolbar.Item` click handlers firing twice – [#1526](https://github.com/radix-ui/primitives/pull/1526)

# Tooltip

1.0.2

- Ensure tooltip doesn't open if interacting with the trigger before the open timer expires – [#1693](https://github.com/radix-ui/primitives/pull/1693)

## [July 21, 2022](#july-21-2022)

With this release, we start following semantic versioning strictly. All primitives are now versioned 1.0.0.

We also move the [`Select`](/primitives/docs/components/select), [`Toast`](/primitives/docs/components/toast) and [`NavigationMenu`](/primitives/docs/components/navigation-menu) from preview to stable.

# All primitives

- Improve support for React 18 – [#1329](https://github.com/radix-ui/primitives/pull/1329)
- **[Breaking]** Improve RTL performance. You need to use [`DirectionProvider`](/primitives/docs/utilities/direction-provider) if you were relying on `dir` attribute inheritance from document (or any element). – [#1119](https://github.com/radix-ui/primitives/pull/1119)

# Alert Dialog

1.0.0Major

- **[Breaking]** Remove `allowPinchZoom` prop, now defaults to `true` – [#1514](https://github.com/radix-ui/primitives/pull/1514)
- Improve compatibility with JS animation libraries with `forceMount` on `AlertDialog.Portal` – [#1075](https://github.com/radix-ui/primitives/pull/1075)
- Fix regressions with page interactivity while/after closing dialog – [#1401](https://github.com/radix-ui/primitives/pull/1401)

# Context Menu

1.0.0Major

- **[Breaking]** Improve indirect nesting of context menus. Submenus must now be created using explicit parts. – [#1394](https://github.com/radix-ui/primitives/pull/1394)
- **[Breaking]** Remove `allowPinchZoom` prop, now defaults to `true` – [#1514](https://github.com/radix-ui/primitives/pull/1514)
- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. Note that `z-index` isn't managed anymore so you have full control of layering. – [#1429](https://github.com/radix-ui/primitives/pull/1429)
- **[Breaking]** Remove `offset` on `Arrow` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- **[Breaking]** Rename `collisionTolerance` to `collisionPadding` on `Content` part and accepts a number or a padding object – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- Fix issue with native context menu appearing in React 18 – [#1378](https://github.com/radix-ui/primitives/pull/1378)
- Add `data-highlighted` attribute to support styling – [#1388](https://github.com/radix-ui/primitives/pull/1388)
- Add `data-state` attribute to `Trigger` part – [#1455](https://github.com/radix-ui/primitives/pull/1455)
- Add `collisionBoundary`, `arrowPadding`, `sticky`, `hideWhenDetached` props on `Content` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)

# Dialog

1.0.0Major

- **[Breaking]** Remove `allowPinchZoom` prop, now defaults to `true` – [#1514](https://github.com/radix-ui/primitives/pull/1514)
- Improve compatibility with JS animation libraries with `forceMount` on `Dialog.Portal` – [#1075](https://github.com/radix-ui/primitives/pull/1075)
- Fix regressions with page interactivity while/after closing dialog – [#1401](https://github.com/radix-ui/primitives/pull/1401)

# Dropdown Menu

1.0.0Major

- **[Breaking]** Improve indirect nesting of dropdown menus. Submenus must now be created using explicit parts. – [#1394](https://github.com/radix-ui/primitives/pull/1394)
- **[Breaking]** Remove `allowPinchZoom` prop, now defaults to `true` – [#1514](https://github.com/radix-ui/primitives/pull/1514)
- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. Note that `z-index` isn't managed anymore so you have full control of layering. – [#1429](https://github.com/radix-ui/primitives/pull/1429)
- **[Breaking]** Remove `offset` on `Arrow` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- **[Breaking]** Rename `collisionTolerance` to `collisionPadding` on `Content` part and accepts a number or a padding object – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- Add `data-highlighted` attribute to support styling – [#1388](https://github.com/radix-ui/primitives/pull/1388)
- Prevent escape key from exiting fullscreen mode in Firefox & Safari – [#1423](https://github.com/radix-ui/primitives/pull/1423)
- Add `collisionBoundary`, `arrowPadding`, `sticky`, `hideWhenDetached` props on `Content` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)

# Hover Card

1.0.0Major

- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. Note that `z-index` isn't managed anymore so you have full control of layering. – [#1426](https://github.com/radix-ui/primitives/pull/1426)
- **[Breaking]** Remove `offset` on `Arrow` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- **[Breaking]** Rename `collisionTolerance` to `collisionPadding` on `Content` part and accepts a number or a padding object – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- Add `collisionBoundary`, `arrowPadding`, `sticky`, `hideWhenDetached` props on `Content` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)

# Navigation Menu

1.0.0Major

- Ensure menu closes after clicking `NavigationMenu.Link` – [#1347](https://github.com/radix-ui/primitives/pull/1347)
- Add `onSelect` prop to `NavigationMenu.Link` – [#1372](https://github.com/radix-ui/primitives/pull/1372)

# Popover

1.0.0Major

- **[Breaking]** Remove `allowPinchZoom` prop, now defaults to `true` – [#1514](https://github.com/radix-ui/primitives/pull/1514)
- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. Note that `z-index` isn't managed anymore so you have full control of layering. – [#1425](https://github.com/radix-ui/primitives/pull/1425)
- **[Breaking]** Remove `offset` on `Arrow` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- **[Breaking]** Rename `collisionTolerance` to `collisionPadding` on `Content` part and accepts a number or a padding object – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- Add `collisionBoundary`, `arrowPadding`, `sticky`, `hideWhenDetached` props on `Content` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)

# Portal

1.0.0Major

- **[Breaking]** Note that `z-index` isn't managed anymore so you have full control of layering. The prop to provide a custom container evolves from `containerRef` (ref) to `container` (element). The `data-radix-portal` was removed because you can use `asChild` to control the element. – [#1463](https://github.com/radix-ui/primitives/pull/1463)

# RadioGroup

1.0.0Major

- Add `aria-required` to root – [#1422](https://github.com/radix-ui/primitives/pull/1422)

# Scroll Area

1.0.0Major

- `ScrollArea.Thumb` is now animatable – [#1392](https://github.com/radix-ui/primitives/pull/1392)

# Select

1.0.0Major

- **[Breaking]** Renamed `data-state` values from `active|inactive` to `checked|unchecked` – [#1388](https://github.com/radix-ui/primitives/pull/1388)
- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. Note that `z-index` isn't managed anymore so you have full control of layering. – [#1459](https://github.com/radix-ui/primitives/pull/1459)
- Fix position breaking when using `asChild` on `Select.Content` – [#1245](https://github.com/radix-ui/primitives/pull/1245)
- Improve trigger/content alignment when `Select.Content` has padding – [#1312](https://github.com/radix-ui/primitives/pull/1312)
- Fix trigger/content alignment when there are less than 5 items – [#1355](https://github.com/radix-ui/primitives/pull/1355)
- Support trigger/content alignment when no value is provided – [#1379](https://github.com/radix-ui/primitives/pull/1379)
- Add `data-highlighted` attribute to support styling – [#1388](https://github.com/radix-ui/primitives/pull/1388)
- Add support for placeholder via `placeholder` prop on `Select.Value` – [#1384](https://github.com/radix-ui/primitives/pull/1384)
- Resolve value mismatch with underlying native select – [#1421](https://github.com/radix-ui/primitives/pull/1421)

# Slot

1.0.0Major

- Fix issue with children ordering when using `Slottable` – [#1376](https://github.com/radix-ui/primitives/pull/1376)

# Tabs

1.0.0Major

- Add support for lifecycle animation to `Tabs.Content` – [#1346](https://github.com/radix-ui/primitives/pull/1346)

# Toast

1.0.0Major

- **[Breaking]** The default toast order has changed, they now render top to bottom from oldest to newest – [#1469](https://github.com/radix-ui/primitives/pull/1469)
- Improve Typescript types when using `asChild` – [#1300](https://github.com/radix-ui/primitives/pull/1300)
- Fix issue with toast reordering when updating React's `key` prop – [#1283](https://github.com/radix-ui/primitives/pull/1283)
- Improve compatability with animation libraries – [#1468](https://github.com/radix-ui/primitives/pull/1468)

# Tooltip

1.0.0Major

- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. Note that `z-index` isn't managed anymore so you have full control of layering. – [#1427](https://github.com/radix-ui/primitives/pull/1427)
- **[Breaking]** By default `Tooltip.Content` will remain open when hovering (WCAG 2.1 Content on Hover compliance). `disableHoverableContent` can be supplied to `Tooltip.Provider` to restore previous behavior – [#1490](https://github.com/radix-ui/primitives/pull/1490)
- **[Breaking]** `side` on `Tooltip.Content` now defaults to `top` – [#1490](https://github.com/radix-ui/primitives/pull/1490)
- **[Breaking]** `Tooltip.Provider` is now required, you must wrap your app to avoid regressions. – [#1490](https://github.com/radix-ui/primitives/pull/1490)
- **[Breaking]** Remove `offset` on `Arrow` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- **[Breaking]** Rename `collisionTolerance` to `collisionPadding` on `Content` part and accepts a number or a padding object – [#1531](https://github.com/radix-ui/primitives/pull/1531)
- Improve layering of tooltip with other primitives – [#1314](https://github.com/radix-ui/primitives/pull/1314)
- Fix tooltip closing when transforming/animation trigger – [#937](https://github.com/radix-ui/primitives/pull/937)
- Add `collisionBoundary`, `arrowPadding`, `sticky`, `hideWhenDetached` props on `Content` part – [#1531](https://github.com/radix-ui/primitives/pull/1531)

## [February 28, 2022](#february-28-2022)

This release introduces 3 brand new primitives in preview: [`Select`](/primitives/docs/components/select), [`Toast`](/primitives/docs/components/toast) and [`NavigationMenu`](/primitives/docs/components/navigation-menu), whilst also shipping a ton of fixes and improvements.

# Accordion

0.1.6

- Prevent form submission when pressing `Accordion.Trigger` – [#1085](https://github.com/radix-ui/primitives/pull/1085)
- Fix animation issue with React 18 – [#1125](https://github.com/radix-ui/primitives/pull/1125)

# Alert Dialog

0.1.7

- Improve pointer-events management – [#1079](https://github.com/radix-ui/primitives/pull/1079)

# Checkbox

0.1.5

- Prevent activation via enter key – [#1104](https://github.com/radix-ui/primitives/pull/1104)

# Collapsible

0.1.6

- Fix animation issue with React 18 – [#1125](https://github.com/radix-ui/primitives/pull/1125)

# Context Menu

0.1.6

- Prevent `DropdownMenu.TriggerItem` click from firing twice – [#1057](https://github.com/radix-ui/primitives/pull/1057)
- Improve idle performance – [#1040](https://github.com/radix-ui/primitives/pull/1040)

# Dialog

0.1.7Major

- Improve pointer-events management – [#1079](https://github.com/radix-ui/primitives/pull/1079)
- **[Breaking]** `Dialog.Title` is now a required part so will throw an error if not used. `aria-describedby={undefined}` must be passed to `Dialog.Content` if no description is needed. – [#1098](https://github.com/radix-ui/primitives/pull/1098)

# Dropdown Menu

0.1.6

- Improve composability with `Dialog`/`AlertDialog` – [#1097](https://github.com/radix-ui/primitives/pull/1097)
- Prevent clicking trigger to close from immediately reopening in non-modal mode – [#1059](https://github.com/radix-ui/primitives/pull/1059)
- Prevent `DropdownMenu.TriggerItem` click from firing twice – [#1057](https://github.com/radix-ui/primitives/pull/1057)
- Improve idle performance – [#1040](https://github.com/radix-ui/primitives/pull/1040)

# Navigation Menu

0.1.2Preview

- New primitive – [#1172](https://github.com/radix-ui/primitives/pull/1172)

# Radio Group

0.1.5

- Prevent activation via enter key – [#1104](https://github.com/radix-ui/primitives/pull/1104)

# Select

0.1.1Preview

- New primitive – [#1169](https://github.com/radix-ui/primitives/pull/1169)

# Slider

0.1.4

- Prevent page scroll when using `Home` and `End` keys – [#1076](https://github.com/radix-ui/primitives/pull/1076)

# Tabs

0.1.5

- Prevent accidental focus activation via right click – [#1114](https://github.com/radix-ui/primitives/pull/1114)

# Toast

0.1.1Preview

- New primitive – [#1165](https://github.com/radix-ui/primitives/pull/1165)

# Toggle Group

0.1.5

- Improve accessibility by using radio role for single toggle group – [#1118](https://github.com/radix-ui/primitives/pull/1118)

## [December 13, 2021](#december-13-2021)

This release focuses on React 18 support and introduces a number of breaking changes to some packages, mostly related to portalling dialogs.

# All primitives

- **[Breaking]** Deprecate `IdProvider`. Improves support for React 18 going forward and is no longer needed in older versions. Remove from your app to avoid deprecation warnings. – [#1006](https://github.com/radix-ui/primitives/pull/1006)

# Accordion

0.1.5Major

- Improve React 18 support – [#984](https://github.com/radix-ui/primitives/pull/984)
- Improve dev mode errors with mismatched `type` and `value` props – [#979](https://github.com/radix-ui/primitives/pull/979)
- Prevent `Accordion.Content` height animation on initial page load – [#977](https://github.com/radix-ui/primitives/pull/977)

# Alert Dialog

0.1.5Major

- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. – [#936](https://github.com/radix-ui/primitives/pull/936)
- **[Breaking]** Support scrolling within `AlertDialog.Overlay`. Move `allowPinchZoom` to root. – [#963](https://github.com/radix-ui/primitives/pull/963)
- Fix `asChild` TypeScript error – [#924](https://github.com/radix-ui/primitives/pull/924)

# Collapsible

0.1.5

- Prevent `Collapsible.Content` height animation on initial page load – [#977](https://github.com/radix-ui/primitives/pull/977)

# Dialog

0.1.5Major

- **[Breaking]** Add new `Portal` part. To avoid regressions, use this part if you want portalling behavior. – [#936](https://github.com/radix-ui/primitives/pull/936)
- **[Breaking]** Support scrolling within `Dialog.Overlay`. Move `allowPinchZoom` to root. – [#963](https://github.com/radix-ui/primitives/pull/963)

# Dropdown Menu

0.1.4

- Prevent disabled trigger from opening menu – [#974](https://github.com/radix-ui/primitives/pull/974)

# Hover Card

0.1.3

- Fix ability to focus `HoverCard` when inside a dialog – [#920](https://github.com/radix-ui/primitives/pull/920)

# Radio Group

0.1.4

- Prevent programmatic focus from changing value – [#939](https://github.com/radix-ui/primitives/pull/939)

# Tabs

0.1.4Major

- **[Breaking]** Change `Tabs.Trigger` to `button` element – [#981](https://github.com/radix-ui/primitives/pull/981)
- Improve TSDocs – [#978](https://github.com/radix-ui/primitives/pull/978)

# Toggle Group

0.1.4

- Remove invalid `aria-orientation` attribute on `role=group` element – [#965](https://github.com/radix-ui/primitives/pull/965)

# Toolbar

0.1.4

- Fix `asChild` TypeScript error – [#924](https://github.com/radix-ui/primitives/pull/924)
- Remove invalid `toolbaritem` role – [#950](https://github.com/radix-ui/primitives/pull/950)

# Tooltip

0.1.6Major

- **[Breaking]** Add new `TooltipProvider` part. You must wrap your app to avoid regressions. – [#1007](https://github.com/radix-ui/primitives/pull/1007)
- **[Breaking]** Remove `type=button` attribute from `Tooltip.Trigger` – [#1011](https://github.com/radix-ui/primitives/pull/1011)
- Fix tooltip activation regression – [#1035](https://github.com/radix-ui/primitives/pull/1035)

# Slot

0.1.2

- Fix `key` warnings – [#1015](https://github.com/radix-ui/primitives/pull/1015)

## [October 15, 2021](#october-15-2021)

# All primitives

- All primitives are now versioned 0.1.1
- Fix composability issues between primitives by scoping context – [#906](https://github.com/radix-ui/primitives/pull/906)
- Fix CSS unmount animations – [#851](https://github.com/radix-ui/primitives/pull/851)

# Accordion

0.1.1

- Add new CSS variable to `Accordion.Content` to help with width animations – [#879](https://github.com/radix-ui/primitives/pull/879)

# Alert Dialog

0.1.1Major

- Improve composability with `Dialog` – [#906](https://github.com/radix-ui/primitives/pull/906)
- **[Breaking]** Remove `AlertDialog.Content` `onInteractOutside` prop – [#846](https://github.com/radix-ui/primitives/pull/846)

# Dialog

0.1.1

- Improve composability with `AlertDialog` – [#906](https://github.com/radix-ui/primitives/pull/906)
- Add pinch to zoom support to `DropdownMenu.Content` via `allowPinchZoom` prop – [#884](https://github.com/radix-ui/primitives/pull/884)

# Context Menu

0.1.1

- Add pinch to zoom support to `ContextMenu.Content` via `allowPinchZoom` prop – [#884](https://github.com/radix-ui/primitives/pull/884)
- Prevent scroll via arrow keypress on submenu triggers – [#908](https://github.com/radix-ui/primitives/pull/908)

# Collapsible

0.1.1

- Add new CSS variable to `Collapsible.Content` to help with width animations – [#879](https://github.com/radix-ui/primitives/pull/879)

# Checkbox

0.1.1

- Prevent screen reader virtual cursor from accessing hidden input – [#870](https://github.com/radix-ui/primitives/pull/870)

# Dropdown Menu

0.1.1

- Improve composability with `Tooltip` – [#906](https://github.com/radix-ui/primitives/pull/906)
- Add pinch to zoom support to `DropdownMenu.Content` via `allowPinchZoom` prop – [#884](https://github.com/radix-ui/primitives/pull/884)
- Prevent scroll via arrow keypress on submenu triggers – [#908](https://github.com/radix-ui/primitives/pull/908)

# Hover Card

0.1.1

- Open on focus to improve keyboard support – [#902](https://github.com/radix-ui/primitives/pull/902)
- Compose correct pointer events internally – [#893](https://github.com/radix-ui/primitives/pull/893)

# Label

0.1.1

- Allow its children to prevent event propagation – [#861](https://github.com/radix-ui/primitives/pull/861)

# Radio Group

0.1.1

- Prevent screen reader virtual cursor from accessing hidden inputs – [#870](https://github.com/radix-ui/primitives/pull/870)

# Popover

0.1.1

- Add pinch to zoom support to `Popover.Content` via `allowPinchZoom` prop – [#884](https://github.com/radix-ui/primitives/pull/884)

# Slider

0.1.1

- Fix calculations when value is `0` – [#866](https://github.com/radix-ui/primitives/pull/866)

# Switch

0.1.1

- Prevent screen reader virtual cursor from accessing hidden input – [#870](https://github.com/radix-ui/primitives/pull/870)

# Tabs

0.1.1Major

- **[Breaking]** Unmount content within `Tabs.Content` when tab is inactive – [#859](https://github.com/radix-ui/primitives/pull/859)

## [September 7, 2021](#september-7-2021)

# All primitives

- All primitives moved to **Beta** and are now versioned 0.1.0
- **[Breaking]** Replace polymorphic `as` prop with `asChild` boolean prop. Learn more
  about how to [change the rendered element here](/primitives/docs/guides/composition) – [#835](https://github.com/radix-ui/primitives/pull/835)

# Dialog

0.1.0

- Improve composability with `DropdownMenu` – [#818](https://github.com/radix-ui/primitives/pull/818)

# Dropdown Menu

0.1.0

- Improve composability with `Dialog` – [#818](https://github.com/radix-ui/primitives/pull/818)
- Re-enable `pointer-events` when closed – [#819](https://github.com/radix-ui/primitives/pull/819)
- Prevent body text from selecting on close (Firefox) – [#812](https://github.com/radix-ui/primitives/pull/812)
- Ensure sub triggers receive focus on click (iOS Safari) – [#820](https://github.com/radix-ui/primitives/pull/820)

# Primitive

0.1.0Major

- **[Breaking]** Deprecate `extendPrimitive` utility – [#840](https://github.com/radix-ui/primitives/pull/840)

## [August 4, 2021](#august-4-2021)

# All primitives

- Improve polymorphic types performance – [#784](https://github.com/radix-ui/primitives/pull/784)

# Alert Dialog

0.0.20Major

- **[Breaking]** Remove `AlertDialog.Content` `onPointerDownOutside` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- Prevent outside pointer events triggering prematurely on touch devices – [#767](https://github.com/radix-ui/primitives/pull/767)

# Context Menu

0.0.24Major

- Add modality support via `modal` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- **[Breaking]** Remove `ContextMenu.Content` `disableOutsidePointerEvents` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- Prevent outside pointer events triggering prematurely on touch devices – [#767](https://github.com/radix-ui/primitives/pull/767)

# Dialog

0.0.20

- Add modality support via `modal` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- Improve animation rendering in React 18 – [#776](https://github.com/radix-ui/primitives/pull/776)
- Ensure focus is restored to trigger on close when using the `autofocus` attribute on a child element – [#739](https://github.com/radix-ui/primitives/pull/739)
- Prevent outside pointer events triggering prematurely on touch devices – [#767](https://github.com/radix-ui/primitives/pull/767)
- Ensure iOS Safari consistently focuses the first focusable element – [#776](https://github.com/radix-ui/primitives/pull/776)

# Dropdown Menu

0.0.23Major

- Add modality support via `modal` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- **[Breaking]** Remove `DropdownMenu.Content` `disableOutsideScroll` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- **[Breaking]** Remove `DropdownMenu.Content` `disableOutsidePointerEvents` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- Prevent outside pointer events triggering prematurely on touch devices – [#767](https://github.com/radix-ui/primitives/pull/767)

# Popover

0.0.20Major

- Add modality support via `modal` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- **[Breaking]** Remove `Popover.Content` `disableOutsideScroll` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- **[Breaking]** Remove `Popover.Content` `disableOutsidePointerEvents` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- **[Breaking]** Remove `Popover.Content` `trapFocus` prop – [#700](https://github.com/radix-ui/primitives/pull/700)
- Improve animation rendering in React 18 – [#776](https://github.com/radix-ui/primitives/pull/776)
- Ensure focus is restored to trigger on close when using the `autofocus` attribute on a child element – [#739](https://github.com/radix-ui/primitives/pull/739)
- Prevent outside pointer events triggering prematurely on touch devices – [#767](https://github.com/radix-ui/primitives/pull/767)
- Ensure iOS Safari consistently focuses the first focusable element – [#776](https://github.com/radix-ui/primitives/pull/776)

# Scroll Area

0.0.16

- Add `data-state` to `ScrollBar` part – [#801](https://github.com/radix-ui/primitives/pull/801)

# Slider

0.0.17

- Prevent thumb receiving focus when disabled – [#777](https://github.com/radix-ui/primitives/pull/777)
- Prevent focus loss on thumb when using `React.StrictMode` – [#794](https://github.com/radix-ui/primitives/pull/794)

## [June 24, 2021](#june-24-2021)

# Context Menu

0.0.23

- Can now be triggered on touch with a long press – [#743](https://github.com/radix-ui/primitives/pull/743)

# Dialog

0.0.19

- Add optional `Title` and `Description` parts for simpler labelling – [#741](https://github.com/radix-ui/primitives/pull/741)

# Scroll Area

0.0.15

- Add `data-orientation` to `Scrollbar` for styling convenience – [#720](https://github.com/radix-ui/primitives/pull/720)
- Fix `forceMount` type issue on `Scrollbar` – [#738](https://github.com/radix-ui/primitives/pull/738)

# Slider

0.0.16

- Ensure the correct thumb is focused when using keyboard and crossing another thumb – [#731](https://github.com/radix-ui/primitives/pull/731)
- Ensure only one arrow press is needed when crossing another thumb – [#733](https://github.com/radix-ui/primitives/pull/733)

# Slot

0.0.12

- Improve types compatibility – [#737](https://github.com/radix-ui/primitives/pull/737)

# Toggle Group

0.0.10

- Ensure only one click is needed to toggle a single controlled toggle group – [#722](https://github.com/radix-ui/primitives/pull/722)
- Ensure focus behavior is consistent on Safari – [#727](https://github.com/radix-ui/primitives/pull/727)

## [June 15, 2021](#june-15-2021)

# All primitives

- Improve polymorphic types – [#648](https://github.com/radix-ui/primitives/pull/648)

# Accordion

0.0.16Major

- **[Breaking]** Rename `Accordion.Button` to `Accordion.Trigger` – [#651](https://github.com/radix-ui/primitives/pull/651)
- **[Breaking]** Rename `Accordion.Panel` to `Accordion.Content` – [#651](https://github.com/radix-ui/primitives/pull/651)
- **[Breaking]** Rename custom property accordingly (`--radix-accordion-content-height`) – [#651](https://github.com/radix-ui/primitives/pull/651)
- **[Breaking]** `type=“single”` `Accordion` now has a new `collapsible` prop which is `false` by default. This means that the default behavior has now changed. By default a user cannot close all items. – [#651](https://github.com/radix-ui/primitives/pull/651)

# Alert Dialog

0.0.18Major

- **[Breaking]** Allow preventing default in `onPointerDownOutside` without inadvertently preventing focus – [#654](https://github.com/radix-ui/primitives/pull/654)

# Checkbox

0.0.16Major

- **[Breaking]** `onCheckedChange(event)` is now `onCheckedChange(checked: CheckedState)` – [#672](https://github.com/radix-ui/primitives/pull/672)
- Improve compatibility with native form validation – [#650](https://github.com/radix-ui/primitives/pull/650)
- Allow stopping propagation on `Checkbox` `onClick` – [#672](https://github.com/radix-ui/primitives/pull/672)
- Improve compatibility with native `label` – [#672](https://github.com/radix-ui/primitives/pull/672)
- Improve accessibility when wrapped in native `label` – [#672](https://github.com/radix-ui/primitives/pull/672)

# Collapsible

0.0.16Major

- **[Breaking]** Rename `Collapsible.Button` to `Collapsible.Trigger` – [#651](https://github.com/radix-ui/primitives/pull/651)

# Context Menu

0.0.22Major

- Add submenu support – [#682](https://github.com/radix-ui/primitives/pull/682)
- Add `ContextMenu.TriggerItem` – [#682](https://github.com/radix-ui/primitives/pull/682)
- Add `ContextMenu.Arrow` – [#682](https://github.com/radix-ui/primitives/pull/682)
- Add `dir` prop for RTL support with submenus – [#682](https://github.com/radix-ui/primitives/pull/682)
- **[Breaking]** Allow preventing default in `onPointerDownOutside` without inadvertently preventing focus – [#654](https://github.com/radix-ui/primitives/pull/654)
- **[Breaking]** Remove `ContextMenu.Content` `side` prop – [#658](https://github.com/radix-ui/primitives/pull/658)
- **[Breaking]** Remove `ContextMenu.Content` `align` prop – [#658](https://github.com/radix-ui/primitives/pull/658)
- **[Breaking]** If you had `sideOffset` on `ContextMenu.Content` before, you should now use `alignOffset`. This is to standardize vertical alignment for both root and sub-menus. – [#712](https://github.com/radix-ui/primitives/pull/712)
- **[Breaking]** `onFocusOutside` is now a custom event – [#671](https://github.com/radix-ui/primitives/pull/671)
- Improve support of content and item with no padding – [#658](https://github.com/radix-ui/primitives/pull/658)
- Align with WAI-ARIA spec by focusing first item when opening via keyboard – [#694](https://github.com/radix-ui/primitives/pull/694)

# Dialog

0.0.18Major

- **[Breaking]** Allow preventing default in `onPointerDownOutside` without inadvertently preventing focus – [#654](https://github.com/radix-ui/primitives/pull/654)

# Dropdown Menu

0.0.21Major

- Add submenu support – [#682](https://github.com/radix-ui/primitives/pull/682)
- Add `DropdownMenu.TriggerItem` – [#682](https://github.com/radix-ui/primitives/pull/682)
- Add `dir` prop for RTL support with submenus – [#682](https://github.com/radix-ui/primitives/pull/682)
- **[Breaking]** Allow preventing default in `onPointerDownOutside` without inadvertently preventing focus – [#654](https://github.com/radix-ui/primitives/pull/654)
- **[Breaking]** `onFocusOutside` is now a custom event – [#671](https://github.com/radix-ui/primitives/pull/671)
- **[Breaking]** The up arrow no longer opens the menu – [#702](https://github.com/radix-ui/primitives/pull/702)
- Align with WAI-ARIA spec by focusing first item when opening via keyboard – [#694](https://github.com/radix-ui/primitives/pull/694)

# Popover

0.0.18Major

- **[Breaking]** Allow preventing default in `onPointerDownOutside` without inadvertently preventing focus – [#654](https://github.com/radix-ui/primitives/pull/654)
- **[Breaking]** `onFocusOutside` is now a custom event – [#671](https://github.com/radix-ui/primitives/pull/671)

# Radio Group

0.0.17Major

- **[Breaking]** `onValueChange(event)` is now `onValueChange(value: string)` – [#685](https://github.com/radix-ui/primitives/pull/685)
- **[Breaking]** Remove `RadioGroup.Item` `onCheckedChange` prop – [#685](https://github.com/radix-ui/primitives/pull/685)
- Improve compatibility with native form validation – [#650](https://github.com/radix-ui/primitives/pull/650)
- Improve usage within forms – [#685](https://github.com/radix-ui/primitives/pull/685)

# Scroll Area

0.0.14Major

- Brand new version with a simpler API – [#624](https://github.com/radix-ui/primitives/pull/624)
- Improve Safari support – [#624](https://github.com/radix-ui/primitives/pull/624)
- Improve RTL support – [#624](https://github.com/radix-ui/primitives/pull/624)
- Improve touch support – [#624](https://github.com/radix-ui/primitives/pull/624)
- `Scrollbar` mount/unmount can now be animated – [#624](https://github.com/radix-ui/primitives/pull/624)
- Add minimum width/height to thumb so it's always grabbable – [#624](https://github.com/radix-ui/primitives/pull/624)
- Move functional CSS into component to improve DX – [#624](https://github.com/radix-ui/primitives/pull/624)
- Bundle size significantly reduced – [#624](https://github.com/radix-ui/primitives/pull/624)
- **[Breaking]** Remove `overflowX` and `overflowY` props – [#624](https://github.com/radix-ui/primitives/pull/624)
- **[Breaking]** Remove `ScrollAreaButtonStart`, `ScrollAreaButtonEnd` and `ScrollAreaTrack` – [#624](https://github.com/radix-ui/primitives/pull/624)
- **[Breaking]** Rename `scrollbarVisibility` prop to `type`. The values are `auto`, `always`, `scroll` or `hover` – [#624](https://github.com/radix-ui/primitives/pull/624)
- **[Breaking]** Rename `scrollbarVisibilityRestTimeout` prop to `scrollHideDelay` – [#624](https://github.com/radix-ui/primitives/pull/624)
- **[Breaking]** Remove `trackClickBehavior` prop as we've removed built-in animation. Clicking on track always snaps to pointer position – [#624](https://github.com/radix-ui/primitives/pull/624)
- **[Breaking]** `ScrollAreaScrollbarX` and `ScrollAreaScrollbarY` are now `<ScrollAreaScrollbar orientation="horizontal" />` and `<ScrollAreaScrollbar orientation="vertical" />` – [#624](https://github.com/radix-ui/primitives/pull/624)
- Ensure no scrollbars are shown when scrolling is disabled – [#624](https://github.com/radix-ui/primitives/pull/624)
- Ensure children event handlers don't break – [#624](https://github.com/radix-ui/primitives/pull/624)
- Ensure scroll area updates when children content size changes – [#624](https://github.com/radix-ui/primitives/pull/624)

# Slider

0.0.15

- Improve usage within forms – [#678](https://github.com/radix-ui/primitives/pull/678)
- Fix key binding issue in LTR – [#718](https://github.com/radix-ui/primitives/pull/718)

# Switch

0.0.14Major

- **[Breaking]** `onCheckedChange(event)` is now `onCheckedChange(checked: boolean)` – [#679](https://github.com/radix-ui/primitives/pull/679)
- Improve compatibility with native form validation – [#650](https://github.com/radix-ui/primitives/pull/650)
- Improve usage within forms – [#679](https://github.com/radix-ui/primitives/pull/679)
- Improve accessibility when wrapped in native `label` – [#679](https://github.com/radix-ui/primitives/pull/679)

# Tabs

0.0.14Major

- **[Breaking]** Rename `Tabs.Tab` to `Tabs.Trigger` – [#652](https://github.com/radix-ui/primitives/pull/652)
- **[Breaking]** Rename `Tabs.Panel` to `Tabs.Content` – [#652](https://github.com/radix-ui/primitives/pull/652)

## [May 3, 2021](#may-3-2021)

# All primitives

- Improve polymorphic types performance – [#613](https://github.com/radix-ui/primitives/pull/613)

# Accordion

0.0.14

- Ensure only one click is needed to close a single controlled accordion – [#594](https://github.com/radix-ui/primitives/pull/594)

# Checkbox

0.0.14Major

- **[Breaking]** Remove `readOnly` prop – [#600](https://github.com/radix-ui/primitives/pull/600)

# Context Menu

0.0.18

- Add `onOpenChange` prop – [#604](https://github.com/radix-ui/primitives/pull/604)

# Dialog

0.0.16

- Ensure focus position isn't lost when blurring out window and re-focusing it – [#589](https://github.com/radix-ui/primitives/pull/589)

# Dropdown Menu

0.0.18Major

- Take into account non-visible items – [#618](https://github.com/radix-ui/primitives/pull/618)
- **[Breaking]** Remove `anchorRef` prop – [#580](https://github.com/radix-ui/primitives/pull/580)
- Prevent page from scrolling when selecting an item with space key – [#626](https://github.com/radix-ui/primitives/pull/626)

# Hover Card

0.0.1

- New primitive – [#595](https://github.com/radix-ui/primitives/pull/595)

# Popover

0.0.16Major

- **[Breaking]** Remove `anchorRef` prop and replace with optional `Anchor` part – [#580](https://github.com/radix-ui/primitives/pull/580)

# Radio Group

0.0.15Major

- Add optional `orientation`, `dir`, `loop` props – [#618](https://github.com/radix-ui/primitives/pull/618)
- **[Breaking]** Remove `readOnly` prop – [#600](https://github.com/radix-ui/primitives/pull/600)

# Switch

0.0.12Major

- **[Breaking]** Remove `readOnly` prop – [#600](https://github.com/radix-ui/primitives/pull/600)

# Toggle Group

0.0.7

- Add optional `orientation`, `dir`, `loop` props – [#618](https://github.com/radix-ui/primitives/pull/618)

# Tooltip

0.0.17Major

- **[Breaking]** Remove `anchorRef` prop – [#580](https://github.com/radix-ui/primitives/pull/580)

## [March 26, 2021](#march-26-2021)

# All primitives

- Improve tree-shaking – [#577](https://github.com/radix-ui/primitives/pull/577)

# Context Menu

0.0.17

- Ensure you can open a context menu when one is already open – [#565](https://github.com/radix-ui/primitives/pull/565)

# Dropdown Menu

0.0.17

- Fix potential overlap issue – [#541](https://github.com/radix-ui/primitives/pull/541)

# Popover

0.0.15

- Ensure `Content` closes when it has multiple close animations – [#571](https://github.com/radix-ui/primitives/pull/571)

# Toggle

0.0.6Major

- **[Breaking]** Rename `ToggleButton` primitive to `Toggle` – [#546](https://github.com/radix-ui/primitives/pull/546)
- **[Breaking]** Rename `toggled` prop to `pressed` – [#546](https://github.com/radix-ui/primitives/pull/546)
- **[Breaking]** Rename `defaultToggled` prop to `defaultPressed` – [#546](https://github.com/radix-ui/primitives/pull/546)
- **[Breaking]** Rename `onToggledChange` prop to `onPressedChange` – [#546](https://github.com/radix-ui/primitives/pull/546)

# Toggle Group

0.0.6

- New primitive – [#376](https://github.com/radix-ui/primitives/pull/376)

# Toolbar

0.0.9

- New primitive – [#412](https://github.com/radix-ui/primitives/pull/412) [#451](https://github.com/radix-ui/primitives/pull/451) [#545](https://github.com/radix-ui/primitives/pull/545)

# Tooltip

0.0.16

- Add custom timing support – [#550](https://github.com/radix-ui/primitives/pull/550) [#551](https://github.com/radix-ui/primitives/pull/551) [#554](https://github.com/radix-ui/primitives/pull/554) [#558](https://github.com/radix-ui/primitives/pull/558)
- Add unmount animation support – [#558](https://github.com/radix-ui/primitives/pull/558)

## [March 5, 2021](#march-5-2021)

# Accordion

0.0.7

- Add height CSS custom property to panel for easier animation – [#537](https://github.com/radix-ui/primitives/pull/537)

# Collapsible

0.0.7

- Add height CSS custom property to content for easier animation – [#537](https://github.com/radix-ui/primitives/pull/537)

# Tooltip

0.0.9

- Fix type definition conflicts – [#538](https://github.com/radix-ui/primitives/pull/538)

## [March 3, 2021](#march-3-2021)

# All primitives

- Add support for SSR
- **[Breaking]** Remove `selector` prop and `data-radix-*` atributes – [#517](https://github.com/radix-ui/primitives/pull/517)

# Accordion

0.0.6Major

- **[Breaking]** Add support for multiple values. Note that this is a breaking change because the new `type` prop is required – [#527](https://github.com/radix-ui/primitives/pull/527)

# Slider

0.0.6

- Ensure `step` is rounded correctly – [#463](https://github.com/radix-ui/primitives/pull/463)

# Tabs

0.0.6

- Add RTL support (`dir` prop) – [#497](https://github.com/radix-ui/primitives/pull/497)

## [February 17, 2021](#february-17-2021)

# Tooltip

0.0.7

- Ensure events are composed when using `<Trigger as={Slot}>` – [#461](https://github.com/radix-ui/primitives/pull/461)

## [February 15, 2021](#february-15-2021)

# Context Menu

0.0.8

- Expose `onCloseAutoFocus` prop – [#456](https://github.com/radix-ui/primitives/pull/456)

# Dropdown Menu

0.0.8

- Expose `onCloseAutoFocus` prop – [#456](https://github.com/radix-ui/primitives/pull/456)

## [February 10, 2021](#february-10-2021)

# All primitives

- Fix type autocompletion when using `as` prop – [#421](https://github.com/radix-ui/primitives/pull/421)

# Accordion

0.0.5

- Prevent open/close flickering – [#431](https://github.com/radix-ui/primitives/pull/431)

# Dialog

0.0.6

- Ensure focus is returned properly on close – [#422](https://github.com/radix-ui/primitives/pull/422)

# Radio Group

0.0.5Major

- **[Breaking]** Move `name` prop from `Item` to `Root` – [#424](https://github.com/radix-ui/primitives/pull/424)

## [February 1, 2021](#february-1-2021)

# Context Menu

0.0.6

- Re–add missing `children` – [#414](https://github.com/radix-ui/primitives/pull/414)

# Dropdown Menu

0.0.6

- Re–add missing `children` – [#414](https://github.com/radix-ui/primitives/pull/414)

# Popover

0.0.5

- Prevent flickering (sliding) issue – [#415](https://github.com/radix-ui/primitives/pull/415)

## [January 29, 2021](#january-29-2021)

# Slot

0.0.1

- New utility – [#409](https://github.com/radix-ui/primitives/pull/409)

## [January 25, 2021](#january-25-2021)

# Dialog

0.0.3

- Fix regression when tabbing out would close – [#403](https://github.com/radix-ui/primitives/pull/403)

# Dropdown Menu

0.0.3

- Fix broken arrow keys navigation – [#404](https://github.com/radix-ui/primitives/pull/404)

## [January 22, 2021](#january-22-2021)

# All primitives

- Add `selector` prop – [#347](https://github.com/radix-ui/primitives/pull/347)

# Accordion

0.0.2

- Ensure setting `disabled={false}` on `Root` doesn't enable disabled items – [#400](https://github.com/radix-ui/primitives/pull/400)

# Dropdown Menu

0.0.2

- Add enter key support on trigger – [#381](https://github.com/radix-ui/primitives/pull/381)
- Prevent focus race condition – [#394](https://github.com/radix-ui/primitives/pull/394)

# Popover

0.0.2

- Ensure `Content` repositions on window resize – [#359](https://github.com/radix-ui/primitives/pull/359)
- Ensure last element inside `Content` triggers blur event – [#395](https://github.com/radix-ui/primitives/pull/395)

## [December 15, 2020](#december-15-2020)

# All primitives

0.0.1Major

- Initial release! 🎉 – [#338](https://github.com/radix-ui/primitives/pull/338)

Previous[Accessibility](/primitives/docs/overview/accessibility)

Next[Styling](/primitives/docs/guides/styling)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/overview/releases.mdx "Edit this page on GitHub.")