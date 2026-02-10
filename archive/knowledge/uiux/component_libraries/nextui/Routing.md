# Routing

Source: https://nextui.org/docs/guide/routing

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

# Routing

HeroUI Components such as [Tabs](/docs/components/tabs), [Listbox](/docs/components/listbox), [Dropdown](/docs/components/dropdown) and many others offer
the flexibility to be rendered as **HTML links**.

## [Introduction](#introduction)

By default, links perform native browser navigation when they are interacted with. However, many apps and
frameworks use client side routers to avoid a full page reload when navigating between pages.

The `HeroUIProvider` component configures all HeroUI components within it to navigate using the client side
router you provide.

Set this up once in the `root` of your app, and any HeroUI component with the `href` prop will automatically navigate
using your router.

## [HeroUIProvider Setup](#herouiprovider-setup)

The `HeroUIProvider` component accepts `navigate` and `useHref` props. `navigate` is a router function for client-side
navigation, while `useHref` optionally converts router hrefs to native HTML hrefs. Here's the pattern:

> **Note**: Framework-specific examples are shown below.

### [Router Options](#router-options)

All `HeroUI` link components accept a `routerOptions` prop that passes options to the router's navigate function for
controlling behavior like scrolling and history navigation.

When using TypeScript, you can configure the RouterConfig type globally so that all link components have auto
complete and type safety using a type provided by your router.

## [Next.js](#nextjs)

#### [App Router](#app-router)

Go to your `app/providers.tsx` or `app/providers.jsx` (create it if it doesn't exist) and add the
`useRouter` hook from `next/navigation`, it returns a router object that can be used to perform navigation.

> Check the [Next.js docs](https://nextjs.org/docs/app/api-reference/functions/use-router) for more details.

#### [Add the `useRouter`](#add-the-userouter)

#### [Add Provider to Root](#add-provider-to-root)

Now, Go to your `root` layout page and wrap it with the `HeroUIProvider`:

> **Note**: Skip this step if you already set up the `HeroUIProvider` in your app.

#### [Next.js Base Path (Optional)](#nextjs-base-path-optional)

If you are using the Next.js [basePath](https://nextjs.org/docs/app/api-reference/next-config-js/basePath) setting,
you'll need to configure an environment variable to access it.

Then, provide a custom `useHref` function to prepend it to the href for all links.

### [Pages Router](#pages-router)

Go to pages`/_app.js` or `pages/_app.tsx` (create it if it doesn't exist) and add the`useRouter` hook
from `next/router`, it returns a router object that can be used to perform navigation.

When using the [basePath](https://nextjs.org/docs/app/api-reference/next-config-js/basePath) configuration option,
provide a `useHref` option to the router passed to Provider to prepend it to links automatically.

## [React Router](#react-router)

Use the `useNavigate` hook from `react-router-dom` to get the `navigate` function for routing. The `useHref` hook can be used with React Router's `basename` option.

Make sure to place the component using these hooks inside `BrowserRouter` and keep `<Routes>` within `HeroUIProvider`. Here's how to set it up in your App component:

Ensure that the component that calls `useNavigate` and renders `HeroUIProvider` is inside the router
component (e.g. `BrowserRouter`) so that it has access to React Router's internal context. The React Router `<Routes>`
element should also be defined inside `HeroUIProvider` so that links inside the rendered routes have access
to the router.

## [Remix](#remix)

Remix uses React Router under the hood, so the same `useNavigate` and `useHref` hook described above also works in Remix
apps. `HeroUIProvider` should be rendered at the `root` of each page that includes HeroUI components, or in
`app/root.tsx` to add it to all pages. See the [Remix docs](https://remix.run/docs/en/main/file-conventions/root)
for more details.

## [TanStack](#tanstack)

To use [TanStack Router](https://tanstack.com/router/latest), use the [createLink](https://tanstack.com/router/latest/docs/framework/react/guide/custom-link) function to wrap each HeroUI component as a link. `RouterProvider` is not needed.

## [Usage examples](#usage-examples)

Now that you have set up the `HeroUIProvider` in your app, you can use the `href` prop in the `Tabs`,
`Listbox` and `Dropdown` items to navigate between pages.

The [Link](/docs/components/link) component will also use the `navigate` function from the
`HeroUIProvider` to navigate between pages.

CLIForms

On this page

- [Introduction](#introduction)
- [HeroUIProvider Setup](#herouiprovider-setup)
- [Router Options](#router-options)
- [Next.js](#nextjs)
- [App Router](#app-router)
- [Add the `useRouter`](#add-the-userouter)
- [Add Provider to Root](#add-provider-to-root)
- [Next.js Base Path (Optional)](#nextjs-base-path-optional)
- [Pages Router](#pages-router)
- [React Router](#react-router)
- [Remix](#remix)
- [TanStack](#tanstack)
- [Usage examples](#usage-examples)
- ---

  [Back to top](#routing)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components