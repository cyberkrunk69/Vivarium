# Override styles

Source: https://nextui.org/docs/customization/override-styles

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

# Override styles

Overriding default component styles is as simple as passing your own class names to the `className`
or to the `classNames` prop for components with slots.

### [What is a Slot?](#what-is-a-slot)

A slot is a part of a component that can be styled separately using the `classNames` prop. For example, the [CircularProgress](/docs/components/circular-progress) component has slots like `track`, `indicator`, and `value` that can each be styled independently.

### [Overriding a component](#overriding-a-component)

Let's override the default styles of the [Button](/docs/components/button) component, which is a component that has no slots.

### [Components with slots](#components-with-slots)

Some HeroUI components have slots that can be styled individually using the `classNames` prop. The [CircularProgress](/docs/components/circular-progress) component has the following slots:

- **base**: The base slot of the circular progress, it is the main container.
- **svgWrapper**: The wrapper of the svg circles and the value label.
- **svg**: The svg element of the circles.
- **track**: The track is the background circle of the circular progress.
- **indicator**: The indicator is the one that is filled according to the `value`.
- **value**: The value content.
- **label**: The label content.

The example below demonstrates styling these slots to create a custom circular progress:

> **Note**: You will find a `Slots` section in the documentation of each component that has slots.

### [CSS Modules](#css-modules)

CSS Modules allow for the creation of local scope classes and variables. Here's how
you can use it to override styles:

With the corresponding CSS module:

### [CSS-in-JS](#css-in-js)

If you are using a CSS-in-JS library such as [styled-components](https://styled-components.com/) or [emotion](https://emotion.sh/), you can use the following
example to override the styles of a component:

Each styled component combines the original component styles with custom styles defined in the template strings. The `StyledCircularProgress` uses `.attrs` to add classNames.

Dark modeCustom variants

On this page

- [What is a Slot?](#what-is-a-slot)
- [Overriding a component](#overriding-a-component)
- [Components with slots](#components-with-slots)
- [CSS Modules](#css-modules)
- [CSS-in-JS](#css-in-js)
- ---

  [Back to top](#override-styles)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components