# Timeline | GSAP | Docs & Learning

Source: https://gsap.com/docs/v3/GSAP/Timeline/

---

On this page

### Returns : [Timeline](/docs/v3/GSAP/Timeline)[â](#returns--timeline "Direct link to returns--timeline")

A [Timeline](/docs/v3/GSAP/Timeline) is a powerful sequencing tool that acts as a container for tweens and other timelines, making it simple to control them as a whole and precisely manage their timing. Without Timelines, building complex sequences would be far more cumbersome because you'd need to use a `delay` for every animation. For example:

```
// WITHOUT Timelines (only using delays):  
gsap.to("#id", { x: 100, duration: 1 });  
gsap.to("#id", { y: 50, duration: 2, delay: 1 }); //wait 1 second  
gsap.to("#id", { opacity: 0, duration: 1, delay: 3 }); //wait 3 seconds
```

What if you wanted to make the first animation longer? You'd need to adjust *every* delay thereafter. And what if you want to `pause()` the whole sequence or `restart()` it or `reverse()` it on-the-fly or repeat it twice? This could become quite messy, but GSAP's Timelines make it incredibly simple:

0

1

2blueSpin

3

4

Play

```
// then we can control the whole thing easily...  
tl.pause();  
tl.resume();  
tl.seek(1.5);  
tl.reverse();
```

Now we can adjust the timing without worrying about trickle-down changes to delays! Increase the duration of that first tween and everything automatically adjusts.

## Positioning animations in a timeline[â](#positioning-animations-in-a-timeline "Direct link to Positioning animations in a timeline")

The secret to building gorgeous animations with intricate timing is understanding the [position parameter](/resources/position-parameter) which is used in many various Timeline methods. This one super-flexible parameter controls the placement of your tweens, labels, callbacks, pauses, and even nested timelines. In other words, it tells the timeline exactly where to insert the animation. It typically comes after the **vars** parameter and it has multiple behaviors:

- Absolute time, like `3` (a number)

```
//insert exactly 3 seconds from the start of the timeline  
tl.to(".class", { x: 100 }, 3);
```

- Relative time, like `"+=1"` or `"-=1"` (relative to the **end** of the timeline)

```
//create a gap (insert 1 second after end of timeline)  
tl.to(".class", { x: 100 }, "+=1");  
  
//overlap end by 1 second  
tl.to(".class", { y: 100 }, "-=1");
```

- Label, like `"someLabel"`

```
//insert at the "someLabel" label (if it doesn't exist yet, it gets added to the end of the timeline)  
tl.to(".class", { x: 100 }, "someLabel");
```

- Relative to a label, like `"someLabel+=1"`

```
//insert 2 seconds after the "someLabel" label  
tl.to(".class", { x: 100 }, "someLabel+=2");
```

- At the **start** of most recently-added animation, `"<"`

```
//insert at the START of the most recently added animation  
tl.to(".class", { x: 100 }, "<");
```

- At the **end** of the most recently-added animation, `">"`

```
//insert at the END of the most recently added animation  
tl.to(".class", { x: 100 }, ">");
```

- Relative to the start of the most recently-added animation, like `"<1"`

```
//insert 1 second after the START of the most recently added animation  
tl.to(".class", { x: 100 }, "<1");  
  
//insert 2 seconds before the START of the most recently added animation (negative number)  
tl.to(".class", { y: 100 }, "<-2");
```

- Relative to the end of the most recently-added animation, like `">1"`

```
//insert 1 second after the END of the most recently added animation  
tl.to(".class", { x: 100, duration: 1 }, ">1");  
  
//insert 2 seconds before the END of the most recently added animation (negative number)  
tl.to(".class", { y: 100, duration: 1 }, ">-2");
```

**Hint**: think of `"<"` and `">"` as pointers to the start or end of the most recently-added animation.

## Special Properties and Callbacks[â](#special-properties-and-callbacks "Direct link to Special Properties and Callbacks")

Add any of these to your vars object to give your animation special powers:

```
gsap.timeline({  
  onComplete: myFunction,  
  repeat: 2,  
  repeatDelay: 1,  
  yoyo: true,  
});
```

All of timeline's `vars` properties are described below:

### Property

### Description

- #### autoRemoveChildren

  Boolean If `autoRemoveChildren` is set to `true`, as soon as child tweens/timelines complete, they will automatically get killed/removed. This is normally undesireable because it prevents going backwards in time (like if you want to `reverse()` or set the progress lower, etc.). It can, however, improve speed and memory management. The root timelines use `autoRemoveChildren: true`.
- #### callbackScope

  Object The scope to be used for all of the callbacks (`onStart`, `onUpdate`, `onComplete`, etc.). The scope is what `this` refers to inside any of the callbacks.
- #### defaults

  Object A simple way to set defaults that get inherited by the child animations. See the "[defaults](https://gsap.com/docs/v3/GSAP/Timeline#setting-defaults)" section for details.
- #### delay

  Number Amount of delay in seconds before the animation should begin.
- #### onComplete

  Function A function that should be called when the animation has completed.
- #### onCompleteParams

  Array An array of parameters to pass the `onComplete` function. For example, `gsap.timeline({onComplete: myFunction, onCompleteParams: ["param1", "param2"]});`.
- #### onInterrupt

  A function to call when the animation is interrupted min animation. Note that this does not fire if the animation completes normally.
- #### onInterruptParams

  An Array of parameters to pass the onInterrupt function. For example, `gsap.to(".class", {x:100, onInterrupt:myFunction, onInterruptParams:["param1", "param2"]});`.
- #### onRepeat

  Function A function that should be called each time the animation repeats.
- #### onRepeatParams

  Array An Array of parameters to pass the `onRepeat` function. For example, `gsap.timeline({onRepeat: myFunction, onRepeatParams: ["param1", "param2"]});`.
- #### onReverseComplete

  Function A function that should be called when the animation has reached its beginning again from the reverse direction. For example, if `reverse()` is called the tween will move back towards its beginning and when its `time` reaches `0`, `onReverseComplete` will be called. This can also happen if the animation is placed in a timeline instance that gets reversed and plays the animation backwards to (or past) the beginning.
- #### onReverseCompleteParams

  Array An array of parameters to pass the `onReverseComplete` function. For example, `gsap.timeline({onReverseComplete: myFunction, onReverseCompleteParams: ["param1", "param2"]});`.
- #### onStart

  Function A function that should be called when the animation begins (when its `time` changes from `0` to some other value which can happen more than once if the tween is restarted multiple times).
- #### onStartParams

  Array An array of parameters to pass the `onStart` function. For example, `gsap.timeline({onStart: myFunction, onStartParams: ["param1", "param2"]});`.
- #### onUpdate

  Function A function that should be called every time the animation updates (on every frame while the animation is active).
- #### onUpdateParams

  Array An array of parameters to pass the `onUpdate` function. For example, `gsap.timeline({onUpdate: myFunction, onUpdateParams: ["param1", "param2"]});`.
- #### paused

  Boolean If `true`, the animation will pause itself immediately upon creation.
- #### repeat

  Number Number of times that the animation should repeat after its first iteration. For example, if `repeat` is `1`, the animation will play a total of twice (the initial play plus 1 repeat). To repeat indefinitely, use `-1`. `repeat` should always be an integer.
- #### repeatDelay

  Number Amount of time in seconds between repeats. For example, if `repeat` is `2` and `repeatDelay` is `1`, the animation will play initially, then wait for 1 second before it repeats, then play again, then wait 1 second again before doing its final repeat.
- #### repeatRefresh

  Setting `repeatRefresh: true` causes a repeating timeline to `invalidate()` all of its child tweens and re-record their starting/ending values internally on each full iteration (not including yoyo's). This is useful when you use dynamic values (relative, random, or function-based). For example, `x: "random(-100, 100)"` would get a new random x value on each repeat. `duration`, `delay`, and `stagger` do **NOT** refresh.
- #### smoothChildTiming

  Boolean Controls whether or not child animations are repositioned automatically (changing their `startTime`) in order to maintain smooth playback when timing-related properties are changed on-the-fly. For example, imagine that the timelineâs playhead is on a child tween that is 75% complete, moving elementâs left from 0 to 100 and then that tweenâs `reverse()` method is called. If `smoothChildTiming` is `false` (the default except for the globalTimeline), the tween would flip in place, keeping its `startTime` consistent. Therefore the playhead of the timeline would now be at the tweenâs 25% completion point instead of 75%. See the "[How to timelines work?](https://gsap.com/docs/v3/GSAP/Timeline#mechanics)" section for details.
- #### yoyo

  Boolean If `true`, every other repeat cycle will run in the opposite direction so that the tween appears to go back and forth (forward then backward). This has no affect on the `reversed` property though. So if `repeat` is `2` and `yoyo` is `false`, it will look like: start - 1 - 2 - 3 - 1 - 2 - 3 - 1 - 2 - 3 - end. But if `yoyo` is `true`, it will look like: start - 1 - 2 - 3 - 3 - 2 - 1 - 1 - 2 - 3 - end.

## Setting Defaults[â](#setting-defaults "Direct link to Setting Defaults")

Anything in the `defaults` object of a timeline gets inherited by its child animations when they get created, so if you find yourself setting the same `ease` or `duration` (or any value) over and over again, this can help make your code more concise. For example:

```
// WITHOUT defaults (long)  
var tl = gsap.timeline();  
tl.to(".class1", { rotation: -270, duration: 1, ease: "elastic" })  
  .to(".class2", { rotation: -360, duration: 1, ease: "elastic" })  
  .to(".class3", { rotation: -180, duration: 1, ease: "elastic" });  
  
//WITH defaults (shorter)  
var tl = gsap.timeline({ defaults: { duration: 1, ease: "elastic" } });  
tl.to(".class1", { rotation: -270 }) //child tweens will inherit the duration and from the parent timeline!  
  .to(".class2", { rotation: -360 })  
  .to(".class3", { rotation: -180 });
```

Any defaults you set this way will get pushed into every child tween - it's not limited to a certain subset of properties. Inherited defaults are easily overwritten anytime a property is declared on a child animation.

## Nesting[â](#nesting "Direct link to Nesting")

Nest timelines within timelines as deeply as you want. This lets you modularize your code and make it more maintainable. For example, you could build your animation in sections and stitch them together in a master timeline like:

```
function intro() {  
  var tl = gsap.timeline();  
  //...add animations here...  
  return tl;  
}  
  
function middle() {  
  var tl = gsap.timeline();  
  //...add animations here...  
  return tl;  
}  
  
function conclusion() {  
  var tl = gsap.timeline();  
  //...add animations here...  
  return tl;  
}  
  
// stitch them together in a master timeline...  
var master = gsap.timeline();  
master  
  .add(intro())  
  .add(middle(), "+=2") //with a gap of 2 seconds  
  .add(conclusion(), "-=1"); //overlap by 1 second
```

## Other Timeline Features[â](#other-timeline-features "Direct link to Other Timeline Features")

- Speed up or slow down the entire timeline with its `timeScale()` method. You can even tween it to gradually speed up or slow down the animation smoothly!
- Get or set the progress of the timeline using its `progress()` or `totalProgress()` methods (totalProgress() just includes any repeats). For example, to skip to the halfway point, set `myTimeline.progress(0.5);`.
- Tween the `time()`, `totalTime()`, `progress()`, or `totalProgress()` to fast-forward or rewind the timeline. You could even attach a slider to one of these to give the user the ability to drag forward or backward through the timeline.
- Add `onComplete`, `onStart`, `onUpdate`, `onRepeat` and/or `onReverseComplete` callbacks using the constructor's `vars` object like `var tl = gsap.timeline({onComplete: myFunction});`.
- Kill the tweens of a particular object inside the timeline with `killTweensOf(target)` or get the tweens of an object with `getTweensOf()` or get all the tweens and timelines in the timeline with `getChildren()`.
- Set the timeline to repeat any number of times or indefinitely. You can even set a delay between each repeat cycle and/or cause the repeat cycles to yoyo, appearing to reverse direction every other cycle.
- Get the `currentLabel()` or find labels at various positions in the timeline using `nextLabel()` and `previousLabel()`

**Sample code:**

```
// create the timeline that repeats 3 times  
// with 1 second between each repeat and  
// then call myFunction() when it completes  
var tl = gsap.timeline({ repeat: 3, repeatDelay: 1, onComplete: myFunction });  
  
// add a tween  
tl.to(".class", { duration: 1, x: 200, y: 100 });  
  
// add another tween 0.5 seconds after the end  
// of the timeline (makes sequencing easy)  
tl.to("#id", { duration: 0.8, opacity: 0 }, "+=0.5");  
  
// reverse anytime  
tl.reverse();  
  
// Add a "spin" label 3-seconds into the timeline  
tl.addLabel("spin", 3);  
  
// insert a rotation tween at the "spin" label  
// (you could also define the insertion point as the time instead of a label)  
tl.to(".class", { duration: 2, rotation: "+=360" }, "spin");  
  
// go to the "spin" label and play the timeline from there  
tl.play("spin");  
  
// nest another timeline inside your timeline...  
var nested = gsap.timeline();  
nested.to(".class2", { duration: 1, x: 200 });  
tl.add(nested, "+=3"); //add nested timeline after a 3-second gap
```

## How do timelines work?[â](#mechanics "Direct link to How do timelines work?")

Every animation (Tween and Timeline) is placed on a parent Timeline. In a sense, they all have their own playheads (that's what its "time" refers to, or "totalTime" which is identical except that it includes repeats and repeatDelays) and when the parent's playhead moves to a new position, it updates the childrens' too (unless they're paused).

When a timeline renders at a particular time, it loops through its children and says "okay, you should render as if your playhead is at \_\_\_\_" and if that child is a Timeline with children, it does the same to its children, right on down the line. So the playheads generally remain synchronized.

When you unpause an animation (`resume()` or `play()`), it essentially picks up the playhead and moves it so that its internal playhead is synchronized with wherever the parent's playhead is at that moment, thus things play perfectly smoothly. That is, unless the timeline's `smoothChildTiming` is `false` in which case that child won't move - its `startTime` will remain locked to where it was.

So basically when `smoothChildTiming` is `true`, the engine will rearrange things on the fly to ensure the playheads line up so that playback feels seamless and smooth. The same thing happens when you `reverse()` or alter the `timeScale`, etc. - the animation's startTime shifts automatically. But sometimes you might not want that behavior - that's when `smoothChildTiming: false` is handy on a parent timeline.

One more example: let's say you've got a 10-second tween that's just sitting on the root timeline and you're 2-seconds into the tween. Let's assume it started at exactly 0 on the root to make this easy, and then when it's at 2-seconds, you do `tween.seek(5)`. The playhead of the root isn't affected - it keeps going exactly as it always did, but in order to make that tween jump to 5 seconds and play appropriately, the tween's `startTime` gets changed to -3. That way, the tween's playhead and the root playhead are perfectly aligned.

note

- You can access GSAP's global timeline via [`gsap.globalTimeline`](/docs/v3/GSAP/gsap.globalTimeline()) but be careful because if, for example, you pause() or timeScale() it, that affects EVERYTHING including delayedCalls(). You can use [`gsap.exportRoot()`](/docs/v3/GSAP/gsap.exportRoot()) instead to basically wrap all of the existing animations on the root (optionally excluding delayedCalls) into a new Timeline instance, isolating those from future animations you create. For example, if you have a bunch of animations going on in a game and then the user clicks a button to pop open a modal window that should slow all the game animations to 1/10ths speed...but you want you modal animations to be full-speed, that's the perfect case for exportRoot().

## **Properties**[â](#properties "Direct link to properties")

|  |  |
| --- | --- |
| [autoRemoveChildren](/docs/v3/GSAP/Timeline/autoRemoveChildren) : Boolean | If `true`, child tweens and timelines will be removed as soon as they complete. |
| [data](/docs/v3/GSAP/Timeline/data) : \* | A place to store any data you want (initially populated with `vars.data` if it exists). |
| [labels](/docs/v3/GSAP/Timeline/labels) : Object | This stores any labels that have been added to the timeline. |
| [parent](/docs/v3/GSAP/Timeline/parent) : Timeline | The parent [Timeline](/docs/v3/GSAP/Timeline) to which the animation is attached. Anything that's not in a Timeline that you create is placed on the [gsap.globalTimeline](/docs/v3/GSAP/gsap.globalTimeline) by default. |
| [scrollTrigger](/docs/v3/GSAP/Timeline/scrollTrigger): [ScrollTrigger](/docs/v3/Plugins/ScrollTrigger/) | undefined | A handy way to access the ScrollTrigger associated with a timeline. This is only accessible if the timeline has a ScrollTrigger. |
| [smoothChildTiming](/docs/v3/GSAP/Timeline/smoothChildTiming) : Boolean | Controls whether or not child tweens and timelines are repositioned automatically (changing their `startTime`) in order to maintain smooth playback when properties are changed on-the-fly. |
| [vars](/docs/v3/GSAP/Timeline/vars) : Object | The configuration object passed into the original timeline via the constructor, like `gsap.timeline({onComplete: func});` |

## **Methods**[â](#methods "Direct link to methods")

|  |  |
| --- | --- |
| [add](/docs/v3/GSAP/Timeline/add())( child:[Tween | Timeline | Label | Callback | Array], position:[Number | String | Label] ) : self | [override] Adds a tween, timeline, callback, or label (or an array of them) to the timeline. |
| [addLabel](/docs/v3/GSAP/Timeline/addLabel())( label:String, position:[Number | String] ) : self | Adds a label to the timeline, making it easy to mark important positions/times. |
| [addPause](/docs/v3/GSAP/Timeline/addPause())( position:[String | Number | Label], callback:Function, params:Array ) : self | Inserts a special callback that pauses playback of the timeline at a particular time or label. |
| [call](/docs/v3/GSAP/Timeline/call())( callback:Function, params:Array, position:\* ) : self | Adds a callback to the end of the timeline (or elsewhere using the `position` parameter) - this is a convenience method that accomplishes exactly the same thing as `add( gsap.delayedCall(...) )` but with less code. |
| [clear](/docs/v3/GSAP/Timeline/clear())( labels:Boolean ) : self | Empties the timeline of all tweens, timelines, and callbacks (and optionally labels too). |
| [currentLabel](/docs/v3/GSAP/Timeline/currentLabel())( value:String ) : [String | self] | Gets the closest label that is at or before the current time, or jumps to a provided label (behavior depends on whether or not you pass a parameter to the method). |
| [delay](/docs/v3/GSAP/Timeline/delay())( value:Number ) : [Number | self] | Gets or sets the animation's initial `delay` which is the length of time in seconds before the animation should begin. |
| [duration](/docs/v3/GSAP/Timeline/duration())( value:Number ) : [Number | self] | [override] Gets the timeline's duration or, if used as a setter, adjusts the timeline's timeScale to fit it within the specified duration. |
| [endTime](/docs/v3/GSAP/Timeline/endTime())( includeRepeats:Boolean ) : [Number | self] | Returns the time at which the animation will finish according to the parent timeline's local time. |
| [eventCallback](/docs/v3/GSAP/Timeline/eventCallback())( type:String, callback:Function, params:Array ) : [Function | self] | Gets or sets an event callback like `onComplete`, `onUpdate`, `onStart`, `onReverseComplete`, or `onRepeat` along with any parameters that should be passed to that callback. |
| [from](/docs/v3/GSAP/Timeline/from())( target:[ Object | Array | String ], vars:Object, position:[ Number | String ] ) : self | Adds a `.from()` tween to the end of the timeline (or elsewhere using the `position` parameter) - this is a convenience method that accomplishes exactly the same thing as `add( gsap.from(...) )` but with less code. |
| [fromTo](/docs/v3/GSAP/Timeline/fromTo())( target:[ Object | Array | String ], fromVars:Object, toVars:Object, position:[ Number | String ] ) : self | Adds a `.fromTo()` tween to the end of the timeline - this is a convenience method that accomplishes exactly the same thing as `add( gsap.fromTo(...) )` but with less code. |
| [getById](/docs/v3/GSAP/Timeline/getById())( id:String ) : Animation |  |
| [getChildren](/docs/v3/GSAP/Timeline/getChildren())( nested:Boolean, tweens:Boolean, timelines:Boolean, ignoreBeforeTime:Number ) : Array | Returns an array containing all the tweens and/or timelines nested in this timeline. |
| [getTweensOf](/docs/v3/GSAP/Timeline/getTweensOf())( target:[Object | Selector text | Array], nested:Boolean ) : Array | Returns the tweens of a particular object that are inside this timeline. |
| [globalTime](/docs/v3/GSAP/Timeline/globalTime())( localTime:Number ) : Number | Converts a local time to the corresponding time on the [gsap.globalTimeline](/docs/v3/GSAP/gsap.globalTimeline) (factoring in all nesting, timeScales, etc.). |
| [invalidate](/docs/v3/GSAP/Timeline/invalidate())( ) : self | [override] Flushes any internally-recorded starting/ending values which can be useful if you want to restart an animation without reverting to any previously recorded starting values. |
| [isActive](/docs/v3/GSAP/Timeline/isActive())( ) : Boolean | Indicates whether or not the animation is currently active (meaning the virtual playhead is actively moving across this instance's time span and it is not paused, nor are any of its ancestor timelines). |
| [iteration](/docs/v3/GSAP/Timeline/iteration())( value:Number ) : [Number | self] | Gets or sets the iteration (the current repeat) of timelines. |
| [kill](/docs/v3/GSAP/Timeline/kill())( ) : Timeline | Immediately kills the timeline and removes it from its parent timeline, stopping its animation. |
| [killTweensOf](/docs/v3/GSAP/Timeline/killTweensOf())( targets:Selector text | Array | Object, props:String, onlyActive:Boolean ) : Timeline | Kills all of the tweens inside this timeline that affect the provided `targets`. You can optionally specify specific properties that you want killed. |
| [nextLabel](/docs/v3/GSAP/Timeline/nextLabel())( time:Number ) : String | Returns the next label in the timeline from the provided time. If no `time` is provided, the timeline's current playhead time will be used. |
| [pause](/docs/v3/GSAP/Timeline/pause())( atTime:\*, suppressEvents:Boolean ) : self | Pauses the instance, optionally jumping to a specific time. |
| [paused](/docs/v3/GSAP/Timeline/paused())( value:Boolean ) : [Boolean | self] | Gets or sets the animation's paused state which indicates whether or not the animation is currently paused. |
| [play](/docs/v3/GSAP/Timeline/play())( from:\*, suppressEvents:Boolean ) : self | Begins playing forward, optionally from a specific time (by default playback begins from wherever the playhead currently is). |
| [previousLabel](/docs/v3/GSAP/Timeline/previousLabel())( time:Number ) : String | Returns the previous label in the timeline from the provided `time`. If no `time` is provided, the timeline's current playhead time will be used. |
| [progress](/docs/v3/GSAP/Timeline/progress())( value:Number, suppressEvents:Boolean ) : [Number | self] | [override] Gets or sets the timeline's progress which is a value between 0 and 1 indicating the position of the virtual playhead (excluding repeats) where 0 is at the beginning, 0.5 is halfway complete, and 1 is complete. |
| [recent](/docs/v3/GSAP/Timeline/recent())( ) : [Tween | Timeline | Callback] | Returns the most recently added child tween/timeline/callback regardless of its position in the timeline. |
| [remove](/docs/v3/GSAP/Timeline/remove())( value:[Tween | Timeline | Callback | Label] ) : self | Removes a tween, timeline, callback, or label (or array of them) from the timeline. |
| [removeLabel](/docs/v3/GSAP/Timeline/removeLabel())( label:String ) : self | Removes a label from the timeline and returns the time of that label. |
| [removePause](/docs/v3/GSAP/Timeline/removePause())( position:[Number | Label] ) : self | Removes pauses that were added to a timeline via its `.addPause()` method. |
| [repeat](/docs/v3/GSAP/Timeline/repeat())( value:Number ) : [Number | self] | Gets or sets the number of times that the timeline should repeat after its first iteration. |
| [repeatDelay](/docs/v3/GSAP/Timeline/repeatDelay())( value:Number ) : [Number | self] | Gets or sets the amount of time in seconds between repeats. |
| [restart](/docs/v3/GSAP/Timeline/restart())( includeDelay:Boolean, suppressEvents:Boolean ) : self | Restarts and begins playing forward from the beginning. |
| [resume](/docs/v3/GSAP/Timeline/resume())( ) : self | Resumes playing without altering direction (forward or reversed). |
| [reverse](/docs/v3/GSAP/Timeline/reverse())( from:\*, suppressEvents:Boolean ) : self | Reverses playback so that all aspects of the animation are oriented backwards including, for example, a tween's ease. |
| [reversed](/docs/v3/GSAP/Timeline/reversed())( value:Boolean ) : [Boolean | self] | Gets or sets the animation's reversed state which indicates whether or not the animation should be played backwards. |
| [revert](/docs/v3/GSAP/Timeline/revert())( ) : Self | Reverts the Timeline and kills it, returning the targets to their pre-animation state including the removal of inline styles added by the Timeline. |
| [seek](/docs/v3/GSAP/Timeline/seek())( position:\*, suppressEvents:Boolean ) : self | [override] Jumps to a specific time (or label) without affecting whether or not the instance is paused or reversed. |
| [set](/docs/v3/GSAP/Timeline/set())( target:[ Object | Array | String ], vars:Object, position:[ Number | String ] ) : self | Adds a zero-duration tween to the end of the timeline (or elsewhere using the `position` parameter) that sets values immediately when the virtual playhead reaches that position on the timeline - this is a convenience method that accomplishes exactly the same thing as `add( gsap.to(target, {duration: 0, ...}) )` but with less code. |
| [shiftChildren](/docs/v3/GSAP/Timeline/shiftChildren())( amount:Number, adjustLabels:Boolean, ignoreBeforeTime:Number ) : self | Shifts the startTime of the timeline's children by a certain amount and optionally adjusts labels too. |
| [startTime](/docs/v3/GSAP/Timeline/startTime())( value:Number ) : [Number | self] | Gets or sets the time at which the animation begins on its parent timeline (after any delay that was defined). |
| [then](/docs/v3/GSAP/Timeline/then())( callback:Function ) : Promise | Returns a promise so that you can uses promises to track when a tween or timeline is complete. |
| [time](/docs/v3/GSAP/Timeline/time())( value:Number, suppressEvents:Boolean ) : [Number | self] | [override] Gets or sets the local position of the playhead (essentially the current time), not including any repeats or repeatDelays. |
| [timeScale](/docs/v3/GSAP/Timeline/timeScale())( value:Number ) : [Number | self] | Factor that's used to scale time in the animation where 1 = normal speed (the default), 0.5 = half speed, 2 = double speed, etc. |
| [to](/docs/v3/GSAP/Timeline/to())( target:[ Object | Array | String ], vars:Object, position:[ Number | String ] ) : self | Adds a `gsap.to()` tween to the end of the timeline (or elsewhere using the `position` parameter) - this is a convenience method that accomplishes exactly the same thing as `add( gsap.to(...) )` but with less code. |
| [totalDuration](/docs/v3/GSAP/Timeline/totalDuration())( value:Number ) : [Number | self] | Gets or sets the total duration of the timeline in seconds including any repeats or repeatDelays. |
| [totalProgress](/docs/v3/GSAP/Timeline/totalProgress())( value:Number, suppressEvents:Boolean ) : [Number | self] | [override] Gets or sets the timeline's total progress which is a value between 0 and 1 indicating the position of the virtual playhead (including repeats) where 0 is at the beginning, 0.5 is at the halfway point, and 1 is at the end (complete). |
| [totalTime](/docs/v3/GSAP/Timeline/totalTime())( time:Number, suppressEvents:Boolean ) : [Number | self] | Gets or sets the position of the playhead according to the `totalDuration` which includes any repeats and repeatDelays. |
| [tweenFromTo](/docs/v3/GSAP/Timeline/tweenFromTo())( fromPosition:[Number | Label], toPosition:[Number | Label], vars:Object ) : Tween | Creates a linear tween that essentially scrubs the playhead from a particular time or label to another time or label and then stops. |
| [tweenTo](/docs/v3/GSAP/Timeline/tweenTo())( position:[Number | Label], vars:Object ) : Tween | Creates a linear tween that essentially scrubs the playhead to a particular time or label and then stops. |
| [yoyo](/docs/v3/GSAP/Timeline/yoyo())( value:Boolean ) : [Boolean | self] | Gets or sets the timeline's yoyo state, where true causes the timeline to go back and forth, alternating backward and forward on each repeat. |

## Contents

- [Returns : Timeline](#returns--timeline)
- [Positioning animations in a timeline](#positioning-animations-in-a-timeline)
- [Special Properties and Callbacks](#special-properties-and-callbacks)
- [Setting Defaults](#setting-defaults)
- [Nesting](#nesting)
- [Other Timeline Features](#other-timeline-features)
- [How do timelines work?](#mechanics)
- [**Properties**](#properties)
- [**Methods**](#methods)