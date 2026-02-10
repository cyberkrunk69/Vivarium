# Changelog

Source: https://ui.shadcn.com/docs/changelog

---

Sections

- [Introduction](/docs)
- [Components](/docs/components)
- [Installation](/docs/installation)
- [Directory](/docs/directory)
- [RTL](/docs/rtl)
- [MCP Server](/docs/mcp)
- [Registry](/docs/registry)
- [Forms](/docs/forms)
- [Changelog](/docs/changelog)

Components

- [Accordion](/docs/components/radix/accordion)
- [Alert](/docs/components/radix/alert)
- [Alert Dialog](/docs/components/radix/alert-dialog)
- [Aspect Ratio](/docs/components/radix/aspect-ratio)
- [Avatar](/docs/components/radix/avatar)
- [Badge](/docs/components/radix/badge)
- [Breadcrumb](/docs/components/radix/breadcrumb)
- [Button](/docs/components/radix/button)
- [Button Group](/docs/components/radix/button-group)
- [Calendar](/docs/components/radix/calendar)
- [Card](/docs/components/radix/card)
- [Carousel](/docs/components/radix/carousel)
- [Chart](/docs/components/radix/chart)
- [Checkbox](/docs/components/radix/checkbox)
- [Collapsible](/docs/components/radix/collapsible)
- [Combobox](/docs/components/radix/combobox)
- [Command](/docs/components/radix/command)
- [Context Menu](/docs/components/radix/context-menu)
- [Data Table](/docs/components/radix/data-table)
- [Date Picker](/docs/components/radix/date-picker)
- [Dialog](/docs/components/radix/dialog)
- [Direction](/docs/components/radix/direction)
- [Drawer](/docs/components/radix/drawer)
- [Dropdown Menu](/docs/components/radix/dropdown-menu)
- [Empty](/docs/components/radix/empty)
- [Field](/docs/components/radix/field)
- [Hover Card](/docs/components/radix/hover-card)
- [Input](/docs/components/radix/input)
- [Input Group](/docs/components/radix/input-group)
- [Input OTP](/docs/components/radix/input-otp)
- [Item](/docs/components/radix/item)
- [Kbd](/docs/components/radix/kbd)
- [Label](/docs/components/radix/label)
- [Menubar](/docs/components/radix/menubar)
- [Native Select](/docs/components/radix/native-select)
- [Navigation Menu](/docs/components/radix/navigation-menu)
- [Pagination](/docs/components/radix/pagination)
- [Popover](/docs/components/radix/popover)
- [Progress](/docs/components/radix/progress)
- [Radio Group](/docs/components/radix/radio-group)
- [Resizable](/docs/components/radix/resizable)
- [Scroll Area](/docs/components/radix/scroll-area)
- [Select](/docs/components/radix/select)
- [Separator](/docs/components/radix/separator)
- [Sheet](/docs/components/radix/sheet)
- [Sidebar](/docs/components/radix/sidebar)
- [Skeleton](/docs/components/radix/skeleton)
- [Slider](/docs/components/radix/slider)
- [Sonner](/docs/components/radix/sonner)
- [Spinner](/docs/components/radix/spinner)
- [Switch](/docs/components/radix/switch)
- [Table](/docs/components/radix/table)
- [Tabs](/docs/components/radix/tabs)
- [Textarea](/docs/components/radix/textarea)
- [Toast](/docs/components/radix/toast)
- [Toggle](/docs/components/radix/toggle)
- [Toggle Group](/docs/components/radix/toggle-group)
- [Tooltip](/docs/components/radix/tooltip)
- [Typography](/docs/components/radix/typography)

Get Started

- [Installation](/docs/installation)
- [components.json](/docs/components-json)
- [Theming](/docs/theming)
- [Dark Mode](/docs/dark-mode)
- [CLI](/docs/cli)
- [Monorepo](/docs/monorepo)
- [Open in v0](/docs/v0)
- [JavaScript](/docs/javascript)
- [Blocks](/docs/blocks)
- [Figma](/docs/figma)
- [llms.txt](/llms.txt)
- [Legacy Docs](/docs/legacy)

Forms

- [React Hook Form](/docs/forms/react-hook-form)
- [TanStack Form](/docs/forms/tanstack-form)

Registry

- [Introduction](/docs/registry)
- [Getting Started](/docs/registry/getting-started)
- [Namespaces](/docs/registry/namespace)
- [Authentication](/docs/registry/authentication)
- [Examples](/docs/registry/examples)
- [MCP Server](/docs/registry/mcp)
- [Add a Registry](/docs/registry/registry-index)
- [Open in v0](/docs/registry/open-in-v0)
- [registry.json](/docs/registry/registry-json)
- [registry-item.json](/docs/registry/registry-item-json)

# Changelog

[RSS](/rss.xml)

Latest updates and announcements.

## February 2026 - Unified Radix UI Package

The `new-york` style now uses the unified `radix-ui` package instead of individual `@radix-ui/react-*` packages.

### What's Changed

When you add components using the `new-york` style, they will now import from `radix-ui` instead of separate packages:

components/ui/dialog.tsx

```
Copy- import * as DialogPrimitive from "@radix-ui/react-dialog"
+ import { Dialog as DialogPrimitive } from "radix-ui"
```

This results in a cleaner `package.json` with a single `radix-ui` dependency instead of multiple `@radix-ui/react-*` packages.

### Migrating Existing Projects

If you have an existing project using the `new-york` style, you can migrate to the new `radix-ui` package using the migrate command:

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest migrate radix
```

Copy
```

This will update all imports in your UI components and add `radix-ui` to your dependencies.

To migrate components outside of your `ui` directory, use the `path` argument:

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest migrate radix src/components/custom
```

Copy
```

Once complete, you can remove any unused `@radix-ui/react-*` packages from your `package.json`.

See the [migrate radix documentation](/docs/cli#migrate-radix) for more details.

## January 2026 - RTL Support

shadcn/ui now has first-class support for right-to-left (RTL) layouts. Your components automatically adapt for languages like Arabic, Hebrew, and Persian.

**This works with the [shadcn/ui components](/docs/components) as well as any component distributed on the shadcn registry.**

Arabic (العربية)Toggle

تم الدفع بنجاح

تمت معالجة دفعتك البالغة 29.99 دولارًا. تم إرسال إيصال إلى عنوان بريدك الإلكتروني.

ميزة جديدة متاحة

لقد أضفنا دعم الوضع الداكن. يمكنك تفعيله في إعدادات حسابك.

Copy

```
"use client"

import * as React from "react"
```

View Code

### Our approach to RTL

Traditionally, component libraries that support RTL ship with logical classes baked in. This means everyone has to work with classes like `ms-4` and `start-2`, even if they're only building for LTR layouts.

We took a different approach. The shadcn CLI transforms classes at install time, so you only see logical classes when you actually need them. If you're not building for RTL, you work with familiar classes like `ml-4` and `left-2`. When you enable RTL, the CLI handles the conversion for you.

**You don't have to learn RTL until you need it.**

### How it works

When you add components with `rtl: true` set in your `components.json`, the CLI automatically converts physical CSS classes like `ml-4` and `text-left` to their logical equivalents like `ms-4` and `text-start`.

- Physical positioning classes like `left-*` and `right-*` become `start-*` and `end-*`.
- Margin and padding classes like `ml-*` and `pr-*` become `ms-*` and `pe-*`.
- Text alignment classes like `text-left` become `text-start`.
- Directional props are updated to use logical values.
- Supported icons are automatically flipped using `rtl:rotate-180`.
- Animations like `slide-in-from-left` become `slide-in-from-start`.

### RTL examples for every component

We've added RTL examples for every component. You'll find live previews and code on each [component page](/docs/components).

Arabic (العربية)Toggle

تسجيل الدخول إلى حسابك

أدخل بريدك الإلكتروني أدناه لتسجيل الدخول إلى حسابك

إنشاء حساب

البريد الإلكتروني

كلمة المرور[نسيت كلمة المرور؟](#)

تسجيل الدخولتسجيل الدخول باستخدام Google

Copy

```
"use client"

import * as React from "react"
```

View Code

### CLI updates

**New projects**: Use the `--rtl` flag with `init` or `create` to enable RTL from the start.

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest init --rtl
```

Copy
```

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest create --rtl
```

Copy
```

**Existing projects**: Migrate your components with the `migrate rtl` command.

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest migrate rtl
```

Copy
```

This transforms all components in your `ui` directory to use logical classes. You can also pass a specific path or glob pattern.

## Try it out

Click the link below to open a Next.js project with RTL support in v0.

[![Open in v0](https://v0.app/chat-static/button.svg)](https://v0.app/chat/api/open?url=https://github.com/shadcn-ui/next-template-rtl)

### Links

- [RTL Documentation](/docs/rtl)
- [Font Recommendations](/docs/rtl#font-recommendations)
- [Animations](/docs/rtl#animations)
- [Migrating Existing Components](/docs/rtl#migrating-existing-components)
- [Next.js Setup](/docs/rtl/next)
- [Vite Setup](/docs/rtl/vite)
- [TanStack Start Setup](/docs/rtl/start)

## January 2026 - Inline Start and End Styles

We've updated the styles for Base UI components to support `inline-start` and `inline-end` side values. The following components now support these values:

- Tooltip
- Popover
- Combobox
- Context Menu
- Dropdown Menu
- Hover Card
- Menubar
- Select

### What Changed

We added new Tailwind classes to handle the logical side values:

```
Copy<PopoverPrimitive.Popup
  className={cn(
    "... data-[side=bottom]:slide-in-from-top-2
    data-[side=left]:slide-in-from-right-2
    data-[side=right]:slide-in-from-left-2
    data-[side=top]:slide-in-from-bottom-2
+   data-[side=inline-start]:slide-in-from-right-2
+   data-[side=inline-end]:slide-in-from-left-2 ...",
    className
  )}
/>
```

### Usage

```
Copy<Popover>
  <PopoverTrigger>Open</PopoverTrigger>
  <PopoverContent side="inline-start">
    {/* Opens on the left in LTR, right in RTL */}
  </PopoverContent>
</Popover>
```

### LLM Prompt

Ask your LLM to update your components by running the following prompt:

```
CopyAdd inline-start and inline-end support to my shadcn/ui components. Add the following Tailwind classes to each component:
 
| File | Component | Add Classes |
|------|-----------|-------------|
| tooltip.tsx | TooltipContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
| tooltip.tsx | TooltipArrow | `data-[side=inline-start]:top-1/2! data-[side=inline-start]:-right-1 data-[side=inline-start]:-translate-y-1/2
data-[side=inline-end]:top-1/2! data-[side=inline-end]:-left-1 data-[side=inline-end]:-translate-y-1/2` |
| popover.tsx | PopoverContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
| hover-card.tsx | HoverCardContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
| select.tsx | SelectContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2
data-[align-trigger=true]:animate-none` and add `data-align-trigger={alignItemWithTrigger}` attribute |
| combobox.tsx | ComboboxContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
| dropdown-menu.tsx | DropdownMenuContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
| context-menu.tsx | ContextMenuContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
| menubar.tsx | MenubarContent | `data-[side=inline-start]:slide-in-from-right-2 data-[side=inline-end]:slide-in-from-left-2` |
 
Add these classes next to the existing `data-[side=top]`, `data-[side=bottom]`, `data-[side=left]`, `data-[side=right]` classes.
```

## January 2026 - Base UI Documentation

We've shipped full documentation for Base UI components.

When we launched `npx shadcn create` in December, we introduced the ability to choose between Radix and Base UI as your component library. Today, we're following up with complete documentation for all Base UI components.

### What's New

- **Full Base UI docs** - Every component now has dedicated documentation for Base UI, covering usage, props, and examples.
- **Rebuilt examples** - All component examples have been rebuilt for both Radix and Base UI. Switch between them to see the implementation differences.
- **Side-by-side comparison** - The docs make it easy to compare how components work across both libraries.

### Same Abstraction, Different Primitives

The goal remains the same: give you a consistent API regardless of which primitive library you choose. The components look and behave the same way. Only the underlying implementation changes.

```
Copy// Works the same whether you're using Radix or Base UI.
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"
```

If you're starting a new project, run `npx shadcn create` and pick your preferred library. The CLI handles the rest.

[Try shadcn/create](/create)

## December 2025 - npx shadcn create

From the very first commit, the goal of shadcn/ui was to make it customizable.

The idea is to give you solid defaults, spacing, color tokens, animations, accessibility, and then let you take it from there. Tweak the code. Add new components. Change the colors. Build your own version.

But somewhere along the way, all apps started looking the same. I guess the defaults were a little *too* good. My bad.

Today, we're changing that: **npx shadcn create**.

Customize Everything. Pick your component library, icons, base color, theme, fonts and create your own version of shadcn/ui.

We're starting with **5 new visual styles,** designed to help your UI actually feel like *your* UI.

- **Vega** – The classic shadcn/ui look.
- **Nova** – Reduced padding and margins for compact layouts.
- **Maia** – Soft and rounded, with generous spacing.
- **Lyra** – Boxy and sharp. Pairs well with mono fonts.
- **Mira** – Compact. Made for dense interfaces.

**This goes beyond theming**.

Your config doesn't just change colors, it rewrites the component code to match your setup. Fonts, spacing, structure, even the libraries you use, everything adapts to your preferences.

The new CLI takes care of it all.

Start with a component library. Choose between Radix or Base UI.

We rebuilt every component for Base UI, keeping the same abstraction.
They are fully compatible with your existing components, even those pulled from remote registries.

When you pull down components, we auto-detect your library and apply the right transformations.

**It's time to build something that doesn't look like everything else.**

Now available for Next.js, Vite, TanStack Start and v0.

[Get Started](/create)

## More Updates

[October 2025Registry Directory](/docs/changelog/2025-10-registry-directory)[October 2025New Components](/docs/changelog/2025-10-new-components)[September 2025Registry Index](/docs/changelog/2025-09-registry-index)[August 2025shadcn CLI 3.0 and MCP Server](/docs/changelog/2025-08-cli-3-mcp)[July 2025Universal Registry Items](/docs/changelog/2025-07-universal-registry)[July 2025Local File Support](/docs/changelog/2025-07-local-file-support)[June 2025radix-ui Migration](/docs/changelog/2025-06-radix-ui)[June 2025Calendar Component](/docs/changelog/2025-06-calendar)[May 2025New Site](/docs/changelog/2025-05-new-site)[April 2025MCP](/docs/changelog/2025-04-mcp)[March 2025shadcn 2.5.0](/docs/changelog/2025-04-shadcn-2-5)[March 2025Cross-framework Route Support](/docs/changelog/2025-04-cross-framework)[February 2025Tailwind v4](/docs/changelog/2025-02-tailwind-v4)[February 2025Updated Registry Schema](/docs/changelog/2025-02-registry-schema)[January 2025Blocks Community](/docs/changelog/2025-01-blocks)[December 2024Monorepo Support](/docs/changelog/2024-12-monorepo)[November 2024Icons](/docs/changelog/2024-11-icons)[October 2024React 19](/docs/changelog/2024-10-react-19)[October 2024Sidebar](/docs/changelog/2024-10-sidebar)[August 2024npx shadcn init](/docs/changelog/2024-08-npx-shadcn-init)[April 2024Lift Mode](/docs/changelog/2024-04-lift-mode)[March 2024Introducing Blocks](/docs/changelog/2024-03-blocks)[March 2024Breadcrumb and Input OTP](/docs/changelog/2024-03-breadcrumb-otp)[December 2023New Components](/docs/changelog/2023-12-new-components)[July 2023JavaScript](/docs/changelog/2023-07-javascript)[June 2023New CLI, Styles and more](/docs/changelog/2023-06-new-cli)

On This Page

[February 2026 - Unified Radix UI Package](/docs/changelog/2026-02-radix-ui)[January 2026 - RTL Support](/docs/changelog/2026-01-rtl)[January 2026 - Inline Start and End Styles](/docs/changelog/2026-01-inline-side-styles)[January 2026 - Base UI Documentation](/docs/changelog/2026-01-base-ui)[December 2025 - npx shadcn create](/docs/changelog/2025-12-shadcn-create)[More Updates](#more-updates)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)