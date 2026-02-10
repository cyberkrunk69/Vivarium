# Droppable | @dnd-kit – Documentation

Source: https://docs.dndkit.com/api-documentation/droppable

---

![](https://docs.dndkit.com/~gitbook/image?url=https%3A%2F%2F3633755066-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-MMujhzqaYbBEEmDxnZO%252F-MNQc_e_FVewH2dAwjx9%252F-MNQdykNUAckcRaS-rWa%252Fdroppable-large.svg%3Falt%3Dmedia%26token%3D18af3a4e-b911-4149-82af-5d67c7198eea&width=768&dpr=3&quality=100&sign=e52f37ee&sv=2)

Use the `useDroppable` hook to set up DOM nodes as droppable areas that [draggable](/api-documentation/draggable) elements can be dropped over.

## Usage

The `useDroppable` hook isn't opinionated about how you should structure your application.

At minimum though, you need to pass the `setNodeRef` function that is returned by the `useDroppable` hook to a DOM element so that it can register the underlying DOM node and keep track of it to detect collisions and intersections with other draggable elements.

If the concept of `ref` is new to you, we recommend you first check out the [Refs and the DOM article](https://reactjs.org/docs/refs-and-the-dom.html#adding-a-ref-to-a-dom-element) on the React documentation website.

You can set up as many droppable containers as you want, just make sure they all have a unique `id` so that they can be differentiated. Each droppable needs to have its own unique node though, so make sure you don't try to connect a single droppable to multiple refs.

To set up multiple droppable targets, simply use the `useDroppable` hook as many times as needed.

If you need to dynamically render a list of droppable containers, we recommend you create a re-usable Droppable component and render that component as many times as needed:

For more details usage of the `useDroppable` hook, refer to the API documentation section:

[useDroppable](/api-documentation/droppable/usedroppable)

Last updated 5 years ago