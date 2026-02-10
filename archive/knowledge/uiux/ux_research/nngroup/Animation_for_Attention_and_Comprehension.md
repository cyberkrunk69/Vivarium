# Animation for Attention and Comprehension

Source: https://www.nngroup.com/articles/animation-usability/

---

8

# Animation for Attention and Comprehension

Aurora Harley

![](https://media.nngroup.com/media/people/photos/Aurora-Harley-20190601SF.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Aurora Harley](/articles/author/aurora-harley/)

September 21, 2014
2014-09-21

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Animation for Attention and Comprehension&body=https://www.nngroup.com/articles/animation-usability/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/animation-usability/&title=Animation for Attention and Comprehension&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/animation-usability/&text=Animation for Attention and Comprehension&via=nngroup)

Summary: 
Moving elements are a powerful tool to attract users’ attention. When designing an animation consider its goal, its frequency of occurrence, and its mechanics.

Thanks to the rise of HTML5 and CSS3 transforms and transitions, animations and movement are becoming increasingly commonplace in modern web design. At a recent web and mobile conference, several of the talks discussed visual design and development considerations for adding interactivity to UI elements. Unfortunately, the majority of conversations around this topic barely address the usability of such animations and what types of motion are most appropriate for different design goals.

Animations and interactivity on web pages usually have one of these user experience objectives:

- Draw **attention to and explain changes** on the page: Changes in the state of an element, revealing and hiding of content, or shifts to another area of content are all common areas for transitional animations.
- Add **fun and whimsy**: Elements that fade in, change color, or otherwise move are thought to delight users and to make a design “pop”. Animations and sound effects are especially common on [sites geared toward children and teens](/reports/topic/young-users/). (Such ploys often distract children; however, because young audiences are less goal-oriented than adults, these effects annoy them less and are better tolerated.)
- Appear **modern and up to date** with new design trends: Use of new technology and techniques in web design is not only an exciting exercise for developers, but presumably communicates an updated brand that is current and knowledgeable.

Before adding animations to a web page or application, ensure that their goal and purpose are well defined. When considering an animation, contemplate the following questions:

1. **User attention**: Where would the user’s attention otherwise be focused at the time when the animation occurs?
2. **Goal of the animation**: Is it to:
   1. Attract users’ attention: is the object to be animated something the user must notice and act on immediately?
   2. [Show continuity in a transition](/articles/guidelines-for-multimedia-on-the-web/) between the states of an object?
   3. Indicate a relationship between objects that are already in the user’s focus of attention?
3. **Frequency of the animation**: How often will one user encounter it during one session?
4. **Mechanics of the animation**: Is it:
   1. Directly caused by a user’s action?
   2. Indirectly triggered (upon page load, while scrolling, or by some other unrelated activity)?

Only once these questions are answered can an appropriate animation be designed.

## In This Article:

- [Users’ Attention: Peripheral Motion Demands Attention](#toc-users-attention-peripheral-motion-demands-attention-1)
- [Goal: Animation to Aid Comprehension and Understanding](#toc-goal-animation-to-aid-comprehension-and-understanding-2)
- [Frequency: Don’t Get in the User’s Way](#toc-frequency-dont-get-in-the-users-way-3)
- [Mechanics: Choosing an Appropriate Animation](#toc-mechanics-choosing-an-appropriate-animation-4)
- [Animated UI: Proceed with Caution](#toc-animated-ui-proceed-with-caution-5)

## Users’ Attention: Peripheral Motion Demands Attention

Movement in a person’s peripheral vision triggers a stimulus-driven shift in visual attention and is an example of bottom–up processing. This is in contrast to a goal-directed shift (top–down processing), where a person voluntarily adjusts attention to an area of interest. The instinctual attention shift to motion is a remnant of the days when we needed to quickly notice a snake in the grass and other forms of looming danger or potential prey (you can decide into which category the snake belongs). (More about top­–down and bottom–up processing in our class on [User Interface Principles that Every Designer Should Know](/courses/hci/).)

On a web page, the periphery generally includes any areas outside the [F-shaped pattern of reading](/articles/f-shaped-pattern-reading-web-content/). Blinking images and video advertisements in the right rail are the most obvious examples of utilizing peripheral animation for business-oriented goals (with their overuse leading to [banner blindness](/articles/banner-blindness-old-and-new-findings/) and [right-rail blindness](/articles/fight-right-rail-blindness/)), but even well-meaning animations can prove to be distracting and annoying (Clippy, we’re looking at you). Notifications appearing near the edges of the screen and promoting related content, recent activity, or the capability of live chat are all examples of peripheral animation that is intended to alert the user to relevant features or content, but in practice can be as interrupting and unwanted as a [pop-up window](/articles/most-hated-advertising-techniques/).

[![Your browser does not support the video tag.](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/slideUp-peripheralElement.png)](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/slideup-peripheralelement.mp4)

*Shortly after loading the homepage of Olark, a* How can we help? *window slides up from the bottom right of the screen with an additional* Hey … *window then popping up above it. While the animation certainly succeeds in alerting the user to the existence of the chat feature, its sudden appearance in the periphery of the user’s vision distracts from the primary task of consuming the main content of the page.*

How fast visual attention shifts toward a moving object in the periphery depends on the **perceived animacy** of the object. Factors such as the increasing speed of the object, the magnitude of its shift in position, and, most importantly, whether this motion appears to be self-propelled (rather than caused by an external collision of some sort) all influence the perception of animacy. In terms of interaction design, this means that elements that slide in or otherwise display a shift in position at any degree of speed will attract attention faster than elements that slowly fade into place.

[![Your browser does not support the video tag.](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/SlideUp-BackToTopElement.png)](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/SlideUp-BackToTopElement.mp4)

*The* Back to Top *link on the Festival of Marketing site slides up from the bottom left of the page as the user scrolls, a motion which immediately draws attention toward the element in the periphery of the screen and distracts from the main task of reading the main page content.*

[![Your browser does not support the video tag.](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/Fade-BackToTopElement.png)](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/Fade-BackToTopElement.mp4)

*The arrow button to scroll back to the top of the page slowly fades in at the right edge of the screen as the user scrolls down the page. This slow animation with no position change is less visually distracting than the slide-in animation seen in the previous example. Of course, another solution, which avoids the issue of possibility interrupting the user from the task of browsing products, is to always display the link somewhere within the page.*

If the goal were to quickly draw attention to the new object, then an animation sliding in from one direction would be very effective. On the other hand, if the goal were to provide access to a contextual feature without interrupting users from their primary task, then a more subtle animation with no position shift would be the better choice. (No animation at all would be the least distracting, and an even better choice if possible.)

## Goal: Animation to Aid Comprehension and Understanding

Motion within a person’s current point of focus does not trigger the same visual response as when it occurs in the periphery. Because we already have the user’s attention, we no longer need to attract it and can focus on designing an animation that will increase the user’s ability to understand the UI: how the element is related to other elements, changes in state for the particular element, and so on.

When used for the right reasons, animating an element on the screen can help convey how that element relates to other elements on the page and to any actions that the user has just taken. For example, if a form contains conditional logic, what the user enters in one field may lead to other dependent fields appearing immediately under that input field. (For instance, in many ecommerce checkout forms, if a user indicates different billing and shipping addresses, the fields for the second address are animated and appear underneath as a result of the user’s action.) This animation reinforces the relationship between the triggering field and the dependent fields.

[![Your browser does not support the video tag.](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/AppearingFormFields.png)](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/AppearingFormFields.mp4)

*Once the checkbox for* My billing address and shipping address are the same *is deselected on the Nest checkout form, the input fields for the billing address are exposed using a slide toggle animation, which clearly indicates the dependent relationship of these new fields. Rechecking the box collapses the then-unneeded fields, as expected.*

For an animation to effectively convey a cause-and-effect relationship between UI elements, the effect must begin **within 0.1 seconds** of the initial user action. This [0.1-second response time](/articles/website-response-times/) maintains the feeling of direct manipulation and supports the perception that the user action caused the new element to appear.

## Frequency: Don’t Get in the User’s Way

Another important aspect to consider when designing an animation is the frequency with which it would likely occur within a single visit of a typical user. Animations that are repeatedly encountered are roadblocks to content and lengthen the amount of time to complete a task. Users do not want to wait and watch a lengthy animation sequence over and over again, especially when it has no purpose other than being “fun” and showing off the coding capabilities of the developer. Remember: just because you can implement an animation, it doesn’t mean that you *should*.

We can’t even count the number of times we’ve sat in user testing and heard test participants utter some variant of the following: *“this [animation] was nice the first time, but now it’s getting annoying.”*

One example of an increasingly common gratuitous animation is the transition associated with revealing a hidden main menu. [Hiding the global navigation](/articles/killing-global-navigation-one-trend-avoid/) is in itself bad, but forcing users to sit through an animation each time the main menu needs to be accessed is even worse. While the animation may be cute and visually appealing the first time, the second viewing is tiresome, and the third is downright [annoying](/articles/does-user-annoyance-matter/) (and may never occur should the user become frustrated and abandon the site entirely).

For example, the website Newton Running buries its 4 navigational options behind the 3-line [hamburger menu icon](https://www.nngroup.com/articles/hamburger-menus/). Clicking the icon triggers an animation that shows the current page zooming out and transforming into a colored square, while other colored squares enter the screen and become the menu options. Once an option is selected, the animation is repeated in reverse and ends with zooming into the newly selected page. Of course there is no way to skip the animation once it has been triggered. Indicating dimensionality is a strongpoint of animations, but in this example the spatial relationship between the pages is meaningless, and the animation is a completely unnecessary roadblock, since the 4 menu options could easily be displayed as static links on the page.

[![Your browser does not support the video tag.](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/Menu-SlowRepeatedAnimation.png)](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/09/09/Menu-SlowRepeatedAnimation.mp4)

*The main menu of* Newton Running *is revealed at the end of a lengthy animation sequence, which is then played in reverse once an option has been selected. Whenever users want to use the main menu, they must endure the entire animation sequence again. Gratuitous, purposeless animations discourage the user from interacting further with the website, as they needlessly waste precious time that could be spent absorbing actual content.*

## Mechanics: Choosing an Appropriate Animation

If you are using an animation within a design, be sure to choose a speed appropriate to the context and the goal of the animation:

- **Slower transitions** are less likely to cause an attention shift and are thus less distracting. They are appropriate for animations indirectly triggered by the user or not user initiated in any way. In these situations, the new element should appear with little or no change in position to minimize distraction.
- **Fast animations** are more likely to attract attention when they happen outside the user’s focus of attention. They are suitable for important elements that users must attend to and act upon.

Fast transitions also waste less of the users’ time. They are appropriate when users trigger the animation directly and are already focused on the element. These types of transitions should not be jarring, however, nor displace any text that the user may still be reading. Although rare, there are times when the [UI is too fast](/articles/too-fast-ux/), and users cannot register the change to respond accordingly.

## Animated UI: Proceed with Caution

Animated user interface elements are tempting and powerful tools, yet they can easily waste a precious currency: users’ attention and time. Employ animations sparingly and only when they add meaning to the interaction. Think about whether the animation will cause an attention shift or not and whether the same user is likely to stumble over it again and again. Will the animation reinforce relationships between UI elements? Will users trigger it directly or not? All these aspects matter in the design of a successful animation.

### References:

Pratt, J., Radulescu, P., Guo, R.M., & Abrams, R.A. (2010). [It's Alive! Animate motion captures visual attention](http://abrams.wustl.edu/artsci/reprints/PrattRadulescuGuoAbrams2010.pdf). *Psychological Science*, 21, 1724–1730. (Warning: link leads to a **PDF file**.)

animation,Design Patterns,Human Computer Interaction,Visual Design,ui elements

## Related Topics

- Design Patterns
  [Design Patterns](/topic/design-patterns/)
- [Human Computer Interaction](/topic/human-computer-interaction/)
- [Visual Design](/topic/visual-design/)

## Learn More:

[![Animations Are Distracting!](https://media.nngroup.com/media/videos/thumbnails/animations-distracting-disigning-appropriate-animations-thumbnail.jpg.1300x728_q75_autocrop_crop-smart_upscale.jpg)](https://www.youtube.com/watch?v=mqyBPuq3enI "Animations Are Distracting! on YouTube (new window)")

Enable cookies
 to watch NN/g videos

Animations Are Distracting!

 Aurora Harley
·
2 min

- [![](https://media.nngroup.com/media/videos/thumbnails/Validate_Your_Visual_Design-_6_Methods.png.650x364_q75_autocrop_crop-smart_upscale.png)

  Validate Your Visual Design: 6 Methods

  Megan Brown
  ·
  5 min](/videos/validate-visual-design/?lm=animation-usability&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Teslers_Law-_Shift_Complexity_to_Simplify_UX_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Tesler’s Law: Shift Complexity to Simplify UX

  Lola Famulegun
  ·
  3 min](/videos/teslers-law/?lm=animation-usability&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Experience_Design_The_Next_Iteration_of_UX_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Experience Design: The Next Iteration of UX?

  Kate Moran
  ·
  4 min](/videos/experience-design/?lm=animation-usability&pt=article)

## Related Articles:

- [Change Blindness in UX: Definition

  Raluca Budiu
  ·
  8 min](/articles/change-blindness-definition/?lm=animation-usability&pt=article)
- [AI-Powered Tools for UX Research in 2023: Issues and Limitations

  Feifei Liu and Kate Moran
  ·
  10 min](/articles/ai-powered-tools-limitations/?lm=animation-usability&pt=article)
- [Accordions on Desktop: When and How to Use

  Huei-Hsin Wang
  ·
  10 min](/articles/accordions-on-desktop/?lm=animation-usability&pt=article)
- [Memory Recognition and Recall in User Interfaces

  Raluca Budiu
  ·
  8 min](/articles/recognition-and-recall/?lm=animation-usability&pt=article)
- [Timing Guidelines for Exposing Hidden Content

  Aurora Harley
  ·
  6 min](/articles/timing-exposing-content/?lm=animation-usability&pt=article)
- [Fitts's Law and Its Applications in UX

  Raluca Budiu
  ·
  10 min](/articles/fitts-law/?lm=animation-usability&pt=article)