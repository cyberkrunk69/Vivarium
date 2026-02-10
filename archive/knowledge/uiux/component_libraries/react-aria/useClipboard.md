# useClipboard

Source: https://react-spectrum.adobe.com/react-aria/useClipboard.html

---

# useClipboard

Handles clipboard interactions for a focusable element. Supports items of multiple
data types, and integrates with the operating system native clipboard.

## Introduction

Copy and paste is a common way to transfer data between locations, either within or between apps. Browsers support copy and paste of selected text content by default, but rich objects with custom data can also be copied and pasted using the [clipboard events](https://developer.mozilla.org/en-US/docs/Web/API/ClipboardEvent) API. For example, an app could support copying and pasting a selected card representing a rich object to a new location, or allow a user to paste files from their device to upload them. This can provide a keyboard accessible alternative to drag and drop.

The useClipboard hook provides a simple way to implement copy and paste for a focusable element. When focused, users can press keyboard shortcuts like `âC` and `âV`, or even use the browser's "Copy" and "Paste" menu commands, to trigger clipboard events. Multiple items can be copied and pasted at once, each represented in one or more different data formats. Because it uses native browser APIs under the hood, copy and paste uses the operating system clipboard, which means it works between applications (e.g. Finder, Windows Explorer, a native email app, etc.) in addition to within the app.

## Example

This example shows a simple focusable element which supports copying a string when focused, and another element which supports pasting plain text.

Hello world`âC`

Paste here`âV`

Example

useClipboardExample.css

Example

useClipboardExample.css

Example

useClipboardExample.css

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useClipboard} from 'react-aria';
import './useClipboardExample.css';
import './theme.css';

function Copyable() {
  let {clipboardProps} = useClipboard({
    getItems() {
      return [{
        'text/plain': 'Hello world'
      }];
    }
  });

  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Copyable text">
      Hello world
      <kbd>âC</kbd>
    </div>
  );
}

function Pasteable() {
  let [pasted, setPasted] = React.useState<any[] | string | null>(null);
  let {clipboardProps} = useClipboard({
    async onPaste(items) {
      let pasted = await Promise.all(
        items
          .filter((item): item is TextDropItem => item.kind === 'text' && item.types.has('text/plain'))
          .map((item) => item.getText('text/plain'))
      );
      setPasted(pasted.join('\n'));
    }
  });

  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Paste target">
      {pasted || 'Paste here'}
      <kbd>âV</kbd>
    </div>
  );
}

<div>
  <Copyable />
  <Pasteable />
</div>
```

Expand code

## Copy data

Data to copy can be provided in multiple formats at once. This allows the destination where the user pastes to choose the data that it understands. For example, you could serialize a complex object as JSON in a custom format for use within your own application, and also provide plain text and/or rich HTML fallbacks that can be used when a user pastes in an external application (e.g. an email message).

This can be done by returning multiple keys for an item from the `getItems` function. Types can either be a standard [mime type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) for interoperability with external applications, or a custom string for use within your own app.

In addition to providing items in multiple formats, you can also return multiple drag items from `getItems` to transfer multiple objects in a single copy and paste operation.

This example copies two items, each of which contains representations as plain text, HTML, and a custom app-specific data format. Pasting on the target will use the custom data format to render formatted items. If you paste in an external application supporting rich text, the HTML representation will be used. Dropping in a text editor will use the plain text format.

**hello world**

*foo bar*

`âC`

Paste here

`âV`

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useClipboard} from 'react-aria';

function Copyable() {
  let {clipboardProps} = useClipboard({
    getItems() {
      return [{
        'text/plain': 'hello world',
        'text/html': '<strong>hello world</strong>',
        'my-app-custom-type': JSON.stringify({
          message: 'hello world',
          style: 'bold'
        })
      }, {
        'text/plain': 'foo bar',
        'text/html': '<em>foo bar</em>',
        'my-app-custom-type': JSON.stringify({
          message: 'foo bar',
          style: 'italic'
        })
      }];
    }
  });

  return (
    <div role="textbox" tabIndex={0} {...clipboardProps}>
      <div>
        <div><strong>hello world</strong></div>
        <div><em>foo bar</em></div>
      </div>
      <kbd>âC</kbd>
    </div>
  );
}

function Pasteable() {</div>

let [pasted, setPasted] = React.useState<any[] | string | null>(null);
  let {clipboardProps} = useClipboard({
    async onPaste(items) {
      let pasted = await Promise.all(
        items
          .filter((item): item is TextDropItem => item.kind === 'text' && (item.types.has('text/plain') || item.types.has('my-app-custom-type')))
          .map(async (item) => {
            if (item.types.has('my-app-custom-type')) {
              return JSON.parse(await item.getText('my-app-custom-type'));
            } else {
              return {message: await item.getText('text/plain')};
            }
          })
      );
      setPasted(pasted);
    }
  });

  let message: React.ReactElement[] = [<div key="placeholder">Paste here</div>];
  if (pasted && Array.isArray(pasted)) {
    message = pasted.map((d, i) => {
      let message = d.message;
      if (d.style === 'bold') {
        message = <strong>{message}</strong>;
      } else if (d.style === 'italic') {
        message = <em>{message}</em>;
      }
      return <div key={i}>{message}</div>;
    });
  }

  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Rich text paste target">
      <div>{message || 'Paste here'}</div>
      <kbd>âV</kbd>
    </div>
  );
}

<div>
  <Copyable />
  <Pasteable />
</div>
```

Expand code

## Paste data

`useClipboard` allows users to paste one or more items, each of which contains data to be pasted. There are three kinds of items:

- `text` â represents data inline as a string in one or more formats
- `file` â references a file on the user's device
- `directory` â references the contents of a directory

### Text

A TextDropItem represents textual data in one or more different formats. These may be either standard [mime types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) or custom app-specific formats. Representing data in multiple formats allows drop targets both within and outside an application to choose data in a format that they understand. For example, a complex object may be serialized in a custom format for use within an application, with fallbacks in plain text and/or rich HTML that can be used when a user drops data from an external application.

The example below works with the above `Copyable` example using a custom app-specific data format to transfer rich data. If no such data is available, it falls back to pasting plain text data.

**hello world**

*foo bar*

`âC`

Paste here

`âV`

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useClipboard} from 'react-aria';

function Copyable() {}

let {clipboardProps} = useClipboard({
    getItems() {
      return [{
        'text/plain': 'hello world',
        'text/html': '<strong>hello world</strong>',
        'my-app-custom-type': JSON.stringify({
          message: 'hello world',
          style: 'bold'
        })
      }, {
        'text/plain': 'foo bar',
        'text/html': '<em>foo bar</em>',
        'my-app-custom-type': JSON.stringify({
          message: 'foo bar',
          style: 'italic'
        })
      }];
    }
  });

  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Rich text to copy">
      <div>
        <div><strong>hello world</strong></div>
        <div><em>foo bar</em></div>
      </div>
      <kbd>âC</kbd>
    </div>
  );
}

function Pasteable() {
  let [pasted, setPasted] = React.useState<any[] | string | null>(null);
  let {clipboardProps} = useClipboard({
    async onPaste(items) {
      let pasted = await Promise.all(
        items
          .filter((item): item is TextDropItem => item.kind === 'text' && (item.types.has('text/plain') || item.types.has('my-app-custom-type')))
          .map(async (item) => {
            if (item.types.has('my-app-custom-type')) {
              return JSON.parse(await item.getText('my-app-custom-type'));
            } else {
              return {message: await item.getText('text/plain')};
            }
          })
      );
      setPasted(pasted);
    }
  });

  let message: React.ReactElement[] = [<div key="placeholder">Paste here</div>];
  if (pasted && Array.isArray(pasted)) {
    message = pasted.map((d, i) => {
      let message = d.message;
      if (d.style === 'bold') {
        message = <strong>{message}</strong>;
      } else if (d.style === 'italic') {
        message = <em>{message}</em>;
      }
      return <div key={i}>{message}</div>;
    });
  }

  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Rich text paste target">
      <div>{message || 'Paste here'}</div>
      <kbd>âV</kbd>
    </div>
  );
}

<div></div>

<Copyable />
  <Pasteable />
</div>
```

Expand code

### Files

A FileDropItem references a file on the user's device. It includes the name and mime type of the file, and methods to read the contents as plain text, or retrieve a native [File](https://developer.mozilla.org/en-US/docs/Web/API/File) object which can be attached to form data for uploading.
This example accepts JPEG and PNG image files, and renders them by creating a local [object URL](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL).

Paste image here

```
import React from 'react';
import {useClipboard} from 'react-aria';
import type {FileDropItem} from 'react-aria';

function Pasteable() {
  let [file, setFile] = React.useState<string | null>(null);
  let {clipboardProps} = useClipboard({
    async onPaste(items) {
      let item = items.find(item => item.kind === 'file' && (item.type === 'image/jpeg' || item.type === 'image/png')) as FileDropItem;
      if (item) {
        setFile(URL.createObjectURL(await item.getFile()));
      }
    }
  });
  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} style={{width: 150, height: 100}} aria-label="Image paste target">
      {file ? <img src={file} alt="Pasted image" style={{width: '100%', height: '100%', objectFit: 'contain'}} /> : 'Paste image here'}
    </div>
  );
}
```

Expand code

### Directories

A DirectoryDropItem references the contents of a directory on the user's device. It includes the name of the directory, as well as a method to iterate through the files and folders within the directory. The contents of any folders within the directory can be accessed recursively.
The `getEntries` method returns an [async iterable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of) object, which can be used in a `for await...of` loop. This provides each item in the directory as either a FileDropItem or DirectoryDropItem, and you can access the contents of each file as discussed above.
This example renders the file names within a dropped directory in a grid.

Paste directory here

Example

useClipboardGrid.css

Example

useClipboardGrid.css

Example

useClipboardGrid.css

```
import React from 'react';
import {useClipboard} from 'react-aria'
import type {DirectoryDropItem} from 'react-aria';
import File from '@react-spectrum/s2/icons/File';
import Folder from '@react-spectrum/s2/icons/Folder';
import './useClipboardGrid.css';

function Pasteable() {
  let [files, setFiles] = React.useState<Array<{name: string, kind: 'file' | 'directory'}> | null>(null);
  let {clipboardProps} = useClipboard({
    async onPaste(items) {
      // Find the first dropped item that is a directory.
      let dir = items.find(item => item.kind === 'directory') as DirectoryDropItem;
      if (dir) {
        // Read entries in directory and update state with relevant info.
        let files: Array<{name: string, kind: 'file' | 'directory'}> = [];
        for await (let entry of dir.getEntries()) {
          files.push({
            name: entry.name,
            kind: entry.kind
          });
        }
        setFiles(files);
      }
    }
  });
  let contents = <>Paste directory here</>;
  if (files) {
    contents = (
      <ul>
        {files.map(f => (
          <li key={f.name}>
            {f.kind === 'directory' ? <Folder /> : <File />}
            <span>{f.name}</span>
          </li>
        ))}
      </ul>
    );
  }
  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} className="grid" aria-label="Directory paste target">
      {contents}
    </div>
  );
}
```

Expand code

## Disabling copy and paste

If you need to temporarily disable copying and pasting, you can pass the `isDisabled` option to `useClipboard`. This will prevent copying and pasting on the element until it is re-enabled.

Hello world`âC`

Paste here`âV`

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useClipboard} from 'react-aria';

function Copyable() {
  let {clipboardProps} = useClipboard({
    getItems() {
      return [{
        'text/plain': 'Hello world'
      }];
    },
    isDisabled: true
  });
  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Disabled copyable text">
      Hello world
      <kbd>âC</kbd>
    </div>
  );
}
function Pasteable() {
  let [pasted, setPasted] = React.useState<any[] | string | null>(null);
  let {clipboardProps} = useClipboard({
    async onPaste(items) {
      let pasted = await Promise.all(
        items
          .filter((item): item is TextDropItem => item.kind === 'text' && item.types.has('text/plain'))
          .map((item) => item.getText('text/plain'))
      );
      setPasted(pasted.join('\n'));
    },
    isDisabled: true
  });
  return (
    <div role="textbox" tabIndex={0} {...clipboardProps} aria-label="Disabled paste target">
      {pasted || 'Paste here'}
      <kbd>âV</kbd>
    </div>
  );
}

<div>
  <Copyable />
  <Pasteable />
</div>
```

Expand code

## API

`useClipboard(options: ClipboardProps): ClipboardResult`

### ClipboardProps

| Name | Type |
| --- | --- |
| `isDisabled` | `boolean` |
| Whether the clipboard is disabled. | | |
| `onPaste` | `(items: DropItem[]) => void` |
| Handler that is called when the user triggers a paste interaction. | | |
| `onCut` | `() => void` |
| Handler that is called when the user triggers a cut interaction. | | |
| `onCopy` | `() => void` |
| Handler that is called when the user triggers a copy interaction. | | |
| `getItems` | `(details: { action: 'cut' |Â 'copy' }) => DragItem[]` |
| A function that returns the items to copy. | | |

### ClipboardResult

| Name | Type |
| --- | --- |
| `clipboardProps` | `DOMAttributes` |
| Props for the element that will handle clipboard events. | | |