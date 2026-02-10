# Theme

Source: https://nextui.org/docs/customization/theme

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

# Theme

Theming allows you to maintain a consistent look and feel across your application. HeroUI provides theme customization through a TailwindCSS plugin based on [tw-colors](https://github.com/L-Blondy/tw-colors), enabling you to easily customize colors, layouts and other UI elements.

## [What is a Theme?](#what-is-a-theme)

A theme is a predefined set of colors and layout attributes that ensure visual consistency across your application. It simplifies managing and updating your app's appearance.

## [Setup](#setup)

The first step to using HeroUI's theming capability is adding the `heroui` plugin to your
`tailwind.config.js` file. Below is an example of how to do this:

> **Note**: If you are using pnpm and monorepo architecture, please make sure you are pointing to the ROOT `node_modules`

### [Usage](#usage)

After adding the plugin to your `tailwind.config.js` file, you can utilize any of the default
themes (light/dark) or a custom one. Here's how you can apply these themes in your `main.jsx` or `main.tsx`:

Go to the src directory and inside `main.jsx` or `main.tsx`, apply the following class names to the root element:

- `light` for the light theme.
- `dark` for the dark theme.
- `text-foreground` to set the text color.
- `bg-background` to set the background color.

> **Note**: See the [Colors](/docs/customization/colors) section to learn more about the color classes.

### [Default Plugin Options](#default-plugin-options)

The `heroui` plugin provides a default structure. It is outlined as follows:

### [Themes Options](#themes-options)

These are the options that you can use to apply custom configurations to your themes.

### [Nested themes](#nested-themes)

HeroUI supports nested themes, allowing you to apply different themes to different sections
of your application:

### [Theme based variants](#theme-based-variants)

HeroUI enables you to apply TailwindCSS styles based on the currently active theme. Below are
examples of how to do this:

### [API Reference](#api-reference)

The following table provides an overview of the various attributes you can use when working
with themes in HeroUI:

| Attribute | Type | Description | Default |
| --- | --- | --- | --- |
| prefix | `string` | The prefix for the css variables. | `heroui` |
| addCommonColors | `boolean` | If true, the common heroui colors (e.g. "blue", "green", "purple") will replace the TailwindCSS default colors. | `false` |
| defaultTheme | `light` | `dark` | The default theme to use. | `light` |
| defaultExtendTheme | `light` | `dark` | The default theme to extend. | `light` |
| layout | [LayoutTheme](#layouttheme) | The layout definitions. | - |
| themes | [ConfigThemes](#configthemes) | The theme definitions. | - |

### [Types](#types)

#### [ConfigThemes](#configthemes)

#### [LayoutTheme](#layouttheme)

#### [ThemeColors](#themecolors)

Frameworks: LaravelLayout

On this page

- [What is a Theme?](#what-is-a-theme)
- [Setup](#setup)
- [Usage](#usage)
- [Default Plugin Options](#default-plugin-options)
- [Themes Options](#themes-options)
- [Nested themes](#nested-themes)
- [Theme based variants](#theme-based-variants)
- [API Reference](#api-reference)
- [Types](#types)
- [ConfigThemes](#configthemes)
- [LayoutTheme](#layouttheme)
- [ThemeColors](#themecolors)
- ---

  [Back to top](#theme)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components