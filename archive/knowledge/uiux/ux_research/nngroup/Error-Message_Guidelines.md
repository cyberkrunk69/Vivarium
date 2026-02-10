# Error-Message Guidelines

Source: https://www.nngroup.com/articles/error-message-guidelines/

---

6

# Error-Message Guidelines

Tim Neusesser, Evan Sunwall

![](https://media.nngroup.com/media/people/photos/Tim-portrait-2022.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)
![](https://media.nngroup.com/media/people/photos/Evan_Headshot.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Tim Neusesser](/articles/author/tim-neusesser/) and
[Evan Sunwall](/articles/author/evan-sunwall/)

May 14, 2023
2023-05-14

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Error-Message Guidelines&body=https://www.nngroup.com/articles/error-message-guidelines/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/error-message-guidelines/&title=Error-Message Guidelines&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/error-message-guidelines/&text=Error-Message Guidelines&via=nngroup)

Summary: 
Design effective error messages by ensuring they are highly visible, provide constructive communication, and respect user effort.

Over 30 years ago, Jakob Nielsen created [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) as general guidelines for designing digital products. These heuristics equally apply today as they did back then. Usability heuristic #9 emphasizes the importance of good error-message design: "Help Users Recognize, Diagnose, and Recover from Errors." Effectively handling errors is crucial because it's one of the [5 quality components of usable experiences.](https://www.nngroup.com/articles/usability-101-introduction-to-usability/)

> **Error message**: A system-generated interruption to the user's workflow that informs the user of an incomplete, incompatible, or undesirable situation according to the system's implementation.

Quality and error messages rarely go together, though. Product teams can be so focused on designing or engineering the idealistic user path that deviations from that path become a frustrating afterthought.

## In This Article:

- [Visibility Guidelines](#toc-visibility-guidelines-1)
- [Communication Guidelines](#toc-communication-guidelines-2)
- [Efficiency Guidelines](#toc-efficiency-guidelines-3)
- [Mitigate Failure with Novelty in Dire Situations](#toc-mitigate-failure-with-novelty-in-dire-situations-4)
- [Conclusion](#toc-conclusion-5)

## Visibility Guidelines

Error messages must present themselves noticeably and recognizably to users.

**Display the error message close to the error's source.** Reduce [cognitive load](https://www.nngroup.com/articles/minimize-cognitive-load/) by displaying an error indicator adjacent to the interface where the error occurred. [Proximity](https://www.nngroup.com/articles/gestalt-proximity/) helps users associate the error message content with the interface elements needing attention.

![](https://media.nngroup.com/media/editor/2023/04/26/linkedin.jpg)

*Bad: When the user adds an unrecognizable URL to their Instagram profile, the resulting error message is subtly styled and positioned far away from the URL field.*

**Use noticeable, redundant, and accessible indicators.** Text and highlights that are bold, high-contrast, and red are conventional error-message visuals. Use this styling for the message and for the affected elements needing correction. Another technique for improving noticeability is leveraging [carefully designed animations](https://www.nngroup.com/articles/animation-usability/) to guide the user's visual attention for corrections. Remember [accessibility guidelines](https://www.nngroup.com/articles/visual-treatments-accessibility/) to aid the roughly 350 million people worldwide with a color-vision deficiency, and never use exclusively color or animation to indicate errors.

![](https://media.nngroup.com/media/editor/2023/04/26/amazon.jpg)

*Good: Amazon utilizes several techniques to indicate an error: border highlighting, iconography, and red text.*

[![ ](https://media.nngroup.com/media/editor/2023/04/26/cafepress-banner-thumb.jpg)](https://media.nngroup.com/media/editor/2023/04/26/cafepress-banner.mp4)

*Good: CafePress displays an animated banner to attract the user’s attention to the blank customization field.*

**Design errors based on their impact.** Design your error messages to indicate the problem's severity. For example, sometimes users only need to be warned of unexpected or potentially undesirable outcomes but can otherwise advance their workflow. Differentiate between these "good to know" messages from those posing a barrier to the user's progress. For example, conditionally displayed labels, toast notifications, or banners can be used for issues needing minimal user interaction, whereas [modal dialogs](https://www.nngroup.com/articles/modes/) require the user's attention and resolution and should be reserved for severe errors.

![](https://media.nngroup.com/media/editor/2023/04/26/kohls.jpg)

*Good: Kohl’s uses a message without conventional red formatting to notify users about potential shipping delays.*

**Avoid prematurely displaying errors.** Timing is a crucial aspect of designing effective error messages. Presenting errors too early is a [hostile pattern](https://www.nngroup.com/articles/hostile-error-messages/). It’s like grading a test before the student has had a chance to answer. It can make users feel annoyed, belittled, or confused. Don't assume that exploratory interactions (like the user moving text focus from a text box without filling it in) are errors. However, do consider inline, real-time errors for error-prone interactions where users are unlikely to enter the correct information on their first try. This immediate guidance reduces [interaction costs](https://www.nngroup.com/articles/interaction-cost-definition/) for correction.

![](https://media.nngroup.com/media/editor/2023/04/26/clear.jpg)

*Good: CLEAR provides clear, accessible indicators close to the text input about meeting specific password requirements, which could be a highly error-prone interaction.*

![](https://media.nngroup.com/media/editor/2023/04/26/txtdot.jpg)

*Bad: This Texas vehicle-registration–renewal page displays an error if the email text input loses focus while empty, which suggests the user did something wrong by merely exploring the interface.*

## Communication Guidelines

Error messages cannot rely on visuals alone. They must contain copy to elaborate and assist the user with recovering from the error.

**Use human-readable language.** Error messages should be plainspoken using [legible and readable text](https://www.nngroup.com/articles/legibility-readability-comprehension/) (many writing apps can give you feedback on a message's readability). Avoid technical jargon and use language familiar to your users instead. The Web's most common error message, the 404 page, violates this guideline. Hide or minimize the use of obscure error codes or abbreviations; show them for technical diagnostic purposes only.

**Concisely and precisely describe the issue.** Generic messages such as *An error occurred* lack context. Provide descriptions of the exact problems to help users understand what happened. That said, beware of excessive technical precision and accuracy that can undermine understandability. The user's [mental model](https://www.nngroup.com/articles/mental-models/) of how the system works likely differs from the conceptual model of how it was coded.

![](https://media.nngroup.com/media/editor/2023/04/26/disney.jpg)

*Bad: When searching for dining locations with very narrow filters, Disneyworld obfuscates the lack of results with puns instead of clearly conveying the situation.*

**Offer constructive advice.** Merely stating the problem is also not enough; offer some potential remedies. One example is an *Out of stock* message for an ecommerce website. Include details of when the product will be available again or suggest that users sign up for a restock notification by entering their emails.

**Take a positive tone and don't blame the user.** Write with a positive and nonjudgmental [tone of voice](https://www.nngroup.com/articles/tone-of-voice-dimensions/). Don't usephrasing that blames users or implies they are doing something wrong, such as *invalid*, *illegal*, or *incorrect*. The proper usage of any system lies with its creators and not with the system's users, so the system must gracefully adapt and not shift blame. Avoid humor since it can become stale if users encounter the error frequently.

![](https://media.nngroup.com/media/editor/2023/04/26/target.jpg)

*Good: Target gives clear feedback that users must spend more to qualify for same-day shipping. Note how the message avoids blaming the user for not purchasing enough and focuses instead on the threshold.*

![](https://media.nngroup.com/media/editor/2023/04/26/natgeo.jpg)

*Bad: The National Geographic Kids website does not explain itself if an underage user clicks on the shop. A better message would clarify that only adults can use the shop and that the user should ask for their help.*

## Efficiency Guidelines

Good errors go beyond just explaining but protect the user's effort and time. Offer [accelerators](https://www.nngroup.com/articles/ui-accelerators/) to resolve the situation or share a bit of instruction to aid users' understanding and hopefully avoid the problem in the future.

**Safeguard against likely mistakes.** The very worst error messages are those that don't exist. When users make a mistake and receive no feedback, it can create a cascade of misunderstanding, wasted effort, and frustration. Years ago, email apps would dutifully send your email even though it referred to an attachment you forgot to include. Now, most apps will detect this situation and prompt you with an error message before sending it, thus sparing you embarrassment.

![](https://media.nngroup.com/media/editor/2023/04/26/email.jpg)

*Good: Email apps have evolved to detect and warn about common email mistakes, such as forgetting to include attachments.*

**Preserve the user's input.** Let users correct errors by editing their original action instead of starting over. For example, display the original text entered into a text field even if it does not match the requirements for that field and allow the user to modify it.

![](https://media.nngroup.com/media/editor/2023/04/26/instagram.jpg)

*Good: If the user navigates back while adding an image to an Instagram story, the system provides an option to save their work as a draft to avoid losing it.*

**Reduce error-correction effort.** If possible, guess the correct action and let users pick it from a small list of fixes. For example, instead of just saying *City and ZIP code don't match,* let users click on a button for the city that matches the ZIP code they entered.

**Concisely educate on how the system works**. Explain to your users how the system works and how to resolve an error. If additional information is required, use hypertextlinks to connect a concise error message to a page with supplementary material or an explanation of the problem. (Don't overdo this, though.)

![](https://media.nngroup.com/media/editor/2023/04/26/vistaprint.jpg)

*Good: Vistaprint communicates what will happen to text placed outside the printable area for a custom shirt.*

![](https://media.nngroup.com/media/editor/2023/04/26/zazzle.jpg)

*Bad: Although Zazzle displays guides for a shirt's printable area, it does not warn the user about the cut-off text, potentially resulting in designing and purchasing an undesired shirt.*

## Mitigate Failure with Novelty in Dire Situations

The above guidelines are essential and applicable to all error messages. That said, there is one last guideline to consider when the system becomes incapable of serving users in any functional capacity:

**Mitigate total failure with novelty.** Errors are **unenjoyable for everyone involved** as they interfere with user and business goals. Yet sometimes users may encounter an error so catastrophic (e.g., overloaded servers) there is no recourse but to wait or try again later. It's these specific moments (which should be rare and avoided at all costs) where blending an apology with something surprising or novel may salvage a disappointing situation that users will likely remember due to [negativity bias](https://www.nngroup.com/articles/negativity-bias-ux/) and the [peak-end rule](https://www.nngroup.com/articles/peak-end-rule/). Don't underestimate the challenge of communicating humility and delight — especially if user input is in jeopardy or the context has severe implications for users. Yet this tactic might enhance memorability and sustain user interest with low-stakes experiences until the system resumes functioning.

![](https://media.nngroup.com/media/editor/2023/04/26/chatgpt.jpg)

*Good: Generative AI experiences like ChatGPT can use downtime to entertain and teach users about its open-ended capabilities until the service is restored.*

![](https://media.nngroup.com/media/editor/2023/04/26/twitter.jpg)

*Good: Although Twitter stopped using the "Fail Whale" (by artist Yiying Lu) to notify users of service disruptions, the image transcended its error-message status and became famous for its whimsical depiction of effort.*

## Conclusion

Interactions between humans and computers are constantly evolving, but there will inevitably be mistakes, misunderstandings, and, thus, a need for error messages. Follow these guidelines to ease these frustrating moments and help the user accomplish their task efficiently and with renewed confidence.

## Free Downloads

- ![](https://media.nngroup.com/static/img/icons/download_24px.svg)
  [Jakob's Usability Heuristic #9 Poster (PDF)](//media.nngroup.com/media/articles/attachments/NNg_Jakob's_Usability_Heuristic_9.pdf)
- ![](https://media.nngroup.com/static/img/icons/download_24px.svg)
  [Jakob's Usability Heuristic #9 Poster, A4 Size (PDF)](//media.nngroup.com/media/articles/attachments/Heuristic_9_A4-compressed.pdf)
- ![](https://media.nngroup.com/static/img/icons/download_24px.svg)
  [Jakob's Usability Heuristic #9 Poster, Letter Size (PDF)](//media.nngroup.com/media/articles/attachments/Heuristic_9_Letter-compressed.pdf)

## Related Courses

- [#### UX Basic Training

  Foundational concepts that everyone should know

  Interaction](/courses/ux-basic-training/?lm=error-message-guidelines&pt=article)
- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=error-message-guidelines&pt=article)

errors,Heuristic Evaluation,Application Design

## Related Topics

- Heuristic Evaluation
  [Heuristic Evaluation](/topic/heuristic-evaluation/)
- [Application Design](/topic/applications/)

## Learn More:

[![Error Messages 101](https://media.nngroup.com/media/videos/thumbnails/Error_Messages_101_Thumbnail.jpg.1300x728_q75_autocrop_crop-smart_upscale.jpg)](https://www.youtube.com/watch?v=sReni_EeZUM "Error Messages 101 on YouTube (new window)")

Enable cookies
 to watch NN/g videos

Error Messages 101

 Tim Neusesser
·
3 min

- [![](https://media.nngroup.com/media/videos/thumbnails/Check_Error_Message_Quality_With_a_Scoring_Rubric_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Check Error-Message Quality with a Scoring Rubric

  Evan Sunwall
  ·
  4 min](/videos/error-message-scoring-rubric/?lm=error-message-guidelines&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Create_Efficient_Error_Messages_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Create Efficient Error Messages

  Evan Sunwall
  ·
  4 min](/videos/efficient-error-messages/?lm=error-message-guidelines&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Time_to_Make_Tech_Work_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Time to Make Tech Work

  Jakob Nielsen
  ·
  3 min](/videos/make-tech-work/?lm=error-message-guidelines&pt=article)

## Related Articles:

- [How to Conduct a Heuristic Evaluation

  Kate Moran and Kelley Gordon
  ·
  6 min](/articles/how-to-conduct-a-heuristic-evaluation/?lm=error-message-guidelines&pt=article)
- [10 Usability Heuristics for User Interface Design

  Jakob Nielsen
  ·
  8 min](/articles/ten-usability-heuristics/?lm=error-message-guidelines&pt=article)
- [Evaluate Interface Learnability with Cognitive Walkthroughs

  Kim Flaherty
  ·
  8 min](/articles/cognitive-walkthroughs/?lm=error-message-guidelines&pt=article)
- [10 Design Guidelines for Reporting Errors in Forms

  Rachel Krause
  ·
  6 min](/articles/errors-forms-design-guidelines/?lm=error-message-guidelines&pt=article)
- [Memory Recognition and Recall in User Interfaces

  Raluca Budiu
  ·
  8 min](/articles/recognition-and-recall/?lm=error-message-guidelines&pt=article)
- [Match Between the System and the Real World (Usability Heuristic #2)

  Anna Kaley
  ·
  5 min](/articles/match-system-real-world/?lm=error-message-guidelines&pt=article)