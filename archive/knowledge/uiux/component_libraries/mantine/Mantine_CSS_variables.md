# Mantine CSS variables

Source: https://mantine.dev/styles/css-variables/

---

# Mantine CSS variables

[MantineProvider](/theming/mantine-provider/) exposes all Mantine CSS variables based on the given [theme](/theming/theme-object/).
You can use these variables in [CSS](/styles/css-modules/) files, [style prop](/styles/style/) or any other styles.
Note that not all values are documented on this page, you can find full list of variables on [this page](/styles/css-variables-list/).

## [Typography variables](#typography-variables)

Typography variables control font family, font size, line height, font weight, and other text-related properties
of all Mantine components.

### [Font family](#font-family)

The following CSS variables are used to assign font families to all Mantine components:

| Variable | Default value |
| --- | --- |
| `--mantine-font-family` Controls font-family property of most Mantine components | system sans-serif fonts |
| `--mantine-font-family-monospace` Controls font-family property of code blocks | system monospace fonts |
| `--mantine-font-family-headings` Controls font-family property of headings | system sans-serif fonts |

You can control these variables in the [theme](/theming/theme-object/). Note that if
`theme.headings.fontFamily` is not set, `--mantine-font-family-headings` value
will be the same as `--mantine-font-family`.

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  // Controls --mantine-font-family
  fontFamily: 'Arial, sans-serif',

  // Controls --mantine-font-family-monospace
  fontFamilyMonospace: 'Courier New, monospace',

  headings: {
    // Controls --mantine-font-family-headings
    fontFamily: 'Georgia, serif',
  },
});
```

Expand code

If you want to use system fonts as a fallback for custom fonts, you can reference `DEFAULT_THEME`
value instead of defining it manually:

```
import { createTheme, DEFAULT_THEME } from '@mantine/core';

const theme = createTheme({
  fontFamily: `Roboto, ${DEFAULT_THEME.fontFamily}`,
});
```

Expand code

You can reference font family variables in your CSS:

```
.text {
  font-family: var(--mantine-font-family);
}

.code {
  font-family: var(--mantine-font-family-monospace);
}

.heading {
  font-family: var(--mantine-font-family-headings);
}
```

Expand code

And in [ff style prop](/styles/style-props/):

- `ff="text"` will use `--mantine-font-family` variable
- `ff="monospace"` will use `--mantine-font-family-monospace` variable
- `ff="heading"` will use `--mantine-font-family-headings` variable

```
import { Text } from '@mantine/core';

function Demo() {
  return (
    <Text ff="monospace">
      This text uses --mantine-font-family-monospace variable
    </Text>
  );
}
```

Expand code

### [Font size](#font-size)

Font size variables are used in most Mantine components to control text size. The
variable that is chosen depends on the component and its `size` prop.

| Variable | Default value |
| --- | --- |
| `--mantine-font-size-xs` | 0.75rem (12px) |
| `--mantine-font-size-sm` | 0.875rem (14px) |
| `--mantine-font-size-md` | 1rem (16px) |
| `--mantine-font-size-lg` | 1.125rem (18px) |
| `--mantine-font-size-xl` | 1.25rem (20px) |

You can reference font size variables in CSS:

```
.demo {
  font-size: var(--mantine-font-size-md);
}
```

Expand code

And in [fz style prop](/styles/style-props/):

```
import { Text } from '@mantine/core';

function Demo() {
  return (
    <Text fz="xl">
      This text uses --mantine-font-size-xl variable
    </Text>
  );
}
```

Expand code

To define custom font sizes, can use `theme.fontSizes` property:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  fontSizes: {
    xs: '0.5rem',
    sm: '0.75rem',
    md: '1rem',
    lg: '1.25rem',
    xl: '1.5rem',
  },
});
```

Expand code

Note that `theme.fontSizes` object is merged with the `DEFAULT_THEME.fontSizes` –
it is not required to define all values, only those that you want to change.

```
import { createTheme } from '@mantine/core';

// Changes only xs font size,
// other values will be taken from the DEFAULT_THEME
const theme = createTheme({
  fontSizes: {
    xs: '0.5rem',
  },
});
```

Expand code

You can add any number of additional font sizes to the `theme.fontSizes` object.
These values will be defined as CSS variables in `--mantine-font-size-{size}` format:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  fontSizes: {
    xxs: '0.125rem',
    xxl: '2rem',
  },
});
```

Expand code

After defining `theme.fontSizes`, you can reference these variables in your CSS:

```
.demo {
  font-size: var(--mantine-font-size-xxs);
}
```

Expand code

> **Case conversion**
>
> Case conversion (camelCase to kebab-case) is not automatically applied to custom font sizes.
> If you define `theme.fontSizes` with camelCase keys, you need to reference them in camelCase format.
> For example, if you define `{ customSize: '1rem' }`, you need to reference it as `--mantine-font-size-customSize`.

### [Line height](#line-height)

Line height variables are used in [Text](/core/text/) component. In other components,
line-height is either calculated based on font size or set to `--mantine-line-height`,
which is an alias for `--mantine-line-height-md`.

| Variable | Default value |
| --- | --- |
| `--mantine-line-height` | 1.55 |
| `--mantine-line-height-xs` | 1.4 |
| `--mantine-line-height-sm` | 1.45 |
| `--mantine-line-height-md` | 1.55 |
| `--mantine-line-height-lg` | 1.6 |
| `--mantine-line-height-xl` | 1.65 |

You can reference line height variables in your CSS:

```
.demo {
  line-height: var(--mantine-line-height-md);
}
```

Expand code

And in [lh style prop](/styles/style-props/):

```
import { Text } from '@mantine/core';

function Demo() {
  return (
    <Text lh="xl">
      This text uses --mantine-line-height-xl variable
    </Text>
  );
}
```

Expand code

To define custom line heights, you can use `theme.lineHeights` property:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  lineHeights: {
    xs: '1.2',
    sm: '1.3',
    md: '1.4',
    lg: '1.5',
    xl: '1.6',
  },
});
```

Expand code

### [Headings](#headings)

`theme.headings` controls font-size, line-height, font-weight and text-wrap CSS properties
of headings in [Title](/core/title/) and [Typography](/core/typography/) components.

| Variable | Default value |
| --- | --- |
| General variables | |
| `--mantine-heading-font-weight` Controls font-weight property of all headings if not overridden | 700 |
| `--mantine-heading-text-wrap` Controls text-wrap property of all headings | wrap |
| h1 heading | |
| `--mantine-h1-font-size` | 2.125rem (34px) |
| `--mantine-h1-line-height` | 1.3 |
| `--mantine-h1-font-weight` | 700 |
| h2 heading | |
| `--mantine-h2-font-size` | 1.625rem (26px) |
| `--mantine-h2-line-height` | 1.35 |
| `--mantine-h2-font-weight` | 700 |
| h3 heading | |
| `--mantine-h3-font-size` | 1.375rem (22px) |
| `--mantine-h3-line-height` | 1.4 |
| `--mantine-h3-font-weight` | 700 |
| h4 heading | |
| `--mantine-h4-font-size` | 1.125rem (18px) |
| `--mantine-h4-line-height` | 1.45 |
| `--mantine-h4-font-weight` | 700 |
| h5 heading | |
| `--mantine-h5-font-size` | 1rem (16px) |
| `--mantine-h5-line-height` | 1.5 |
| `--mantine-h5-font-weight` | 700 |
| h6 heading | |
| `--mantine-h6-font-size` | 0.875rem (14px) |
| `--mantine-h6-line-height` | 1.5 |
| `--mantine-h6-font-weight` | 700 |

These variables are used in [Title](/core/title/) component, `order` prop
controls which heading level to use. For example, `order={3}` Title will use:

- `--mantine-h3-font-size`
- `--mantine-h3-line-height`
- `--mantine-h3-font-weight`

# This is h1 title

## This is h2 title

### This is h3 title

#### This is h4 title

##### This is h5 title

###### This is h6 title

Demo.tsx

```
import { Title } from '@mantine/core';

function Demo() {
  return (
    <>
      <Title order={1}>This is h1 title</Title>
      <Title order={2}>This is h2 title</Title>
      <Title order={3}>This is h3 title</Title>
      <Title order={4}>This is h4 title</Title>
      <Title order={5}>This is h5 title</Title>
      <Title order={6}>This is h6 title</Title>
    </>
  );
}
```

Expand code

You can reference heading variables in your CSS:

```
.h1 {
  font-size: var(--mantine-h1-font-size);
  line-height: var(--mantine-h1-line-height);
  font-weight: var(--mantine-h1-font-weight);
}
```

Expand code

And in [fz and lh style props](/styles/style-props/):

```
import { Box } from '@mantine/core';

function Demo() {
  return (
    <Box fz="h1" lh="h1">
      This text uses --mantine-h1-* variables
    </Box>
  );
}
```

Expand code

To change heading styles, can use `theme.headings` property:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  headings: {
    sizes: {
      h1: {
        fontSize: '2rem',
        lineHeight: '1.5',
        fontWeight: '500',
      },
      h2: {
        fontSize: '1.5rem',
        lineHeight: '1.6',
        fontWeight: '500',
      },
    },
    // ...
  },
});
```

Expand code

`theme.headings` object is deeply merged with the `DEFAULT_THEME.headings` object –
it is not required to define all values, only those that you want to change.

```
import { createTheme } from '@mantine/core';

// Changes only font-size of h1,
// other values will be taken from the DEFAULT_THEME
const theme = createTheme({
  headings: {
    sizes: {
      h1: {
        fontSize: '2rem',
      },
    },
  },
});
```

Expand code

### [Font smoothing](#font-smoothing)

Font smoothing variables control [-webkit-font-smoothing and moz-osx-font-smoothing](https://developer.mozilla.org/en-US/docs/Web/CSS/font-smooth)
CSS properties. These variables are used to make text look better on screens with high pixel density.

Font smoothing variables are controlled by `theme.fontSmoothing` [theme](/theming/theme-object/) property, it is `true` by default. If `theme.fontSmoothing` is `false`, both variables will be set to `unset`.

| Variable | Default value |
| --- | --- |
| `--mantine-webkit-font-smoothing` Controls -webkit-font-smoothing CSS property | antialiased |
| `--mantine-moz-font-smoothing` Controls -moz-osx-font-smoothing CSS property | grayscale |

If you need to override font smoothing values, the best way is to disable `theme.fontSmoothing` and set [global styles](/styles/global-styles/#add-global-styles-in-your-application)
on the body element:

```
import { createTheme } from '@mantine/core';

// Disable font smoothing in your theme
const theme = createTheme({
  fontSmoothing: false,
});
```

Expand code

```
// Add global styles to your project with desired font smoothing values
body {
  -webkit-font-smoothing: subpixel-antialiased;
  -moz-osx-font-smoothing: auto;
}
```

Expand code

## [Colors variables](#colors-variables)

Colors variables are controlled by `theme.colors` and `theme.primaryColor`. Each color
defined in `theme.colors` object is required to have 10 shades. Theme color can be
referenced by its name and shade index, for example, `--mantine-color-red-6`.

You can define new colors on the theme object or override existing colors:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  colors: {
    demo: [
      '#FF0000',
      '#FF3333',
      '#FF6666',
      '#FF9999',
      '#FFCCCC',
      '#FFEEEE',
      '#FFFAFA',
      '#FFF5F5',
      '#FFF0F0',
      '#FFEBEB',
    ],
  },
});
```

Expand code

The code above will define the following CSS variables:

| Variable | Default value |
| --- | --- |
| `--mantine-color-demo-0` | #FF0000 |
| `--mantine-color-demo-1` | #FF3333 |
| `--mantine-color-demo-2` | #FF6666 |
| `--mantine-color-demo-3` | #FF9999 |
| `--mantine-color-demo-4` | #FFCCCC |
| `--mantine-color-demo-5` | #FFEEEE |
| `--mantine-color-demo-6` | #FFFAFA |
| `--mantine-color-demo-7` | #FFF5F5 |
| `--mantine-color-demo-8` | #FFF0F0 |
| `--mantine-color-demo-9` | #FFEBEB |

### [Variant colors](#variant-colors)

Some Mantine components like [Button](/core/button/) or [Badge](/core/badge/) have `variant` prop
that in combination with `color` prop controls the component text, background and border colors.
For each variant and color, Mantine defines a set of CSS variables that control these colors.
For example, for the default `blue` color the following CSS variables are defined:

| Variable | Default value |
| --- | --- |
| Filled variant | |
| `--mantine-color-blue-filled` Background color of filled variant | var(--mantine-color-blue-6) |
| `--mantine-color-blue-filled-hover` Background color of filled variant on hover | var(--mantine-color-blue-7) |
| Light variant | |
| `--mantine-color-blue-light` Background color of light variant | rgba(34, 139, 230, 0.1) |
| `--mantine-color-blue-light-hover` Background color of light variant on hover | rgba(34, 139, 230, 0.12) |
| `--mantine-color-blue-light-color` Text color of light variant | var(--mantine-color-blue-6) |
| Outline variant | |
| `--mantine-color-blue-outline` Border color of outline variant | var(--mantine-color-blue-6) |
| `--mantine-color-blue-outline-hover` Border color of outline variant | rgba(34, 139, 230, 0.05) |

For example, if you use [Button](/core/button/) component the following way:

```
import { Button } from '@mantine/core';

function Demo() {
  return (
    <Button color="pink" variant="filled">
      Filled pink button
    </Button>
  );
}
```

Expand code

The component will have the following styles:

- Background color will be `var(--mantine-color-pink-filled)`
- Background color on hover will be `var(--mantine-color-pink-filled-hover)`
- Text color will be `var(--mantine-color-white)`
- Border color will be `transparent`

Note that the variables above are not static, they are generated based on the values of
`theme.colors` and `theme.primaryShade`. Additionally, their values are different for
dark and light color schemes.

Variant colors variables are used in all components that support `color` prop, for example,
[Button](/core/button/), [Badge](/core/badge/), [Avatar](/core/avatar/) and [Pagination](/core/pagination/).
Colors values that are used by these components are determined by `cssVariablesResolver` described below
and [variantColorResolver](/styles/variants-sizes/#variantcolorresolver).

### [Primary color variables](#primary-color-variables)

Primary color variables are defined by `theme.primaryColor` (which must be a key of `theme.colors`).
The following CSS variables are defined for the primary color:

| Variable | Default value |
| --- | --- |
| `--mantine-primary-color-{shade}` Shade is 0-9 to reference specific primary color shade | var(--mantine-color-{primaryColor}-{shade}) |
| `--mantine-primary-color-filled` Background color of filled variant | var(--mantine-color-{primaryColor}-filled) |
| `--mantine-primary-color-filled-hover` Background color of filled variant on hover | var(--mantine-color-{primaryColor}-filled-hover) |
| `--mantine-primary-color-light` Background color of light variant | var(--mantine-color-{primaryColor}-light) |
| `--mantine-primary-color-light-hover` Background color of light variant on hover | var(--mantine-color-{primaryColor}-light-hover) |
| `--mantine-primary-color-light-color` Text color of light variant | var(--mantine-color-{primaryColor}-light-color) |

You can reference primary color variables in CSS:

```
.demo {
  color: var(--mantine-primary-color-0);
  background-color: var(--mantine-primary-color-filled);
}
```

Expand code

### [Other color variables](#other-color-variables)

The following colors are used in various Mantine components. Note that default values
are provided for the light color scheme, dark color scheme values are different.

| Variable | Default value |
| --- | --- |
| `--mantine-color-white` Value of theme.white | #fff |
| `--mantine-color-black` Value of theme.black | #000 |
| `--mantine-color-text` Color used for text in the body element | var(--mantine-color-black) |
| `--mantine-color-body` Body background color | var(--mantine-color-white) |
| `--mantine-color-error` Color used for error messages and states | var(--mantine-color-red-6) |
| `--mantine-color-placeholder` Color used for input placeholders | var(--mantine-color-gray-5) |
| `--mantine-color-dimmed` Color used for dimmed text | var(--mantine-color-gray-6) |
| `--mantine-color-bright` Color used for bright text | var(--mantine-color-black) |
| `--mantine-color-anchor` Color used for links | var(--mantine-primary-color-6) |
| `--mantine-color-default` Background color of default variant | var(--mantine-color-white) |
| `--mantine-color-default-hover` Background color of default variant on hover | var(--mantine-color-gray-0) |
| `--mantine-color-default-color` Text color of default variant | var(--mantine-color-black) |
| `--mantine-color-default-border` Border color of default variant | var(--mantine-color-gray-4) |
| `--mantine-color-disabled` Background color of disabled elements | var(--mantine-color-gray-2) |
| `--mantine-color-disabled-color` Text color of disabled elements | var(--mantine-color-gray-5) |
| `--mantine-color-disabled-border` Border color of disabled elements | var(--mantine-color-gray-3) |

## [Spacing variables](#spacing-variables)

`theme.spacing` values are used in most Mantine components to control paddings, margins, and other
spacing-related properties. The following CSS variables are defined based on `theme.spacing`:

| Variable | Default value |
| --- | --- |
| `--mantine-spacing-xs` | 0.625rem (10px) |
| `--mantine-spacing-sm` | 0.75rem (12px) |
| `--mantine-spacing-md` | 1rem (16px) |
| `--mantine-spacing-lg` | 1.25rem (20px) |
| `--mantine-spacing-xl` | 2rem (32px) |

To define custom spacing values, use `theme.spacing` property:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  spacing: {
    xs: '0.5rem',
    sm: '0.75rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
});
```

Expand code

## [Border radius variables](#border-radius-variables)

Mantine components that support `radius` prop use border radius variables to control border radius.
The following CSS variables are defined based on `theme.radius`:

| Variable | Default value |
| --- | --- |
| `--mantine-radius-xs` | 0.125rem (2px) |
| `--mantine-radius-sm` | 0.25rem (4px) |
| `--mantine-radius-md` | 0.5rem (8px) |
| `--mantine-radius-lg` | 1rem (16px) |
| `--mantine-radius-xl` | 2rem (32px) |

Additionally, `--mantine-radius-default` variable is defined based on `theme.defaultRadius`
value. If `radius` prop on components is not set explicitly, `--mantine-radius-default` is used instead.

To define custom border radius values, use `theme.radius` and `theme.defaultRadius` properties:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  defaultRadius: 'sm',
  radius: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '2rem',
    xl: '3rem',
  },
});
```

Expand code

## [Shadow variables](#shadow-variables)

Shadow variables are used in all Mantine components that support `shadow` prop. The following CSS
variables are defined based on `theme.shadows`:

| Variable | Default value |
| --- | --- |
| `--mantine-shadow-xs` | 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1) |
| `--mantine-shadow-sm` | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 10px 15px -5px, rgba(0, 0, 0, 0.04) 0 7px 7px -5px |
| `--mantine-shadow-md` | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 20px 25px -5px, rgba(0, 0, 0, 0.04) 0 10px 10px -5px |
| `--mantine-shadow-lg` | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 28px 23px -7px, rgba(0, 0, 0, 0.04) 0 12px 12px -7px |
| `--mantine-shadow-xl` | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 36px 28px -7px, rgba(0, 0, 0, 0.04) 0 17px 17px -7px |

To define custom shadow values, use `theme.shadows` property:

```
import { createTheme } from '@mantine/core';

const theme = createTheme({
  shadows: {
    xs: '0 1px 2px rgba(0, 0, 0, 0.1)',
    sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
    md: '0 2px 4px rgba(0, 0, 0, 0.1)',
    lg: '0 4px 8px rgba(0, 0, 0, 0.1)',
    xl: '0 8px 16px rgba(0, 0, 0, 0.1)',
  },
});
```

Expand code

## [z-index variables](#z-index-variables)

z-index variables are defined in `@mantine/core/styles.css`. Unlike other variables,
z-index variables are not controlled by the theme and are not exposed in the theme object.

| Variable | Default value |
| --- | --- |
| `--mantine-z-index-app` | 100 |
| `--mantine-z-index-modal` | 200 |
| `--mantine-z-index-popover` | 300 |
| `--mantine-z-index-overlay` | 400 |
| `--mantine-z-index-max` | 9999 |

You can reference z-index variables in CSS:

```
/* Display content above the modal */
.my-content {
  z-index: calc(var(--mantine-z-index-modal) + 1);
}
```

Expand code

And in components by referencing CSS variable:

```
import { Modal } from '@mantine/core';

function Demo() {
  return (
    <Modal
      zIndex="var(--mantine-z-index-max)"
      opened
      onClose={() => {}}
    >
      Modal content
    </Modal>
  );
}
```

Expand code

## [CSS variables resolver](#css-variables-resolver)

`cssVariablesResolver` prop on [MantineProvider](/theming/mantine-provider/) allows you to
modify values of Mantine CSS variables or even add your own variables.
`cssVariablesResolver` is a function that accepts [theme](/theming/theme-object/) as a single
argument and returns an object with CSS variables divided into three groups:

- `variables` – variables that do not depend on color scheme
- `light` – variables for light color scheme only
- `dark` – variables for dark color scheme only

Example of adding new CSS variables based on `theme.other`:

```
import {
  createTheme,
  CSSVariablesResolver,
  MantineProvider,
} from '@mantine/core';

const themeOverride = createTheme({
  other: {
    deepOrangeLight: '#E17900',
    deepOrangeDark: '#FC8C0C',
    heroHeight: 400,
  },
});

const resolver: CSSVariablesResolver = (theme) => ({
  variables: {
    '--mantine-hero-height': theme.other.heroHeight,
  },
  light: {
    '--mantine-color-deep-orange': theme.other.deepOrangeLight,
  },
  dark: {
    '--mantine-color-deep-orange': theme.other.deepOrangeDark,
  },
});

function Demo() {
  return (
    <MantineProvider
      theme={themeOverride}
      cssVariablesResolver={resolver}
    >
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

Then you will be able to use `--mantine-hero-height` and `--mantine-color-deep-orange` variables
in any part of your application:

```
.hero {
  height: var(--mantine-hero-height);

  /* background color will automatically change based on color scheme */
  background-color: var(--mantine-color-deep-orange);
}
```

Expand code

[Global styles](/styles/global-styles/)[CSS variables list](/styles/css-variables-list/)