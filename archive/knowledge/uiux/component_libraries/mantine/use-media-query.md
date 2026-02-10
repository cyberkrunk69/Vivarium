# use-media-query

Source: https://mantine.dev/hooks/use-media-query/

---

# use-media-query

Subscribes to media queries with window.matchMedia

Source

[View source code](https://github.com/mantinedev/mantine/blob/master/packages/@mantine/hooks/src/use-media-query/use-media-query.ts)

Docs

[Edit this page](https://github.com/mantinedev/mantine/blob/master/apps/mantine.dev/src/pages/hooks/use-media-query.mdx)

Package

[@mantine/hooks](https://www.npmjs.com/package/@mantine/hooks)

## [Usage](#usage)

`use-media-query` subscribes to media queries.
It receives a media query as an argument and returns `true` if the given media query matches the current state.
The hook relies on `window.matchMedia()` [API](https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia)
and will return `false` if the API is not available, unless an initial value is provided in the second argument.

Resize browser window to trigger `window.matchMedia` event:

Breakpoint does not match

Demo.tsx

```
import { Badge } from '@mantine/core';
import { useMediaQuery } from '@mantine/hooks';

function Demo() {
  const matches = useMediaQuery('(min-width: 56.25em)');

  return (
    <Badge color={matches ? 'teal' : 'red'} variant="filled">
      Breakpoint {matches ? 'matches' : 'does not match'}
    </Badge>
  );
}
```

Expand code

## [Server Side Rendering](#server-side-rendering)

During server side rendering the hook will always return `false` as `window.matchMedia` api is not available,
if that is not a desired behavior, you can override the initial value:

```
import { useMediaQuery } from '@mantine/hooks';

function Demo() {
  // Set initial value in second argument and getInitialValueInEffect option to false
  const matches = useMediaQuery('(max-width: 40em)', true, {
    getInitialValueInEffect: false,
  });
}
```

Expand code

## [Definition](#definition)

```
interface UseMediaQueryOptions {
  getInitialValueInEffect: boolean;
}

function useMediaQuery(
  query: string,
  initialValue?: boolean,
  options?: UseMediaQueryOptions,
): boolean;
```

Expand code

## [Exported types](#exported-types)

`UseMediaQueryOptions` type is exported from `@mantine/hooks` package,
you can import it in your application:

```
import type { UseMediaQueryOptions } from '@mantine/hooks';
```

Expand code

[use-long-press](/hooks/use-long-press/)[use-mouse](/hooks/use-mouse/)