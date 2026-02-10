# Usage with Sass

Source: https://mantine.dev/styles/sass/

---

# Usage with Sass

This guide will explain how to use [Sass](https://sass-lang.com/) in combination with
[postcss-preset-mantine](/styles/postcss-preset/). Note that examples on mantine.dev website
use only `postcss-preset-mantine` – you will need to modify them to use with Sass.

## [Sass modules](#sass-modules)

You can use Sass modules the same way as [CSS modules](/styles/css-modules/):

- Use `*.module.scss`/`*.module.sass` extension for your files to enable modules
- Use `*.scss`/`*.sass` extension for global styles

## [Usage with Vite](#usage-with-vite)

Install `sass`:

yarn

npm

```
yarn add --dev sass-embedded
```

Expand code

```
npm install --save-dev sass-embedded
```

Expand code

Add mantine resources in your `vite.config.js` file:

```
import path from 'node:path';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler',
        additionalData: `@use "${path.join(process.cwd(), 'src/_mantine').replace(/\\/g, '/')}" as mantine;`,
      },
    },
  },
});
```

Expand code

Create `src/_mantine.scss` file:

```
@use 'sass:math';

// Define variables for your breakpoints,
// values must be the same as in your theme
$mantine-breakpoint-xs: '36em';
$mantine-breakpoint-sm: '48em';
$mantine-breakpoint-md: '62em';
$mantine-breakpoint-lg: '75em';
$mantine-breakpoint-xl: '88em';

@function rem($value) {
  @return #{math.div(math.div($value, $value * 0 + 1), 16)}rem;
}

@mixin light {
  [data-mantine-color-scheme='light'] & {
    @content;
  }
}

@mixin dark {
  [data-mantine-color-scheme='dark'] & {
    @content;
  }
}

@mixin hover {
  @media (hover: hover) {
    &:hover {
      @content;
    }
  }

  @media (hover: none) {
    &:active {
      @content;
    }
  }
}

@mixin smaller-than($breakpoint) {
  @media (max-width: $breakpoint) {
    @content;
  }
}

@mixin larger-than($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

// Add direction mixins if you need rtl support
@mixin rtl {
  [dir='rtl'] & {
    @content;
  }
}

@mixin ltr {
  [dir='ltr'] & {
    @content;
  }
}
```

Expand code

All done! you can now use breakpoint variables, `rem` function, `hover`, `light`/`dark` mixins:

```
// example.module.scss
.title {
  // light-dark function is handled by PostCSS
  color: light-dark(
    var(--mantine-color-black),
    var(--mantine-color-white)
  );
  font-size: mantine.rem(100px);
  font-weight: 900;
  letter-spacing: mantine.rem(-2px);

  @include mantine.light {
    background-color: red;
  }

  @include mantine.dark {
    background-color: blue;
  }

  @include mantine.smaller-than(mantine.$mantine-breakpoint-md) {
    font-size: mantine.rem(50px);
  }
}
```

Expand code

## [Usage with Next.js](#usage-with-nextjs)

Install `sass`:

yarn

npm

```
yarn add --dev sass-embedded
```

Expand code

```
npm install --save-dev sass-embedded
```

Expand code

Add mantine resources in your `next.config.mjs` file:

```
import path from 'node:path';

export default {
  // ...other config
  sassOptions: {
    implementation: 'sass-embedded',
    additionalData: `@use "${path.join(process.cwd(), '_mantine').replace(/\\/g, '/')}" as mantine;`,
  },
};
```

Expand code

Create `_mantine.scss` file in the root folder of your project:

```
@use 'sass:math';

// Define variables for your breakpoints,
// values must be the same as in your theme
$mantine-breakpoint-xs: '36em';
$mantine-breakpoint-sm: '48em';
$mantine-breakpoint-md: '62em';
$mantine-breakpoint-lg: '75em';
$mantine-breakpoint-xl: '88em';

@function rem($value) {
  @return #{math.div(math.div($value, $value * 0 + 1), 16)}rem;
}

@mixin light {
  [data-mantine-color-scheme='light'] & {
    @content;
  }
}

@mixin dark {
  [data-mantine-color-scheme='dark'] & {
    @content;
  }
}

@mixin hover {
  @media (hover: hover) {
    &:hover {
      @content;
    }
  }

  @media (hover: none) {
    &:active {
      @content;
    }
  }
}

@mixin smaller-than($breakpoint) {
  @media (max-width: $breakpoint) {
    @content;
  }
}

@mixin larger-than($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

// Add direction mixins if you need rtl support
@mixin rtl {
  [dir='rtl'] & {
    @content;
  }
}

@mixin ltr {
  [dir='ltr'] & {
    @content;
  }
}
```

Expand code

All done! you can now use breakpoint variables, `rem` function, `hover`, `light`/`dark` mixins:

```
// example.module.scss
.title {
  // light-dark function is handled by PostCSS
  color: light-dark(
    var(--mantine-color-black),
    var(--mantine-color-white)
  );
  font-size: mantine.rem(100px);
  font-weight: 900;
  letter-spacing: mantine.rem(-2px);

  @include mantine.light {
    background-color: red;
  }

  @include mantine.dark {
    background-color: blue;
  }

  @include mantine.smaller-than(mantine.$mantine-breakpoint-md) {
    font-size: mantine.rem(50px);
  }
}
```

Expand code

[Usage with Emotion](/styles/emotion/)[Vanilla extract](/styles/vanilla-extract/)