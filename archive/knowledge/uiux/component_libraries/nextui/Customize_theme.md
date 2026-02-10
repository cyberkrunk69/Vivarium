# Customize theme

Source: https://nextui.org/docs/customization/customize-theme

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

# Customize theme

HeroUI provides `light` and `dark` themes that can be customized to match your needs. You can also create custom themes based on these defaults, using [Layout](/docs/customization/layout) and [Color](/docs/customization/colors) tokens.

## [Customizing Layout](#customizing-layout)

Layout tokens let you customize spacing, typography, borders and more - either globally or per theme.

### [Global Layout Customization](#global-layout-customization)

You can customize border radius, border width, and disabled opacity across all themes by modifying your `tailwind.config.js` file:

Layout tokens are used across all HeroUI components. For example, the [Button](/docs/components/button) component uses `radius` and `borderWidth` tokens for its styling. Here's how it looks with the customized values:

> See the [Layout](/docs/customization/layout#default-layout) section for more details about the available tokens.

### [Customizing Colors](#customizing-colors)

Now, Let's say you wish to modify the primary and focus colors of the dark theme. This can
be achieved by adding the following code to your `tailwind.config.js` file.

This modification will impact all components using the `primary` color. For instance,
the [Button](/docs/components/button) component uses the `primary` color as background color when the
variant is `solid` or `ghost`.

> 🎉 That's it! You have successfully customized the default theme. See the [Colors](/docs/customization/colors)
> section for more details about the available semantic colors and color tokens.

ColorsCreate theme

On this page

- [Customizing Layout](#customizing-layout)
- [Global Layout Customization](#global-layout-customization)
- [Customizing Colors](#customizing-colors)
- ---

  [Back to top](#customize-theme)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components