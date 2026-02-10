# MantineProvider

Source: https://mantine.dev/theming/mantine-provider/

---

# MantineProvider

`MantineProvider` provides a [theme object](/theming/theme-object/) context value, manages color scheme
changes and injects [CSS variables](/styles/css-variables/). It must be rendered at the root of your
application and should be used only once.

## [Usage](#usage)

```
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  /** Your theme override here */
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

## [MantineProvider props](#mantineprovider-props)

`MantineProvider` supports the following props:

```
interface MantineProviderProps {
  /** Theme override object */
  theme?: MantineThemeOverride;

  /** Used to retrieve/set color scheme value in external storage, by default uses `window.localStorage` */
  colorSchemeManager?: MantineColorSchemeManager;

  /** Default color scheme value used when `colorSchemeManager` cannot retrieve value from external storage, `light` by default */
  defaultColorScheme?: MantineColorScheme;

  /** Forces color scheme value, if set, MantineProvider ignores `colorSchemeManager` and `defaultColorScheme` */
  forceColorScheme?: 'light' | 'dark';

  /** CSS selector to which CSS variables should be added, by default variables are applied to `:root` and `:host` */
  cssVariablesSelector?: string;

  /** Determines whether theme CSS variables should be added to given `cssVariablesSelector`, `true` by default */
  withCssVariables?: boolean;

  /** Determines whether CSS variables should be deduplicated: if CSS variable has the same value as in default theme, it is not added in the runtime. `true` by default. */
  deduplicateCssVariables?: boolean;

  /** Function to resolve root element to set `data-mantine-color-scheme` attribute, must return undefined on server, `() => document.documentElement` by default */
  getRootElement?: () => HTMLElement | undefined;

  /** A prefix for components static classes (for example {selector}-Text-root), `mantine` by default */
  classNamesPrefix?: string;

  /** Function to generate nonce attribute added to all generated `<style />` tags */
  getStyleNonce?: () => string;

  /** Function to generate CSS variables based on theme object */
  cssVariablesResolver?: CSSVariablesResolver;

  /** Determines whether components should have static classes, for example, `mantine-Button-root`. `true` by default */
  withStaticClasses?: boolean;

  /** Determines whether global classes should be added with `<style />` tag. Global classes are required for `hiddenFrom`/`visibleFrom` and `lightHidden`/`darkHidden` props to work. `true` by default. */
  withGlobalClasses?: boolean;

  /** Environment at which the provider is used, `'test'` environment disables all transitions and portals */
  env?: 'default' | 'test';

  /** Your application */
  children?: React.ReactNode;
}
```

Expand code

### [theme](#theme)

Pass [theme object](/theming/theme-object/) override to `theme` prop. It will be merged with the default
theme and used in all components.

```
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  fontFamily: 'Open Sans, sans-serif',
  primaryColor: 'cyan',
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

### [colorSchemeManager](#colorschememanager)

`colorSchemeManager` is used to retrieve and set color scheme value in external storage. By default,
`MantineProvider` uses `window.localStorage` to store color scheme value, but you can pass your own
implementation to `colorSchemeManager` prop. You can learn more about color scheme management in the
[color schemes guide](/theming/color-schemes/).

```
import {
  localStorageColorSchemeManager,
  MantineProvider,
} from '@mantine/core';

const colorSchemeManager = localStorageColorSchemeManager({
  key: 'my-app-color-scheme',
});

function Demo() {
  return (
    <MantineProvider colorSchemeManager={colorSchemeManager}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [defaultColorScheme](#defaultcolorscheme)

`defaultColorScheme` value is used when `colorSchemeManager` cannot retrieve the value from external
storage, for example during server side rendering or when the user hasn't selected a preferred color scheme.
Possible values are `light`, `dark` and `auto`. By default, color scheme value is `light`.
You can learn more about color scheme management in the [color schemes guide](/theming/color-schemes/).

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider defaultColorScheme="dark">
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [cssVariablesSelector](#cssvariablesselector)

`cssVariablesSelector` is a CSS selector to which [CSS variables](/styles/css-variables/) should be added.
By default, variables are applied to `:root` and `:host`. `MantineProvider` generates CSS variables based
on given [theme override](/theming/theme-object/) and `cssVariablesResolver`, then these variables are
rendered into `<style />` tag next to your application.
You can learn more about Mantine CSS variables in the [CSS variables guide](/styles/css-variables/).

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider cssVariablesSelector="html">
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [withCssVariables](#withcssvariables)

`withCssVariables` determines whether theme CSS variables should be added to given `cssVariablesSelector`.
By default, it is set to `true`, you should not change it unless you want to manage CSS variables
via `.css` file (Note that in this case you will need to generate all theme tokens
that are not a part of the default theme on your side).

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider withCssVariables={false}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [deduplicateCssVariables](#deduplicatecssvariables)

`deduplicateCssVariables` determines whether CSS variables should be deduplicated: if CSS variable has the same value as in default theme, it is not added in the runtime.
By default, it is set to `true`. If set to `false`, all Mantine CSS variables will be added in `<style />` tag
even if they have the same value as in the default theme.

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider deduplicateCssVariables={false}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [getRootElement](#getrootelement)

`getRootElement` is a function that returns the root application (usually `html`) element to set `data-mantine-color-scheme` attribute.
Default value is `() => document.documentElement` which means that `data-mantine-color-scheme`
attribute will be added to `<html />` tag. You can learn more about color scheme management in the
[color schemes guide](/theming/color-schemes/).

```
import { MantineProvider } from '@mantine/core';

const getRootElement = () =>
  typeof window === 'undefined' ? undefined : document.body;

function Demo() {
  return (
    <MantineProvider getRootElement={getRootElement}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [classNamesPrefix](#classnamesprefix)

`classNamesPrefix` is a prefix for components static classes (for example `{selector}-Text-root`).
Default value is `mantine` – all components will have `mantine-` prefix in their **static classes**.

```
import { MantineProvider, Text } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider>
      <Text>Just some text</Text>
    </MantineProvider>
  );
}
```

Expand code

In this case (default `classNamesPrefix`), [Text](/core/text/) component will have the following classes:

- `mantine-focus-auto` – global utility class
- `m-3nrA4eL` – component class, usually a random string, with this class library styles are applied
- `mantine-Text-root` – component static class, part of [Styles API](/styles/styles-api/)

With `classNamesPrefix` you can change only **static class**:

```
import { MantineProvider, Text } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider classNamesPrefix="app">
      <Text>Just some text</Text>
    </MantineProvider>
  );
}
```

Expand code

Now [Text](/core/text/) component will have the following classes:

- `mantine-focus-auto` – `classNamesPrefix` does not impact global utility classes – it is static and **cannot be changed**
- `m-3nrA4eL` – `classNamesPrefix` does not impact library class – it is static and **cannot be changed**
- `app-Text-root` – component static class has `classNamesPrefix` instead of `mantine`

### [withStaticClasses](#withstaticclasses)

`withStaticClasses` determines whether components should have static classes, for example, `mantine-Button-root`.
By default, static classes are enabled, to disable them set `withStaticClasses` to `false`:

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider withStaticClasses={false}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [withGlobalClasses](#withglobalclasses)

`withGlobalClasses` determines whether global classes should be added with `<style />` tag.
Global classes are required for `hiddenFrom`/`visibleFrom` and `lightHidden`/`darkHidden` props to work.
By default, global classes are enabled, to disable them set `withGlobalClasses` to `false`. Note that
disabling global classes may break styles of some components.

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider withGlobalClasses={false}>
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

### [getStyleNonce](#getstylenonce)

`getStyleNonce` is a function to generate [nonce](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) attribute added to dynamic generated `<style />` tags.

### [cssVariablesResolver](#cssvariablesresolver)

`cssVariablesResolver` is a function to generate CSS variables styles based on the [theme object](/theming/theme-object/).
You can learn more about Mantine CSS variables in the [CSS variables guide](/styles/css-variables/#css-variables-resolver).

### [env](#env)

`env` prop can be used in test environment to disable some features that
might impact tests and/or make it harder to test components:

- transitions that mount/unmount child component with delay
- portals that render child component in a different part of the DOM

To enable test environment, set `env` to `test`:

```
import { MantineProvider } from '@mantine/core';

function Demo() {
  return (
    <MantineProvider env="test">
      {/* Your app here */}
    </MantineProvider>
  );
}
```

Expand code

Note that `env="test"` is indented to be used in test environment only with [Jest](/guides/jest/) or [Vitest](/guides/vitest/), do not use it in
the development or production environments. It is also not recommended to be used with
end-to-end testing tools like [Cypress](/guides/cypress/) or [Playwright](/guides/playwright/).

[Migration guide Tiptap 2 → Tiptap 3](/guides/tiptap-3-migration/)[Theme object](/theming/theme-object/)