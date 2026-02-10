# Confirmation Dialogs Can Prevent User Errors — If Not Overused

Source: https://www.nngroup.com/articles/confirmation-dialog/

---

6

# Confirmation Dialogs Can Prevent User Errors — If Not Overused

Jakob Nielsen

![](https://media.nngroup.com/media/people/photos/Jakob-Nielsen-tie-800x800.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Jakob Nielsen](/articles/author/jakob-nielsen/)

February 18, 2018
2018-02-18

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Confirmation Dialogs Can Prevent User Errors — If Not Overused&body=https://www.nngroup.com/articles/confirmation-dialog/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/confirmation-dialog/&title=Confirmation Dialogs Can Prevent User Errors — If Not Overused&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/confirmation-dialog/&text=Confirmation Dialogs Can Prevent User Errors — If Not Overused&via=nngroup)

Summary: 
8 UX guidelines to avoid many serious user errors reduce the risk that people automatically agree to a warning without realizing the consequences.

Errors are a big deal for UX. They represent one of the [5 key quality components of usability](https://www.nngroup.com/articles/usability-101-introduction-to-usability/): error frequency and severity are negatively related to the usability of a system. And error prevention is one of the [10 heuristics for user interface design](https://www.nngroup.com/articles/ten-usability-heuristics/).

Even though we talk about “user error,” the [true culprit is the designer](https://www.nngroup.com/articles/error-prevention/), for having made it too easy for users to get into trouble. We cannot assume that people will always use our design in the intended manner.

There are many ways to [prevent (or at least reduce) user errors](https://www.nngroup.com/articles/user-mistakes/). Here, we’ll focus on one of the simplest — the confirmation dialog.

> **Confirmation dialog:** Asks users whether they are sure that they want to proceed with a command that they have just issued to a system.

In graphical user interfaces, a confirmation dialog usually takes the form of a [modal dialog box](https://www.nngroup.com/articles/modal-nonmodal-dialog/) that pops up and must be attended to before the system will execute the user’s command. (Other interaction styles may use different formats for confirmation dialogs. For example, a [voice UI](https://www.nngroup.com/articles/voice-interaction-ux/) might use a spoken question that the user can reply to with a “yes” or a “no.”) Whatever the format, confirmation dialogs constitute an interruption initiated by the system; they slow down the user’s task flow. If this delay prevents an error, then it’s time well spent, but, if not, they are disruptive and thus annoying.

Windows 10 offers a good example of a confirmation dialog when the user attempts to empty a recycle bin that contains a single file:

![Windows 10 delete-file (one file)](https://media.nngroup.com/media/editor/2018/01/23/windows-10-delete-file-confirm.png)

*Windows 10: The confirmation dialog to delete a single file is an example of good (though not perfect) design.*

However, when the recycle bin contains multiple files, Windows 10 uses a less usable confirmation dialog:

![Windows 10: delete files (2 files)](https://media.nngroup.com/media/editor/2018/01/23/windows-10-delete-multiple-confirm.png)

*Windows 10: The confirmation dialog to delete multiple files displays questionable design.*

First of all, why does Windows use two different icons to represent the same issue (permanent file deletion)? The X and the exclamation mark are both [reasonable icons](https://www.nngroup.com/articles/icon-usability/) for this type of warning, but pick one, for the sake of [consistency](https://www.nngroup.com/articles/do-interface-standards-stifle-design-creativity/) (another top-10 UI heuristic). However, this is a minor issue, since I’m sure users don’t base their response to these dialogs on an analysis of the icons.

The problem with the multiple-file confirmation plagues many confirmation dialogs: **lack of specificity.** Saying *these 2 items* doesn’t tell users which files will be deleted. In contrast, the single-file confirmation shows the name of the file, as well as some supplementary info that’ll help the user determine whether the right file will be deleted. (For even better usability, display a thumbnail of the file instead of a generic icon.) Admittedly, it’s hard to provide much detail when many files are being deleted, and stating the number of files is one small amount of specificity.

Let’s go back to basics: why have confirmation dialogs in the first place? To **allow users a second chance** to check their work before proceeding with a dangerous action. However, it’s not a second chance at all if users automate their response to the conformation and simply click *Yes* without thinking further.

A confirmation dialog must restate the user’s request and explain what the computer is about to do, with specific information that allows users to understand the effects of their action. Without identifying details it’s useless to ask users to confirm a request, as shown by the video-delete confirmation from YouTube:

![YouTube confirmation dialog](https://media.nngroup.com/media/editor/2018/01/23/youtube-permanently-delete.png)

*YouTube: The confirmation dialog to delete a video lacks specificity. It’s admittedly helpful that the dialog ups the ante by saying* “You can’t undo this,” *though it would be much better if the system provided resilience by keeping a backup copy of the deleted video around for a little time, so that the user could in fact undo a deletion.*

When users are asked *Are you sure you want to do this?* without further details, the only sensible reaction is “of course I want to do the thing I just told you to do,” and hit *Yes* without further thinking. Such automated behavior provides no protection at all, and only serves to [annoy users](https://www.nngroup.com/articles/does-user-annoyance-matter/) — and make them pay less attention to future warnings.

## Guidelines for Confirmation Dialog Design

1. Use a confirmation dialog before committing to **actions with serious consequences** — such as destroying users’ work or costing large amounts of money. In particular, consider a confirmation dialog before actions that cannot be undone. (Though as mentioned, do try your best to offer undo — a key component of another usability heuristic, user control and freedom — in order to reduce anxiety and allow users to recover from major problems.)
2. Do not use confirmation dialogs for **routine actions**. Like in Aesop’s fable, if you cry wolf too many times, people will stop paying attention to the question, and the confirmation dialog will lose its power to prevent errors.
3. Be **specific** and inform users about the consequence of their action. Do not ask *Are you sure you want to do this?* Instead, explain what *this* is, in [user-centric terms](https://www.nngroup.com/articles/user-centric-language/) that are [easy to understand](https://www.nngroup.com/articles/legibility-readability-comprehension/) and make it likely that the user would recognize a mistake.
4. Instead of *Yes/No* answers, provide **response options that summarize** what will happen for each possible response. For example, in the case of file deletion, use buttons labeled *Delete file* and *Keep file*.
5. Consider using [progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/) to allow users to **find out more** about the consequences of their command before they commit, while still keeping the text in the confirmation dialog brief enough to be easily [scannable](https://www.nngroup.com/articles/how-users-read-on-the-web/).
   ![Microsoft Word confirmation dialog with progressive disclosure](https://media.nngroup.com/media/editor/2018/01/23/msword-confirmation-progressive-disclosure.png)

   *Microsoft Word: This confirmation dialog is too verbose, but the* Tell Me More *button is a good example of using progressive disclosure to keep secondary content out of most people’s eyes.*
6. Avoid giving confirmation dialogs a **default** *Yes* answer. Usually it’s good to have the most common options as the [default](https://www.nngroup.com/articles/the-power-of-defaults/) in a dialog box: doing so saves users time and also educates newbies as to the most likely answer. However, the entire purpose of confirmations is to make sure that users double-check their action and don’t proceed unless they’re really sure that they want to perform the dangerous action. You could potentially make *No* into the default, but it’s probably best not to have a default answer at all.
7. For particularly dangerous operations, require a **nonstandard action** from the user to confirm. Rather than simply clicking an *OK* button (or, better, a button with a word or two to describe the action) — which risks becoming an automated behavior — have people do something they would normally not do. For example, type a word into a box, as MailChimp requires before deleting a mailing list. (Don Norman goes so far as to suggest [requiring a different user to confirm](https://www.fastcodesign.com/90157153/don-norman-what-went-wrong-in-hawaii-human-error-nope-bad-design) the most dangerous actions.) Such nonstandard response options have to be reserved for the most dangerous and rare actions, because, if they’re used too frequently, they become a new standard and risk turning into yet another automated behavior that loses its power to make the user think through the consequences before committing.
   ![MailChimp confirmation dialog box](https://media.nngroup.com/media/editor/2018/01/23/mailchimp-type-delete-confirm.png)

   *MailChimp: Confirmation dialog to delete a mailing list follows several of our confirmation-dialog guidelines: (1) specificity through the name of the list and (probably more important) the number of subscribers; (2) extra protection against automated behavior by forcing the user to explicitly type in the word* DELETE*; moreover, the type-in field doesn’t appear until after the user has scrolled. Such a heavy-handed confirmation dialog should be reserved for the most serious cases. (An even better design would provide the user with the opportunity to undo this destructive action.)*
8. Consider a [customization option](https://www.nngroup.com/articles/customization/) that allows the user to **bypass future routine confirmations**. (See the *Do not ask me again about converting documents* checkbox from Microsoft Word under guideline #5.) It’s true that guideline #2 says not to use routine confirmations; however, for educational purposes, occasionally you may want to provide confirmations anyway when introducing new features with undesired side effects, even though these effects are not serious. Such confirmations ought to be temporary, and you should offer users a way to avoid them.

There is admittedly a tension between guidelines #1 and #2: you want to warn against serious consequences, but you don’t want to warn so often that the warning is overlooked and the answer becomes an automated behavior. The solution is to conduct a task analysis to determine the severity of different outcomes and the frequency of possible user actions. For example, a banking site might be [personalized](https://www.nngroup.com/articles/personalization/) to only require confirmation for online payments that are at least twice the amount of each user’s normal range of payments: if I usually pay bills that are around $100–$500, then my first request to pay somebody $1,100 could well be an error, and the desired payment might only be $110. Even if I did want to pay $1,100, I might welcome the chance to doublecheck a payment that would be big — and thus scary — for me. On the other hand, somebody who pays $10,000 bills several times per day would be annoyed to be interrupted for a $1,100 payment. (“Twice the usual amount” is just an example, and not necessarily the optimal threshold — determining that requires user research.)

[Microsoft provides an even larger set of design guidelines](https://msdn.microsoft.com/en-us/library/windows/desktop/dn742470.aspx) for confirmation dialogs, including how to handle bulk confirms for a sequence of actions. Ultimately, though, I think the most important usability considerations in confirmation dialogs is to **not overuse** them and to be sufficiently **specific** that users know what they’re agreeing to. I say again: if you warn people too much, they stop paying attention. If I said this a few more times, you would stop reading.

Finally, for improved total user experience, beyond the design of the dialog box itself, do go to great lengths to provide **undo**, because some user errors will remain despite the even the best of confirmation dialogs. All you can do is to reduce the number of user errors, but that’s an extremely worthy goal that will increase customer satisfaction, possibly save lives, and definitely increase the business value of your design.

## Related Courses

- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=confirmation-dialog&pt=article)

errors,Application Design

## Related Topics

- Application Design
  [Application Design](/topic/applications/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Check_Error_Message_Quality_With_a_Scoring_Rubric_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Check Error-Message Quality with a Scoring Rubric

  Evan Sunwall
  ·
  4 min](/videos/error-message-scoring-rubric/?lm=confirmation-dialog&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Create_Efficient_Error_Messages_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Create Efficient Error Messages

  Evan Sunwall
  ·
  4 min](/videos/efficient-error-messages/?lm=confirmation-dialog&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Error_Messages_101_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Error Messages 101

  Tim Neusesser
  ·
  3 min](/videos/error-messages-101/?lm=confirmation-dialog&pt=article)

## Related Articles:

- [What the Erroneous Hawaiian Missile Alert Can Teach Us About Error Prevention

  Kim Flaherty
  ·
  6 min](/articles/error-prevention/?lm=confirmation-dialog&pt=article)
- [Preventing User Errors: Avoiding Conscious Mistakes

  Page Laubheimer
  ·
  9 min](/articles/user-mistakes/?lm=confirmation-dialog&pt=article)
- [Preventing User Errors: Avoiding Unconscious Slips

  Page Laubheimer
  ·
  6 min](/articles/slips/?lm=confirmation-dialog&pt=article)
- [Input Controls for Parameters: Balancing Exploration and Precision with Sliders, Knobs, and Matrices

  Page Laubheimer
  ·
  9 min](/articles/sliders-knobs/?lm=confirmation-dialog&pt=article)
- [Onboarding Tutorials vs. Contextual Help

  Page Laubheimer
  ·
  7 min](/articles/onboarding-tutorials/?lm=confirmation-dialog&pt=article)
- [Fitts's Law and Its Applications in UX

  Raluca Budiu
  ·
  10 min](/articles/fitts-law/?lm=confirmation-dialog&pt=article)