# Chart

Source: https://ui.shadcn.com/docs/components/chart

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

# Chart

Copy Page

[Previous](/docs/components/radix/carousel)[Next](/docs/components/radix/checkbox)

Beautiful charts. Built using Recharts. Copy and paste into your apps.

[Radix UI](/docs/components/radix/chart)[Base UI](/docs/components/base/chart)

**Note:** We're working on upgrading to Recharts v3. In the meantime, if you'd like to start testing v3, see the code in the comment [here](https://github.com/shadcn-ui/ui/issues/7669#issuecomment-2998299159). We'll have an official release soon.

Bar Chart - Interactive

Showing total visitors for the last 3 months

Desktop7,324Mobile7,250

Introducing **Charts**. A collection of chart components that you can copy and paste into your apps.

Charts are designed to look great out of the box. They work well with the other components and are fully customizable to fit your project.

[Browse the Charts Library](/charts).

## Component

We use [Recharts](https://recharts.org/) under the hood.

We designed the `chart` component with composition in mind. **You build your charts using Recharts components and only bring in custom components, such as `ChartTooltip`, when and where you need it**.

```
Copyimport { Bar, BarChart } from "recharts"
 
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart"
 
export function MyChart() {
  return (
    <ChartContainer>
      <BarChart data={data}>
        <Bar dataKey="value" />
        <ChartTooltip content={<ChartTooltipContent />} />
      </BarChart>
    </ChartContainer>
  )
}
```

We do not wrap Recharts. This means you're not locked into an abstraction. When a new Recharts version is released, you can follow the official upgrade path to upgrade your charts.

**The components are yours**.

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add chart
```

Copy
```

## Your First Chart

Let's build your first chart. We'll build a bar chart, add a grid, axis, tooltip and legend.

### Start by defining your data

The following data represents the number of desktop and mobile users for each month.

**Note:** Your data can be in any shape. You are not limited to the shape of the data below. Use the `dataKey` prop to map your data to the chart.

components/example-chart.tsx

```
Copyconst chartData = [
  { month: "January", desktop: 186, mobile: 80 },
  { month: "February", desktop: 305, mobile: 200 },
  { month: "March", desktop: 237, mobile: 120 },
  { month: "April", desktop: 73, mobile: 190 },
  { month: "May", desktop: 209, mobile: 130 },
  { month: "June", desktop: 214, mobile: 140 },
]
```

### Define your chart config

The chart config holds configuration for the chart. This is where you place human-readable strings, such as labels, icons and color tokens for theming.

components/example-chart.tsx

```
Copyimport { type ChartConfig } from "@/components/ui/chart"
 
const chartConfig = {
  desktop: {
    label: "Desktop",
    color: "#2563eb",
  },
  mobile: {
    label: "Mobile",
    color: "#60a5fa",
  },
} satisfies ChartConfig
```

### Build your chart

You can now build your chart using Recharts components.

**Important:** Remember to set a `min-h-[VALUE]` on the `ChartContainer` component. This is required for the chart to be responsive.

Copy

```
"use client"

import { ChartContainer, type ChartConfig } from "@/components/ui/chart"
```

View Code

### Add a Grid

Let's add a grid to the chart.

### Import the `CartesianGrid` component.

```
Copyimport { Bar, BarChart, CartesianGrid } from "recharts"
```

### Add the `CartesianGrid` component to your chart.

```
Copy<ChartContainer config={chartConfig} className="min-h-[200px] w-full">
  <BarChart accessibilityLayer data={chartData}>
    <CartesianGrid vertical={false} />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
  </BarChart>
</ChartContainer>
```

Copy

```
"use client"

import { ChartContainer, type ChartConfig } from "@/components/ui/chart"
```

View Code

### Add an Axis

To add an x-axis to the chart, we'll use the `XAxis` component.

### Import the `XAxis` component.

```
Copyimport { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
```

### Add the `XAxis` component to your chart.

```
Copy<ChartContainer config={chartConfig} className="h-[200px] w-full">
  <BarChart accessibilityLayer data={chartData}>
    <CartesianGrid vertical={false} />
    <XAxis
      dataKey="month"
      tickLine={false}
      tickMargin={10}
      axisLine={false}
      tickFormatter={(value) => value.slice(0, 3)}
    />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
  </BarChart>
</ChartContainer>
```

Copy

```
"use client"

import { ChartContainer, type ChartConfig } from "@/components/ui/chart"
```

View Code

### Add Tooltip

So far we've only used components from Recharts. They look great out of the box thanks to some customization in the `chart` component.

To add a tooltip, we'll use the custom `ChartTooltip` and `ChartTooltipContent` components from `chart`.

### Import the `ChartTooltip` and `ChartTooltipContent` components.

```
Copyimport { ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
```

### Add the components to your chart.

```
Copy<ChartContainer config={chartConfig} className="h-[200px] w-full">
  <BarChart accessibilityLayer data={chartData}>
    <CartesianGrid vertical={false} />
    <XAxis
      dataKey="month"
      tickLine={false}
      tickMargin={10}
      axisLine={false}
      tickFormatter={(value) => value.slice(0, 3)}
    />
    <ChartTooltip content={<ChartTooltipContent />} />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
  </BarChart>
</ChartContainer>
```

Copy

```
"use client"

import {
```

View Code

Hover to see the tooltips. Easy, right? Two components, and we've got a beautiful tooltip.

### Add Legend

We'll do the same for the legend. We'll use the `ChartLegend` and `ChartLegendContent` components from `chart`.

### Import the `ChartLegend` and `ChartLegendContent` components.

```
Copyimport { ChartLegend, ChartLegendContent } from "@/components/ui/chart"
```

### Add the components to your chart.

```
Copy<ChartContainer config={chartConfig} className="h-[200px] w-full">
  <BarChart accessibilityLayer data={chartData}>
    <CartesianGrid vertical={false} />
    <XAxis
      dataKey="month"
      tickLine={false}
      tickMargin={10}
      axisLine={false}
      tickFormatter={(value) => value.slice(0, 3)}
    />
    <ChartTooltip content={<ChartTooltipContent />} />
    <ChartLegend content={<ChartLegendContent />} />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
  </BarChart>
</ChartContainer>
```

Copy

```
"use client"

import {
```

View Code

Done. You've built your first chart! What's next?

- [Themes and Colors](/docs/components/chart#theming)
- [Tooltip](/docs/components/chart#tooltip)
- [Legend](/docs/components/chart#legend)

## Chart Config

The chart config is where you define the labels, icons and colors for a chart.

It is intentionally decoupled from chart data.

This allows you to share config and color tokens between charts. It can also work independently for cases where your data or color tokens live remotely or in a different format.

```
Copyimport { Monitor } from "lucide-react"
 
import { type ChartConfig } from "@/components/ui/chart"
 
const chartConfig = {
  desktop: {
    label: "Desktop",
    icon: Monitor,
    // A color like 'hsl(220, 98%, 61%)' or 'var(--color-name)'
    color: "#2563eb",
    // OR a theme object with 'light' and 'dark' keys
    theme: {
      light: "#2563eb",
      dark: "#dc2626",
    },
  },
} satisfies ChartConfig
```

## Theming

Charts have built-in support for theming. You can use css variables (recommended) or color values in any color format, such as hex, hsl or oklch.

### CSS Variables

### Define your colors in your css file

app/globals.css

```
Copy@layer base {
  :root {
    --chart-1: oklch(0.646 0.222 41.116);
    --chart-2: oklch(0.6 0.118 184.704);
  }
 
  .dark: {
    --chart-1: oklch(0.488 0.243 264.376);
    --chart-2: oklch(0.696 0.17 162.48);
  }
}
```

### Add the color to your `chartConfig`

components/example-chart.tsx

```
Copyconst chartConfig = {
  desktop: {
    label: "Desktop",
    color: "var(--chart-1)",
  },
  mobile: {
    label: "Mobile",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig
```

### hex, hsl or oklch

You can also define your colors directly in the chart config. Use the color format you prefer.

components/example-chart.tsx

```
Copyconst chartConfig = {
  desktop: {
    label: "Desktop",
    color: "#2563eb",
  },
  mobile: {
    label: "Mobile",
    color: "hsl(220, 98%, 61%)",
  },
  tablet: {
    label: "Tablet",
    color: "oklch(0.5 0.2 240)",
  },
  laptop: {
    label: "Laptop",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig
```

### Using Colors

To use the theme colors in your chart, reference the colors using the format `var(--color-KEY)`.

#### Components

```
Copy<Bar dataKey="desktop" fill="var(--color-desktop)" />
```

#### Chart Data

components/example-chart.tsx

```
Copyconst chartData = [
  { browser: "chrome", visitors: 275, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
]
```

#### Tailwind

components/example-chart.tsx

```
Copy<LabelList className="fill-[--color-desktop]" />
```

## Tooltip

A chart tooltip contains a label, name, indicator and value. You can use a combination of these to customize your tooltip.

Label

Page Views

Desktop

186

Mobile

80

Name

Chrome

1,286

Firefox

1,000

Page Views

Desktop

12,486

Indicator

Chrome

1,286

You can turn on/off any of these using the `hideLabel`, `hideIndicator` props and customize the indicator style using the `indicator` prop.

Use `labelKey` and `nameKey` to use a custom key for the tooltip label and name.

Chart comes with the `<ChartTooltip>` and `<ChartTooltipContent>` components. You can use these two components to add custom tooltips to your chart.

components/example-chart.tsx

```
Copyimport { ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
```

components/example-chart.tsx

```
Copy<ChartTooltip content={<ChartTooltipContent />} />
```

### Props

Use the following props to customize the tooltip.

| Prop | Type | Description |
| --- | --- | --- |
| `labelKey` | string | The config or data key to use for the label. |
| `nameKey` | string | The config or data key to use for the name. |
| `indicator` | `dot` `line` or `dashed` | The indicator style for the tooltip. |
| `hideLabel` | boolean | Whether to hide the label. |
| `hideIndicator` | boolean | Whether to hide the indicator. |

### Colors

Colors are automatically referenced from the chart config.

### Custom

To use a custom key for tooltip label and names, use the `labelKey` and `nameKey` props.

```
Copyconst chartData = [
  { browser: "chrome", visitors: 187, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
]
 
const chartConfig = {
  visitors: {
    label: "Total Visitors",
  },
  chrome: {
    label: "Chrome",
    color: "hsl(var(--chart-1))",
  },
  safari: {
    label: "Safari",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig
```

components/example-chart.tsx

```
Copy<ChartTooltip
  content={<ChartTooltipContent labelKey="visitors" nameKey="browser" />}
/>
```

This will use `Total Visitors` for label and `Chrome` and `Safari` for the tooltip names.

## Legend

You can use the custom `<ChartLegend>` and `<ChartLegendContent>` components to add a legend to your chart.

components/example-chart.tsx

```
Copyimport { ChartLegend, ChartLegendContent } from "@/components/ui/chart"
```

components/example-chart.tsx

```
Copy<ChartLegend content={<ChartLegendContent />} />
```

### Colors

Colors are automatically referenced from the chart config.

### Custom

To use a custom key for legend names, use the `nameKey` prop.

```
Copyconst chartData = [
  { browser: "chrome", visitors: 187, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
]
 
const chartConfig = {
  chrome: {
    label: "Chrome",
    color: "hsl(var(--chart-1))",
  },
  safari: {
    label: "Safari",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig
```

components/example-chart.tsx

```
Copy<ChartLegend content={<ChartLegendContent nameKey="browser" />} />
```

This will use `Chrome` and `Safari` for the legend names.

## Accessibility

You can turn on the `accessibilityLayer` prop to add an accessible layer to your chart.

This prop adds keyboard access and screen reader support to your charts.

components/example-chart.tsx

```
Copy<LineChart accessibilityLayer />
```

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

Copy

```
"use client"

import {
```

View Code

[Carousel](/docs/components/radix/carousel)[Checkbox](/docs/components/radix/checkbox)

On This Page

[Component](#component)[Installation](#installation)[Your First Chart](#your-first-chart)[Add a Grid](#add-a-grid)[Add an Axis](#add-an-axis)[Add Tooltip](#add-tooltip)[Add Legend](#add-legend)[Chart Config](#chart-config)[Theming](#theming)[CSS Variables](#css-variables)[hex, hsl or oklch](#hex-hsl-or-oklch)[Using Colors](#using-colors)[Components](#components)[Chart Data](#chart-data)[Tailwind](#tailwind)[Tooltip](#tooltip)[Props](#props)[Colors](#colors)[Custom](#custom)[Legend](#legend)[Colors](#colors-1)[Custom](#custom-1)[Accessibility](#accessibility)[RTL](#rtl)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)