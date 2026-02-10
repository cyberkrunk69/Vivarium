# Button

Source: https://tremor.so/docs/ui/button

---

UI

# Button

Well, a Button.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Button)

Preview

Code

[Continue to installation](#installation)

```
import { Button } from '@/components/Button';  export const ButtonHero = () => (  <div className="flex justify-center">    <Button asChild>      <a href="#installation">Continue to installation</a>    </Button>  </div>);
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install @radix-ui/react-slot tailwind-variants @remixicon/react
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Button [v1.0.0]
   import React from "react"import { Slot } from "@radix-ui/react-slot"import { RiLoader2Fill } from "@remixicon/react"import { tv, type VariantProps } from "tailwind-variants"
   import { cx, focusRing } from "@/lib/utils"
   const buttonVariants = tv({  base: [    // base    "relative inline-flex items-center justify-center whitespace-nowrap rounded-md border px-3 py-2 text-center text-sm font-medium shadow-xs transition-all duration-100 ease-in-out",    // disabled    "disabled:pointer-events-none disabled:shadow-none",    // focus    focusRing,  ],  variants: {    variant: {      primary: [        // border        "border-transparent",        // text color        "text-white dark:text-white",        // background color        "bg-blue-500 dark:bg-blue-500",        // hover color        "hover:bg-blue-600 dark:hover:bg-blue-600",        // disabled        "disabled:bg-blue-300 disabled:text-white",        "dark:disabled:bg-blue-800 dark:disabled:text-blue-400",      ],      secondary: [        // border        "border-gray-300 dark:border-gray-800",        // text color        "text-gray-900 dark:text-gray-50",        // background color        "bg-white dark:bg-gray-950",        //hover color        "hover:bg-gray-50 dark:hover:bg-gray-900/60",        // disabled        "disabled:text-gray-400",        "dark:disabled:text-gray-600",      ],      light: [        // base        "shadow-none",        // border        "border-transparent",        // text color        "text-gray-900 dark:text-gray-50",        // background color        "bg-gray-200 dark:bg-gray-900",        // hover color        "hover:bg-gray-300/70 dark:hover:bg-gray-800/80",        // disabled        "disabled:bg-gray-100 disabled:text-gray-400",        "dark:disabled:bg-gray-800 dark:disabled:text-gray-600",      ],      ghost: [        // base        "shadow-none",        // border        "border-transparent",        // text color        "text-gray-900 dark:text-gray-50",        // hover color        "bg-transparent hover:bg-gray-100 dark:hover:bg-gray-800/80",        // disabled        "disabled:text-gray-400",        "dark:disabled:text-gray-600",      ],      destructive: [        // text color        "text-white",        // border        "border-transparent",        // background color        "bg-red-600 dark:bg-red-700",        // hover color        "hover:bg-red-700 dark:hover:bg-red-600",        // disabled        "disabled:bg-red-300 disabled:text-white",        "dark:disabled:bg-red-950 dark:disabled:text-red-400",      ],    },  },  defaultVariants: {    variant: "primary",  },})
   interface ButtonProps  extends React.ComponentPropsWithoutRef<"button">,    VariantProps<typeof buttonVariants> {  asChild?: boolean  isLoading?: boolean  loadingText?: string}
   const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(  (    {      asChild,      isLoading = false,      loadingText,      className,      disabled,      variant,      children,      ...props    }: ButtonProps,    forwardedRef,  ) => {    const Component = asChild ? Slot : "button"    return (      <Component        ref={forwardedRef}        className={cx(buttonVariants({ variant }), className)}        disabled={disabled || isLoading}        tremor-id="tremor-raw"        {...props}      >        {isLoading ? (          <span className="pointer-events-none flex shrink-0 items-center justify-center gap-1.5">            <RiLoader2Fill              className="size-4 shrink-0 animate-spin"              aria-hidden="true"            />            <span className="sr-only">              {loadingText ? loadingText : "Loading"}            </span>            {loadingText ? loadingText : children}          </span>        ) : (          children        )}      </Component>    )  },)
   Button.displayName = "Button"
   export { Button, buttonVariants, type ButtonProps }
   ```

## Example: Button variants

There are 4 button variants.

Preview

Code

PrimarySecondaryLightGhostDestructive

```
import { Button } from '@/components/Button';
export const ButtonVariantExample = () => (  <div className="flex flex-wrap justify-center gap-6">    <Button variant="primary">Primary</Button>    <Button variant="secondary">Secondary</Button>    <Button variant="light">Light</Button>    <Button variant="ghost">Ghost</Button>    <Button variant="destructive">Destructive</Button>  </div>);
```

## Example: Loading

To set the button in a loading state, use the isLoading prop. You can also set a custom loading text by passing a string to loadingText.

Preview

Code

LoadingPrimaryLoading textLoading text

```
import { Button } from '@/components/Button';
export const ButtonLoadingExample = () => (  <div className="mx-auto flex w-fit gap-6">    <Button isLoading>Primary</Button>    <Button isLoading loadingText="Loading text">      Primary    </Button>  </div>);
```

## Example: Create anchor with asChild pop

Using the asChild asChild prop, we can wrap an anchor tag with the Button and render an anchor (<a/>) tag instead of a button.

Preview

Code

[API Reference](#api-reference-button)

```
import { Button } from '@/components/Button';  export const ButtonAsChildExample = () => (  <div className="flex justify-center">    <Button asChild>      <a href="#api-reference-button">API Reference</a>    </Button>  </div>);
```

## API Reference: Button

This component is based on the button element and supports all of its props.

variant

"primary" | "secondary" | "light" | "ghost" | "destructive"

:   Set a predefined look.

Default: "primary"

isLoading

boolean

:   If set to true, an animated spinner is shown and the button is in a disabeld state.

Default: false

loadingText

string

:   Alternative text, if loading property is set to true.