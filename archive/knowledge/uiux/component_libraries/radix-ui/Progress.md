# Progress

Source: https://www.radix-ui.com/primitives/docs/components/progress

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

Components

# Progress

Displays an indicator showing the completion progress of a task, typically
displayed as a progress bar.

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Progress } from "radix-ui";

import "./styles.css";

const ProgressDemo = () => {

const [progress, setProgress] = React.useState(13);

React.useEffect(() => {

const timer = setTimeout(() => setProgress(66), 500);

return () => clearTimeout(timer);

}, []);

return (

<Progress.Root className="ProgressRoot" value={progress}>

<Progress.Indicator
				className="ProgressIndicator"
				style={{ transform: `translateX(-${100 - progress}%)` }}
			/>

</Progress.Root>

);

};

export default ProgressDemo;

Expand code
```

## Features

Provides context for assistive technology to read the progress of a task.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-progress
```

### [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Progress } from "radix-ui";

export default () => (

<Progress.Root>

<Progress.Indicator />

</Progress.Root>

);
```

## [Accessibility](#accessibility)

Adheres to the [`progressbar` role requirements](https://www.w3.org/WAI/ARIA/apg/patterns/meter).

## [API Reference](#api-reference)

### [Root](#root)

Contains all of the progress parts.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `value` Prop description | `number | null` | No default value |
| `max` Prop description | `number` | No default value |
| `getValueLabel` Prop description | `function` See full type | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"complete" | "indeterminate" | "loading"` |
| `[data-value]` | The current value |
| `[data-max]` | The max value |

### [Indicator](#indicator)

Used to show the progress visually. It also makes progress accessible to assistive technologies.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"complete" | "indeterminate" | "loading"` |
| `[data-value]` | The current value |
| `[data-max]` | The max value |

Previous[Popover](/primitives/docs/components/popover)

Next[Radio Group](/primitives/docs/components/radio-group)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/progress.mdx "Edit this page on GitHub.")