# Remix

Source: https://ui.shadcn.com/docs/installation/remix

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

# Remix

Copy Page

[Previous](/docs/installation/react-router)[Next](/docs/installation/astro)

Install and configure shadcn/ui for Remix.

**Note:** This guide is for Remix. For React Router, see the [React Router](/docs/installation/react-router) guide.

### Create project

Start by creating a new Remix project using `create-remix`:

```
pnpmnpmyarnbun

```
pnpm dlx create-remix@latest my-app
```

Copy
```

### Run the CLI

Run the `shadcn` init command to setup your project:

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest init
```

Copy
```

### Configure components.json

You will be asked a few questions to configure `components.json`:

```
CopyWhich color would you like to use as base color? › Neutral
```

### App structure

**Note**: This app structure is only a suggestion. You can place the files wherever you want.

- Place the UI components in the `app/components/ui` folder.
- Your own components can be placed in the `app/components` folder.
- The `app/lib` folder contains all the utility functions. We have a `utils.ts` where we define the `cn` helper.
- The `app/tailwind.css` file contains the global CSS.

### Install Tailwind CSS

```
pnpmnpmyarnbun

```
pnpm add -D tailwindcss@latest autoprefixer@latest
```

Copy
```

Then we create a `postcss.config.js` file:

postcss.config.js

```
Copyexport default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

And finally we add the following to our `remix.config.js` file:

remix.config.js

```
Copy/** @type {import('@remix-run/dev').AppConfig} */
export default {
  ...
  tailwind: true,
  postcss: true,
  ...
};
```

### Add `tailwind.css` to your app

In your `app/root.tsx` file, import the `tailwind.css` file:

app/root.tsx

```
Copyimport styles from "./tailwind.css?url"
 
export const links: LinksFunction = () => [
  { rel: "stylesheet", href: styles },
  ...(cssBundleHref ? [{ rel: "stylesheet", href: cssBundleHref }] : []),
]
```

### That's it

You can now start adding components to your project.

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add button
```

Copy
```

The command above will add the `Button` component to your project. You can then import it like this:

app/routes/index.tsx

```
Copyimport { Button } from "~/components/ui/button"
 
export default function Home() {
  return (
    <div>
      <Button>Click me</Button>
    </div>
  )
}
```

[React Router](/docs/installation/react-router)[Astro](/docs/installation/astro)

On This Page

[Create project](#create-project)[Run the CLI](#run-the-cli)[Configure components.json](#configure-componentsjson)[App structure](#app-structure)[Install Tailwind CSS](#install-tailwind-css)[Add `tailwind.css` to your app](#add-tailwindcss-to-your-app)[That's it](#thats-it)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)