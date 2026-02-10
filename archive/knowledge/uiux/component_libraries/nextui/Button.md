# Button

Source: https://nextui.org/docs/components/

---

Getting Started

- [Introduction](/docs/guide/introduction)
- [Design Principles](/docs/guide/design-principles)
- [Installation](/docs/guide/installation)
- [CLI](/docs/guide/cli)
- [Routing

  Updated](/docs/guide/routing)
- [Forms](/docs/guide/forms)
- [Tailwind v4

  New](/docs/guide/tailwind-v4)
- [NextUI to HeroUI](/docs/guide/nextui-to-heroui)
- [Figma](/docs/guide/figma)

Frameworks

- [Next.js](/docs/frameworks/nextjs)
- [Vite](/docs/frameworks/vite)
- [Remix](/docs/frameworks/remix)
- [Astro](/docs/frameworks/astro)
- [Laravel](/docs/frameworks/laravel)

Customization

- [Theme](/docs/customization/theme)
- [Layout](/docs/customization/layout)
- [Colors](/docs/customization/colors)
- [Customize theme](/docs/customization/customize-theme)
- [Create theme](/docs/customization/create-theme)
- [Dark mode](/docs/customization/dark-mode)
- [Override styles](/docs/customization/override-styles)
- [Custom variants](/docs/customization/custom-variants)

Components

- [Accordion](/docs/components/accordion)
- [Autocomplete](/docs/components/autocomplete)
- [Alert](/docs/components/alert)
- [Avatar](/docs/components/avatar)
- [Badge](/docs/components/badge)
- [Breadcrumbs](/docs/components/breadcrumbs)
- [Button](/docs/components/button)
- [Calendar](/docs/components/calendar)
- [Card](/docs/components/card)
- [Checkbox](/docs/components/checkbox)
- [Checkbox Group](/docs/components/checkbox-group)
- [Chip](/docs/components/chip)
- [Circular Progress](/docs/components/circular-progress)
- [Code](/docs/components/code)
- [Date Input](/docs/components/date-input)
- [Date Picker](/docs/components/date-picker)
- [Date Range Picker](/docs/components/date-range-picker)
- [Divider](/docs/components/divider)
- [Dropdown](/docs/components/dropdown)
- [Drawer](/docs/components/drawer)
- [Form](/docs/components/form)
- [Image](/docs/components/image)
- [Input

  Updated](/docs/components/input)
- [Input OTP](/docs/components/input-otp)
- [Kbd](/docs/components/kbd)
- [Link](/docs/components/link)
- [Listbox](/docs/components/listbox)
- [Modal](/docs/components/modal)
- [Navbar](/docs/components/navbar)
- [Number Input](/docs/components/number-input)
- [Pagination](/docs/components/pagination)
- [Popover](/docs/components/popover)
- [Progress](/docs/components/progress)
- [Radio Group](/docs/components/radio-group)
- [Range Calendar](/docs/components/range-calendar)
- [Scroll Shadow](/docs/components/scroll-shadow)
- [Select

  Updated](/docs/components/select)
- [Skeleton](/docs/components/skeleton)
- [Slider

  Updated](/docs/components/slider)
- [Snippet](/docs/components/snippet)
- [Spacer](/docs/components/spacer)
- [Spinner](/docs/components/spinner)
- [Switch](/docs/components/switch)
- [Table

  Updated](/docs/components/table)
- [Tabs](/docs/components/tabs)
- [Toast

  Updated](/docs/components/toast)
- [Textarea](/docs/components/textarea)
- [Time Input](/docs/components/time-input)
- [Tooltip](/docs/components/tooltip)
- [User](/docs/components/user)

API References

- [HeroUI CLI

  Updated](/docs/api-references/cli-api)
- [HeroUIProvider](/docs/api-references/heroui-provider)

# Button

Buttons allow users to perform actions and choose with a single tap.

[Storybook](https://storybook.heroui.com/?path=/story/components-button--default)[@heroui/button](https://www.npmjs.com/package/@heroui/button)[React Aria](https://react-spectrum.adobe.com/react-aria/useButton.html)[Source](https://github.com/heroui-inc/heroui/tree/feat/v2/packages/components/button)[Styles source](https://github.com/heroui-inc/heroui/tree/feat/v2/packages/core/theme/src/components/button.ts)

---

## [Installation](#installation)

CLI

pnpm

npm

yarn

bun

> The above command is for individual installation only. You may skip this step if `@heroui/react` is already installed globally.

## [Import](#import)

HeroUI exports 2 button-related components:

- **Button**: The main component to display a button.
- **ButtonGroup**: A wrapper component to display a group of buttons.

Individual

Global

## [Usage](#usage)

Preview

Code

### [Disabled](#disabled)

Preview

Code

### [Sizes](#sizes)

Preview

Code

### [Radius](#radius)

Preview

Code

### [Colors](#colors)

Preview

Code

### [Variants](#variants)

Preview

Code

### [Loading](#loading)

Pass the `isLoading` prop to display a [Spinner](/docs/components/spinner) component inside the button.

Preview

Code

You can also customize the loading spinner by passing the a custom component to the `spinner` prop.

Preview

Code

### [With Icons](#with-icons)

You can add icons to the `Button` by passing the `startContent` or `endContent` props.

Preview

Code

### [Icon Only](#icon-only)

You can also display a button without text by passing the `isIconOnly` prop and the desired icon as `children`.

Preview

Code

### [Custom Styles](#custom-styles)

You can customize the `Button` component by passing custom Tailwind CSS classes to the component slots.

Preview

Code

> Custom class names will override the default ones thanks to [Tailwind Merge](https://github.com/dcastil/tailwind-merge) library. It
> means that you don't need to worry about class conflicts.

### [Custom Implementation](#custom-implementation)

You can also use the `useButton` hook to create your own button component.

## [Button Group](#button-group)

Preview

Code

### [Group Disabled](#group-disabled)

The `ButtonGroup` component also accepts the `isDisabled` prop to disable all buttons inside it.

Preview

Code

### [Group Use case](#group-use-case)

A common use case for the `ButtonGroup` component is to display a group of two buttons one for the selected value and another for the `dropdown`.

Preview

Code

> See the [Dropdown](/docs/components/dropdown) component for more details.

## [Data Attributes](#data-attributes)

`Button` has the following attributes on the `base` element:

- **data-hover**:
  When the button is being hovered. Based on [useHover](https://react-spectrum.adobe.com/react-aria/useHover.html)
- **data-focus**:
  When the button is being focused. Based on [useFocusRing](https://react-spectrum.adobe.com/react-aria/useFocusRing.html).
- **data-focus-visible**:
  When the button is being focused with the keyboard. Based on [useFocusRing](https://react-spectrum.adobe.com/react-aria/useFocusRing.html).
- **data-disabled**:
  When the button is disabled. Based on `isDisabled` prop.
- **data-pressed**:
  When the button is pressed. Based on [usePress](https://react-spectrum.adobe.com/react-aria/usePress.html)
- **data-loading**:
  When the button is loading. Based on `isLoading` prop.

## [Accessibility](#accessibility)

- Button has role of `button`.
- Keyboard event support for `Space` and `Enter` keys.
- Mouse and touch event handling, and press state management.
- Keyboard focus management and cross browser normalization.

We recommend to read this [blog post](https://react-spectrum.adobe.com/blog/building-a-button-part-1.html) about the complexities of
building buttons that work well across devices and interaction methods.

## [API](#api)

### [Button Props](#button-props)

| Prop | Type | Default |
| --- | --- | --- |
| `children` | `ReactNode` |  |
| `variant` | `solid | bordered | light | flat | faded | shadow | ghost` | `"solid"` |
| `color` | `default | primary | secondary | success | warning | danger` | `"default"` |
| `size` | `sm | md | lg` | `"md"` |
| `radius` | `none | sm | md | lg | full` |  |
| `startContent` | `ReactNode` |  |
| `endContent` | `ReactNode` |  |
| `spinner` | `ReactNode` |  |
| `spinnerPlacement` | `start | end` | `"start"` |
| `fullWidth` | `boolean` | `false` |
| `isIconOnly` | `boolean` | `false` |
| `isDisabled` | `boolean` | `false` |
| `isLoading` | `boolean` | `false` |
| `disableRipple` | `boolean` | `false` |
| `disableAnimation` | `boolean` | `false` |

### [Button Events](#button-events)

| Prop | Type | Default |
| --- | --- | --- |
| `onPress` | `(e: PressEvent) => void` |  |
| `onPressStart` | `(e: PressEvent) => void` |  |
| `onPressEnd` | `(e: PressEvent) => void` |  |
| `onPressChange` | `(isPressed: boolean) => void` |  |
| `onPressUp` | `(e: PressEvent) => void` |  |
| `onKeyDown` | `(e: KeyboardEvent) => void` |  |
| `onKeyUp` | `(e: KeyboardEvent) => void` |  |
| `onClick` | `MouseEventHandler` |  |

### [Button Group Props](#button-group-props)

| Prop | Type | Default |
| --- | --- | --- |
| `children` | `ReactNode | ReactNode[]` |  |
| `variant` | `solid | bordered | light | flat | faded | shadow | ghost` | `"solid"` |
| `color` | `default | primary | secondary | success | warning | danger` | `"default"` |
| `size` | `sm | md | lg` | `"md"` |
| `radius` | `none | sm | md | lg | full` | `"xl"` |
| `fullWidth` | `boolean` | `false` |
| `isDisabled` | `boolean` | `false` |

BreadcrumbsCalendar

On this page

- [Installation](#installation)
- [Import](#import)
- [Usage](#usage)
- [Disabled](#disabled)
- [Sizes](#sizes)
- [Radius](#radius)
- [Colors](#colors)
- [Variants](#variants)
- [Loading](#loading)
- [With Icons](#with-icons)
- [Icon Only](#icon-only)
- [Custom Styles](#custom-styles)
- [Custom Implementation](#custom-implementation)
- [Button Group](#button-group)
- [Group Disabled](#group-disabled)
- [Group Use case](#group-use-case)
- [Data Attributes](#data-attributes)
- [Accessibility](#accessibility)
- [API](#api)
- [Button Props](#button-props)
- [Button Events](#button-events)
- [Button Group Props](#button-group-props)
- ---

  [Back to top](#button)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components