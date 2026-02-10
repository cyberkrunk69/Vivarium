# Style props

Source: https://mantine.dev/styles/style-props/

---

# Style props

With style props, you can add inline styles to any Mantine component.
Style props add styles to the **root** element, if you need to style nested elements,
use [Styles API](/styles/styles-api/) instead.

```
import { Box } from '@mantine/core';

function Demo() {
  return (
    <Box mx="auto" maw={400} c="blue.6" bg="#fff">
      Your component
    </Box>
  );
}
```

Expand code

## [Supported props](#supported-props)

All Mantine components that have root element support the following style props:

| Prop | CSS Property | Theme key |
| --- | --- | --- |
| `m` | `margin` | `theme.spacing` |
| `mt` | `marginTop` | `theme.spacing` |
| `mb` | `marginBottom` | `theme.spacing` |
| `ml` | `marginLeft` | `theme.spacing` |
| `mr` | `marginRight` | `theme.spacing` |
| `ms` | `marginInlineStart` | `theme.spacing` |
| `me` | `marginInlineEnd` | `theme.spacing` |
| `mx` | `marginInline` | `theme.spacing` |
| `my` | `marginBlock` | `theme.spacing` |
| `p` | `padding` | `theme.spacing` |
| `pt` | `paddingTop` | `theme.spacing` |
| `pb` | `paddingBottom` | `theme.spacing` |
| `pl` | `paddingLeft` | `theme.spacing` |
| `pr` | `paddingRight` | `theme.spacing` |
| `ps` | `paddingInlineStart` | `theme.spacing` |
| `pe` | `paddingInlineEnd` | `theme.spacing` |
| `px` | `paddingInline` | `theme.spacing` |
| `py` | `paddingBlock` | `theme.spacing` |
| `bd` | `border` | – |
| `bdrs` | `borderRadius` | – |
| `bg` | `background` | `theme.colors` |
| `c` | `color` | – |
| `opacity` | `opacity` | – |
| `ff` | `fontFamily` | – |
| `fz` | `fontSize` | `theme.fontSizes` |
| `fw` | `fontWeight` | – |
| `lts` | `letterSpacing` | – |
| `ta` | `textAlign` | – |
| `lh` | `lineHeight` | `theme.lineHeights` |
| `fs` | `fontStyle` | – |
| `tt` | `textTransform` | – |
| `td` | `textDecoration` | – |
| `w` | `width` | `theme.spacing` |
| `miw` | `minWidth` | `theme.spacing` |
| `maw` | `maxWidth` | `theme.spacing` |
| `h` | `height` | `theme.spacing` |
| `mih` | `minHeight` | `theme.spacing` |
| `mah` | `maxHeight` | `theme.spacing` |
| `bgsz` | `backgroundSize` | – |
| `bgp` | `backgroundPosition` | – |
| `bgr` | `backgroundRepeat` | – |
| `bga` | `backgroundAttachment` | – |
| `pos` | `position` | – |
| `top` | `top` | – |
| `left` | `left` | – |
| `bottom` | `bottom` | – |
| `right` | `right` | – |
| `inset` | `inset` | – |
| `display` | `display` | – |
| `flex` | `flex` | – |

## [Theme values](#theme-values)

Some style props can reference values from theme, for example `mt` will use `theme.spacing` value
if you set `xs`, `sm`, `md`, `lg`, `xl`:

```
import { Box } from '@mantine/core';

function Demo() {
  return (
    <>
      {/* margin-top: theme.spacing.xs */}
      <Box mt="xs" />

      {/* margin-top: theme.spacing.md * -1 */}
      <Box mt="-md" />

      {/* margin-top: auto */}
      <Box mt="auto" />

      {/* margin-top: 1rem */}
      <Box mt={16} />

      {/* margin-top: 5rem */}
      <Box mt="5rem" />
    </>
  );
}
```

Expand code

In `c`, `bd` and `bg` props you can reference colors from `theme.colors`:

```
import { Box } from '@mantine/core';

function Demo() {
  return (
    <>
      {/* color: theme.colors.blue[theme.primaryShade] */}
      <Box c="blue" />

      {/* background: theme.colors.orange[1] */}
      <Box bg="orange.1" />

      {/* border: 1px solid theme.colors.red[6] */}
      <Box bd="1px solid red.6" />

      {/* color: if colorScheme is dark `var(--mantine-color-dark-2)`,
      if color scheme is light `var(--mantine-color-gray-6)` */}
      <Box c="dimmed" />

      {/* color: if colorScheme is dark `var(--mantine-color-white)`,
      if color scheme is light `var(--mantine-color-black)` */}
      <Box c="bright" />

      {/* background: #EDFEFF */}
      <Box bg="#EDFEFF" />

      {/* background: rgba(0, 34, 45, 0.6) */}
      <Box bg="rgba(0, 34, 45, 0.6)" />
    </>
  );
}
```

Expand code

## [Responsive styles](#responsive-styles)

You can use object syntax to add responsive styles with style props.
Note that responsive style props are [less performant](/styles/styles-performance/) than regular style props,
it is not recommended to use them in large lists of elements.

Box with responsive style props

Demo.tsx

```
import { Box } from '@mantine/core';

function Demo() {
  return (
    <Box
      w={{ base: 200, sm: 400, lg: 500 }}
      py={{ base: 'xs', sm: 'md', lg: 'xl' }}
      bg={{ base: 'blue.7', sm: 'red.7', lg: 'green.7' }}
      c="#fff"
      ta="center"
      mx="auto"
    >
      Box with responsive style props
    </Box>
  );
}
```

Expand code

Responsive values are calculated the following way:

- `base` value is used when none of breakpoint values are applied
- `xs`, `sm`, `md`, `lg`, `xl` values are used when the viewport width is larger that the value of corresponding breakpoint specified in [theme.breakpoints](/styles/responsive/)

```
import { Box } from '@mantine/core';

function Demo() {
  return <Box w={{ base: 320, sm: 480, lg: 640 }} />;
}
```

Expand code

In this case the element will have the following styles:

```
/* Base styles added to element and then get overwritten with responsive values */
.element {
  width: 20rem;
}

/* 48em is theme.breakpoints.sm by default */
@media (min-width: 48em) {
  .element {
    width: 30rem;
  }
}

/* 75em is theme.breakpoints.lg by default */
@media (min-width: 75em) {
  .element {
    width: 40rem;
  }
}
```

Expand code

[Variants and sizes](/styles/variants-sizes/)[Color functions](/styles/color-functions/)