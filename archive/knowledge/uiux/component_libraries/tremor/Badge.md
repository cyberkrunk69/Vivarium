# Badge

Source: https://tremor.so/docs/ui/badge

---

UI

# Badge

Badges highlight information.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Badge)

Preview

Code

DefaultNeutralSuccessWarningError

```
import { Badge } from '@/components/Badge';    export const BadgeHero = () => (  <div className="flex flex-wrap justify-center gap-3">    <Badge>Default</Badge>    <Badge variant="neutral">Neutral</Badge>    <Badge variant="success">Success</Badge>    <Badge variant="warning">Warning</Badge>    <Badge variant="error">Error</Badge>  </div>);
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install tailwind-variants
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Badge [v1.0.0]
   import React from "react"import { tv, type VariantProps } from "tailwind-variants"
   import { cx } from "@/lib/utils"
   const badgeVariants = tv({  base: cx(    "inline-flex items-center gap-x-1 whitespace-nowrap rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset",  ),  variants: {    variant: {      default: [        "bg-blue-50 text-blue-900 ring-blue-500/30",        "dark:bg-blue-400/10 dark:text-blue-400 dark:ring-blue-400/30",      ],      neutral: [        "bg-gray-50 text-gray-900 ring-gray-500/30",        "dark:bg-gray-400/10 dark:text-gray-400 dark:ring-gray-400/20",      ],      success: [        "bg-emerald-50 text-emerald-900 ring-emerald-600/30",        "dark:bg-emerald-400/10 dark:text-emerald-400 dark:ring-emerald-400/20",      ],      error: [        "bg-red-50 text-red-900 ring-red-600/20",        "dark:bg-red-400/10 dark:text-red-400 dark:ring-red-400/20",      ],      warning: [        "bg-yellow-50 text-yellow-900 ring-yellow-600/30",        "dark:bg-yellow-400/10 dark:text-yellow-500 dark:ring-yellow-400/20",      ],    },  },  defaultVariants: {    variant: "default",  },})
   interface BadgeProps  extends React.ComponentPropsWithoutRef<"span">,  VariantProps<typeof badgeVariants> { }
   const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(  ({ className, variant, ...props }: BadgeProps, forwardedRef) => {    return (      <span        ref={forwardedRef}        className={cx(badgeVariants({ variant }), className)}        tremor-id="tremor-raw"        {...props}      />    )  },)
   Badge.displayName = "Badge"
   export { Badge, badgeVariants, type BadgeProps }
   ```

## Example: Customized badge

To customise the badge, use the className attribute.

Preview

Code

Export RequestYour export is ready for download: 263 transactions

Download

```
import { Badge } from '@/components/Badge';
export const BadgeExample = () => (  <div className="flex items-center justify-between gap-8 rounded-md bg-blue-50 py-2.5 pl-2.5 pr-4 text-sm dark:bg-blue-900/50">    <div className="flex items-center gap-2 truncate">      <Badge className="ring-none dark:ring-none rounded-full bg-blue-800 text-white dark:bg-blue-500 dark:text-white">        Export Request      </Badge>      <span className="truncate text-blue-800 dark:text-blue-400">        Your export is ready for download:{" "}        <span className="font-semibold">263 transactions</span>      </span>    </div>    <button className="font-semibold text-blue-800 dark:text-blue-400">      Download    </button>  </div>);
```

## Example: Anchor with badgeVariants style

We can use the created badge styles to style any other component like the badges. Here we apply the badgeVariants to an anchor element.

Preview

Code

Anchor element

```
import { badgeVariants } from "@/components/Badge"import { cx } from "@/lib/utils"
export const BadgeAnchorWithBageStylesExample = () => (  <div className="flex justify-center">    <a className={cx(badgeVariants({ variant: "success" }), "cursor-pointer")}>      Anchor element    </a>  </div>)
```

## API Reference: Badge

This component is based on the span element and supports all of its props.

variant

"default" | "neutral" | "success" | "error" | "warning"

:   Set a predefined look.

Default: "default"