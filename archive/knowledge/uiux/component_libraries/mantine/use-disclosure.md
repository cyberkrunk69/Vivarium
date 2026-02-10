# use-disclosure

Source: https://mantine.dev/hooks/use-disclosure/

---

# use-disclosure

Manages boolean state, provides open, close and toggle handlers, usually used with modals, drawers and popovers

Source

[View source code](https://github.com/mantinedev/mantine/blob/master/packages/@mantine/hooks/src/use-disclosure/use-disclosure.ts)

Docs

[Edit this page](https://github.com/mantinedev/mantine/blob/master/apps/mantine.dev/src/pages/hooks/use-disclosure.mdx)

Package

[@mantine/hooks](https://www.npmjs.com/package/@mantine/hooks)

## [Usage](#usage)

`use-disclosure` hook manages boolean state. It provides `open`, `close` and `toggle` handlers
and accepts optional `onOpen` and `onClose` callbacks. You can use it to manage controlled modals,
popovers and other similar components:

```
import { useDisclosure } from '@mantine/hooks';

function Demo() {
  const [opened, handlers] = useDisclosure(false);

  // Sets opened to true
  handlers.open();

  // Sets opened to false
  handlers.close();

  // Sets opened to true if it was false and vice versa
  handlers.toggle();
}
```

Expand code

## [Callbacks](#callbacks)

The `onOpen` and `onClose` callbacks execute when the opened state changes:

```
import { useDisclosure } from '@mantine/hooks';

function Demo() {
  const [opened, handlers] = useDisclosure(false, {
    onOpen: () => console.log('Opened'),
    onClose: () => console.log('Closed'),
  });

  // Calls `onOpen` callback and sets opened to true
  handlers.open();

  // Does nothing, opened is already true
  handlers.open();

  // Calls `onClose` callback and sets opened to false
  handlers.close();

  // Does nothing, opened is already false
  handlers.close();

  // Calls `onOpen` or `onClose` depending on the current state
  handlers.toggle();
}
```

Expand code

## [Definition](#definition)

```
interface UseDisclosureOptions {
  onOpen?: () => void;
  onClose?: () => void;
}

interface UseDisclosureHandlers {
  open: () => void;
  close: () => void;
  toggle: () => void;
}

type UseDisclosureReturnValue = [boolean, UseDisclosureHandlers];

function useDisclosure(
  initialState?: boolean,
  options?: UseDisclosureOptions,
): UseDisclosureReturnValue
```

Expand code

## [Exported types](#exported-types)

`UseDisclosureOptions`, `UseDisclosureHandlers` and `UseDisclosureReturnValue` types are exported from `@mantine/hooks` package,
you can import them in your application:

```
import type { UseDisclosureOptions, UseDisclosureHandlers, UseDisclosureReturnValue } from '@mantine/hooks';
```

Expand code

[use-debounced-value](/hooks/use-debounced-value/)[use-id](/hooks/use-id/)