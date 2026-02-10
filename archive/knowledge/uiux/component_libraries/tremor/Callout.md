# Callout

Source: https://tremor.so/docs/ui/callout

---

UI

# Callout

Used for hints, disclaimers, tips, warnings, or documentation needs.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Callout)

Preview

Code

Sales Performance

System Update: Enhanced Salesforce and Dynamics 365 integration now delivers key sales performance metrics directly to your dashboard for improved target achievement.

```
import { Callout } from '@/components/Callout';  export const CalloutHero = () => (  <Callout title="Sales Performance">    System Update: Enhanced Salesforce and Dynamics 365 integration now delivers    key sales performance metrics directly to your dashboard for improved target    achievement.  </Callout>);
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
   // Tremor Callout [v0.0.1]
   import React from "react"import { tv, type VariantProps } from "tailwind-variants"
   import { cx } from "@/lib/utils"
   const calloutVariants = tv({  base: "flex flex-col overflow-hidden rounded-md p-4 text-sm",  variants: {    variant: {      default: [        // text color        "text-blue-900 dark:text-blue-400",        // background color        "bg-blue-50 dark:bg-blue-950/70",      ],      success: [        // text color        "text-emerald-900 dark:text-emerald-500",        // background color        "bg-emerald-50 dark:bg-emerald-950/70",      ],      error: [        // text color        "text-red-900 dark:text-red-500",        // background color        "bg-red-50 dark:bg-red-950/70",      ],      warning: [        // text color        "text-yellow-900 dark:text-yellow-500",        // background color        "bg-yellow-50 dark:bg-yellow-950/70",      ],      neutral: [        // text color        "text-gray-900 dark:text-gray-400",        // background color        "bg-gray-100 dark:bg-gray-800/70",      ],    },  },  defaultVariants: {    variant: "default",  },})
   interface CalloutProps  extends React.ComponentPropsWithoutRef<"div">,    VariantProps<typeof calloutVariants> {  title: string  icon?: React.ElementType | React.ReactElement}
   const Callout = React.forwardRef<HTMLDivElement, CalloutProps>(  (    { title, icon: Icon, className, variant, children, ...props }: CalloutProps,    forwardedRef,  ) => {    return (      <div        ref={forwardedRef}        className={cx(calloutVariants({ variant }), className)}        tremor-id="tremor-raw"        {...props}      >        <div className={cx("flex items-start")}>          {Icon && typeof Icon === "function" ? (            <Icon              className={cx("mr-1.5 h-5 w-5 shrink-0")}              aria-hidden="true"            />          ) : (            Icon          )}          <span className={cx("font-semibold")}>{title}</span>        </div>        <div className={cx("overflow-y-auto", children ? "mt-2" : "")}>          {children}        </div>      </div>    )  },)
   Callout.displayName = "Callout"
   export { Callout, calloutVariants, type CalloutProps }
   ```

## Example: Callout with content

Preview

Code

Default Variant

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.

Success Variant

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.

Warning Variant

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.

Neutral Variant

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.

Error Variant

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.

```
import { Callout } from '@/components/Callout';
export const CalloutExample = () => (  <div className="flex flex-col gap-4">    <Callout variant="default" title="Default Variant">      Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy      eirmod tempor invidunt ut labore et dolore magna aliquyam erat.    </Callout>    <Callout variant="success" title="Success Variant">      Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy      eirmod tempor invidunt ut labore et dolore magna aliquyam erat.    </Callout>    <Callout variant="warning" title="Warning Variant">      Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy      eirmod tempor invidunt ut labore et dolore magna aliquyam erat.    </Callout>    <Callout variant="neutral" title="Neutral Variant">      Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy      eirmod tempor invidunt ut labore et dolore magna aliquyam erat.    </Callout>    <Callout variant="error" title="Error Variant">      Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy      eirmod tempor invidunt ut labore et dolore magna aliquyam erat.    </Callout>  </div>);
```

## Example: Callout with icon

To place an icon, use the icon prop.

Preview

Code

AWS Credit Alert

Warning: Your AWS credits are nearly depleted. Please review your usage and consider adding more credits to avoid service interruptions. Visit your account dashboard for details.

```
import { Callout } from '@/components/Callout';import { RiErrorWarningFill } from '@remixicon/react';
export const CalloutIconExample = () => (  <Callout title="AWS Credit Alert" icon={RiErrorWarningFill}>    Warning: Your AWS credits are nearly depleted. Please review your usage and    consider adding more credits to avoid service interruptions. Visit your    account dashboard for details.  </Callout>
  {/* Would also work this way:  <Callout    title="AWS Credit Alert"    icon={<RiErrorWarningFill className="mr-1.5 h-5 w-5 shrink-0" aria-hidden="true" />}  >    Warning: Your AWS credits are nearly depleted. Please review your usage and    consider adding more credits to avoid service interruptions. Visit your    account dashboard for details.  </Callout> */});
```

## API Reference: Callout

This component is based on the div element and supports all of its props.

title

Required

string

:   Add a title to the callout.

variant

"default" | "success" | "error" | "warning" | "neutral"

:   Set a predefined look.

Default: "default"

icon

React.ElementType | React.ReactElement

:   Set an icon displayed left of the title.