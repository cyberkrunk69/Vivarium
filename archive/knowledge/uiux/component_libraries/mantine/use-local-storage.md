# use-local-storage

Source: https://mantine.dev/hooks/use-local-storage/

---

# use-local-storage

Exposes localStorage value as react state, syncs state across opened tabs

Source

[View source code](https://github.com/mantinedev/mantine/blob/master/packages/@mantine/hooks/src/use-local-storage/use-local-storage.ts)

Docs

[Edit this page](https://github.com/mantinedev/mantine/blob/master/apps/mantine.dev/src/pages/hooks/use-local-storage.mdx)

Package

[@mantine/hooks](https://www.npmjs.com/package/@mantine/hooks)

## [Usage](#usage)

`use-local-storage` allows using value from the `localStorage` as react state.
The hook works the same way as `useState`, but also writes the value to the `localStorage`:

```
import { useLocalStorage } from '@mantine/hooks';

// The hook will read value from localStorage.getItem('color-scheme')
// If localStorage is not available or value at a given key does not exist
// 'dark' will be assigned to value variable
const [value, setValue] = useLocalStorage({
  key: 'color-scheme',
  defaultValue: 'dark',
});

// Value is set both to state and localStorage at 'color-scheme'
setValue('light');

// You can also use callback like in useState hook to set value
setValue((current) => (current === 'dark' ? 'light' : 'dark'));
```

Expand code

## [Example](#example)

Example of a color scheme toggle button that uses `use-local-storage` hook
to store current color scheme in the `localStorage`:

```
import { IconMoonStars, IconSun } from '@tabler/icons-react';
import { ActionIcon } from '@mantine/core';
import { useLocalStorage } from '@mantine/hooks';

function ColorSchemeToggle() {
  const [colorScheme, setColorScheme] = useLocalStorage<
    'light' | 'dark'
  >({
    key: 'color-scheme',
    defaultValue: 'light',
  });

  const toggleColorScheme = () =>
    setColorScheme((current) =>
      current === 'dark' ? 'light' : 'dark'
    );

  return (
    <ActionIcon onClick={toggleColorScheme}>
      {colorScheme === 'dark' ? <IconSun /> : <IconMoonStars />}
    </ActionIcon>
  );
}
```

Expand code

## [Remove value](#remove-value)

Use `removeValue` callback to clean `localStorage`/`sessionStorage`.
When value is removed it is reset to `defaultValue`:

```
import { useLocalStorage } from '@mantine/hooks';

const [value, setValue, removeValue] = useLocalStorage({
  key: 'color-scheme',
  defaultValue: 'light',
});
```

Expand code

## [Browser tabs synchronization](#browser-tabs-synchronization)

`use-local-storage` subscribes to [storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event).
When state changes in one tab, it automatically updates the value in all other opened browser tabs.
You can test this feature by opening 2 tabs with Mantine docs side by side and changing the color scheme
(button on the top right or `⌘ + J` on MacOS and `Ctrl + J` on Windows and Linux).

## [Serialize/deserialize JSON](#serializedeserialize-json)

By default, the hook will serialize/deserialize data with `JSON.stringify`/`JSON.parse`.
If you need to store data in local storage that cannot be serialized with `JSON.stringify`
– provide your own serialization handlers:

```
import { useLocalStorage } from '@mantine/hooks';

const [value, setValue] = useLocalStorage({
  key: 'color-scheme',
  serialize: (value) => {
    /* return value serialized to string */
  },
  deserialize: (localStorageValue) => {
    /* parse localStorage string value and return value */
  },
});
```

Expand code

## [Usage with superjson](#usage-with-superjson)

[superjson](https://github.com/blitz-js/superjson) is compatible with `JSON.stringify`/`JSON.parse` but works for `Date`, `Map`, `Set` and `BigInt`:

```
import superjson from 'superjson';
import { useLocalStorage } from '@mantine/hooks';

const defaultValue = { name: 'John', age: 25 };

const [value, setValue] = useLocalStorage({
  key: 'data',
  defaultValue,
  serialize: superjson.stringify,
  deserialize: (str) =>
    str === undefined ? defaultValue : superjson.parse(str),
});
```

Expand code

## [use-session-storage](#use-session-storage)

`use-session-storage` hook works the same way as `use-local-storage` hook but uses `sessionStorage` instead of `window.localStorage`:

```
import { useSessionStorage } from '@mantine/hooks';

const [value, setValue] = useSessionStorage({
  key: 'session-key',
  defaultValue: 'mantine',
});
```

Expand code

## [Set value type](#set-value-type)

You can specify value type same as in `useState` hook:

```
import { useLocalStorage } from '@mantine/hooks';

const [value, setValue] = useLocalStorage<'dark' | 'light'>({
  key: 'color-scheme',
  defaultValue: 'light',
});
```

Expand code

## [Read storage value](#read-storage-value)

To read value from storage without using hook, use `readLocalStorageValue`/`readSessionStorageValue` functions.
Functions accept the same arguments as `use-local-storage`/`use-session-storage` hooks:

```
import { readLocalStorageValue } from '@mantine/hooks';

const value = readLocalStorageValue({ key: 'color-scheme' });
```

Expand code

## [Definition](#definition)

```
interface UseStorageOptions<T> {
  /** Local storage key */
  key: string;

  /** Default value that will be set if value is not found in local storage */
  defaultValue?: T;

  /** If set to true, value will be updated in useEffect after mount. Default value is true. */
  getInitialValueInEffect?: boolean;

  /** Determines whether the value must be synced between browser tabs, `true` by default */
  sync?: boolean;

  /** Function to serialize value into a string to be saved in local storage */
  serialize?: (value: T) => string;

  /** Function to deserialize string value from local storage to value */
  deserialize?: (value: string) => T;
}

type UseStorageReturnValue<T> = [
  T, // current value
  (val: T | ((prevState: T) => T)) => void, // callback to set value in storage
  () => void, // callback to remove value from storage
];

function useLocalStorage<T = string>(
  options: UseStorageOptions<T>,
): UseStorageReturnValue<T>;
```

Expand code

## [Exported types](#exported-types)

`UseStorageOptions` and `UseStorageReturnValue` types are exported from `@mantine/hooks` package,
you can import them in your application:

```
import type { UseStorageOptions, UseStorageReturnValue } from '@mantine/hooks';
```

Expand code

[use-list-state](/hooks/use-list-state/)[use-map](/hooks/use-map/)