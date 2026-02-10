# Size

Source: https://primer.style/foundations/primitives/size

---

# Size

An overview of all available size CSS variables

## [Base](#base)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-base--base)

| Sample | CSS variable | Output value | Source value |
| --- | --- | --- | --- |
|  | `--base-size-2` Copy to clipboard | 0.125rem | 2px |
|  | `--base-size-4` Copy to clipboard | 0.25rem | 4px |
|  | `--base-size-6` Copy to clipboard | 0.375rem | 6px |
|  | `--base-size-8` Copy to clipboard | 0.5rem | 8px |
|  | `--base-size-12` Copy to clipboard | 0.75rem | 12px |
|  | `--base-size-16` Copy to clipboard | 1rem | 16px |
|  | `--base-size-20` Copy to clipboard | 1.25rem | 20px |
|  | `--base-size-24` Copy to clipboard | 1.5rem | 24px |
|  | `--base-size-28` Copy to clipboard | 1.75rem | 28px |
|  | `--base-size-32` Copy to clipboard | 2rem | 32px |
|  | `--base-size-36` Copy to clipboard | 2.25rem | 36px |
|  | `--base-size-40` Copy to clipboard | 2.5rem | 40px |
|  | `--base-size-44` Copy to clipboard | 2.75rem | 44px |
|  | `--base-size-48` Copy to clipboard | 3rem | 48px |
|  | `--base-size-64` Copy to clipboard | 4rem | 64px |
|  | `--base-size-80` Copy to clipboard | 5rem | 80px |
|  | `--base-size-96` Copy to clipboard | 6rem | 96px |
|  | `--base-size-112` Copy to clipboard | 7rem | 112px |
|  | `--base-size-128` Copy to clipboard | 8rem | 128px |

## [Border](#border)

### [Border size](#border-size)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-functional-border--border-size)

| Sample | CSS variable | Output value | Source value |
| --- | --- | --- | --- |
|  | `--boxShadow-thick` Copy to clipboard | inset 0 0 0 0.125rem | inset 0 0 0 {borderWidth.thick} |
|  | `--boxShadow-thicker` Copy to clipboard | inset 0 0 0 0.25rem | inset 0 0 0 {borderWidth.thicker} |
|  | `--boxShadow-thin` Copy to clipboard | inset 0 0 0 0.0625rem | inset 0 0 0 {borderWidth.thin} |
|  | `--borderWidth-default` Copy to clipboard | 0.0625rem | {borderWidth.thin} |
|  | `--borderWidth-thick` Copy to clipboard | 0.125rem | 2px |
|  | `--borderWidth-thicker` Copy to clipboard | 0.25rem | 4px |
|  | `--borderWidth-thin` Copy to clipboard | 0.0625rem | 1px |

### [Border radius](#border-radius)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-functional-border--border-radius)

| Sample | CSS variable | Output value | Source value |
| --- | --- | --- | --- |
|  | `--borderRadius-default` Copy to clipboard | 0.375rem | {borderRadius.medium} |
|  | `--borderRadius-full` Copy to clipboard | 624.9375rem | 9999px |
|  | `--borderRadius-large` Copy to clipboard | 0.75rem | 12px |
|  | `--borderRadius-medium` Copy to clipboard | 0.375rem | 6px |
|  | `--borderRadius-small` Copy to clipboard | 0.1875rem | 3px |

### [Outline](#outline)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-functional-border--outline)

| Sample | CSS variable | Output value | Source value |
| --- | --- | --- | --- |
|  | `--outline-focus-offset` Copy to clipboard | -0.125rem | -2px |
|  | `--outline-focus-width` Copy to clipboard | 0.125rem | 2px |

## [Breakpoints](#breakpoints)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-functional-breakpoints--breakpoints)

| CSS variable | Output value | Source value |
| --- | --- | --- |
| `--breakpoint-xsmall` Copy to clipboard | 20rem | 320px |
| `--breakpoint-small` Copy to clipboard | 34rem | 544px |
| `--breakpoint-medium` Copy to clipboard | 48rem | 768px |
| `--breakpoint-large` Copy to clipboard | 63.25rem | 1012px |
| `--breakpoint-xlarge` Copy to clipboard | 80rem | 1280px |
| `--breakpoint-xxlarge` Copy to clipboard | 87.5rem | 1400px |

## [Viewport](#viewport)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-functional-viewport--viewport)

| CSS variable | Output value |
| --- | --- |
| `--viewportRange-landscape` Copy to clipboard | (orientation: landscape) |
| `--viewportRange-narrow` Copy to clipboard | (max-width: calc(48rem - 0.02px)) |
| `--viewportRange-narrowLandscape` Copy to clipboard | (max-width: calc(63.25rem - 0.02px) and (max-height: calc(34rem - 0.02px)) and (orientation: landscape)) |
| `--viewportRange-portrait` Copy to clipboard | (orientation: portrait) |
| `--viewportRange-regular` Copy to clipboard | (min-width: 48rem) |
| `--viewportRange-wide` Copy to clipboard | (min-width: 87.5rem) |

## [Layout](#layout)

### [Stack](#stack)

| Sample | CSS variable | Output value | Source value |
| --- | --- | --- | --- |
|  | `--stack-gap-condensed` Copy to clipboard | 0.5rem | {base.size.8} |
|  | `--stack-gap-normal` Copy to clipboard | 1rem | {base.size.16} |
|  | `--stack-gap-spacious` Copy to clipboard | 1.5rem | {base.size.24} |
|  | `--stack-padding-condensed` Copy to clipboard | 0.5rem | {base.size.8} |
|  | `--stack-padding-normal` Copy to clipboard | 1rem | {base.size.16} |
|  | `--stack-padding-spacious` Copy to clipboard | 1.5rem | {base.size.24} |

### [Controls](#controls)

### [Overlay](#overlay)

[View in Storybook](https://primer.style/primitives/storybook/?path=/story/size-functional-overlay--overlay)

| CSS variable | Output value | Source value |
| --- | --- | --- |
| `--overlay-borderRadius` Copy to clipboard | 0.375rem | {borderRadius.medium} |
| `--overlay-height-large` Copy to clipboard | 27rem | 432px |
| `--overlay-height-medium` Copy to clipboard | 20rem | 320px |
| `--overlay-height-small` Copy to clipboard | 16rem | 256px |
| `--overlay-height-xlarge` Copy to clipboard | 37.5rem | 600px |
| `--overlay-offset` Copy to clipboard | 0.25rem | 4px |
| `--overlay-padding-condensed` Copy to clipboard | 0.5rem | {base.size.8} |
| `--overlay-padding-normal` Copy to clipboard | 1rem | {base.size.16} |
| `--overlay-paddingBlock-condensed` Copy to clipboard | 0.25rem | {base.size.4} |
| `--overlay-paddingBlock-normal` Copy to clipboard | 0.75rem | {base.size.12} |
| `--overlay-width-large` Copy to clipboard | 40rem | 640px |
| `--overlay-width-medium` Copy to clipboard | 30rem | 480px |
| `--overlay-width-small` Copy to clipboard | 20rem | 320px |
| `--overlay-width-xlarge` Copy to clipboard | 60rem | 960px |
| `--overlay-width-xsmall` Copy to clipboard | 12rem | 192px |