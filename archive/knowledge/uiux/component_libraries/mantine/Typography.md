# Typography

Source: https://mantine.dev/theming/typography/

---

# Typography

Styles provider for html content

Source

[View source code](https://github.com/mantinedev/mantine/blob/master/packages/@mantine/core/src/components/Typography/Typography.tsx)

Docs

[Edit this page](https://github.com/mantinedev/mantine/blob/master/apps/mantine.dev/src/pages/core/typography.mdx)

Package

[@mantine/core](https://www.npmjs.com/package/@mantine/core)

# Typography

## [Change fonts](#change-fonts)

You can change fonts and other text styles for headings, code and all other components with the following theme properties:

- `theme.fontFamily` – controls font-family in all components except [Title](/core/title/), [Code](/core/code/) and [Kbd](/core/kbd/)
- `theme.fontFamilyMonospace` – controls font-family of components that require monospace font: [Code](/core/code/), [Kbd](/core/kbd/) and [CodeHighlight](/x/code-highlight/)
- `theme.headings.fontFamily` – controls font-family of h1-h6 tags in [Title](/core/title/) and [Typography](/core/typography/) components, fallbacks to `theme.fontFamily` if not defined

### Outfit or sans-serif title

Verdana button`Monaco, Courier Code`

Demo.tsx

```
import { Button, Code, Title, MantineProvider, createTheme } from '@mantine/core';

const theme = createTheme({
  fontFamily: 'Verdana, sans-serif',
  fontFamilyMonospace: 'Monaco, Courier, monospace',
  headings: { fontFamily: 'Outfit, sans-serif' },
});

function Demo() {
  return (
    <MantineProvider theme={theme}>
      <Title order={3}>Outfit or sans-serif title</Title>
      <Button>Verdana button</Button>
      <Code>Monaco, Courier Code</Code>
    </MantineProvider>
  );
}
```

Expand code

## [System fonts](#system-fonts)

By default, Mantine uses system fonts. It means that different devices will display components based on available font,
for example, macOS and iOS users will see [San Francisco font](https://developer.apple.com/fonts/),
Windows users will see [Segoe UI font](https://docs.microsoft.com/en-us/typography/font-list/segoe-ui),
Android users will see [Roboto font](https://fonts.google.com/specimen/Roboto) and so on.
This approach provides a familiar experience to the users and allows avoiding common problems
related to custom fonts loading (layout shift, invisible text, etc.), if you do not have strict
requirements, it is recommended to use system fonts for better performance.

Default values for theme properties:

- Default value for `theme.fontFamily` and `theme.headings.fontFamily` is `-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji`
- Default value for `theme.fontFamilyMonospace` is `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace`

## [Font sizes](#font-sizes)

Paras is an orange, insectoid Pokémon that resembles the nymph stage of a cicada. Its ovoid body is segmented, and it has three pairs of legs. The foremost pair of legs is the largest and has sharp claws at the tips. There are five specks on its forehead and three teeth on either side of its mouth. It has circular eyes with large pseudopupils.

Font size

xs

sm

md

lg

xl

Line height

xs

sm

md

lg

xl

Demo.tsx

```
import { Text } from '@mantine/core';

function Demo() {
  return (
    <Text fz="md" lh="md">
      Paras is an orange, insectoid Pokémon that resembles the nymph stage of a cicada. Its ovoid
      body is segmented, and it has three pairs of legs. The foremost pair of legs is the largest
      and has sharp claws at the tips. There are five specks on its forehead and three teeth on
      either side of its mouth. It has circular eyes with large pseudopupils.
    </Text>
  );
}
```

Expand code

`theme.fontSizes` property defines font-size values for all Mantine components:

```
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  fontSizes: {
    xs: 10,
    sm: 11,
    md: 14,
    lg: 16,
    xl: 20,
  },
});

function Demo() {
  return (
    <MantineProvider theme={theme}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

Default `theme.fontSizes` values:

| Key | Value | Value in px |
| --- | --- | --- |
| xs | 0.75rem | 12px |
| sm | 0.875rem | 14px |
| md | 1rem | 16px |
| lg | 1.125rem | 18px |
| xl | 1.25rem | 20px |

## [Line heights](#line-heights)

`theme.lineHeights` property defines line-height values for [Text](/core/text/) component,
most other components use `theme.lineHeights.md` by default:

```
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  lineHeights: {
    xs: '1.4',
    sm: '1.45',
    md: '1.55',
    lg: '1.6',
    xl: '1.65',
  },
});

function Demo() {
  return (
    <MantineProvider theme={theme}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

Default `theme.lineHeights` values:

| Key | Value |
| --- | --- |
| xs | 1.4 |
| sm | 1.45 |
| md | 1.55 |
| lg | 1.6 |
| xl | 1.65 |

## [h1-h6 styles](#h1-h6-styles)

To customize headings styles in [Title](/core/title/) and [Typography](/core/typography/) components
set `theme.headings`:

```
import { createTheme, MantineProvider, rem } from '@mantine/core';

const theme = createTheme({
  headings: {
    // properties for all headings
    fontWeight: '400',
    fontFamily: 'Roboto',

    // properties for individual headings, all of them are optional
    sizes: {
      h1: {
        fontWeight: '100',
        fontSize: 36,
        lineHeight: '1.4',
      },
      h2: { fontSize: 30, lineHeight: '1.5' },
      // ...up to h6
      h6: { fontWeight: '900' },
    },
  },
});

function Demo() {
  return (
    <MantineProvider theme={theme}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

With `theme.headings` you can customize font-size, font-weight and line-height per heading level.
If you need more control over styles, use [:is selector](https://developer.mozilla.org/en-US/docs/Web/CSS/:is)
with [Styles API](/styles/styles-api/) to target specific heading level:

# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

Demo.tsxDemo.module.css

```
import { Title, MantineProvider } from '@mantine/core';
import classes from './Demo.module.css';

const theme = createTheme({
  components: {
    Title: Title.extend({
      classNames: {
        root: classes.heading,
      },
    }),
  },
});

function Demo() {
  return (
    <MantineThemeProvider theme={theme}>
      <Title order={1}>Heading 1</Title>
      <Title order={2}>Heading 2</Title>
      <Title order={3}>Heading 3</Title>
      <Title order={4}>Heading 4</Title>
      <Title order={5}>Heading 5</Title>
      <Title order={6}>Heading 6</Title>
    </MantineThemeProvider>
  );
}
```

Expand code

[Color schemes](/theming/color-schemes/)[Default props](/theming/default-props/)