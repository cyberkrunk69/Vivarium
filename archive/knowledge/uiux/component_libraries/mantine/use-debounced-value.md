# use-debounced-value

Source: https://mantine.dev/hooks/use-debounced-value/

---

# use-debounced-value

Debounces value changes

Source

[View source code](https://github.com/mantinedev/mantine/blob/master/packages/@mantine/hooks/src/use-debounced-value/use-debounced-value.ts)

Docs

[Edit this page](https://github.com/mantinedev/mantine/blob/master/apps/mantine.dev/src/pages/hooks/use-debounced-value.mdx)

Package

[@mantine/hooks](https://www.npmjs.com/package/@mantine/hooks)

## [Usage](#usage)

`use-debounced-value` hook debounces value changes.
This can be useful in case you want to perform a heavy operation based on react state,
for example, send search request. Unlike [use-debounced-state](/hooks/use-debounced-state/) it
is designed to work with controlled components.

Enter value to see debounce effect

Value: [empty string]

Debounced value: [empty string]

Demo.tsx

```
import { useState } from 'react';
import { useDebouncedValue } from '@mantine/hooks';
import { TextInput, Text } from '@mantine/core';

function Demo() {
  const [value, setValue] = useState('');
  const [debounced] = useDebouncedValue(value, 200);

  return (
    <>
      <TextInput
        label="Enter value to see debounce"
        value={value}
        onChange={(event) => setValue(event.currentTarget.value)}
      />

      <Text>Value: {value}</Text>
      <Text>Debounced value: {debounced}</Text>
    </>
  );
}
```

Expand code

## [Differences from use-debounced-state](#differences-from-use-debounced-state)

- You have direct access to the non-debounced value.
- It is used for controlled inputs (`value` prop instead of `defaultValue`), for example renders on every state change like a character typed in an input.
- It works with props or other state providers, and it does not force use of `useState`.

## [Leading update](#leading-update)

You can immediately update value with first call with `{ leading: true }` options:

Enter value to see debounce effect

Value: [empty string]

Debounced value: [empty string]

Demo.tsx

```
import { useState } from 'react';
import { useDebouncedValue } from '@mantine/hooks';
import { TextInput, Text } from '@mantine/core';

function Demo() {
  const [value, setValue] = useState('');
  const [debounced] = useDebouncedValue(value, 200, { leading: true });

  return (
    <>
      <TextInput
        label="Enter value to see debounce"
        value={value}
        onChange={(event) => setValue(event.currentTarget.value)}
      />

      <Text>Value: {value}</Text>
      <Text>Debounced value: {debounced}</Text>
    </>
  );
}
```

Expand code

## [Cancel update](#cancel-update)

Hook provides `cancel` callback, you can use it to cancel update.
Update cancels automatically on component unmount.

In this example, type in some text and click the cancel button
within a second to cancel debounced value change:

Enter value to see debounce effect

Cancel

Value: [empty string]

Debounced value: [empty string]

Demo.tsx

```
import { useState } from 'react';
import { useDebouncedValue } from '@mantine/hooks';
import { TextInput, Text, Button } from '@mantine/core';

function Demo() {
  const [value, setValue] = useState('');
  const [debounced, cancel] = useDebouncedValue(value, 1000);

  return (
    <>
      <TextInput
        label="Enter value to see debounce"
        value={value}
        onChange={(event) => setValue(event.currentTarget.value)}
      />

      <Button onClick={cancel} size="lg">
        Cancel
      </Button>

      <Text>Value: {value}</Text>
      <Text>Debounced value: {debounced}</Text>
    </>
  );
}
```

Expand code

## [Definition](#definition)

```
interface UseDebouncedValueOptions {
  leading?: boolean;
}

type UseDebouncedValueReturnValue<T> = [T, () => void];

function useDebouncedValue<T = any>(
  value: T,
  wait: number,
  options?: UseDebouncedValueOptions,
): UseDebouncedValueReturnValue<T>
```

Expand code

## [Exported types](#exported-types)

`UseDebouncedValueOptions` and `UseDebouncedValueReturnValue` types are exported from `@mantine/hooks` package,
you can import them in your application:

```
import type { UseDebouncedValueOptions, UseDebouncedValueReturnValue } from '@mantine/hooks';
```

Expand code

[use-debounced-state](/hooks/use-debounced-state/)[use-disclosure](/hooks/use-disclosure/)