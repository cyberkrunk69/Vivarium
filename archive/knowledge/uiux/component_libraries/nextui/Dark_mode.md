# Dark mode

Source: https://nextui.org/docs/customization/dark-mode

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

# Dark mode

HeroUI supports both `light` and `dark` themes. To enable dark mode, simply add the `dark` class to your root element (`html`, `body`, or `main`).

This enables dark mode application-wide. For theme switching functionality, you can use a theme library or create a custom implementation.

## [Using next-themes](#using-next-themes)

For [Next.js](/docs/frameworks/nextjs) applications, [next-themes](https://github.com/pacocoursey/next-themes) provides seamless theme switching functionality.

> For more information, refer to the [next-themes](https://github.com/pacocoursey/next-themes) documentation.

### [Next.js App Directory Setup](#nextjs-app-directory-setup)

### [Install next-themes](#install-next-themes)

Install `next-themes` in your project.

pnpm

npm

yarn

### [Add next-themes provider](#add-next-themes-provider)

Wrap your app with the `ThemeProvider` component from `next-themes`.

Go to your `app/providers.tsx` or `app/providers.jsx` (create it if it doesn't exist) and wrap the
Component with the `HeroUIProvider` and the `next-themes` provider components.

> Note: We're using the `class` attribute to switch between themes, this is because HeroUI uses the `className` attribute.

### [Add the theme switcher](#add-the-theme-switcher)

Add the theme switcher to your app.

> **Note**: You can use any theme name you want, but make sure it exists in your
> `tailwind.config.js` file. See [Create Theme](/docs/customization/create-theme) for more details.

### [Next.js Pages Directory Setup](#nextjs-pages-directory-setup)

### [Install next-themes](#install-next-themes-1)

Install `next-themes` in your project.

pnpm

npm

yarn

### [Add next-themes provider](#add-next-themes-provider-1)

Go to pages`/_app.js` or `pages/_app.tsx` (create it if it doesn't exist) and wrap the
Component with the `HeroUIProvider` and the `next-themes` provider components.

> Note: We're using the `class` attribute to switch between themes, this is because HeroUI uses the `className` attribute.

### [Add the theme switcher](#add-the-theme-switcher-1)

Add the theme switcher to your app.

> **Note**: You can use any theme name you want, but make sure it exists in your
> `tailwind.config.js` file. See [Create Theme](/docs/customization/create-theme) for more details.

## [Using use-theme hook](#using-use-theme-hook)

In case you're using plain React with [Vite](/docs/frameworks/vite) or [Create React App](https://create-react-app.dev/)
you can use the [@heroui/use-theme](https://github.com/heroui-inc/heroui/tree/canary/packages/hooks/use-theme) hook to switch between themes.

### [Install @heroui/use-theme](#install-herouiuse-theme)

Install `@heroui/use-theme` in your project.

pnpm

npm

yarn

### [Add the theme switcher](#add-the-theme-switcher-2)

Add the theme switcher to your app.

> **Note**: You can use any theme name you want, but make sure it exists in your
> `tailwind.config.js` file. See [Create Theme](/docs/customization/create-theme) for more details.

Create themeOverride styles

On this page

- [Using next-themes](#using-next-themes)
- [Next.js App Directory Setup](#nextjs-app-directory-setup)
- [Install next-themes](#install-next-themes)
- [Add next-themes provider](#add-next-themes-provider)
- [Add the theme switcher](#add-the-theme-switcher)
- [Next.js Pages Directory Setup](#nextjs-pages-directory-setup)
- [Install next-themes](#install-next-themes-1)
- [Add next-themes provider](#add-next-themes-provider-1)
- [Add the theme switcher](#add-the-theme-switcher-1)
- [Using use-theme hook](#using-use-theme-hook)
- [Install @heroui/use-theme](#install-herouiuse-theme)
- [Add the theme switcher](#add-the-theme-switcher-2)
- ---

  [Back to top](#dark-mode)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components