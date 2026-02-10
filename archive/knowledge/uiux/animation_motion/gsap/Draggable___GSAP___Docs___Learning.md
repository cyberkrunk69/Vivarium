# Draggable | GSAP | Docs & Learning

Source: https://gsap.com/docs/v3/Plugins/Draggable/

---

On this page

Provides a surprisingly simple way to make virtually any DOM element draggable, spinnable, tossable, and even flick-scrollable using mouse and/or touch events

Inertia effects Draggable integrates beautifully with [InertiaPlugin](/docs/v3/Plugins/InertiaPlugin) so that the user can flick and have the motion decelerate smoothly based on momentum. :::

#### loading...

## Features[â](#features "Direct link to Features")

Feature Highlights

- **Touch enabled** - Works great on tablets, phones, and desktop browsers.
- **Incredibly smooth** - GPU-accelerated and `requestAnimationFrame`-driven for ultimate performance. Compared to other options out there, Draggable just feels far more natural and fluid, particularly when imposing bounds and momentum.
- **Momentum-based animation** - If you have InertiaPlugin loaded, you can simply set `inertia: true` in the `config` object and it'll automatically apply natural, momentum-based movement after the mouse/touch is released, causing the object to glide gracefully to a stop. You can even control the amount of `resistance`, maximum or minimum `duration`, etc.

**read more...**

- **Impose bounds** - Tell a draggable element to stay within the bounds of another DOM element (a container) as in `bounds: "#container"` or define bounds as coordinates like `bounds: {top: 100, left: 0, width: 1000, height: 800}` or specific maximum and minimum values like `bounds: {minRotation: 0, maxRotation: 270}`.
- **Sense overlaps with `hitTest()`** - See if one element is overlapping another and even set a tolerance threshold (like at least 20 pixels or 25% of either element's total surface area) using the super-flexible `Draggable.hitTest()` method. Feed it a mouse event and it'll tell you if the mouse is over the element. See [this CodePen](https://codepen.io/GreenSock/pen/GFBvn) for a simple example.
- **Define a trigger element** - Maybe you want only a certain area to trigger the dragging (like the top bar of a window) - it's as simple as `trigger: "#topBar"`, for example.
- \*\*Drag position or rotation \*\*- Lots of drag types to choose from: [`"x,y"` | `"top,left"` | `"rotation"` | `"x"` | `"y"` | `"top"` | `"left"`]
- **Lock movement along a certain axis** - Set `lockAxis: true` and Draggable will watch the direction the user starts to drag and then restrict it to that axis. Or if you only want to allow vertical or horizontal movement, that's easy using the type (`"top"` or `"y"` to only allow vertical movement; `"x"`, or `"left"` to only allow horizontal movement).
- **Rotation honors transform origin** - By default, spinnable elements will rotate around their center, but you can set `transformOrigin` to something else to make the pivot point be elsewhere. For example, if you call `gsap.set(yourElement, {transformOrigin: "top left"})` before dragging, it will rotate around its top left corner. Or use `%` or `px`. Whatever is set in the element's CSS will be honored.
- **Rich callback system and event dispatching** - You can use any of the following callbacks: `onPress`, `onDragStart`, `onDrag`, `onDragEnd`, `onRelease`, `onLockAxis`, and `onClick`. Inside the callbacks, `this` refers to the Draggable instance itself, so you can easily access its `target` or `bounds`, etc. If you prefer event listeners instead, Draggable dispatches events too so you can do things like `yourDraggable.addEventListener("dragend", yourFunc);`
- **Works great with SVG.**
- **Even works in transformed containers!** - Got a Draggable inside a rotated or scaled container? No problem. No other tool handles this properly that we've seen.
- **Auto-scrolling, even in multiple containers** - Set `autoScroll: 1` for normal-speed auto scrolling, or `autoScroll: 2` would scroll twice as fast, etc. The closer you move toward the edge, the faster scrolling gets. See a [demo here](https://codepen.io/GreenSock/pen/YPvdYv/?editors=001).
- **Sense clicks when the element moves less than 3 pixels** - A common challenge is figuring out when a user is trying to click or tap an object rather than drag it, so if the mouse/touch moves less than 3 pixels from its starting position, it will be interpreted as a click and the `onClick` callback will be called (and a `"click"` event dispatched) without actually moving the element. You can define a different threshold using `minimumMovement` config property, like `minimumMovement: 6` for 6 pixels.

## Usage[â](#usage "Direct link to Usage")

In its simplest form, you can make an element draggable (vertically and horizontally) like this:

```
Draggable.create('#yourID');
```

This will simply find the element with the ID `"yourID"` and make it draggable with no bounds or any kinetic motion after release. You don't need to use selector text either - you can pass the element itself or even an array of objects.

Use the `vars` parameter to define various other configuration options. For example, to make the object scroll only vertically using the `y` transform and stay within the bounds of a DOM element with an ID of `"container"`, and call a function when clicked and another when the drag ends and make it have momentum-based motion (assuming you loaded InertiaPlugin), do this:

```
Draggable.create('#yourID', {  
	type: 'y',  
	bounds: document.getElementById('container'),  
	inertia: true,  
	onClick: function () {  
		console.log('clicked');  
	},  
	onDragEnd: function () {  
		console.log('drag ended');  
	}  
});
```

Or to make something **spinnable** (dragging rotates the element), you could simply do:

```
Draggable.create('#yourID', {  
	type: 'rotation',  
	inertia: true  
});
```

And to add the ability to snap to 90-degree increments after the mouse/touch is released (like flick-spinning that always lands on 90-degree increments), use the snap option:

```
Draggable.create('#yourID', {  
	type: 'rotation',  
	inertia: true,  
	snap: function (value) {  
		//this function gets called by InertiaPlugin when the mouse/finger is released and it plots where rotation  
		//should normally end and we can alter that value and return a new one instead. This gives us an easy way to  
		//apply custom snapping behavior with any logic we want. In this case, we'll just make sure the end value snaps  
		//to 90-degree increments but only when the "snap" checkbox is selected.  
		return Math.round(value / 90) * 90;  
	}  
});
```

## **Config Object**[â](#config-object "Direct link to config-object")

### Property

### Description

- #### activeCursor

  String - The cursorâs CSS value that should be used between the time they press and then release the pointer/mouse. This can be different than the regular `cursor` value, like: `cursor: "grab", activeCursor: "grabbing"`.
- #### allowContextMenu

  Boolean - If `true`, Draggable will allow context menus (like if a user right-clicks or long-touches). Normally this is suppressed because it can get in the way of dragging (especially on touch devices). Default: `false`.
- #### allowEventDefault

  Boolean - If `true`, `preventDefault()` wonât be called on the original mouse/pointer/touch event. This can be useful if you want to permit the default behavior like touch-scrolling. Typically, however, itâs best to let Draggable call `preventDefault()` on the events in order to deliver the best usability with dragging. Default: `false`.
- #### allowNativeTouchScrolling

  Boolean - By default, allows you to native touch-scroll in the opposite direction as Draggables that are limited to one axis . For example, a Draggable of `type: "x"` or `"left"` would permit native touch-scrolling in the vertical direction, and `type: "y"` or `"top"` would permit native horizontal touch-scrolling. Default: `true`.
- #### autoScroll

  Number - To enable auto-scrolling when a Draggable is dragged within 40px of an edge of a scrollable container, set autoScroll to a non-zero value, where 1 is normal speed, 2 is double-speed, etc. (you can use any number). For a more intuitive or natural feel, it will scroll faster as the mouse/touch gets closer to the edge. The default value is 0 (no auto-scrolling). See [this CodePen](//codepen.io/GreenSock/pen/YPvdYv/?editors=001) for a demo.
- #### bounds

  [*Element* | *String* | *Object*] - To cause the draggable element to stay within the bounds of another DOM element (like a container), you can pass the element like `bounds: document.getElementById("container")` or even selector text like `"#container"`. If you prefer, you can define bounds as a rectangle instead, like `bounds: {top: 100, left: 0, width: 1000, height: 800}` which is based on the parentâs coordinate system (top and left would be from the upper left corner of the parent). Or you can define specific maximum and minimum values like `bounds: {minX: 10, maxX: 300, minY: 50, maxY: 500}` or `bounds: {minRotation: 0, maxRotation: 270}`.
- #### callbackScope

  Object - The scope to be used for all of the callbacks (`onDrag`, `onDragEnd`, `onDragStart`, etc). The scope is what `this` refers to inside any of the callbacks. The older callback-specific scope properties are deprecated but still work.
- #### clickableTest

  Function - Your Draggable may contain child elements that are âclickableâ, like links `<a>` tags, `<button/>` or `<input>` elements, etc. By default, it treats clicks and taps on those elements differently, not allowing the user to drag them. You can set `dragClickables: true` to override that, but it still may be handy to control exactly what Draggable considers to be a âclickableâ element, so you can use your own function that accepts the clicked-on element as the only parameter and returns true or false accordingly. Draggable will call this function whenever the user presses their mouse or finger down on a Draggable, and the target of that event will be passed to your clickableTest function.
- #### cursor

  String - By default (except for `type: "rotation"`), the cursor CSS property of the element is set to `move` so that when the mouse rolls over it, thereâs a visual cue indicating that itâs moveable, but you may define a different cursor if you prefer (as described at <https://devdocs.io/css/cursor>) like `cursor: "pointer"`.
- #### dragClickables

  Boolean - By default, Draggable will work on pretty much any element, but sometimes you might want clicks on `<a>`, `<input>`, `<select>`, `<button>`, and `<textarea>` elements (as well as any element that has a `data-clickable="true"` attribute) NOT to trigger dragging so that the browserâs default behavior fires (like clicking on an input would give it focus and drop the cursor there to begin typing), so if you want Draggable to ignore those clicks and allow the default behavior instead, set `dragClickables: false`.
- #### dragResistance

  Number - A number between 0 and 1 that controls the degree to which resistance is constantly applied to the element as it is dragged, where 1 wonât allow it to be dragged at all, 0.75 applies a lot of resistance (making the object travel at quarter-speed), and 0.5 would be half-speed, etc. This can even apply to rotation.
- #### edgeResistance

  Number - A number between 0 and 1 that controls the degree to which resistance is applied to the element as it goes outside the bounds (if any are applied), where 1 wonât allow it to be dragged past the bounds at all, 0.75 applies a lot of resistance (making the object travel at quarter-speed beyond the border while dragging), and 0.5 would be half-speed beyond the border, etc. This can even apply to rotation.
- #### force3D

  Boolean - By default, 3D transforms are used (when the browser supports them) in order to force the element onto its own layer on the GPU, thus speeding compositing. Typically this provides the best performance, but you can disable it by setting `force3D: false`. This may be a good idea if the element that youâre dragging contains child elements that are animating.
- #### inertia

  [*Boolean* | *Object*] - InertiaPlugin is the key to getting the momentum-based motion after the usersâ mouse (or touch) is released. To have Draggable auto-apply an InertiaPlugin tween to the element when the mouse is released (or touch ends), you can set `inertia: true` (`inertia` also works). Or for advanced effects, you can define the actual inertia object that will get fed into tween, like `inertia: {top: {min: 0, max: 1000, end: [0,200,400,600]}}`. However, if you want ultimate control over the InertiaPlugin tween, you can simply use an `onDragEnd` to call your own function that creates the tween. If `inertia: true` is defined, you may also use any of the following configuration properties that apply to the movement after the mouse/touch is released...

  View More details

  - **snap** : [*Function* | *Object* | *Array*] - Allows you to define rules for where the element can land after it gets released. For example, maybe you want the rotation to always end at a 90-degree increment or you want the `x` and `y` values to be exactly on a grid (whichever cell is closest to the natural landing spot) or maybe you want it to land on a very specific value. You can define the snap in any of the following ways:
    - **As a function** - This function will be passed one numeric parameter, the natural ending value. The function must return whatever the new ending value should be (you run whatever logic you want inside the function and spit back the value). For example, to make the value snap to the closest increment of 50, youâd do `snap: function(endValue) { return Math.round(endValue / 50) * 50; }`.
    - **As an Array** - If you use an array of values, InertiaPlugin will first plot the natural landing position and then loop through the array and find the closest number (as long as itâs not outside any bounds you defined). For example, to have it choose the closest number from 10, 50, 200, and 450, youâd do `snap: [10,50,200,450]`.
    - **As an object** - If youâd like to use different logic for each property, like if `type` is `"x,y"` and youâd like to have the `x` part snap to one set of values, and the `y` part snap to a different set of values, you can use an object that has matching properties, like: `snap:{x: [5,20,80,400], y: [10,60,80,500]}` or if `type` is `"top,left"` and you want to use a different function for each, you could do something like `snap: {top: function(endValue) { return Math.round(endValue / 50) * 50; }, left: function(endValue) { return Math.round(endValue / 100) * 100; }}`. You can define a points property inside this object that combines both `x` and `y`, like `liveSnap: {points: [{x: 0, y: 0},{x: 100, y: 0}], radius: 20}` which will snap to any point in the array when itâs within 20px (distance). Or you can even use a function-based value to run your own snapping logic, like `liveSnap: {points: function(point) { //run custom logic and return a new point }}`. See the [snapping section](#snapping) of this page for examples.
  - **onThrowUpdate** : *Function* - A function that should be called each time the InertiaPlugin tween updates/renders (basically on each âtickâ of the engine while the tween is active). This only applies to the tween that gets generated after the user releases their mouse/touch - the function is not called while the user is dragging the element (thatâs what `onDrag` is for). By default, the scope of the `onThrowUpdate` is the Draggable instance itself, but you may define an `callbackScope` if you prefer, just like any other tween.
  - **onThrowComplete** : *Function* - A function that should be called when the InertiaPlugin tween finishes. This only applies to the tween that gets generated after the user releases their mouse/touch - the function is not called immediately when the user releases their mouse/touch - thatâs what `onDragEnd` is for. By default, the scope of the `onThrowComplete` is the Draggable instance itself, but you may define an `callbackScope` if you prefer, just like any other tween.
  - **throwResistance** : *Number* - A number (`1000` by default) that controls how much resistance or friction there is when the mouse/touch is released and momentum-based motion is enabled (by setting `inertia: true`). The larger the number, the more resistance and the quicker the motion decelerates. (requires InertiaPlugin and setting `inertia: true`, otherwise `throwResistance` will simply be ignored.)
  - **maxDuration** : *Number* - The maximum duration (in seconds) that the kinetic-based inertia tween can last. InertiaPlugin will automatically analyze the velocity and bounds and determine an appropriate duration (faster movements would typically result in longer tweens to decelerate), but you can cap the duration by defining a `maxDuration`. The default is 10 seconds. This has nothing to do with the maximum amount of time that the user can drag the object - itâs only the inertia tween that results after they release the mouse/touch. (requires InertiaPlugin and setting `inertia: true`, otherwise `maxDuration` will simply be ignored.)
  - **minDuration** : *Number* - The minimum duration (in seconds) that the kinetic-based inertia tween should last. InertiaPlugin will automatically analyze the velocity and bounds and determine an appropriate duration (faster movements would typically result in longer tweens to decelerate), but you can force the tween to take at least a certain amount of time by defining a `minDuration`. The default is 0.2 seconds. This has nothing to do with the minimum amount of time that the user can drag the object - itâs only the inertia tween that results after they release the mouse/touch. (requires InertiaPlugin and setting `inertia: true`, otherwise minDuration will simply be ignored.)
  - **overshootTolerance** : *Number* - Affects how much overshooting is allowed before smoothly returning to the resting position at the end of the tween. This can happen when the initial velocity from the flick would normally cause it to exceed the bounds/min/max. The larger the `overshootTolerance` the more leeway the tween has to temporarily shoot past the max/min if necessary. The default is `1`. If you donât want to allow any overshooting, you can set it to `0`.
- #### liveSnap

  [*Function* | *Boolean* | *Array* | *Object*] - Allows you to define rules that get applied **WHILE** the element is being dragged (whereas regular snap affects only the end value(s), where the element lands after the drag is released). For example, maybe you want the rotation to snap to 10-degree increments while dragging or you want the x and y values to snap to a grid (whichever cell is closest). You can define the `liveSnap` in any of the following ways:

  View More details

  - **As a function** - This function will be passed one numeric parameter, the natural (unaltered) value. The function must return whatever the new value should be (you run whatever logic you want inside your function and spit back the value). For example, to make the value snap to the closest increment of 50, youâd do `liveSnap: function(value) { return Math.round(value / 50) * 50; }`.
  - **As an array** - If you use an array of values, Draggable will loop through the array and find the closest number (as long as itâs not outside any bounds you defined). For example, to have it choose the closest number from 10, 50, 200, and 450, youâd do `liveSnap: [10,50,200,450]`.
  - **As an object** - If youâd like to use different logic for each property, like if `type` is `"x,y"` and youâd like to have the âxâ part snap to one set of values, and the âyâ part snap to a different set of values, you can use an object that has matching properties, like: `liveSnap: {x: [5,20,80,400], y: [10,60,80,500]}`. Or if `type` is `"top,left"` and you want to use a different function for each, youâd do something like `liveSnap: {top: function(value) { return Math.round(value / 50) * 50; }, left: function(value) { return Math.round(value / 100) * 100; }}`. You can define a `points` property inside this object that combines both x and y, like `liveSnap: {points:[{x: 0, y: 0}, {x: 100, y: 0}], radius: 20}` which will snap to any point in the array when itâs within 20px (distance). Or you can even use a function-based value to run your own snapping logic, like `liveSnap: {points: function(point) { //run custom logic and return a new point }}`. See the [snapping section](#snapping) of this page for examples.
  - **As a boolean (`true`)** - Live snapping will use whatever is defined for the `snap` (so that instead of only applying to the end value(s), it will apply it âliveâ while dragging too).
- #### lockAxis

  Boolean - If `true`, dragging more than 2 pixels in either direction (horizontally or vertically) will lock movement into that axis so that the element can only be dragged that direction (horizontally or vertically, whichever had the most initial movement) during that drag. No diagonal movement will be allowed. Obviously this is only applicable for Draggables with a `type` of `"x,y"`, or `"top,left"`. If you only want to allow vertical movement, you should set the `type` to `"y"` or `"top"`. If you only want to allow horizontal movement, you should set the `type` to `"x"` or `"left"`.
- #### minimumMovement

  Number - By default, Draggable requires that the Draggable element moves more than 2 pixels in order to be interpreted as a drag, but you can change that threshold using `minimumMovement`. So `minimumMovement: 6` would require that the Draggable element moves more than 6 pixels to be interpreted as a drag.
- #### onClick

  Function - A function that should be called only when the mouse/touch is pressed on the element and released without moving 3 pixels or more. This makes it easier to discern the userâs intent (click or drag). Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access its `pageX`, `pageY`, `target`, `currentTarget`, etc.
- #### onClickParams

  Array - An optional array of parameters to feed the `onClick` callback. For example, `onClickParams: ["clicked", 5]` would work with this code: `onClick: function(message, num) { console.log("message: " + message + ", num: " + num); }`.
- #### onDrag

  Function - A function that should be called every time the mouse (or touch) moves during the drag. Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access its `pageX`, `pageY`, `target`, `currentTarget`, etc. This is only called once per requestAnimationFrame.
- #### onDragParams

  Array - An optional array of parameters to feed the `onDrag` callback. For example, `onDragParams: ["dragged", 5]` would work with this code: `onDrag: function(message, num) { console.log("message: " + message + ", num: " + num); }`.
- #### onDragEnd

  Function - A function that should be called as soon as the mouse (or touch) is **released** after the drag. Even if nothing is moved, the `onDragEnd` will always fire, whereas the `onClick` callback only fires if the mouse/touch moves is less than 3 pixels. Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access `pageX`, `pageY`, `target`, `currentTarget`, etc.
- #### onDragEndParams

  Array - An optional array of parameters to feed the `onDragEnd` callback. For example, `onDragEndParams: ["drag ended", 5]` would work with this code: `onDragEnd: function(message, num) { console.log("message: " + message + ", num: " + num); }`.
- #### onDragStart

  Function - A function that should be called as soon as the mouse (or touch) moves more than 2 pixels, meaning that dragging has begun. Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access `pageX`, `pageY`, `target`, `currentTarget`, etc.
- #### onDragStartParams

  Array - An optional array of parameters to feed the `onDragStart` callback. For example, `onDragStartParams: ["drag started", 5]` would work with this code: `onDragStart: function(message, num) { console.log("message: " + message + ", num: " + num); }`.
- #### onLockAxis

  Function - A function that should be called as soon as movement is locked into the horizontal or vertical axis. This happens when `lockAxis` is `true` and the user drags enough for Draggable to determine which axis to lock. It also happens on touch-enabled devices when you have a Draggable whose type only permits it to drag along one axis (like `type: "x"`, `type: "y"`, `type: "left"`, or `type: "top"`) and the user touch-drags and Draggable determines the direction, either allowing native touch-scrolling or Draggable-induced dragging. Inside the function, `this` refers to the Draggable instance, making it easy to access the locked axis (`this.lockedAxis` which will either be `"x"` or `"y"`), or the target element (`this.target`), etc. By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access `pageX`, `pageY`, `target`, `currentTarget`, etc.
- #### onMove

  Function - A function that should be called every time the mouse (or touch) moves during the drag. Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access its `pageX`, `pageY`, `target`, `currentTarget`, etc. This is different than `onDrag` in that it can fire multiple times per requestAnimationFrame. In general, it is better to use `onDrag`, but this is available if, for some reason, need to `.stopPropogation` or `.stopImmediatePropogation` on the drag event.
- #### onPress

  Function - A function that should be called as soon as the mouse (or touch) presses down on the element. Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access `pageX`, `pageY`, `target`, `currentTarget`, etc.
- #### onPressInit

  Function - A function that should be called before the starting values are recorded in the `onPress`, allowing you to make changes before any dragging occurs. `onPressInit` always fires BEFORE `onPress`. [See demo](//codepen.io/GreenSock/pen/62fd4014cf86a9a87e632c8b4f967ed4/?editors=0010).
- #### onPressParams

  Array - An optional array of parameters to feed the `onPress` callback. For example, `onPressParams: ["drag started", 5]` would work with this code: `onPress: function(message, num) { console.log("message: " + message + ", num: " + num); }`.
- #### onRelease

  Function - A function that should be called as soon as the mouse (or touch) is released after having been pressed on the target element, regardless of whether or not anything was dragged. Inside that function, `this` refers to the Draggable instance (unless you specifically set the scope using `callbackScope`), making it easy to access the target element (`this.target`) or the boundary coordinates (`this.maxX`, `this.minX`, `this.maxY`, and `this.minY`). By default, the `pointerEvent` (last mouse or touch event related to the Draggable) will be passed as the only parameter to the callback so that you can, for example, access `pageX`, `pageY`, `target`, `currentTarget`, etc.
- #### onReleaseParams

  Array - An optional array of parameters to feed the `onRelease` callback. For example, `onReleaseParams: ["drag ended", 5]` would work with this code: `onRelease: function(message, num) { console.log("message: " + message + ", num: " + num); }`.
- #### trigger

  [*Element* | *String* | *Object*] - If you want only a certain area to trigger the dragging (like the top bar of a window) instead of the entire element, you can define a child element as the trigger, like `trigger: yourElement`, `trigger: "#topBar"`, or `trigger: $("#yourID")`. You may define the trigger as an element or a selector string
- #### type

  String - Indicates the type of dragging (the properties that the dragging should affect). Any of the following work: [`"x,y"` (basically the `translateX` and `translateY` of transform) | `"left,top"` | `"rotation"` |`"x"` | `"y"` | `"top"` | `"left"`]. The default is `"x,y"`.
- #### zIndexBoost

  Boolean - By default, for vertical or horizontal dragging, when an element is pressed/touched, it has its `zIndex` set to a high value (`1000` by default) and that number gets incremented and applied to each new element that gets pressed/touched so that the stacking order looks correct (newly pressed objects rise to the top), but if you prefer to skip this behavior set `zIndexBoost: false`.

## Snapping[â](#snapping "Direct link to Snapping")

Draggable has advanced snapping capabilities. You can define a `snap` value in the `config` object to control where the Draggable will snap **AFTER** it is released, or you can define a `liveSnap` value where the Draggable should snap **WHILE** dragging. You can define these values in any of the following ways:

### As an array of snap-to values[â](#as-an-array-of-snap-to-values "Direct link to As an array of snap-to values")

```
Draggable.create('#id', {  
	type: 'x,y',  
	liveSnap: {  
		//snaps to the closest point in the array, but only when it's within 15px (new in GSAP 1.20.0 release):  
		points: [  
			{ x: 0, y: 0 },  
			{ x: 100, y: 0 },  
			{ x: 200, y: 50 }  
		],  
		radius: 15  
	}  
});
```

`points` is a special property that allows you to combine both `x` and `y` logic into a single place. You can also use separate per-property arrays:

```
Draggable.create('#id', {  
	type: 'x,y',  
	liveSnap: {  
		//x and y (or top and left) can each have their own array of values to snap to:  
		x: [0, 100, 200, 300],  
		y: [0, 50, 100, 150]  
	}  
});
```

### As a function with custom logic[â](#as-a-function-with-custom-logic "Direct link to As a function with custom logic")

```
Draggable.create('#id', {  
	type: 'x,y',  
	liveSnap: {  
		points: function (point) {  
			//if it's within 100px, snap exactly to 500,250  
			var dx = point.x - 500;  
			var dy = point.y - 250;  
			if (Math.sqrt(dx * dx + dy * dy) < 100) {  
				return { x: 500, y: 250 };  
			}  
			return point; //otherwise don't change anything.  
		}  
	}  
});
```

Or use separate per-property functions:

```
Draggable.create('#id', {  
	type: 'x,y',  
	liveSnap: {  
		x: function (value) {  
			//snap to the closest increment of 50.  
			return Math.round(value / 50) * 50;  
		},  
		y: function (value) {  
			//snap to the closest increment of 25.  
			return Math.round(value / 25) * 25;  
		}  
	}  
});
```

It's just as simple for a rotation Draggable:

```
Draggable.create('#id', {  
	type: 'rotation',  
	liveSnap: {  
		rotation: function (value) {  
			//snap to the closest increment of 10.  
			return Math.round(value / 10) * 10;  
		}  
	}  
});
```

## Getting the velocity[â](#getting-the-velocity "Direct link to Getting the velocity")

As long as you've loaded InertiaPlugin and set `inertia: true` on your Draggable, you can tap into the `InertiaPlugin.getVelocity()` method. Draggable will automatically start tracking the velocity of the necessary properties based on whatever its `type` is (`type: "x,y"` will track `x` and `y`, `type: "rotation"` will track rotation, etc.).

```
//positional velocity  
Draggable.create('#movableID', {  
	type: 'x,y',  
	inertia: true,  
	onDragEnd: function () {  
		console.log(  
			'x velocity is: ' +  
				InertiaPlugin.getVelocity(this.target, 'x') +  
				' and the duration is ' +  
				this.tween.duration() +  
				' seconds.'  
		);  
	}  
});
```

## Notes, dependencies, and limitations[â](#notes-dependencies-and-limitations "Direct link to Notes, dependencies, and limitations")

- In most cases, [`.pointerX`](/docs/v3/Plugins/Draggable/pointerX) and [`.pointerY`](/docs/v3/Plugins/Draggable/pointerY) should be used instead of using the event's positioning (like `.pageX`/`.pageY` or something like that) because GSAP tries to normalize positioning across all browsers.
- If you want a particular element to be "clickable", thus ignored by Draggable, simply add a `data-clickable="true"` attribute to it, or an `onclick`. By default, Draggable automatically ignores clicks on `<a>`, `<input>`, `<select>`, `<button>`, and `<textarea>` elements. If you prefer to run your own logic to determine if an object should be considered "clickable", you can set the `clickableTest` config property to a function of your choosing that returns `true` or `false`.
- Draggable can be used without InertiaPlugin, but doing so will disable any momentum-based motion (like being able to flick objects and have them continue while decelerating). These two tools go together perfectly ð«¶.
- In order to make things moveable via their `top` and `left` CSS properties, you must make sure that the elements have their `position` CSS property set to either `relative` or `absolute` (that's just how CSS works).
- By default, all callback functions and `snap` functions and `liveSnap` functions are scoped to the associated Draggable instance, so `this` refers to the Draggable instance. You can get the current horizontal or vertical values using `this.x` and `this.y` inside those functions. And if you applied bounds, you can also get the maximum and minimum "legal" values for that particular instance using `this.maxX`, `this.minX`, `this.maxY`, and `this.minY`.
- Having trouble with momentum-based motion? Make sure you have [InertiaPlugin](/docs/v3/Plugins/InertiaPlugin/) loaded! To use it, set `inertia: true` in the `vars` config object, like `Draggable.create(yourObject, {inertia: true});`.
- If you use an element for the bounds, it should not be rotated differently than the target element.
- If you are mixing timelines and draggable, you may need to use a proxy element. For more information see [this demo](https://codepen.io/GreenSock/pen/WNedayo).

## **Properties**[â](#properties "Direct link to properties")

|  |  |
| --- | --- |
| [autoScroll](/docs/v3/Plugins/Draggable/autoScroll) : Number | How fast to scroll the container element when `autoScroll` is `true`. |
| [deltaX](/docs/v3/Plugins/Draggable/deltaX) : Number | The change in the x-related value since the last drag event. |
| [deltaY](/docs/v3/Plugins/Draggable/deltaY) : Number | The change in the y-related value since the last drag event. |
| [endRotation](/docs/v3/Plugins/Draggable/endRotation) : Number | [read-only] [only applies to type:"rotation"] The ending rotation of the Draggable instance which is calculated as soon as the mouse/touch is released after a drag, meaning you can use it to predict precisely where it'll land after a `inertia` flick. |
| [endX](/docs/v3/Plugins/Draggable/endX) : Number | [read-only] The ending x (horizontal) position of the Draggable instance which is calculated as soon as the mouse/touch is released after a drag, meaning you can use it to predict precisely where it'll land after an `inertia` flick. |
| [endY](/docs/v3/Plugins/Draggable/endY) : Number | [read-only] The ending y (vertical) position of the Draggable instance which is calculated as soon as the mouse/touch is released after a drag, meaning you can use it to predict precisely where it'll land after a `inertia` flick. |
| [isPressed](/docs/v3/Plugins/Draggable/isPressed) : Boolean | If the Draggable is being pressed, this will be `true` |
| [isThrowing](/docs/v3/Plugins/Draggable/isThrowing) : Boolean | Reports if the target of a Draggable is being thrown using a InertiaPlugin tween. |
| [lockAxis](/docs/v3/Plugins/Draggable/lockAxis) : Boolean | Locks movement to one axis based on the how it is moved initially. |
| [lockedAxis](/docs/v3/Plugins/Draggable/lockedAxis) : String |  |
| [maxRotation](/docs/v3/Plugins/Draggable/maxRotation) : Number | When bounds are applied, `maxRotation` refers to the maximum "legal" rotation. |
| [maxX](/docs/v3/Plugins/Draggable/maxX) : Number | When bounds are applied, `maxX` refers to the maximum "legal" horizontal property. |
| [maxY](/docs/v3/Plugins/Draggable/maxY) : Number | When bounds are applied, `maxY` refers to the maximum "legal" vertical property. |
| [minRotation](/docs/v3/Plugins/Draggable/minRotation) : Number | When bounds are applied, `minRotation` refers to the minimum "legal" rotation property. |
| [minX](/docs/v3/Plugins/Draggable/minX) : Number | When bounds are applied, `minX` refers to the minimum "legal" horizontal property. |
| [minY](/docs/v3/Plugins/Draggable/minY) : Number | When bounds are applied, `minY` refers to the minimum "legal" vertical property. |
| [pointerEvent](/docs/v3/Plugins/Draggable/pointerEvent) : Object | [read-only] The last pointer event (either a mouse event or touch event) that affected the Draggable instance. |
| [pointerX](/docs/v3/Plugins/Draggable/pointerX) : Number | [read-only] The x (horizontal) position of the pointer (mouse or touch) associated with the Draggable's last event (like event.pageX). |
| [pointerY](/docs/v3/Plugins/Draggable/pointerY) : Number | [read-only] The y (vertical) position of the pointer (mouse or touch) associated with the Draggable's last event (like event.pageY). |
| [rotation](/docs/v3/Plugins/Draggable/rotation) : Number | [read-only] [only applies to `type: "rotation"`] The current rotation (in degrees) of the Draggable instance. |
| [startX](/docs/v3/Plugins/Draggable/startX) : Number | [read-only] The starting `x` (horizontal) position of the Draggable instance when the most recent drag began. |
| [startY](/docs/v3/Plugins/Draggable/startY) : Number | [read-only] The starting `y` (vertical) position of the Draggable instance when the most recent drag began. |
| [target](/docs/v3/Plugins/Draggable/target) : Object | The object that is being dragged. |
| [tween](/docs/v3/Plugins/Draggable/tween) : Tween | [read-only] The Tween instance that gets created as soon as the mouse (or touch) is released (when `inertia` is `true`). This allows you to check its `duration`, `.pause()` or `.resume()` it, change its `timeScale`, or whatever you want. |
| [vars](/docs/v3/Plugins/Draggable/vars) : Object | The `vars` object passed into the constructor which stores configuration variables like `type`, `bounds`, `onPress`, `onDrag`, etc. |
| [x](/docs/v3/Plugins/Draggable/x) : Number | [read-only] The current x (horizontal) position of the Draggable instance. |
| [y](/docs/v3/Plugins/Draggable/y) : Number | [read-only] The current y (vertical) position of the Draggable instance. |
| [zIndex](/docs/v3/Plugins/Draggable/zIndex) : Number | [static] The starting zIndex that gets applied by default when an element is pressed/touched (for positional types, like `"x,y"`, `"top,left"`, etc. |

## **Methods**[â](#methods "Direct link to methods")

|  |  |
| --- | --- |
| [addEventListener](/docs/v3/Plugins/Draggable/addEventListener())( ) ; |  |
| [applyBounds](/docs/v3/Plugins/Draggable/applyBounds())( bounds:Element | String | Object ) ; | Applies new bounds to the Draggable. |
| [Draggable.create](/docs/v3/Plugins/Draggable/static.create())( target:Object, vars:Object ) : Array | [static] A more flexible way to create Draggable instances than the constructor (`new Draggable(...)`). |
| [disable](/docs/v3/Plugins/Draggable/disable())( ) : Draggable | Disables the Draggable instance so that it cannot be dragged anymore (unless `enable()` is called). |
| [enable](/docs/v3/Plugins/Draggable/enable())( ) : Draggable | Enables the Draggable instance. |
| [enabled](/docs/v3/Plugins/Draggable/enabled())( value:Boolean ) : Boolean | Gets or sets the enabled state. |
| [endDrag](/docs/v3/Plugins/Draggable/endDrag())( event:Object ) : void | You may force the Draggable to immediately stop interactively dragging by calling `endDrag()` and passing it the original mouse or touch event that initiated the stop - this is necessary because Draggable must inspect that event for various information like `pageX`, `pageY`, `target`, etc. |
| [Draggable.get](/docs/v3/Plugins/Draggable/static.get())( target:Object ) : Draggable | [static] Provides an easy way to get the Draggable instance that's associated with a particular DOM element. |
| [getDirection](/docs/v3/Plugins/Draggable/getDirection())( from:String | Element ) : String | Returns the `direction` (`"right"` | `"left"` | `"up"` | `"down"` | `"left-up"` | `"left-down"` | `"right-up"` | `"right-down"`) as measured from either where the drag started (the default) or the moment-by-moment velocity, or its proximity to another element that you define. |
| [Draggable.hitTest](/docs/v3/Plugins/Draggable/static.hitTest())( testObject:Object, threshold:[Number | String] ) : Boolean | Provides an easy way to test whether or not the target element overlaps with a particular element (or the mouse position) according to whatever threshold you [optionally] define. |
| [kill](/docs/v3/Plugins/Draggable/kill())( ) : Draggable | Disables the Draggable instance and removes it from the internal lookup table so that it is made eligible for garbage collection and it cannot be dragged anymore (unless `enable()` is called). |
| [startDrag](/docs/v3/Plugins/Draggable/startDrag())( event:Object, align:Boolean ) : void | Forces the Draggable to begin dragging. |
| [Draggable.timeSinceDrag](/docs/v3/Plugins/Draggable/static.timeSinceDrag())( ) : Number | Returns the time (in seconds) that has elapsed since the last drag ended. |
| [update](/docs/v3/Plugins/Draggable/update())( applyBounds:Boolean, sticky:Boolean ) : Draggable | Updates the Draggable's x/y properties to reflect the target element's current position. |

## **Demos**[â](#demos "Direct link to demos")

Check out the full collection of [How-to demos](https://codepen.io/collection/AtuHb) and our favourite [inspiring community demos](https://codepen.io/collection/DrQGpM) on CodePen.

## Contents

- [Features](#features)
- [Usage](#usage)
- [**Config Object**](#config-object)
- [Snapping](#snapping)
  - [As an array of snap-to values](#as-an-array-of-snap-to-values)
  - [As a function with custom logic](#as-a-function-with-custom-logic)
- [Getting the velocity](#getting-the-velocity)
- [Notes, dependencies, and limitations](#notes-dependencies-and-limitations)
- [**Properties**](#properties)
- [**Methods**](#methods)
- [**Demos**](#demos)