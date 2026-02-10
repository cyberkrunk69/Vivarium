# Sortable | @dnd-kit – Documentation

Source: https://docs.dndkit.com/presets/sortable

---

## Installation

To get started, install the sortable preset via `npm` or `yarn`:

Copy

```
npm install @dnd-kit/sortable
```

## Overview

If you're eager to get started right away, here's the code you'll need:

App.jsx

SortableItem.jsx

Copy

```
import React, {useState} from 'react';
import {
  DndContext, 
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';

import {SortableItem} from './SortableItem';

function App() {
  const [items, setItems] = useState([1, 2, 3]);
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  return (
    <DndContext 
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext 
        items={items}
        strategy={verticalListSortingStrategy}
      >
        {items.map(id => <SortableItem key={id} id={id} />)}
      </SortableContext>
    </DndContext>
  );
  
  function handleDragEnd(event) {
    const {active, over} = event;
    
    if (active.id !== over.id) {
      setItems((items) => {
        const oldIndex = items.indexOf(active.id);
        const newIndex = items.indexOf(over.id);
        
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  }
}
```

For most sortable lists, we recommend you use a [`DragOverlay`](/api-documentation/draggable/drag-overlay) if your sortable list is scrollable or if the contents of the scrollable list are taller than the viewport of the window. Check out the [sortable drag overlay guide](/presets/sortable#drag-overlay) below to learn more.

## Architecture

The sortable preset builds on top of the primitives exposed by `@dnd-kit/core` to help building sortable interfaces.

The sortable preset exposes two main concepts: [`SortableContext`](/presets/sortable#sortable-context) and the [`useSortable`](/presets/sortable#usesortable) hook:

- The `SortableContext` provides information via context that is consumed by the `useSortable` hook.
- The `useSortable` hook is an abstraction that composes the [`useDroppable`](/api-documentation/droppable) and [`useDraggable`](/api-documentation/draggable) hooks:

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MPAGLQu4q5MwkPGcMwL%252F-MPAJ4EP6hgc_WyBRvU2%252FuseSortable%2520%281%29.png%3Falt%3Dmedia%26token%3D5258bd82-7443-4c7d-8b27-7d092d04ab03&width=768&dpr=3&quality=100&sign=8781210d&sv=2)

### Single container

At a high level, the application structure to implement a **sortable list with a single container** looks as follows:

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MP7kCLhAw6rXlUxFILQ%252F-MPA8JRM90_d98a9Tvzz%252FSortable%2520%281%29.png%3Falt%3Dmedia%26token%3Dfc6b976d-f97e-4a07-90c5-dee05d3e1498&width=768&dpr=3&quality=100&sign=9fb5e799&sv=2)

### Multiple containers

To implement sortable list with items that can be dropped within **multiple containers**, the application structure is the same, but we add as many `SortableContext` providers as we have containers:

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MPF80W-heGKUftClbx3%252F-MPF9JDgemy4mwpbni_V%252FSortable%2520Multiple%2520Containers%2520Example.png%3Falt%3Dmedia%26token%3D72170d65-d588-4d93-8da8-26252873c285&width=768&dpr=3&quality=100&sign=77dcea88&sv=2)

In this example, we would use the `onDragOver` callback of `DndContext` to detect when a draggable element is moved over a different container to insert it in that new container while dragging.

If you paid close attention to the illustration above, you may also have noticed that we added a droppable zone around each sortable context. This isn't required, but will likely be the behaviour most people want. If you move all sortable items from one column into the other, you will need a droppable zone for the empty column so that you may drag sortable items back into that empty column:

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MPF80W-heGKUftClbx3%252F-MPF9MpK_A0AGiZaGSl7%252FSortable%2520Multiple%2520Containers%2520Empty%2520Column%2520%281%29.png%3Falt%3Dmedia%26token%3D51cd76c1-1c07-49dd-bc80-69128e8b6cbf&width=768&dpr=3&quality=100&sign=43114e8c&sv=2)

## Concepts

### Sortable Context

In addition to the [`DndContext` provider](/introduction/getting-started#context-provider), the Sortable preset requires its own context provider that contains the **sorted** array of the unique identifiers associated to each sortable item:

The `SortableContext` provides information via context that is consumed by the `useSortable` hook, which is covered in greater detail in the next section.

It's important that the `items` prop passed to `SortableContext` be sorted in the same order in which the items are rendered, otherwise you may see unexpected results.

It does not expose any callback props. To know when a sortable (draggable) item is being picked or moved over another sortable (droppable) item, use the callback props of `DndContext`:

In order for the `SortableContext` component to function properly, make sure it is a descendant of a `DndContext` provider. You may nest multiple `SortableContext` components within the same parent `DndContext`.

### useSortable

As outlined above, the `useSortable` hook combines both the [`useDraggable`](/api-documentation/draggable) and [`useDroppable`](/api-documentation/droppable) hooks to connect elements as both draggable sources and drop targets:

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MPAGLQu4q5MwkPGcMwL%252F-MPALbceK3ZbRNIUEqaN%252FuseSortable%2520%283%29.png%3Falt%3Dmedia%26token%3D85c7c4f9-8f7d-4a28-b9dd-69c50c253d95&width=768&dpr=3&quality=100&sign=76d3d454&sv=2)

In most cases, the draggable and droppable hooks will be attached to the same node, and therefore be identical in size. They are represented as different nodes for illustration purposes above.

If you're already familiar with the [`useDraggable`](/api-documentation/draggable) hook, the [`useSortable`](/presets/sortable/usesortable) hook should look very familiar, since, it is an abstraction on top of it.

In addition to the `attributes`, `listeners`,`transform` and `setNodeRef` properties, which you should already be familiar with if you've used the `useDraggable` hook before, you'll notice that the `useSortable` hook also provides a `transition` property.

The `transform` property for `useSortable` represents the displacement and change of scale transformation that a sortable item needs to apply to transition to its new position without needing to update the DOM order.

The `transform` property for the `useSortable` hook behaves similarly to the [`transform`](/api-documentation/draggable#transforms) property of the [`useDraggable`](/api-documentation/draggable) hook for the active sortable item, when there is no [`DragOverlay`](/api-documentation/draggable/drag-overlay) being used.

SortableItem.jsx

The default transition is `250` milliseconds, with an easing function set to `ease`, but you can customize this and pass any valid [CSS transition timing function](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-timing-function), or set the transition argument to `null` to disable transitions entirely:

For more details on the `useSortable` hook, read the full [API documentation](/presets/sortable/usesortable).

### Sensors

Sensors are an abstraction to manage and listen to different input methods. If you're unfamiliar with the concept of sensors, we recommend you read the [introduction to sensors](/api-documentation/sensors) first.

By default, the [Keyboard](/api-documentation/sensors/keyboard) sensor moves the active draggable item by `25` pixels in the direction of the arrow key that was pressed. This is an arbitrary default, and can be customized using the `coordinateGetter` option of the keyboard sensor.

The sortable preset ships with a custom coordinate getter function for the keyboard sensor that moves the active draggable to the closest sortable element in a given direction within the same `DndContext`.

To use it, import the `sortableKeyboardCoordinates` coordinate getter function provided by `@dnd-kit/sortable`, and pass it to the `coordiniateGetter` option of the Keyboard sensor.

In this example, we'll also be setting up the [Pointer](/api-documentation/sensors/pointer) sensor, which is the other sensor that is enabled by default on `DndContext` if none are defined. We use the `useSensor` and `useSensors` hooks to initialize the sensors:

If you'd like to use the [Mouse](/api-documentation/sensors/mouse) and [Touch](/api-documentation/sensors/touch) sensors instead of the [Pointer](/api-documentation/sensors/pointer) sensor, simply initialize those sensors instead:

To learn more about sensors, read the in-depth documentation on sensors:

[Sensors](/api-documentation/sensors)

### Sorting strategies

The supported use cases of the Sortable preset include vertical lists, horizontal lists, grids, and virtualized lists. Because of the wide variety of use cases supported, it would be difficult to write a single strategy to cover all of these different use cases. Instead, the sortable preset exposes a number of different strategies you can use, that are tailored to these various use cases:

- `rectSortingStrategy`: This is the default value, and is suitable for most use cases. This strategy does not support virtualized lists.
- `verticalListSortingStrategy`: This strategy is optimized for vertical lists, and supports virtualized lists.
- `horizontalListSortingStrategy`: This strategy is optimized for horizontal lists, and supports virtualized lists.
- `rectSwappingStrategy`: Use this strategy to achieve swappable functionality.

Make sure to use the sorting strategy that is the most adapted to the use case you are building for.

### Collision detection algorithm

The default collision detection algorithm of `DndContext` is the [rectangle intersection](/api-documentation/context-provider/collision-detection-algorithms#rectangle-intersection) algorithm. While the rectangle intersection strategy is well suited for many use cases, it can be unforgiving, since it requires both the draggable and droppable bounding rectangles to come into direct contact and intersect.

For sortable lists, we recommend using a more forgiving collision detection strategy such as the [closest center](/api-documentation/context-provider/collision-detection-algorithms#closest-center) or [closest corners](/api-documentation/context-provider/collision-detection-algorithms#closest-corners) algorithms.

In this example, we'll be using the closest center algorithm:

To learn more about collision detection algorithms and when to use one over the other, read our guide on collision detection algorithms:

[Collision detection algorithms](/api-documentation/context-provider/collision-detection-algorithms)

## Connecting all the pieces

First, let's go ahead and render all of our sortable items:

App.jsx

SortableItem.jsx

Next, let's wire up the custom sensors for `DndContext` and add a custom collision detection strategy:

App.jsx

SortableItem.jsx

In this example, we'll be building a vertical sortable list, so we will be using the `verticalListSortingStrategy` sorting strategy:

Finally, we'll need to set up event handlers on the `DndContext` provider in order to update the order of the items on drag end.

### Drag Overlay

For most sortable lists, we recommend you use a [`DragOverlay`](/api-documentation/draggable/drag-overlay) if your sortable list is scrollable or if the contents of the scrollable list are taller than the viewport of the window.

The `<DragOverlay>` component provides a way to render a draggable overlay that is removed from the normal document flow and is positioned relative to the viewport. The drag overlay also implements drop animations.

A **common pitfall** when using the `DragOverlay` component is rendering the same component that calls `useSortable` inside the `DragOverlay`. This will lead to unexpected results, since there will be an `id` collision between the two components both calling `useDraggable` with the same `id`, since `useSortable` is an abstraction on top of `useDraggable`.

Instead, create a presentational version of your component that you intend on rendering in the drag overlay, and another version that is sortable and renders the presentational component. There are two recommended patterns for this, either using [wrapper nodes](/api-documentation/draggable/drag-overlay#wrapper-nodes) or [ref forwarding](/api-documentation/draggable/drag-overlay#ref-forwarding).

In this example, we'll use the [ref forwarding](/api-documentation/draggable/drag-overlay#ref-forwarding) pattern to avoid introducing wrapper nodes:

App.jsx

SortableItem.jsx

Item.jsx

Last updated 3 years ago