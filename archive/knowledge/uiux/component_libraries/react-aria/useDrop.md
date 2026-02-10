# useDrop

Source: https://react-spectrum.adobe.com/react-aria/useDrop.html

---

# useDrop

Handles drop interactions for an element, with support for traditional mouse and touch
based drag and drop, in addition to full parity for keyboard and screen reader users.

## Introduction

React Aria supports traditional mouse and touch based drag and drop, but also implements keyboard and screen reader friendly interactions. Users can press `Enter` on a draggable element to enter drag and drop mode. Then, they can press `Tab` to navigate between drop targets, and `Enter` to drop or `Escape` to cancel. Touch screen reader users can also drag by double tapping to activate drag and drop mode, swiping between drop targets, and double tapping again to drop.

See the [drag and drop guide](dnd) to learn more.

## Example

This example shows how to make a simple drop target that accepts plain text data. In order to support keyboard and screen reader drag interactions, the element must be focusable and have an ARIA role (in this case, `button`). While a drag is hovered over it, a blue outline is rendered by applying an additional CSS class.

Drag me

Drop here

Example

Draggable.tsx

useDragExample.css

Example

Draggable.tsx

useDragExample.css

Example

Draggable.tsx

useDragExample.css

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useDrop} from 'react-aria';
import {Draggable} from './Draggable';
import './useDragExample.css';
import './theme.css';

function DropTarget() {
  let [dropped, setDropped] = React.useState<string | null>(null);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    async onDrop(e) {
      let items = await Promise.all(
        e.items
          .filter((item): item is TextDropItem => item.kind === 'text' && item.types.has('text/plain'))
          .map((item) => item.getText('text/plain'))
      );
      setDropped(items.join('\n'));
    }
  });

  return (
    <div {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable ${isDropTarget ? 'target' : ''}`}>
      {dropped || 'Drop here'}
    </div>
  );
}

<div>
  <Draggable />
  <DropTarget />
</div>
```

Expand code

## Drop data

`useDrop` allows users to drop one or more **drag items**, each of which contains data to be transferred from the drag source to drop target. There are three kinds of drag items:

- `text` â represents data inline as a string in one or more formats
- `file` â references a file on the user's device
- `directory` â references the contents of a directory

### Text

A TextDropItem represents textual data in one or more different formats. These may be either standard [mime types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) or custom app-specific formats. Representing data in multiple formats allows drop targets both within and outside an application to choose data in a format that they understand. For example, a complex object may be serialized in a custom format for use within an application, with fallbacks in plain text and/or rich HTML that can be used when a user drops data from an external application.

The example below finds the first available item that includes a custom app-specific type. The same draggable component as used in the above example is used here, but rather than displaying the plain text representation, the custom format is used instead.

Drag me

Drop here

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useDrop} from 'react-aria';
import {Draggable} from './Draggable';

function DropTarget() {
  let [dropped, setDropped] = React.useState<string | null>(null);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    async onDrop(e) {
      let item = e.items.find(item => item.kind === 'text' && item.types.has('my-app-custom-type')) as TextDropItem;
      if (item) {
        setDropped(await item.getText('my-app-custom-type'));
      }
    }
  });
  // ...

return ();

<div {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable ${isDropTarget ? 'target' : ''}`}>
      {dropped || 'Drop here'}
    </div>
  );

}

<div></div>

<Draggable />
  <DropTarget />
</div>
```

Expand code

### Files

A FileDropItem references a file on the user's device. It includes the name and mime type of the file, and methods to read the contents as plain text, or retrieve a native [File](https://developer.mozilla.org/en-US/docs/Web/API/File) object which can be attached to form data for uploading.

This example accepts JPEG and PNG image files, and renders them by creating a local [object URL](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL).

Drop image here

```
import React from 'react';
import type {FileDropItem} from 'react-aria';
import {useDrop} from 'react-aria';
function DropTarget() {
  let [file, setFile] = React.useState<string | null>(null);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    async onDrop(e) {
      let item = e.items.find(item => item.kind === 'file' && (item.type === 'image/jpeg' || item.type === 'image/png')) as FileDropItem;
      if (item) {
        setFile(URL.createObjectURL(await item.getFile()));
      }
    }
  });
  return (
    <div {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable ${isDropTarget ? 'target' : ''}`}>
      {file ? <img src={file} style={{width: '100%', height: '100%', objectFit: 'contain'}} /> : 'Drop image here'}
    </div>
  );
}
```

Expand code

### Directories

A DirectoryDropItem references the contents of a directory on the user's device. It includes the name of the directory, as well as a method to iterate through the files and folders within the directory. The contents of any folders within the directory can be accessed recursively.
The `getEntries` method returns an [async iterable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of) object, which can be used in a `for await...of` loop. This provides each item in the directory as either a FileDropItem or DirectoryDropItem, and you can access the contents of each file as discussed above.

This example renders the file names within a dropped directory in a grid.

Drop directory here

Example

useClipboardGrid.css

Example

useClipboardGrid.css

Example

useClipboardGrid.css

```
import React from 'react';
import type {DirectoryDropItem} from 'react-aria';
import File from '@react-spectrum/s2/icons/File';
import Folder from '@react-spectrum/s2/icons/Folder';
import {useDrop} from 'react-aria';
import './useClipboardGrid.css';

function DropTarget() {
  let [files, setFiles] = React.useState<Array<{name: string, kind: 'file' | 'directory'}> | null>(null);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    async onDrop(e) {
      // Find the first dropped item that is a directory.
      let dir = e.items.find(item => item.kind === 'directory') as DirectoryDropItem;
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
  let contents = <>Drop directory here</>;
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
    <div {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable grid ${isDropTarget ? 'target' : ''}`} style={{overflow: 'auto'}}>
      {contents}
    </div>
  );
}
```

Expand code

## Drop operations

A DropOperation is an indication of what will happen when dragged data is dropped on a particular drop target. These are:

- `move` â indicates that the dragged data will be moved from its source location to the target location.
- `copy` â indicates that the dragged data will be copied to the target destination.
- `link` â indicates that there will be a relationship established between the source and target locations.
- `cancel` â indicates that the drag and drop operation will be canceled, resulting in no changes made to the source or target.

Many operating systems display these in the form of a cursor change, e.g. a plus sign to indicate a copy operation. The user may also be able to use a modifier key to choose which drop operation to perform, such as `Option` or `Alt` to switch from move to copy.
The drag source can specify which drop operations are allowed for the dragged data (see the [useDrag docs](useDrag) for how to customize this). By default, the first allowed operation is allowed by drop targets, meaning that the drop target accepts data of any type and operation.

### getDropOperation

The `getDropOperation` function passed to `useDrop` can be used to provide appropriate feedback to the user when a drag hovers over the drop target. If a drop target only supports data of specific types (e.g. images, videos, text, etc.), then it should implement `getDropOperation` and return `'cancel'` for types that aren't supported. This will prevent visual feedback indicating that the drop target accepts the dragged data when this is not true.
When the data is supported, either return one of the drop operations in `allowedOperation` or a specific drop operation if only that drop operation is supported. If the returned operation is not in `allowedOperations`, then the drop target will act as if `'cancel'` was returned.

In the below example, the drop target only supports dropping PNG images. If a PNG is dragged over the target, it will be highlighted and the operating system displays a copy cursor. If another type is dragged over the target, then there is no visual feedback, indicating that a drop is not accepted there. If the user holds a modifier key such as `Control` while dragging over the drop target in order to change the drop operation, then the drop target does not accept the drop.

Drop image here

```
import React from 'react';
import {useDrop} from 'react-aria';
import type {FileDropItem} from 'react-aria';
function DropTarget() {
  let [file, setFile] = React.useState<string | null>(null);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    getDropOperation(types, allowedOperations) {
      return types.has('image/png') ? 'copy' : 'cancel';
    },
    async onDrop(e) {
      let item = e.items.find(item => item.kind === 'file' && item.type === 'image/png') as FileDropItem;
      if (item) {
        setFile(URL.createObjectURL(await item.getFile()));
      }
    }
  });
  // ...

return ();

<div {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable ${isDropTarget ? 'target' : ''}`}>
      {file ? <img src={file} style={{width: '100%', height: '100%', objectFit: 'contain'}} /> : 'Drop image here'}
    </div>
  );

}
```

Expand code

### onDrop

The `onDrop` event also includes the `dropOperation`. This can be used to perform different actions accordingly, for example, when communicating with a backend API.

```
function DropTarget(props) {
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    async onDrop(e) {
      let item = e.items.find(item => item.kind === 'text' && item.types.has('my-app-file')) as TextDropItem;
      if (!item) {
        return;
      }
      let data = JSON.parse(await item.getText('my-app-file'));
      switch (e.dropOperation) {
        case 'move':
          MyAppFileService.move(data.filePath, props.filePath);
          break;
        case 'copy':
          MyAppFileService.copy(data.filePath, props.filePath);
          break;
        case 'link':
          MyAppFileService.link(data.filePath, props.filePath);
          break;
      }
    }
  });
  // ...
}
```

## Events

Drop targets receive a number of events during a drag session. These are:

| Name | Type |
| --- | --- |
| `y` | `number` |
| The y coordinate of the event, relative to the target element. | | |
| `x` | `number` |
| The x coordinate of the event, relative to the target element. | | |
| `items` | `DropItem[]` |
| The dropped items. | | |
| `dropOperation` | `DropOperation` |
| The drop operation that should occur. | | |
| `type` | `'drop'` |
| The event type. | | |

This example logs all events that occur within the drop target:

Drag me

```
import React from 'react';
import {useDrop} from 'react-aria';
import {Draggable} from './Draggable';

function DropTarget() {
  let [events, setEvents] = React.useState<string[]>([]);
  let onEvent = e => setEvents(events => [JSON.stringify(e), ...events]);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    onDropEnter: onEvent,
    onDropMove: onEvent,
    onDropExit: onEvent,
    onDrop: onEvent
  });
  return (
    <ul {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable ${isDropTarget ? 'target' : ''}`} style={{display: 'block', width: 'auto', overflow: 'auto'}} aria-label="Drop events">
      {events.map((e, i) => <li key={i}>{e}</li>)}
    </ul>
  );
}
<div>
  <Draggable />
  <DropTarget />
</div>
```

Expand code

## Disabling dropping

If you need to temporarily disable dropping, you can pass the `isDisabled` option to `useDrop`. This will prevent the drop target from accepting any drops until it is re-enabled.

Drag me

Drop here

```
import React from 'react';
import type {TextDropItem} from 'react-aria';
import {useDrop} from 'react-aria';
import {Draggable} from './Draggable';

function DropTarget() {
  let [dropped, setDropped] = React.useState<string | null>(null);
  let ref = React.useRef(null);
  let {dropProps, isDropTarget} = useDrop({
    ref,
    async onDrop(e) {
      let items = await Promise.all(
        e.items
          .filter((item): item is TextDropItem => item.kind === 'text' && item.types.has('text/plain'))
          .map((item) => item.getText('text/plain'))
      );
      setDropped(items.join('\n'));
    },
    isDisabled: true
  });
  return (
    <div {...dropProps} role="button" tabIndex={0} ref={ref} className={`droppable ${isDropTarget ? 'target' : ''}`}>
      {dropped || 'Drop here'}
    </div>
  );
}
<div>
  <Draggable />
  <DropTarget />
</div>
```

Expand code

## API

`useDrop(options: DropOptions): DropResult`

### DropOptions

| Name | Type |
| --- | --- |
| `ref` | `RefObject<FocusableElement |Â null>` |
| A ref for the droppable element. | | |
| `isDisabled` | `boolean` |
| Whether the drop target is disabled. If true, the drop target will not accept any drops. | | |
| `hasDropButton` | `boolean` |
| Whether the item has an explicit focusable drop affordance to initiate accessible drag and drop mode. If true, the dropProps will omit these event handlers, and they will be applied to dropButtonProps instead. | | |
| `onDrop` | `(e: DropEvent) => void` |
| Handler that is called when a valid drag is dropped on the drop target. | | |
| `onDropExit` | `(e: DropExitEvent) => void` |
| Handler that is called when a valid drag exits the drop target. | | |
| `onDropActivate` | `(e: DropActivateEvent) => void` |
| Handler that is called after a valid drag is held over the drop target for a period of time. This typically opens the item so that the user can drop within it. | | |
| `onDropMove` | `(e: DropMoveEvent) => void` |
| Handler that is called when a valid drag is moved within the drop target. | | |
| `onDropEnter` | `(e: DropEnterEvent) => void` |
| Handler that is called when a valid drag enters the drop target. | | |
| `getDropOperationForPoint` | `( types: DragTypes, allowedOperations: DropOperation[], x: number, y: number ) => DropOperation` |
| A function that returns the drop operation for a specific point within the target. | | |
| `getDropOperation` | `(types: DragTypes, allowedOperations: DropOperation[]) => DropOperation` |
| A function returning the drop operation to be performed when items matching the given types are dropped on the drop target. | | |

### DropResult

| Name | Type |
| --- | --- |
| `isDropTarget` | `boolean` |
| Whether the drop target is currently focused or hovered. | | |
| `dropProps` | `DOMAttributes` |
| Props for the droppable element. | | |
| `dropButtonProps` | `AriaButtonProps` |
| Props for the explicit drop button affordance, if any. | | |