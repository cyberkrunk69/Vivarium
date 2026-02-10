# ScrollTrigger | GSAP | Docs & Learning

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/

---

On this page

ScrollTrigger enables anyone to create [jaw-dropping scroll-based animations](https://youtu.be/uYMYlipIReA) with minimal code. Infinitely flexible. Scrub, pin, snap, or just trigger anything scroll-related, even if it has nothing to do with animation.

Detailed walkthrough

Get ahead of the game by also learning about [the most common ScrollTrigger mistakes.](/resources/st-mistakes)

## Simple example[â](#simple-example "Direct link to Simple example")

```
gsap.to('.box', {  
	scrollTrigger: '.box', // start the animation when ".box" enters the viewport (once)  
	x: 500  
});
```

## Advanced example[â](#advanced-example "Direct link to Advanced example")

```
let tl = gsap.timeline({  
	// yes, we can add it to an entire timeline!  
	scrollTrigger: {  
		trigger: '.container',  
		pin: true, // pin the trigger element while active  
		start: 'top top', // when the top of the trigger hits the top of the viewport  
		end: '+=500', // end after scrolling 500px beyond the start  
		scrub: 1, // smooth scrubbing, takes 1 second to "catch up" to the scrollbar  
		snap: {  
			snapTo: 'labels', // snap to the closest label in the timeline  
			duration: { min: 0.2, max: 3 }, // the snap animation should be at least 0.2 seconds, but no more than 3 seconds (determined by velocity)  
			delay: 0.2, // wait 0.2 seconds from the last scroll event before doing the snapping  
			ease: 'power1.inOut' // the ease of the snap animation ("power3" by default)  
		}  
	}  
});  
  
// add animations and labels to the timeline  
tl.addLabel('start')  
	.from('.box p', { scale: 0.3, rotation: 45, autoAlpha: 0 })  
	.addLabel('color')  
	.from('.box', { backgroundColor: '#28a92b' })  
	.addLabel('spin')  
	.to('.box', { rotation: 360 })  
	.addLabel('end');
```

## Standalone/Custom example[â](#standalonecustom-example "Direct link to Standalone/Custom example")

You don't need to put ScrollTriggers directly into animations (though that's probably the most common use case). Use the callbacks for anything...

```
ScrollTrigger.create({  
	trigger: '#id',  
	start: 'top top',  
	endTrigger: '#otherID',  
	end: 'bottom 50%+=100px',  
	onToggle: (self) => console.log('toggled, isActive:', self.isActive),  
	onUpdate: (self) => {  
		console.log(  
			'progress:',  
			self.progress.toFixed(3),  
			'direction:',  
			self.direction,  
			'velocity',  
			self.getVelocity()  
		);  
	}  
});
```

## Features[â](#features "Direct link to Features")

Feature Highlights

- **Link any animation to a particular element** so that it only plays when that element is in the viewport. This improves performance and ensures that your beautiful animations actually get seen!
- ScrollTriggers can perform an actions on an animation (play, pause, resume, restart, reverse, complete, reset) when entering/leaving the defined area or link it directly to the scrollbar so that it acts like a **scrubber** (`scrub: true`).
- **Soften the link between the animation and the the scrollbar** so that takes a certain amount of time to "catch up", like `scrub: 1` would take one second to catch up.
- **Integrated with [ScrollSmoother](/docs/v3/Plugins/ScrollSmoother)**, GreenSock's smooth-scrolling tool built on native scroll technology (members-only benefit).

**read more...**

- **Snap to certain points in the animation** based on velocity. In fact, you can `getVelocity()` of the scrolling anytime. Snap to the closest label in a timeline or progress value in an Array, or run your own custom function-based logic for snapping
- **Embed scroll triggers directly into any GSAP animation** (including timelines) or create **standalone instances** and tap into the rich callback system to do anything you want.
- **Advanced pinning** capabilities can lock an element in place between certain scroll positions. Padding is automatically added to push other elements down accordingly, so they catch up when the element gets unpinned (disable this with `pinSpacing: false`). You can even pin the same element multiple times at different points.
- **Incredible flexibility for defining scroll positions** - like *"start when the center of this element hits the center of the viewport, and end when the bottom of that other element hits the bottom of the viewport"*, use keywords (top, center, bottom, left, right), percentages, pixels, or even relative values like `"+=300px"`. Once you get the hang of the syntax, it's remarkably intuitive.
- Accommodates **vertical or horizontal scrolling**.
- **Rich callback system** including onEnter, onLeave, onEnterBack, onLeaveBack, onToggle, onUpdate, onScrubComplete, and onRefresh.
- **Automatically recalculates positions** when the window resizes.
- **Enable visual markers** during development to see exactly where the start/end/trigger points are. Customization options abound, like `markers: {startColor:"green", endColor:"red", fontSize:"12px"}`.
- **Toggle a CSS class**. For example, `toggleClass: "active"` adds the "active" class to the trigger element while the ScrollTrigger is active. You can affect other elements too.
- **Responsive** - use the [matchMedia()](/docs/v3/GSAP/gsap.matchMedia()) method to create different setups for various screen sizes using standard media queries.
- **Custom containers** - you don't need to use the viewport; define a custom scroller like a `<div>` instead.
- **Highly optimized for maximum performance** - scroll events are debounced, updates are synchronized with GSAP and screen refreshes, resize recalculations are throttled, etc.
- **No scroll-jacking**, so it can be combined with native technologies like CSS scroll snapping. If you want scroll-smoothing, you can use [ScrollSmoother](/docs/v3/Plugins/ScrollSmoother) which integrates seamlessly with ScrollTrigger, or use the [scrollerProxy()](/docs/v3/Plugins/ScrollTrigger/static.scrollerProxy()) method to integrate with a 3rd party smooth-scrolling library.

## **Config Object**[â](#config-object "Direct link to config-object")

`scrollTrigger` can be used as either a shorthand for the `trigger` (described below) or as a configuration object with any of the following properties:

### Property

### Description

- #### animation

  Tween | Timeline - A GSAP [Tween](/docs/v3/GSAP/Tween) or [Timeline](/docs/v3/GSAP/Timeline) instance that should be controlled by the ScrollTrigger. Only one animation is controlled per ScrollTrigger, but you can wrap all your animations in a single Timeline (recommended) or create multiple ScrollTriggers if you prefer.
- #### anticipatePin

  Number - If you pin large sections/panels you may notice what looks like a slight delay in pinning when you scroll quickly. That's caused by the fact that most modern browsers handle scroll repaints on a separate thread, so at the moment of pinning the browser may have already painted the pre-pinned content, making it visible for perhaps 1/60th of a second. The only way to counteract that is to have ScrollTrigger monitor the scroll velocity and anticipate the pin, applying it slightly early to avoid that flash of unpinned content. A value of `anticipatePin: 1` is typically fine, but you can reduce or increase that number to control how early it does the pinning. In many cases, however, you don't need any anticipatePin (the default is 0).
- #### containerAnimation

  Tween | Timeline Easily trigger animations inside 'horizontally' scrolling sections that are controlled by vertical scrolling

  View More details

  A popular effect is to create horizontally-moving sections that are tied to vertical scrolling but since that horizontal movement isn't a native scroll, a regular ScrollTrigger can't know when, for example, an element comes into view horizontally, so you must tell ScrollTrigger to monitor the container's [horizontal] animation to know when to trigger, like `containerAnimation: yourTween`.

   

  **Caveats****:** the container's animation must use a linear ease ( `ease: "none"`). Also, pinning and snapping aren't available on containerAnimation-based ScrollTriggers. You should avoid animating the `trigger` element horizontally or if you do, just offset the start/end values according to how far you're animating the trigger.

  [more information here](/blog/3-8/#containeranimation).
- #### end

  String | Number | Function - Determines the ending position of the ScrollTrigger.

  View More details

  It can be any of the following:

  - **String** - Describes a place on the **endTrigger** (or trigger if one isn't defined) and a place on the **scroller** that must meet in order to end the ScrollTrigger. So, for example, `"bottom center"` means *"when the bottom of the endTrigger hits the center of the scroller"*. `"center 100px"` means *"when the center of the endTrigger hits 100px down from the top of the scroller"* (assuming vertical scroll). You can use keywords like "top", "bottom", "center" (or "left" and "right" if `horizontal: true`) or percentages like "80%" or pixel values like "100px". Percentages and pixels are always relative to the top/left of the element/viewport. You can also define a single relative value like "+=300" which means *"300px beyond where the start is"*, or "+=100%" means *"the height of the scroller beyond where the start is".* `"max"` is a special keyword indicating the maximum scroll position.
  - **Number** - An exact scroll value, so `200` would trigger when the viewport/scroller scrolls by exactly 200 pixels.
  - **Function** - A function that gets called whenever the ScrollTrigger refreshes and calculates its positions (typically upon creation and any time the scroller resizes). It should return a String or Number, as described above. This makes it easy to dynamically calculate values. Like all callbacks, the function receives the ScrollTrigger instance itself as the only parameter. 

  This is a *static* position that is calculated when the ScrollTrigger is created and when the scroller is resized, based on where things are in the normal document flow. It is not constantly recalculated, so for example if you animate the trigger/endTrigger, it won't constantly update the start/end values accordingly because ScrollTrigger is highly optimized for performance. You can call `ScrollTrigger.refresh()` to force things to be recalculated. The default is `"bottom top"`.
  **clamp() the value** *(version 3.12+)*Wrap your end value in `"clamp()"` to tell ScrollTrigger to always keep the calculated value between 0 (the top of the page) and the maximum scroll position so that it'll never leak outside the page bounds. Practically-speaking, this ensures that any trigger elements toward the very bottom of the page won't end with partially-scrubbed animations. For example, `end: "clamp(bottom top)"` - any normal string-based value can be inside the clamp(). Like `"clamp(20px 80%)"`. Here's a video explaining further:
- #### endTrigger

  String | Element - The element (or selector text for the element) whose position in the normal document flow is used for calculating where the ScrollTrigger ends. You don't need to define an `endTrigger` unless it's DIFFERENT than the `trigger` element because that's the default.
- #### fastScrollEnd

  Boolean | Number - if `true`, it will force the current ScrollTrigger's animation to completion if you **leave** its trigger area faster than a certain velocity (default 2500px/s). This helps avoid overlapping animations when the user scrolls quickly. You can specify a number for the minimum velocity, so `fastScrollEnd: 3000` would only activate if the velocity exceeds 3000px/s. See a [demo here](https://codepen.io/GreenSock/pen/7d22c763b9edd0c0c48150ecd1c921c9).
- #### horizontal

  Boolean - By default, it assumes your setup uses vertical scrolling but simply set `horizontal: true` if your setup uses horizontal scrolling instead.
- #### id

  String - An arbitrary unique identifier for the ScrollTrigger instance which can be used with `ScrollTrigger.getById()`. This id is also added to the markers.
- #### invalidateOnRefresh

  Boolean - If `true`, the animation associated with the ScrollTrigger will have its [invalidate()](/docs/v3/GSAP/Tween/invalidate()) method called whenever a refresh() occurs (typically on resize). This flushes out any internally-recorded starting values.
- #### markers

  Object | Boolean - Adds markers that are helpful during development/troubleshooting. `markers: true` adds them with the defaults (startColor: "green", endColor: "red", fontSize: "16px", fontWeight: "normal", indent: 0) but you can customize them by using an object like 

  ```
  markers: {startColor: "white", endColor: "white", fontSize: "18px", fontWeight: "bold", indent: 20}
  ```
- #### once

  Boolean - If `true`, the ScrollTrigger will kill() itself as soon as the end position is reached once. This causes it to stop listening for scroll events and it becomes eligible for garbage collection. This will only call onEnter a maximum of one time as well. It does **not** kill the associated animation. It's perfect for times when you only want an animation to play once when scrolling forward and never get reset or replayed. It also sets the toggleActions to "play none none none".
- #### onEnter

  Function - A callback for when the scroll position moves forward past the "start" (typically when the trigger is scrolled into view). It receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onEnter: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onEnterBack

  Function - A callback for when the scroll position moves backward past the "end" (typically when the trigger is scrolled back into view). It receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onEnterBack: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onLeave

  Function - A callback for when the scroll position moves forward past the "end" (typically when the trigger is scrolled out of view). It receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onLeave: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onLeaveBack

  Function - A callback for when the scroll position moves backward past the "start" (typically when the trigger is scrolled all the way backward past the start). It receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onLeaveBack: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onRefresh

  Function - A callback for when the a refresh occurs (typically a resize event) which forces the ScrollTrigger to recalculate all of its positioning. It receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onRefresh: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onUpdate

  Function - A callback that gets called every time the progress of the ScrollTrigger changes (meaning the scroll position changed). If you have a numeric `scrub` applied, keep in mind that the associated animation will keep scrubbing for a little while after the scroll position stops, so if your goal is to update something whenever the animation updates, it's best to apply an `onUpdate` to the animation itself rather than the ScrollTrigger. [See a demo here](https://codepen.io/osublake/pen/2152a28cffe2c2c0cca8a3e47f7b21c6?editors=0010).

  The onUpdate callback receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`.

   Example: 

  ```
  onUpdate: self => console.log("progress", self.progress)
  ```
- #### onScrubComplete

  Function - A callback for when a numerical scrub has completed. This is only useful when a numerical scrub (like `scrub: 1`) is applied. The callback receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onScrubComplete: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onSnapComplete

  Function - A callback for when the snapping has completed. This only applies when there's a `snap` defined. A snap will be cancelled if/when the user (or anything else) interacts in any way with scrolling, so the onSnapComplete would not be triggered at all in that case. The callback receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onSnapComplete: ({progress, direction, isActive}) => console.log(progress, direction, isActive)
  ```
- #### onToggle

  Function - A callback for when the ScrollTrigger toggles from inactive to active **or** the other way around. This is typically when the scroll position moves past the "start" or "end" in either direction, but if it shoots past BOTH on the same tick, like if the user scrolls extremely fast, onToggle won't fire because the state hasn't changed. You can often use this one callback in the place of onEnter, onLeave, onEnterBack, and onLeaveBack by just checking the isActive property for toggling things. It receives one parameter - the ScrollTrigger instance itself which has properties/methods like `progress`, `direction`, `isActive`, and `getVelocity()`. Example: 

  ```
  onToggle: self => console.log("toggled to active:", isActive)
  ```
- #### pin

  Boolean | String | Element - An element (or selector text for the element) that should be pinned during the time that the ScrollTrigger is active, meaning it will appear to "stick" in its starting position while the rest of the content continues scrolling underneath it. Only one pinned element is allowed, but it can contain as many elements as you want. Setting `pin: true` will cause it to pin the `trigger` element.

  **Warning** don't animate the pinned element itself because that will throw off the measurements (ScrollTrigger is highly optimized for performance and pre-calculates as much as possible). Instead, you could nest things such that you're animating only elements INSIDE the pinned element.

  **Note:** if you are pinning something that is nested *inside* another element that *also* gets pinned, make sure you define a `pinnedContainer` so that ScrollTrigger knows to offset the start/end positions accordingly.

  Using React? Make sure to do proper cleanup - read [this article](/resources/React).
- #### pinnedContainer

  Element | String - If your ScrollTrigger's `trigger`/`endTrigger` element is **INSIDE** an element that gets pinned by *another* ScrollTrigger (pretty uncommon), that would cause the start/end positions to be thrown off by however long that pin lasts, so you can set the `pinnedContainer` to that parent/container element to have ScrollTrigger calculate those offsets accordingly. Again, this is very rarely needed. **Important**: nested pinning is not supported, so this feature is only for non-pinning ScrollTriggers

  *(added in 3.7.0)*
- #### pinReparent

  Boolean - If `true`, the pinned element will be reparented to the `<body>` while it is actively pinned so that it can escape any ancestor containing blocks. If you notice odd behavior while pinning (like the pinned element suddenly shifting and then moving with the scroll), you probably have a `transform` or `will-change` on an ancestor element which [breaks](https://stackoverflow.com/questions/15194313/transform3d-not-working-with-position-fixed-children) `position: fixed` behavior (it's a browser thing, not ScrollTrigger). It's best to set up your project to avoid those because reparenting can be expensive, but `pinReparent: true` can bail you out if you can't avoid them. Only use this feature if you must. 

  **Warning:** if you have CSS rules that rely on specific nesting that'd be affected by the reparenting, they'll break. For example, a CSS rule like `.section .panel p {color: white}` wouldn't apply to the nested `<p>` anymore if you pin the `.panel` element with `pinReparent: true` because during the pin, it would no longer be inside the `<section>`, so make sure you write your CSS rules to accommodate the reparenting.
- #### pinSpacer

  Element | String - normally ScrollTrigger creates a `<div>` internally to wrap around pinned elements but in the *extremely* rare scenario where you're loading an iframe into the pinned element, it can cause the iframe to refresh when ScrollTrigger refreshes (like on window resize), so this feature allows you to specify an element that should be used as the spacer instead of the internally-created one. That way, ScrollTrigger won't remove/add it during its refresh, keeping iframe content intact.
- #### pinSpacing

  Boolean | String - By default, padding will be added to the bottom (or right for `horizontal: true`) to push other elements down so that when the pinned element gets unpinned, the following content catches up perfectly. Otherwise, things may scroll UNDER the pinned element. You can tell ScrollTrigger not to add any padding by setting `pinSpacing: false`.

  View More details

  If you'd rather it use margin instead of padding, you can set `pinSpacing: "margin"`.

  **Note:** pinSpacing works in most cases, but it really depends on the way you set up your DOM and CSS. For example, if you pin something in a parent that has display: flex or position: absolute, the extra padding won't push other elements down/right so you may need to manually space things out. pinSpacing is just a convenience that works in most situations.

  **Important**: if the container is `display: flex`, `pinSpacing` is set to `false` by default because that's typically what is desired since padding works differently in that context.

  This video on pinning that's part of SnorklTV's [ScrollTrigger Express course](https://www.creativecodingclub.com/courses/scrolltrigger-express?ref=44f484) may help your understanding.
- #### pinType

  "fixed" | "transform" - by default, `position: fixed` is used for pinning only if the scroller is the `<body>`, otherwise transforms are used (because `position: fixed` won't work in various nested scenarios), but you can **force** ScrollTrigger to use `position: fixed` by setting `pinType: "fixed"`. Typically this isn't necessary or helpful. Beware that if you set the CSS property `will-change: transform`, browsers treat it just like having a transform applied, breaking `position: fixed` elements (this is unrelated to ScrollTrigger/GSAP).
- #### preventOverlaps

  Boolean | String - this feature activates as a ScrollTrigger is about to trigger an animation; it finds preceding scrollTrigger-based animations and forces those previous animations to their end state â avoiding unsightly overlaps. if `true`, it will affect all preceding ScrollTriggers. You can use an arbitrary string to limit their effect to only others with a matching string. So `preventOverlaps: "group1"` would only affect other ScrollTriggers with `preventOverlaps: "group1"`. See a [demo here](https://codepen.io/GreenSock/pen/7d22c763b9edd0c0c48150ecd1c921c9).
- #### refreshPriority

  number - it's **VERY** unlikely that you'd need to define a `refreshPriority` as long as you create your ScrollTriggers in the order they'd happen on the page (top-to-bottom or left-to-right)...which we *strongly* recommend doing. Otherwise, use `refreshPriority` to influence the order in which ScrollTriggers get refreshed to ensure that the pinning distance gets added to the start/end values of subsequent ScrollTriggers further down the page (that's why order matters). See the [sort()](/docs/v3/Plugins/ScrollTrigger/static.sort()) method for details. A ScrollTrigger with `refreshPriority: 1` will get refreshed earlier than one with `refreshPriority: 0` (the default). You're welcome to use negative numbers too, and you can assign the same number to multiple ScrollTriggers.
- #### scroller

  String | Element - By default, the `scroller` is the **viewport** itself, but if you'd like to add a ScrollTrigger to a scrollable `<div>`, for example, just define that as the scroller. You can use selector text like "#elementID" or the element itself.
- #### scrub

  Boolean | Number - Links the progress of the animation directly to the scrollbar so it acts like a scrubber. You can apply smoothing so that it takes a little time for the playhead to catch up with the scrollbar's position! It can be any of the following 
  - **Boolean** - `scrub: true` links the animation's progress directly to the ScrollTrigger's progress.
  - **Number** - The amount of time (in seconds) that the playhead should take to "catch up", so `scrub: 0.5` would cause the animation's playhead to take 0.5 seconds to catch up with the scrollbar's position. It's great for smoothing things out.
- #### snap

  Number | Array | Function | Object | "labels" | "labelsDirectional" - Allows you to snap to certain progress values (between 0 and 1) after the user stops scrolling. So `snap: 0.1` would snap in increments of 0.1 (10%, 20%, 30%, etc.). `snap: [0, 0.1, 0.5, 0.8, 1]` would only let it come to rest on one of those specific progress values. It can be any of the following...

  View More details

  - **Number** - `snap: 0.1` snaps in increments of 0.1 (10%, 20%, 30%, etc.). If you have a certain number of sections, simply do `1 / (sections - 1)`.
  - **Array** - `snap: [0, 0.1, 0.5, 0.8, 1]` snaps to the closest progress value in the Array in the direction of the last scroll (unless you set `directional: false`).
  - **Function** - `snap: (value) => Math.round(value / 0.2) * 0.2` feeds the natural destination value (based on velocity) into the function and uses whatever is returned as the final progress value (in this case increments of 0.2), so you can run whatever logic you want. These values should always be between 0 and 1 indicating the progress of the animation, so 0.5 would be in the middle.
  - **"labels"** - `snap: "labels"` snaps to the closest label in the timeline (animation must be a timeline with labels, of course)
  - **"labelsDirectional"** - `snap: "labelsDirectional"` snaps to the closest label in the timeline that's in the direction of the most recent scroll. So if you scroll a little bit toward the next label (and stop), even if the current scroll position is technically closest to the current/last label, it'll snap to the next one in that direction instead. This can make it feel more intuitive for users.
  - **Object** - Like `snap: {snapTo: "labels", duration: 0.3, delay: 0.1, ease: "power1.inOut"}`, fully customizable with any of the following properties (only "snapTo" is required):
    - **snapTo** [Number | Array | Function | "labels"] - determines the snapping logic (described above)
    - **delay** [Number] - the delay (in seconds) between the last scroll event and the start of the snapping animation. Default is half the scrub amount (or 0.1 if scrub isn't a number)
    - **directional** [Boolean] - by default (as of version 3.8.0), snapping is directional by default meaning it'll go in the direction the user last scrolled, but you can disable this by setting `directional: false`.
    - **duration** [Number | Object] - the duration of the snapping animation (in seconds). `duration: 0.3` would always take 0.3 seconds, but you can also define a range as an object like `duration: {min: 0.2, max: 3}` to clamp it within the provided range, based on the velocity. That way, if the user stops scrolling close to a snapping point, it'd take less time to snap than if the natural stopping point is far from a snapping point.
    - **ease** [String | Function] - the [ease](/docs/v3/Eases) that the snapping animation should use. The default is "power3".
    - **inertia** [Boolean] - to tell ScrollTrigger **not** to factor in the inertia, set `inertia: false`
    - **onStart** [Function] - a function that should be called when snapping starts
    - **onInterrupt** [Function] - a function that should be called when snapping gets interrupted (like if the user starts scrolling mid-snap)
    - **onComplete** [Function] - a function that should be called when snapping completes
- #### start

  String | Number | Function - Determines the starting position of the ScrollTrigger.

  View More details

  It can be any of the following:
  - **String** - Describes a place on the **trigger** and a place on the **scroller** that must meet in order to start the ScrollTrigger. So, for example, `"top center"` means *"when the top of the trigger hits the center of the scroller"* (and the scroller is the viewport by default). `"bottom 80%"` means *"when the bottom of the trigger hits 80% down from the top of the viewport" (assuming vertical scroll). You can use keywords like "top", "bottom", "center" (or "left" and "right"* if `horizontal: true`) or percentages like "80%" or pixel values like "100px". Percentages and pixels are always relative to the top/left of the element/scroller. You can even use a complex relative value like `"top bottom-=100px"` which means *"when the top of the trigger hits 100px above the bottom of the viewport/scroller"*
  - **Number** - An exact scroll value, so `200` would trigger when the viewport/scroller scrolls by exactly 200 pixels.
  - **Function** - A function that gets called whenever the ScrollTrigger calculates its positions (typically upon creation and any time the scroller resizes). It should return a String or Number, as described above. This makes it easy to dynamically calculate values. Like all callbacks, the function receives the ScrollTrigger instance itself as the only parameter, so you can, for example, base the position on the previous ScrollTrigger's end like `start: self => self.previous().end`

  This is a *static* position that is calculated when the ScrollTrigger is created and when the scroller is resized, based on where things are in the normal document flow. It is not constantly recalculated, so for example if you animate the trigger/endTrigger, it won't constantly update the start/end values accordingly because ScrollTrigger is highly optimized for performance. You can call `ScrollTrigger.refresh()` to force things to be recalculated. The default is `"top bottom"` unless `pin: true` is set in which case the default value is `"top top"`.
  **clamp() the value** *(version 3.12+)*Wrap your start value in `"clamp()"` to tell ScrollTrigger to always keep the calculated value between 0 (the top of the page) and the maximum scroll position so that it'll never leak outside the page bounds. Practically-speaking, this ensures that any "above the fold" (triggers inside the viewport at the top of the page) won't start out with partially-scrubbed animations. For example, `start: "clamp(top bottom)"` - any normal string-based value can be inside the clamp(). Like `"clamp(20px 80%)"`. Here's a video explaining further:
- #### toggleActions

  String - Determines how the linked animation is controlled at the 4 distinct toggle places - **onEnter**, **onLeave**, **onEnterBack**, and **onLeaveBack**, in that order. The default is `play none none none`. So `toggleActions: "play pause resume reset"` will play the animation when entering, pause it when leaving, resume it when entering again backwards, and reset (rewind back to the beginning) when scrolling all the way back past the beginning. You can use any of the following keywords for each action: "play", "pause", "resume", "reset", "restart", "complete", "reverse", and "none".
- #### toggleClass

  String | Object - Adds/removes a class to an element (or multiple elements) when the ScrollTrigger toggles active/inactive. It can be either of the following: 
  - **String** - The name of the class to add to the `trigger` element, like `toggleClass: "active"`
  - **Object** - To toggle a class for elements other than just the trigger, use the object syntax like `toggleClass: {targets: ".my-selector", className: "active"}`. The "targets" can be selector text, a direct reference to an element, or an Array of elements. Note that `toggleActions` don't apply to `toggleClass`. To have toggle class names in a different way, use the callback functions (onEnter, onLeave, onLeaveBack, and onEnterBack).
- #### trigger

  String | Element - The element (or selector text for the element) whose position in the normal document flow is used to calculate where the ScrollTrigger starts.

Looking for Smooth Scrolling?

GSAP's own [ScrollSmoother](/docs/v3/Plugins/ScrollSmoother) tool is built on top of ScrollTrigger, so it is totally integrated and super easy to use. Built on native scroll technology, it avoids most of the accessibility issues that plague other smooth-scrolling libraries.

## **Properties**[â](#properties "Direct link to properties")

|  |  |
| --- | --- |
| [.animation](/docs/v3/Plugins/ScrollTrigger/animation) : Tween | Timeline | undefined | [read-only] The [Tween](/docs/v3/GSAP/Tween) or [Timeline](/docs/v3/GSAP/Timeline) associated with the ScrollTrigger instance (if any). |
| [.direction](/docs/v3/Plugins/ScrollTrigger/direction) : Number | [read-only] Reflects the moment-by-moment direction of scrolling where `1` is forward and `-1` is backward. |
| [.end](/docs/v3/Plugins/ScrollTrigger/end) : Number | [read-only] The ScrollTrigger's ending scroll position (numeric, in pixels). |
| [.isActive](/docs/v3/Plugins/ScrollTrigger/isActive) : Boolean | [read-only] Only `true` if the scroll position is between the start and end positions of the ScrollTrigger instance. |
| [ScrollTrigger.isTouch](/docs/v3/Plugins/ScrollTrigger/static.isTouch) : Number | A way to discern the touch capabilities of the current device - `0` is mouse/pointer only (no touch), `1` is touch-only, `2` accommodates both. |
| [.pin](/docs/v3/Plugins/ScrollTrigger/pin) : Element | undefined | [read-only] The pin element (if one was defined). If selector text was used, like ".pin", the `pin` will be the element itself (not selector text) |
| [progress](/docs/v3/Plugins/ScrollTrigger/progress) : Number | [read-only] The overall progress of the ScrollTrigger instance where 0 is at the start, 0.5 is in the middle, and 1 is at the end. |
| [scroller](/docs/v3/Plugins/ScrollTrigger/scroller) : Element | window | [read-only] The scroller element (or window) associated with the ScrollTrigger. It's the thing whose scrollbar is linked to the ScrollTrigger. By default, it's the window (viewport). |
| [start](/docs/v3/Plugins/ScrollTrigger/start) : Number | [read-only] The ScrollTrigger's starting scroll position (numeric, in pixels). |
| [.trigger](/docs/v3/Plugins/ScrollTrigger/trigger) : Element | undefined | [read-only] The trigger element (if one was defined). If selector text was used, like ".trigger", the `trigger` will be the element itself (not selector text) |
| [.vars](/docs/v3/Plugins/ScrollTrigger/vars) : Object | [read-only] The vars configuration object used to create the ScrollTrigger instance |

## **Methods**[â](#methods "Direct link to methods")

|  |  |
| --- | --- |
| [.disable](/docs/v3/Plugins/ScrollTrigger/disable())( revert:boolean, allowAnimation:Boolean ) | Disables the ScrollTrigger instance, immediately unpinning and restoring any pin-related changes made to the DOM by ScrollTrigger. |
| [.enable](/docs/v3/Plugins/ScrollTrigger/enable())( reset:Boolean ) | Enables the ScrollTrigger instance |
| [.getTween](/docs/v3/Plugins/ScrollTrigger/getTween())( snap:Boolean ) : Tween | Returns the `scrub` tween (default) or the snapping tween (`getTween(true)`) |
| [.getVelocity](/docs/v3/Plugins/ScrollTrigger/getVelocity())( ) : Number | Gets the scroll velocity in pixels-per-second |
| [.kill](/docs/v3/Plugins/ScrollTrigger/kill())( revert:boolean, allowAnimation:Boolean ) | Kills the ScrollTrigger instance, immediately unpinning and restoring any pin-related changes made to the DOM by ScrollTrigger and removing all scroll-related listeners, etc. so that the instance is eligible for garbage collection. If you only want to temporarily disable the ScrollTrigger, use the [disable()](/docs/v3/Plugins/ScrollTrigger/disable()) method instead. |
| [.labelToScroll](/docs/v3/Plugins/ScrollTrigger/labelToScroll())( label:String ) : Number | Converts a timeline label into the associated scroll position (only applicable to ScrollTriggers whose "animation" is a timeline) |
| [.next](/docs/v3/Plugins/ScrollTrigger/next())( ) : ScrollTrigger instance | Returns the next ScrollTrigger in the refresh order. |
| [.previous](/docs/v3/Plugins/ScrollTrigger/previous())( ) : ScrollTrigger instance | Returns the previous ScrollTrigger in the refresh order. |
| [.refresh](/docs/v3/Plugins/ScrollTrigger/refresh())() | Forces the ScrollTrigger instance to re-calculate its start and end values (the scroll positions where it'll be activated). |
| [.scroll](/docs/v3/Plugins/ScrollTrigger/scroll())( position:Number ) : Number | null | Gets/Sets the scroll position of the associated scroller (numeric). |
| [ScrollTrigger.addEventListener](/docs/v3/Plugins/ScrollTrigger/static.addEventListener())( type:String, callback:Function ) : null | Add a listener for any of the following events: "scrollStart", "scrollEnd", "refreshInit", "revert", "matchMedia", or"refresh" which get dispatched globally when **any** such ScrollTrigger-related event occurs (it is not tied to a particular instance). |
| [ScrollTrigger.batch](/docs/v3/Plugins/ScrollTrigger/static.batch())( triggers:Selector text | Array, vars:Object ) : Array | Creates a coordinated group of ScrollTriggers (one for each target element) that batch their callbacks (onEnter, onLeave, etc.) within a certain interval, delivering a neat Array so that you can easily do something like create a staggered animation of all the elements that enter the viewport around the same time. |
| [ScrollTrigger.clearMatchMedia](/docs/v3/Plugins/ScrollTrigger/static.clearMatchMedia())( query:String ) |  |
| [ScrollTrigger.clearScrollMemory](/docs/v3/Plugins/ScrollTrigger/static.clearScrollMemory())( scrollRestoration:String ) | Clears any recorded scroll positions in ScrollTrigger so that no scroll positions get restored after a refresh(). Normally, this isn't necessary but in some frameworks that handle routing in unconventional ways, it can be useful. |
| [ScrollTrigger.config](/docs/v3/Plugins/ScrollTrigger/static.config())( vars:Object ) | Allows you to configure certain global behaviors of ScrollTrigger like `limitCallbacks` |
| [ScrollTrigger.create](/docs/v3/Plugins/ScrollTrigger/static.create())( vars:Object ) : ScrollTrigger | Creates a standalone ScrollTrigger instance |
| [ScrollTrigger.defaults](/docs/v3/Plugins/ScrollTrigger/static.defaults())( config:Object ) : null | Allows you to set the default values that apply to every ScrollTrigger upon creation, like `toggleActions`, `markers`, etc. |
| [ScrollTrigger.getAll](/docs/v3/Plugins/ScrollTrigger/static.getAll())( ) : Array | Returns an Array of all ScrollTrigger instances |
| [ScrollTrigger.getById](/docs/v3/Plugins/ScrollTrigger/static.getById())( id:String ) : ScrollTrigger | Returns the ScrollTrigger that was assigned the corresponding `id` |
| [ScrollTrigger.isInViewport](/docs/v3/Plugins/ScrollTrigger/static.isInViewport())( Element:Element | String, proportion:Number, horizontal:Boolean ) : Boolean | Returns `true` if the element is in the viewport. You can optionally specify a minimum proportion, like `ScrollTrigger.isInViewport(element, 0.2)` would only return `true` if at least 20% of the element is in the viewport. |
| [ScrollTrigger.isScrolling](/docs/v3/Plugins/ScrollTrigger/static.isScrolling())( ) : Boolean | Indicates whether or not any ScrollTrigger-related scroller is in the process of scrolling. |
| [ScrollTrigger.killAll](/docs/v3/Plugins/ScrollTrigger/static.killAll())( ) ; | Immediately calls `kill()` on **all** ScrollTriggers (except the main ScrollSmoother one if it exists). |
| [ScrollTrigger.matchMedia](/docs/v3/Plugins/ScrollTrigger/static.matchMedia())( vars:Object ) | [DEPRECATED] Allows you to set up ScrollTriggers that only apply to certain viewport sizes (using media queries). |
| [ScrollTrigger.maxScroll](/docs/v3/Plugins/ScrollTrigger/static.maxScroll())( scroller:Element | window, horizontal:Boolean ) : Number | A utility function for getting the maximum scroll value for a particular element/scroller. For example, if the element/scroller is 500px tall and contains 800px of content, maxScroll() would return 300. |
| [ScrollTrigger.normalizeScroll](/docs/v3/Plugins/ScrollTrigger/static.normalizeScroll())( normalize:Boolean | Object ) : ScrollObserver | null | Forces scrolling to be done on the JavaScript thread, ensuring screen updates are synchronized and the address bar doesn't show/hide on [most] mobile devices. |
| [ScrollTrigger.observe](/docs/v3/Plugins/ScrollTrigger/static.observe())( config:Object ) : Observer | Super-flexible, unified way to sense meaningful events across all (touch/mouse/pointer) devices without wrestling with all the implementation details. Trigger simple callbacks like onUp, onDown, onLeft, onRight, onChange, onHover, onDrag, etc. Functionally identical to [Observer.create()](/docs/v3/Plugins/Observer/static.create()) |
| [ScrollTrigger.positionInViewport](/docs/v3/Plugins/ScrollTrigger/static.positionInViewport())( element:Element | String, referencePoint:String | Number, horizontal:Boolean ) : Number | Returns a normalized value representing the element's position in relation to the viewport where 0 is at the top of the viewport, 0.5 is in the center, and 1 is at the bottom. So, for example, if the top of the element is 80% down from the top of the viewport, the following code would return 0.8: `ScrollTrigger.positionInViewport(element, "top");` |
| [ScrollTrigger.refresh](/docs/v3/Plugins/ScrollTrigger/static.refresh())( safe:Boolean ) | Recalculates the positioning of all of the ScrollTriggers on the page; this typically happens automatically when the window/scroller resizes but you can force it by calling `ScrollTrigger.refresh()` |
| [ScrollTrigger.removeEventListener](/docs/v3/Plugins/ScrollTrigger/static.removeEventListener())( type:String, callback:Function ) : null | Removes an event listener |
| [ScrollTrigger.saveStyles](/docs/v3/Plugins/ScrollTrigger/static.saveStyles())( targets:String | Element | Array ) | Internally records the current inline CSS styles for the given elements so that when ScrollTrigger reverts (typically for a refresh() or matchMedia() change) those elements will be reverted accordingly even if they had animations that added/changed inline styles. Think of it like taking a snapshot of the inline CSS and telling ScrollTrigger "re-apply these inline styles only and dump all others when you revert internally". |
| [ScrollTrigger.scrollerProxy](/docs/v3/Plugins/ScrollTrigger/static.scrollerProxy())( scroller:String | Element, vars:Object ) | Allows you to hijack the `scrollTop` and/or `scrollLeft` getters/setters for a particular scroller element so that you can implement things like smooth scrolling or other custom effects. |
| [ScrollTrigger.snapDirectional](/docs/v3/Plugins/ScrollTrigger/static.snapDirectional())( incrementOrArray:Number | Array ) : Function | Returns a snapping function to which you can feed any value to snap, along with a direction where `1` is forward (greater than) and `-1` is backward (less than). |
| [ScrollTrigger.sort](/docs/v3/Plugins/ScrollTrigger/static.sort())( func:Function ) : Array | Sorts the internal Array of ScrollTrigger instances to control the order in which they [refresh()](/docs/v3/Plugins/ScrollTrigger/static.refresh()) (calculate their start/end values). |
| [ScrollTrigger.update](/docs/v3/Plugins/ScrollTrigger/static.update())( ) | Checks where the scrollbar is and updates all ScrollTrigger instances' `progress` and `direction` values accordingly, controls the animation (if necessary) and fires the appropriate callbacks. |

## FAQs[â](#faqs "Direct link to FAQs")

#### How does ScrollTrigger work? Is it just like IntersectionObserver?

ScrollTrigger does **NOT** constantly watch every element and check its positioning in the viewport on each tick. We're obsessed with performance and that'd be far too costly. Instead, ScrollTrigger does the processing up-front to figure out where the start/end points are *in the natural document flow*. In other words, *"this ScrollTrigger will be active when the scrollbar is between \_\_\_ and \_\_\_\_"*. Then, it debounces the "scroll" events and only updates things on the next requestAnimationFrame, perfectly synced with GSAP and screen refreshes. It **ONLY** watches the scroll position. **Period.** That means it's ***FAST***.

ScrollTrigger automatically listens for viewport/scroller "resize" events and recalculates all the start/end positions accordingly (`onRefresh`). In fact, since resizing/refreshing is CPU-intensive, it waits until there's a 200ms gap in resize events before starting its work. Yeah, we looked for every opportunity to maximize performance.

[IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) is a native feature in most modern browsers that's different in the following ways:

- It constantly "watches" elements to sense when they enter/leave regardless of scrolling.
- It's **not** helpful for tracking an element's position between two points, like for scrubbing an animation accordingly.
- It does let you watch multiple elements and have a single callback triggered that could loop through and fire a staggered animation on just the elements that entered, for example.

ScrollTrigger does not use IntersectionObserver under the hood because it lacks the necessary functionality and compatibility. You can certainly use IntersectionObserver and ScrollTrigger together.

#### How does pinning work under the hood?

- The pinned element gets immediately wrapped in a `<div>` with a **fixed** width/height to match. A class of "pin-spacer" is added to that wrapper. Think of it like a proxy element that props open the space where the pinned element was in the DOM so that when it flips to `position: fixed` things don't collapse.
- By default, padding will be added to the bottom (or right for horizontal: true) of the pin-spacer so that [in most cases] things get pushed further down/right. When the pinned element gets unpinned, the content below/right will have caught up. So if, for example, the pinned element stays pinned for 300px, there would be padding of 300px added.

walkthrough

This video on pinning that's part of SnorklTV's [ScrollTrigger Express course](https://www.creativecodingclub.com/courses/scrolltrigger-express?ref=44f484) may help your understanding.

- When the ScrollTrigger is active (when the scroll position is between the start and end), it sets the pinned element to `position: fixed` and positions it with fixed top/left/width/height values...unless the scroller isn't the viewport in which case it never uses `position: fixed` because that'd break sub-scrolling, so it uses pure transforms. If `pinReparent` is set to `true` (we recommend avoiding that if you can), the pinned element will get reparented to the `<body>` and styles will be moved inline to ensure appearance is maintained.
- When the ScrollTrigger becomes inactive, the pinned element reverts to its original `position` value and a **transform** is applied to place it correctly.
- When the window/scroller gets resized, all ScrollTriggers re-calculate their start/end positions (`onRefresh`). As a part of that process, the pin-spacer is removed from the DOM and the pinned element is swapped back in so that measurements are accurate with the original CSS. Then the pin-spacer is swapped back in as a wrapper.

Why not just use transforms and avoid `position: fixed`? Many browsers don't render consistently using that technique. There are annoying visual glitches due to the fact that scroll repaints are handled on a different thread in most modern browsers. Surprisingly, `position: fixed` seemed to deliver better performance overall. And performance is EXTREMELY important for scrolling.

#### How does duration work with scrub: true?

If you have a ScrollTrigger `scrub: true` and that ScrollTrigger has a timeline or tween animation associated with it, the durations of tweens within that animation serve as proportions for the total amount of distance that the tween will play. The proportion of how much distance it's animated between is in regards to the total duration of the animation. It's easiest to understand with an example:

Say you have a timeline with three sequenced tweens: a 1 second tween, a 3 second tween, and then another 1 second tween. And the ScrollTrigger applied to it will animate for a full viewport height's distance (perhaps the trigger uses the values of `start: "center bottom"` and `end: "center top"`).

If `scrub: true` (or a number) is applied, then the first tween will be animated between when the center of the trigger element is between the 100% mark (from the top; the bottom of the viewport) and the 80% mark (from the top) of the viewport. The second tween will fire when the center of the element is at the 80% mark until the 20% mark. And the third tween will fire when the center of the element is between the 20% mark and the 0% mark. This is because the total duration of the timeline is 5 seconds. So â is 20% and â is 60%.

#### loading...

If you change the duration of all the tweens to the same number, say 1, then the percentages would all be equal: 100% -> 66%, 66% -> 33%, 33% -> 0%. This is because the total duration is 3, so â is 33%.

In other words, the duration values don't matter as much as the proportions of the duration of each tween compared to the total time of the timeline.

If you want to make the animation take a longer distance of scroll to complete, affect the distance from start to end longer. For example you could set `end: "+=4000"` to make it take a lot of scrolling to complete.

#### How do I include undefined in my project?

See the [installation page](/docs/v3/Installation) for all the options (CDN, NPM, download, etc.) where there's even an interactive helper that provides the necessary code. Easy peasy. Don't forget to [register undefined](/docs/v3/GSAP/gsap.registerPlugin()) like this in your project:

```
gsap.registerPlugin(undefined)
```

#### Is this included in the GSAP core?

No, you must load/import it separately

#### It works fine during development, but suddenly stops working in the production build! What do I do?

Your build tool is probably dropping the plugin when [tree shaking](https://developer.mozilla.org/en-US/docs/Glossary/Tree_shaking) and you forgot to [register undefined](/docs/v3/GSAP/gsap.registerPlugin()) (which protects it from tree shaking). Just register the plugin like this:

```
gsap.registerPlugin(undefined)
```

#### Is it bad to register a plugin multiple times?

No, it's perfectly fine. It doesn't help anything, nor does it hurt.

#### How do I include ScrollTrigger in my project?

See the [installation page](/docs/v3/Installation) for all the options (CDN, NPM, download, etc.) where there's even an interactive helper that provides the necessary code. Easy peasy. Don't forget to [register ScrollTrigger](/docs/v3/GSAP/gsap.registerPlugin()) like this in your project:

```
gsap.registerPlugin(ScrollTrigger)
```

#### Is this included in the GSAP core?

No, you must load/import it separately

#### It works fine during development, but suddenly stops working in the production build! What do I do?

Your build tool is probably dropping the plugin when [tree shaking](https://developer.mozilla.org/en-US/docs/Glossary/Tree_shaking) and you forgot to [register ScrollTrigger](/docs/v3/GSAP/gsap.registerPlugin()) (which protects it from tree shaking). Just register the plugin like this:

```
gsap.registerPlugin(ScrollTrigger)
```

#### Is it bad to register a plugin multiple times?

No, it's perfectly fine. It doesn't help anything, nor does it hurt.

## **Demos**[â](#demos "Direct link to demos")

Check out the full collection of [Scroll animation demos](https://codepen.io/collection/bNPYOw) on CodePen.

## Contents

- [Simple example](#simple-example)
- [Advanced example](#advanced-example)
- [Standalone/Custom example](#standalonecustom-example)
- [Features](#features)
- [**Config Object**](#config-object)
- [**Properties**](#properties)
- [**Methods**](#methods)
- [FAQs](#faqs)
- [**Demos**](#demos)