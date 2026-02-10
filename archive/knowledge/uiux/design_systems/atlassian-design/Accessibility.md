# Accessibility

Source: https://atlassian.design/foundations/accessibility

---

# Accessibility

When apps are accessible, the experience is better for everyone.

![Banner for Accessibility page](/static/hero.light-e9e151cb94e030c1011a31f01b28ff618fadd66592785fae14ec1adf78e6da18.png)

## Building accessible apps

An accessible app means people of all abilities can interact with, understand, and navigate it.

ADS components ship with built-in accessibility features, such as keyboard support and sensible ARIA
usage. However, you still need to review your patterns, content, and interactions so your app is
accessible end-to-end.

### Follow our accessibility principles

Our principles cover the main requirements to design and build accessible experiences, helping you
to put accessibility into action.

#### Build consistent experiences

The user experience should be familiar, identifiable, and work as expected regardless of device,
screen size, platform, or assistive technology.

- Use design system components as the basis of every experience. They have inbuilt accessibility
  features and create consistency across apps.
- Ensure the same components, patterns, and interactions are used for the same experiences across
  pages and apps to lessen cognitive load.

#### Keep experiences and language simple

Respect people’s time by making apps that are uncomplicated and easy to use.

- Avoid complex process and experiences.
- Use similar patterns across apps and experiences.
- Use concise and plain language.
- Aim for content to be written at a reading level of ages 12 to 14.

#### Be inclusive

Accessible design is inclusive of people of all races, ethnicities, genders, sexual orientations,
and backgrounds.

- Use [inclusive language](https://atlassian.design/foundations/content/inclusive-writing).
- Don’t make assumptions about people’s abilities.
- Avoid jargon,
  [metaphors, and non-literal phrases](https://atlassian.design/foundations/content/inclusive-writing#avoid-metaphors-and-idioms).

#### Give people control

People should be able to adapt our apps to suit their needs.

- Enable [reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html) across all screen sizes.
- Allow people to adjust scale, contrast, and colors.
- Make sure personal reduced motion settings are respected by our apps.
- Inform people about high-impact changes before you make them.

#### Provide text alternatives

Text is powerful for assistive technologies, as it can be seen on a screen, heard using
text-to-speech, and touched with a braille screen reader.

- Use visible and accessible labels.
- Write clear and concise labels and
  [alternative (alt) text](https://accessibility.huit.harvard.edu/describe-content-images).
- Include a transcript for videos on the page or link to it.

#### Ensure color is accessible

Some people can’t perceive color, while others perceive limited color.

- Never rely on color alone to convey meaning.
- Use a color contrast ratio of 4.5:1 for regular text and 3:1 for large text and graphics.

#### Use semantic HTML

[Semantic HTML](https://www.w3schools.com/html/html5_semantic_elements.asp) describes the exact
meaning of an element to a web browser. It helps people using assistive technology navigate and
interpret page elements.

- Use `header` , `nav`, `footer` (for example).
- Don't use `div` or `span` (for example) as they don't convey meaning.

#### Test apps broadly

Test with different tools and a diverse array of people.

- Test apps with people with disabilities and across different levels of technical experience.
- Use different types of technology and accessibility tools, such as
  [Accessibility Insights](https://accessibilityinsights.io), to test your app.

## What to consider when building accessible apps

Everyone will experience a disability at some point in their lives, whether it's a situational
impairment or a permanent or temporary disability. At these times, assistive technology can help
people use our apps — but only if they’re built to be accessible.

Consider the following when designing and building your app. And remember: people are multi-faceted,
so it's important not to solve for one disability in isolation.

### Visual disabilities

- Provide clear and informative alternative (alt) text and semantic HTML.
- Don’t rely on color alone to convey meaning, and make sure color contrast is accessible.
- Examples of visual disabilities include:
  - Blind (permanent)
  - Migraine (temporary)
  - Lost glasses (situational)

### Auditory disabilities

- Include closed captions and transcripts for videos.
- Make sure transcripts for audio are available.
- Examples of auditory disabilities include:
  - Deaf (permanent)
  - Ear infection (temporary)
  - On public transport (situational)

### Limited mobility

- Support keyboard navigation, large selectable targets, and correct semantic HTML.
- Examples of limited mobility include:
  - Cerebral palsy (permanent)
  - Broken wrist (temporary)
  - Crying baby (situational)

### Cognitive disabilities

- Use wording that’s clear and in plain language.
- Break up big chunks of text using headings and subheadings, bullet points, and small paragraphs.
- Design experiences that are easy to navigate.
- Examples of cognitive disabilities include:
  - Dyslexia (permanent)
  - Anxiety (temporary)
  - Busy office (situational)

## Benefits of accessible apps

When we consider accessibility and inclusion throughout every part of the design and development process, we create apps that benefit everyone on a team, reach more people, comply with legislation, and keep us innovative.

## Helpful tools (Atlassians only)

[#### A11y Office Hours

Book time with our accessibility specialists.

, (opens new window)](https://hello.atlassian.net/wiki/spaces/A11Y/pages/940530583/Accessibility+Office+Hours)[#### Accessibility annotations

Communicate accessibility requirements to engineers.

, (opens new window)](https://hello.atlassian.net/wiki/spaces/A11YKB/pages/3370798642/Accessibility+annotations+for+your+Figma+designs)[#### A11y Mate

A Rovo agent that answers your accessibility questions.

, (opens new window)](https://home.atlassian.com/o/2346a038-3c8c-498b-a79b-e7847859868d/chat?cloudId=a436116f-02ce-4520-8fbb-7301462a1674&rovoChatCloudId=a436116f-02ce-4520-8fbb-7301462a1674&rovoChatPathway=chat&rovoChatAgentId=a7f547de-aa39-4d25-9234-65ac13c19acd)[#### Accessibility Knowledge Base

Access hundreds of articles on applying a11y at Atlassian.

, (opens new window)](https://hello.atlassian.net/wiki/spaces/A11YKB/overview?homepageId=2991104530)[#### Accessible design requirements

Your checklist for creating inclusive experiences.

, (opens new window)](https://hello.atlassian.net/wiki/spaces/DHub/pages/4461719822/Accessible+design+requirements)[#### Content Assistant

A Rovo agent to help write clear, concise content that follows a11y standards.

, (opens new window)](https://home.atlassian.com/o/2346a038-3c8c-498b-a79b-e7847859868d/chat?rovoChatPathway=chat&rovoChatCloudId=a436116f-02ce-4520-8fbb-7301462a1674&rovoChatAgentId=51c363f3-5896-43f3-be92-528557b6510f&cloudId=a436116f-02ce-4520-8fbb-7301462a1674)

---

##### Was this page helpful?

YesNo

We use this feedback to improve our documentation.