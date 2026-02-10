# Placeholders in Form Fields Are Harmful

Source: https://www.nngroup.com/articles/form-design-placeholders/

---

5

# Placeholders in Form Fields Are Harmful

Katie Sherwin

![](https://media.nngroup.com/media/people/photos/Katie_Sherwin_portrait.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Katie Sherwin](/articles/author/katie-sherwin/)

May 11, 2014 · Updated Sep. 10, 2018
2018-09-10

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Placeholders in Form Fields Are Harmful&body=https://www.nngroup.com/articles/form-design-placeholders/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/form-design-placeholders/&title=Placeholders in Form Fields Are Harmful&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/form-design-placeholders/&text=Placeholders in Form Fields Are Harmful&via=nngroup)

Summary: 
Placeholder text within a form field makes it difficult for people to remember what information belongs in a field, and to check for and fix errors. It also poses additional burdens for users with visual and cognitive impairments.

In-context descriptions or hints can help clarify what goes inside each form field, and therefore improve completion and [conversion rates](http://www.nngroup.com/articles/conversion-rates/). There are many ways to provide hints. A common implementation is by inserting instructions within form fields. Unfortunately, user testing continually shows that **placeholders in form fields often hurt usability** more than help it.

## In This Article:

- [Labels and Placeholders](#toc-labels-and-placeholders-1)
- [Placeholders that Replace Labels](#toc-placeholders-that-replace-labels-2)
- [Placeholder Text in Addition to Labels](#toc-placeholder-text-in-addition-to-labels-3)
- [Placeholders and Accessibility](#toc-placeholders-and-accessibility-4)
- [Floating Labels](#toc-floating-labels-5)
- [Conclusion](#toc-conclusion-6)

## Labels and Placeholders

Labels tell users what information belongs in a given form field and are usually positioned outside the form field. Placeholder text, located inside a form field, is an additional hint, description, or example of the information required for a particular field. These hints typically disappear when the user types in the field.

![Labels and placeholders](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/05/03/label-placeholder-captions.png)

## Placeholders that Replace Labels

Some forms replace field labels with in-field placeholder text to reduce clutter on the page, or to shorten the length of the form. While this approach is based on good intentions, our research shows that it has many negative consequences.

![Placeholder as label](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/05/03/placeholder-as-label.png)

*Worst: In this example, placeholder text is used instead of a label.*

Below are 7 main reasons why placeholders should not be used as replacements for field labels.

### 1. Disappearing placeholder text strains users’ [short-term memory](http://www.nngroup.com/articles/short-term-memory-and-web-usability/).

If the user forgets the hint, which people often do while filling out long forms, he has to delete what he wrote and, in some cases, click away from the field to reveal the placeholder text again. In an ideal world, users would be entirely focused when filling out a form. But in reality, **users multitask**. They [have different tabs open](/articles/multi-tab-page-parking/), or they might be pulled away by an email or phone call. For complex tasks, they might have to stop and go retrieve a document or order number. From our [research on mobile usability](http://www.nngroup.com/reports/mobile-website-and-application-usability), we know that mobile users are also frequently distracted and interrupted while using their devices. So, it’s important to help users pick up where they left off.  
  
On simple, frequently used forms with one or two fields, such as a search box or login form, the strain on memory is less of an issue than with complex or rarely used forms. That is because with simple, familiar forms, users can guess what they are supposed to enter. Although, on even a simple login form without labels, users may not remember if they have the option to type *Username or Email* or just *Username.*

### 2. Without labels, users cannot check their work before submitting a form.

The lack of labels makes it impossible for customers to glance through the form and make sure that their responses are correct. Similarly, browsers that **autocomplete form fields may fill in information incorrectly.** If there are no labels, or if special instructions are no longer visible, customers must reveal the placeholder text by deleting the text in each field one by one in order verify that it matches the description. Realistically though, many won’t even realize that potential for error, and they won’t make the effort to double check.

### 3. When error messages occur, people don’t know how to fix the problem.

If the form has been filled out, but there are no labels or instructions visible outside the form fields, then users have to go back to each field to reveal the description in order to fix the error.

### 4. Placeholder text that disappears when the cursor is placed in a form field is irritating for users [navigating with the keyboard](http://www.nngroup.com/articles/keyboard-accessibility/).

People using the *Tab* key move quickly from field to field, and they don’t stop to study the next field before tabbing to it.

### 5. Fields with stuff in them are less noticeable.

[Eyetracking](http://www.nngroup.com/topic/eyetracking/) studies show that **users’ eyes are drawn to empty fields**. At the minimum, users will spend more time locating a non-empty field — a [nuisance](http://www.nngroup.com/articles/does-user-annoyance-matter/). At the worst, they will overlook the field completely—a potential business-killing disaster.

### 6. Users may mistake a placeholder for data that was automatically filled in.

When there is already text in the field, people are less likely to realize that they can type there. Some users assume the placeholder text is a default value and **skip the field completely**.

### 7. Occasionally users have to delete placeholder text manually.

Sometimes placeholders do not disappear when users move their input focus into the field. If the placeholder remains in the field as **editable text**, users are forced to manually select and delete it. This creates an unnecessary burden on users and increases the [interaction cost](http://www.nngroup.com/articles/interaction-cost-definition/) of filling in the form.  
  
Sometimes the placeholder dims when the cursor is placed in a text field. Unfortunately, this interaction pattern is rare and users are not familiar with it: some still think they have to delete the text manually. It often takes a few failed attempts and lots of clicking to realize that they can start typing over the dimmed text.

## Placeholder Text in Addition to Labels

Using placeholder text in combination with form labels is a step in the right direction. Labels outside the form fields make the essential information visible at all times, while placeholder text inside form fields is reserved for supplementary information. However, even when using labels, placing important hints or instructions within a form field **can still cause the 7 issues mentioned above**, albeit with less severity. If some of the fields require an extra description that is **essential** to completing the form correctly, it’s best to place that text outside the field so that it is always visible.

![Label outside, placeholder inside](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/05/03/label-outside-placeholder-inside.png)

*Better: Here, placeholder text is used as a hint in addition to the label.*

## Placeholders and Accessibility

One last issue to consider is that placeholder text is generally **bad for** [**accessibility**](http://www.nngroup.com/topic/accessibility/). Certainly, accessibility software and modern browsers are improving, but they still have a long way to go. Three of the biggest problems for accessibility are as follows:

1. **The default light-grey color of placeholder text has poor color contrast against most backgrounds.** For users with a visual impairment, poor color contrast makes it difficult to read the text. Because not all browsers allow placeholder text to be styled using CSS, this is a difficult issue to mitigate.
2. **Users with cognitive or motor impairments are more heavily burdened.**As we saw, placeholders can be problematic for all users: disappearing placeholders increase the memory load; persistent dimmable placeholders cause confusion when they look clickable but aren’t, and placeholders that do not disappear require more keyboard or mouse interaction to be deleted. These difficulties are magnified for people with cognitive or motor impairments.
3. **Not all screen readers read placeholder text aloud**. Blind or visually impaired users may miss the hint completely if their software does not speak the placeholder content.

## Floating Labels

Rooted in [minimalist web design](https://www.nngroup.com/articles/characteristics-minimalism/), the floating-label pattern is a modified approach to placeholders that mitigates some of the disadvantages of traditional placeholders. This pattern has been around for years, but it has finally made way onto mainstream websites, and it has even been officially embraced by Google's Material Design.

In this pattern, labels are placed within the form field as placeholders until the field becomes active and the user moves the input focus into the field. At that point, the placeholder label moves to the top of the field. As a result, the floating label (also known as an adaptive placeholder) is always visible, either in the center of the form field, or above the text that the user entered.

![Placeholder label 'First name' rises to the top of the field on input focus](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/10/08/adaptive-placeholder.jpg)

*Good: Floating labels move to the top of the form field when the user selects it to start typing (Warbyparker.com).*

There are two main advantages to this approach:

- It can save space on mobile devices, by not requiring extra vertical space to put the label above the field.
- The visible label serves as a memory aid while people are in the typing stage. This therefore addresses points 1-4 from the list of pitfalls above.

However, **issues #5 and #6 from above are still a problem**: fields with text in them are less noticeable, and users might think there is already a default value entered in the field. Also, the accessibility issues described earlier may still apply, because some browsers and assistive technologies don’t properly or reliably read placeholder text.

Ultimately, floating labels do offer a better user experience than the label as a placeholder. But if you have the screen space, placing the label and hint outside the field is still the best way to go.

## Conclusion

Rather than risk having users stumble while filling out forms or waste valuable time figuring out how they work, the best solution is to have clear, visible labels that are placed outside empty form fields.

![Label and placeholder text outside form field](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/05/03/label-hint-outside.png)

*Best: The label and hint are placed outside the form field and are always visible to the user.*

Hints and instructions should also be persistent and placed outside of the field. Forms are an important part of many [conversion goals](http://www.nngroup.com/articles/conversion-rates/), so it’s worthwhile to make sure that your users can get through them quickly and accurately.

## Related Courses

- [#### Web Page UX Design

  Strategically combine content, visuals, and interactive components to design successful web pages

  Interaction](/courses/web-page-design/?lm=form-design-placeholders&pt=article)
- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=form-design-placeholders&pt=article)
- [#### The Human Mind and Usability

  Use psychology to predict and explain how your customers think and act

  Interaction](/courses/human-mind/?lm=form-design-placeholders&pt=article)

forms,Accessibility,Application Design,Web Usability

## Related Topics

- Accessibility
  [Accessibility](/topic/accessibility/)
- [Application Design](/topic/applications/)
- [Web Usability](/topic/web-usability/)

## Learn More:

[![Placeholders in Form Fields Are Harmful](https://media.nngroup.com/media/videos/thumbnails/Placeholders_in_Form_Fields_are_Harmful_Thumbnail.jpg.1300x728_q75_autocrop_crop-smart_upscale.jpg)](https://www.youtube.com/watch?v=jrigp2L-P-0 "Placeholders in Form Fields Are Harmful on YouTube (new window)")

Enable cookies
 to watch NN/g videos

Placeholders in Form Fields Are Harmful

 Katie Sherwin
·
3 min

- [![](https://media.nngroup.com/media/videos/thumbnails/Semantic_Differential_Scales-_Measure_User_Attitudes_with_Nuance_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Semantic Differential Scales: Measure User Attitudes with Nuance

  Rachel Banawa
  ·
  4 min](/videos/semantic-differential-scales/?lm=form-design-placeholders&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Overflow_Menu_Icons_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Overflow Menu Icons

  Kate Kaplan
  ·
  4 min](/videos/overflow-menu-icons/?lm=form-design-placeholders&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Better_Forms_Through_Visual_Organization_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Better Forms Through Visual Organization

  Kathryn Whitenton
  ·
  3 min](/videos/better-forms-visual-organization/?lm=form-design-placeholders&pt=article)

## Related Articles:

- [Website Forms Usability: Top 10 Recommendations

  Kathryn Whitenton
  ·
  6 min](/articles/web-form-design/?lm=form-design-placeholders&pt=article)
- [Inclusive Design

  Alita Kendrick
  ·
  6 min](/articles/inclusive-design/?lm=form-design-placeholders&pt=article)
- [Reset and Cancel Buttons

  Jakob Nielsen
  ·
  5 min](/articles/reset-and-cancel-buttons/?lm=form-design-placeholders&pt=article)
- [Contextual Menus: Delivering Relevant Tools for Tasks

  Anna Kaley
  ·
  7 min](/articles/contextual-menus/?lm=form-design-placeholders&pt=article)
- [6 Tips for Successful Personalization

  Amy Schade
  ·
  6 min](/articles/personalization/?lm=form-design-placeholders&pt=article)
- [A Checklist for Designing Mobile Input Fields

  Raluca Budiu
  ·
  2 min](/articles/mobile-input-checklist/?lm=form-design-placeholders&pt=article)