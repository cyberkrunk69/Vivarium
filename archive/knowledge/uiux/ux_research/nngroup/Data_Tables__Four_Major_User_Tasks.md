# Data Tables: Four Major User Tasks

Source: https://www.nngroup.com/articles/data-tables/

---

7

# Data Tables: Four Major User Tasks

Page Laubheimer

![](https://media.nngroup.com/media/people/photos/2022-portrait-page-3.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

Page Laubheimer

April 3, 2022
2022-04-03

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Data Tables: Four Major User Tasks&body=https://www.nngroup.com/articles/data-tables/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/data-tables/&title=Data Tables: Four Major User Tasks&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/data-tables/&text=Data Tables: Four Major User Tasks&via=nngroup)

Summary: 
Table design should support four common user tasks: find records that fit specific criteria, compare data, view/edit/add a single row’s data, and take actions on records.

If you have lots of data, there’s a strong likelihood that you will end up displaying it in a table. Tables are present in many [workplace applications](https://www.nngroup.com/videos/workplace-application-usability/) precisely because they are a compact way of showing a large multivariate dataset. However, big tables present challenges to both designers and users.

This article is part of a series that covers various aspects of designing usable tables:

- Common user tasks associated with tables and how to support them on desktop
- How to deal with [tables that are too big for the screens](https://www.nngroup.com/videos/big-tables-small-screens/) on which they are displayed — including tables for mobile or variable-size viewports (as in [responsive design](https://www.nngroup.com/articles/mobile-tables/?lm=big-tables-small-screens))

Note: this article is primarily concerned with large data tables used in the workplace rather than with [product-comparison tables](https://www.nngroup.com/articles/comparison-tables/) (common on ecommerce websites).

## In This Article:

- [Tables vs. Cards or Modules for Data Presentation](#toc-tables-vs-cards-or-modules-for-data-presentation-1)
- [Main User Tasks in Tables](#toc-main-user-tasks-in-tables-2)
- [Taking Action on Records](#toc-taking-action-on-records-3)
- [Summary](#toc-summary-4)

## Tables vs. Cards or Modules for Data Presentation

Tables are not usually winners of a UI beauty contest — they are a utilitarian part of our designs. To embrace their functional advantages over other, perhaps more aesthetically pleasing, forms of multivariate-data displays (such as collections of [cards](https://www.nngroup.com/articles/cards-component/) or [dashboards](https://www.nngroup.com/videos/data-visualizations-dashboards/) with various [information visualizations](https://www.nngroup.com/articles/choosing-chart-types/) and [data charts](https://www.nngroup.com/videos/better-charts-analytics-quantitative-ux-data/)), we need to understand when to use tables and what kinds of user tasks are suited to them.

The primary advantages of a data table over other data-presentation options are:

1. **Scalability**: It’s easy to increase both the number of rows and the number of columns in a table if your dataset changes.
2. Support for **comparison** tasks: In a table, two adjacent data points are easy to compare because, unlike with a card-based UI, users don’t need to either move their eyes much or store information in their [working memory](https://www.nngroup.com/videos/working-memory-external-memory/), as they can see both items at the same time.

![A card-based display of data, with each card requiring a lot of eye movement and short term memory burden to compare](https://media.nngroup.com/media/editor/2022/01/31/cards.png)

*A card-based presentation of multivariate data requires users to spatially reorient each time they move their eyes from one card to another, making comparison tasks cognitively effortful and slow.*

## Main User Tasks in Tables

While the specific tasks carried out on a table will vary depending on applications or even users, the following 4 tasks are frequently performed and can be considered the core tasks to be supported by a table design:

- Find record(s) that fit specific criteria
- Compare data
- View, edit or add a single row’s data
- Take action(s) on records

### Find Record(s) that Fit Specific Criteria

When users engage in this type of task, they may seek a specific item (whose name or other pertinent details they already know) or may look for several items that meet a few criteria they have in mind.

This process might involve filtering, sorting, using a search feature (or using the browser’s built-in *CTRL-F* feature on the page), or simply [visually scanning](https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/) down the table. The reasons users will choose one of those interactions can be hard to predict and it’s based on the specifics of the data table, as well as on their expectations of what will be the least effortful way to find what they’re looking for.

![An eye tracking visualization of a user looking horizontally across table rows for comparison tasks](https://media.nngroup.com/media/editor/2022/01/31/finviz-screenerview-evenmorefilters-gazeplotzoomed.png)

*An eyetracking gazeplot shows a participant fixating back and forth between the table’s data and the filters above. At one point, the participant engages in a hierarchical search of the table, moving his eyes between the first column, second column, then skipping to the fourth and sixth columns before moving to the next row of data and repeating the procedure.*

Designing to support this task involves a few different things:

1. The (default**) first column should be a human-readable record identifier** instead of a “mystery meat” automatically generated ID. This design will allow users to scan and locate a record of interest.
2. The **default order of the columns should reflect the importance of the data** to the user and related columns should be adjacent. In other words, once a user has located a potential record of interest, don’t force them to move their eyes back and forth between column 1 and column 20 because those are the most relevant columns.
3. **Filters** need to be discoverable, quick, and powerful. Filter syntax should be transparent to users. Moreover, users should be able to easily understand that they are looking at filtered data (that is, there should be a clear visual indication that filters are active).

### Compare Data

Tables are most effective when they allow users to easily compare data — whether this data is in two or more records or in different columns. Often, these comparisons aim to detect relationships between different variables or records, data ranges for a column, outliers or to simply explore what is typical for one or more variables.

There are two common issues that users encounter when performing comparisons in complex, big tables:

- Because of the sheer volume of data filling up the screen, it can be complicated to understand **what each cell stands for and to which record it belongs**.
- Sometimes the **columns users wish to compare are far away** from each other — with one being even perhaps off canvas and requiring horizontal scrolling to view. Not only is scrolling back and forth tedious, but users will also need to memorize data from one column, bring the other column into view, and compare what they remember with what they see.
- The same thing can happen with **rows** — if people need to compare data from nonadjacent rows, it can be difficult to move back and forth between them and also ensure that the user is looking at the right cell.

The primary design solutions ensure that:

1. Users will always know what they’re looking at.
2. Data points of interest can be brought in close proximity.

Here are some specific guidelines related to these two principles.

### 1. Locating Relevant Info

- **Freeze** **header** rows and header columns (if the table is larger than the screen).
- The visual design needs to enable users to keep their place as they move their eyes across the table. **Borders**, **zebra striping**, and **hover-triggered highlighting** of a record can all help.

### 2. Making Information Adjacent for Comparison

- **Hiding and reordering columns** must be easy to accomplish (low [interaction cost](https://www.nngroup.com/articles/interaction-cost-definition/) and accessible for those that don’t use [drag and drop](https://www.nngroup.com/articles/drag-drop/) interactions). These features should be [discoverable](https://www.nngroup.com/videos/findability-vs-discoverability/) and clear visual [state indicators](https://www.nngroup.com/articles/state-switch-buttons/) should signal to users that some columns are hidden.
- **Hiding or reordering records** and **sorting** after a particular variable should also be easy to accomplish. (This feature is often related to filtering, but is not exactly the same — the user should be able to manually hide one or more records.)

![Frozen header row and first column enables easier recognition of which row the user is investigating.](https://media.nngroup.com/media/editor/2022/01/31/frozen-headers.png)

*A frozen header row and first column, light borders, and zebra striping all support visual scanning behaviors and help users to keep their place as they look around and compare data. The subtle use of a drop shadow suggests that that the frozen first column and header row are floating “above” the rest of the table’s data, assisting with spatial orientation.*

![A dropdown menu for hiding table columns](https://media.nngroup.com/media/editor/2022/01/31/hidden-fields.png)

*An easily noticeable menu for hiding columns, that clearly indicates the current state (15 columns are currently hidden). Reordering columns here can be done in two ways: (1) dragging and dropping the column headers themselves (which has relatively low discoverability and poor accessibility, but is an efficient [accelerator](https://www.nngroup.com/articles/ui-accelerators/) once learned) or (2) dragging and dropping from the list of columns in this visible menu.*

### View, Edit, or Add a Single Row

Another common task in tables involves viewing, creating, or editing a single record. For all three cases, a tabular presentation of a single record can be challenging to read (and even more so to edit), especially when the table is wide and the user will have to scroll horizontally in order to access all the fields.

There are a variety of ways to present a single record as a complete unit, optimized for readability and editability. Each has different tradeoffs to consider:

![A modal popup for data editing that obscures the underlying data in the table](https://media.nngroup.com/media/editor/2022/01/31/modal-overlay.png)

*A modal popup for editing obscures information on the table.*

- **Edit in place** (where the table row becomes editable). This solution works only if the table is narrow. Make sure that the row looks different in *Edit* [mode,](https://www.nngroup.com/articles/modes/) so that the user can clearly see what is editable to prevent accidental edits.
- **Modal popup**. The big downside with a [modal implementation](https://www.nngroup.com/articles/modal-nonmodal-dialog/) (and why we generally don’t recommend modals for deep editing work) is that it will cover adjacent records in the table and the user won’t be able to reference or copy data from a similar record. We routinely observe in testing that users refer to existing data in other records while they edit a record (as that helps them to [recognize, rather than recall](https://www.nngroup.com/videos/recognition-vs-recall/) reasonable value ranges).
- **Nonmodal panel or separate window**. Either of these options will cover some of the table, but still allow users access to the table data.
- **Opening the row as an** [**accordion**](https://www.nngroup.com/articles/accordions-complex-content/). While this presentation doesn’t obscure other parts of the table, a downside is that users don’t tend to clean up after themselves (i.e., close accordions when they are done with them) and they may end up with cluttered displays unsuited for the other core table tasks. More important, users will have difficulty referring to records that are not in immediate proximity of the one being edited.

![A non-modal panel on the right side allows the user to edit but still review the underlying table data.](https://media.nngroup.com/media/editor/2022/01/31/nonmodal-panel.png)

*A nonmodal side panel allows for the full display (and editing) of a single record while still allowing the user to view the rest of the table’s data.*

## Taking Action on Records

Another important task in a table is to take action on one or multiple records (beyond editing the record itself) — for example, deleting, sharing, or performing some other data-specific action (like sending out invoices, changing deadlines, etc.).

Traditionally, there are two ways to implement this task: **single-record actions** and **batch actions**.

### Single-Record Actions

Placing the **single-record actions** inline within a table row can work if you just have one or two actions, but, when there are more, screen space becomes an issue. As a result, multiple single-record actions end up either:

- **Crowded**, with no text labels, and thus be [hard to click](https://www.nngroup.com/videos/fittss-law-links-buttons/) and also hard to distinguish, or
- **Hidden** under a hover gesture or a generic *Actions* menu, and thus hard to discover (and potentially with low accessibility if a hover gesture is used).

### Batch Actions

**Batch actions** usually involve a mechanism for selecting records (e.g., a [checkbox](https://www.nngroup.com/videos/checkboxes-vs-switches-forms/) for each record) and then a series of action buttons or menus above or below the table. This type of design allows for a space-efficient presentation of multiple options. If applying the same action to the full data set is a common need, it’s a convenient shortcut to have a single-click option to *Select All*.

## Summary

Compared to modular presentations such as card-based displays, tables are space efficient and well suited for comparing records and for detecting patterns in the data.

Data tables must support the following frequent user tasks:

- Find record(s) that fit specific criteria
- Compare data
- View, edit or add a single row
- Taking action on records

## Related Courses

- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=data-tables&pt=article)

Application Design,tables,complex applications,digital workplace,Human Computer Interaction

## Related Topics

- Application Design
  [Application Design](/topic/applications/)
- [Human Computer Interaction](/topic/human-computer-interaction/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Icon_Interpretation_vs_Recognizability_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Icon Interpretation vs. Recognizability

  Kate Kaplan
  ·
  4 min](/videos/icon-interpretation-vs-recognizability/?lm=data-tables&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Is_the_Floppy_Disk_Dead_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Is the Floppy Disk Dead?

  Kate Kaplan
  ·
  4 min](/videos/is-the-floppy-disk-dead/?lm=data-tables&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/2-Factor_Authentication_2-FA_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  2-Factor Authentication (2-FA)

  Tim Neusesser
  ·
  4 min](/videos/2-factor-authentication/?lm=data-tables&pt=article)

## Related Articles:

- [Designing for Long Waits and Interruptions: Mitigating Breaks in Workflow in Complex Application Design

  Kate Kaplan
  ·
  9 min](/articles/designing-for-waits-and-interruptions/?lm=data-tables&pt=article)
- [8 Design Guidelines for Complex Applications

  Kate Kaplan
  ·
  8 min](/articles/complex-application-design/?lm=data-tables&pt=article)
- [State-Switch Controls: The Infamous Case of the "Mute" Button

  Raluca Budiu
  ·
  6 min](/articles/state-switch-buttons/?lm=data-tables&pt=article)
- [Complex Application Design: A 5-Layer Framework

  Kate Kaplan
  ·
  12 min](/articles/complex-application-design-framework/?lm=data-tables&pt=article)
- [Mobile-App Onboarding: An Analysis of Components and Techniques

  Alita Kendrick
  ·
  10 min](/articles/mobile-app-onboarding/?lm=data-tables&pt=article)
- [Listboxes vs. Dropdown Lists

  Anna Kaley
  ·
  10 min](/articles/listbox-dropdown/?lm=data-tables&pt=article)