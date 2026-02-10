# Server-side rendering

Source: https://www.radix-ui.com/primitives/docs/guides/server-side-rendering

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

Guides

# Server-side rendering

Radix Primitives can be rendered on the server. However, Primitives in React
versions less than 18 rely on hydration for ids.

## [Overview](#overview)

Server-side rendering or `SSR`, is a technique used to render components to HTML on the server, as opposed to rendering them only on the client.

Static rendering is another similar approach. Instead it pre-renders pages to HTML at build time rather than on each request.

You should be able to use all of our primitives with both approaches, for example with [Next.js](https://nextjs.org/), [Remix](https://remix.run/), or [Gatsby](https://www.gatsbyjs.com/).

## [Gotcha](#gotcha)

Primitives in React versions less than 18 rely on hydration for ids (used in aria attributes) to avoid server/client mismatch errors.

In other words, the equivalent of [Time to Interactive](https://web.dev/interactive/) for screen reader users will depend on the download speed of the JS bundle. If you'd like to generate ids server-side to improve this experience, we suggest upgrading to React 18.

Previous[Composition](/primitives/docs/guides/composition)

Next[Accordion](/primitives/docs/components/accordion)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/guides/server-side-rendering.mdx "Edit this page on GitHub.")