# Quick start | @dnd-kit – Documentation

Source: https://docs.dndkit.com/introduction/getting-started

---

Before getting started, make sure you have followed the installation steps outlined in the [Installation guide](/introduction/installation).

### Context provider

First, we'll set up the general structure of the app. In order for the `useDraggable` and `useDroppable` hooks to function correctly, you'll need to ensure that the components where they are used are wrapped within a [`<DndContext />`](/api-documentation/context-provider) component:

App.jsx

Copy

```
import React from 'react';
import {DndContext} from '@dnd-kit/core';

import {Draggable} from './Draggable';
import {Droppable} from './Droppable';

function App() {
  return (
    <DndContext>
      <Draggable />
      <Droppable />
    </DndContext>
  )
}
```

### Droppable

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MNQc_e_FVewH2dAwjx9%252F-MNQdykNUAckcRaS-rWa%252Fdroppable-large.svg%3Falt%3Dmedia%26token%3D18af3a4e-b911-4149-82af-5d67c7198eea&width=768&dpr=3&quality=100&sign=e52f37ee&sv=2)

Next, let's set up your first **Droppable** component. To do so, we'll be using the `useDroppable` hook.
The `useDroppable` hook isn't opinionated about how your app should be structured. At minimum though, it requires you pass a [ref](https://reactjs.org/docs/refs-and-the-dom.html) to the DOM element that you would like to become droppable. You'll also need to provide a unique `id` attribute to all your droppable components.

When a **draggable** element is moved over your droppable element, the `isOver` property will become true.

Droppable.jsx

### Draggable

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MN0Kqdqp2CU1CxUV_hg%252F-MN0LCrhtymDDEQ6kaJj%252Fdraggable-large.svg%3Falt%3Dmedia%26token%3D16954bf4-1357-4890-9e99-a74ca336ddf1&width=768&dpr=3&quality=100&sign=151c59c1&sv=2)

Next, let's take a look at implementing our first **Draggable** component. To do so, we'll be using the `useDraggable` hook.

The `useDraggable`hook isn't opinionated about how your app should be structured. It does however require you to be able to attach listeners and a ref to the DOM element that you would like to become draggable. You'll also need to provide a unique `id` attribute to all your draggable components.

After a draggable item is picked up, the `transform` property will be populated with the `translate` coordinates you'll need to move the item on the screen.

The `transform` object adheres to the following shape: `{x: number, y: number, scaleX: number, scaleY: number}`

Draggable.jsx

As you can see from the example above, it really only takes just a few lines to transform your existing components into draggable components.

**Tips:**

- For performance reasons, we recommend you use `transform` over other positional CSS properties to move the dragged element.
- You'll likely want to alter the `z-index` of your Draggable component to ensure it appears on top of other elements.
- If your item needs to move from one container to another, we recommend you use the [`<DragOverlay>`](/api-documentation/draggable/drag-overlay) component.

Converting the `transform` object to a string can feel tedious. Fear not, you can avoid having to do this by hand by importing the `CSS` utility from the `@dnd-kit/utilities` package:

### Assembling all the pieces

Once you've set up your **Droppable** and **Draggable** components, you'll want to come back to where you set up your [`<DndContext>`](/api-documentation/context-provider) component so you can add event listeners to be able to respond to the different events that are fired.

In this example, we'll assume you want to move your `<Draggable>` component from outside into your `<Droppable>` component:

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MPBiS011L5t61nqKkYr%252F-MPBjPjCz5hhHlavOpZE%252FExample.png%3Falt%3Dmedia%26token%3D8f1b9699-24ce-42c3-9dd7-17ed4bba15a7&width=768&dpr=3&quality=100&sign=76b6d3e8&sv=2)

To do so, you'll want to listen to the `onDragEnd` event of the `<DndContext>` to see if your draggable item was dropped over your droppable:

App.jsx

Droppable.jsx

Draggable.jsx

That's it! You've set up your first [**Droppable**](/api-documentation/droppable)and [**Draggable**](/api-documentation/draggable) components.

### Pushing things a bit further

The example we've set up above is a bit simplistic. In a real world example, you may have multiple droppable containers, and you may also want to be able to drag your items back out of the droppable containers once they've been dragged within them.

Here's a slightly more complex example that contains multiple **Droppable** containers:

App.jsx

Droppable.jsx

Draggable.jsx

We hope this quick start guide has given you a glimpse of the simplicity and power of @dnd-kit. There's much more to learn, and we encourage you to keep reading about all of the different options you can pass to `<DndContext>` , `useDroppable` and `useDraggable` by reading their respective API documentation.

Last updated 3 years ago