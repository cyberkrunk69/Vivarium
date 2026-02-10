# Common actions

Source: https://carbondesignsystem.com/patterns/common-actions/

---

# Common actions

Common actions frequently appear across different components and workflows. For
platform consistency, these actions should only be applied in the ways described
below.

- [Add](#add)
- [Cancel](#cancel)
- [Clear](#clear)
- [Close](#close)
- [Copy](#copy)
- [Delete](#delete)
- [Edit](#edit)
- [Errors](#errors)
- [Next](#next)
- [Refresh](#refresh)
- [Remove](#remove)
- [Reset](#reset)

## Add

Add inserts an existing object to a list, set, or system. For example, adding a
document to a folder.

![Example of add as a button with an icon in a data table](/static/f93b00ffd0be0d0716c617c6e57d09aa/3cbba/common-action-7.png)

### Hierarchy and placement

Depending on the importance of the add action on the page, the emphasis can be
high, medium, or low. For example, a high emphasis action should use a single
primary button with all others being secondary.

### Considerations

Small adjustments in your messaging will reduce user uncertainty. Consider the
following:

- What are the implications of the add action for the user? Are there financial,
  access, or legal considerations?
- Does the user have the correct permissions for this action?
- Is the action permanent?
- What timeframe will the action take (seconds, minutes, hours, days)?
- What should a user do if the action fails?
- Is this a single or bulk action?

## Cancel

Cancel stops the current action and closes the component or item. Warn the user
of any negative consequences if the process doesn’t progress, such as data
corruption or data loss.

Use a secondary button or a link for cancel actions.

![Example of cancel in a modal](/static/b0692d68691d985469a96af45b920b01/3cbba/common-action-1.png)

## Clear

Clear removes data from a field or removes selections. Clear can also delete the
contents of a document, such as a log. For controls that have a default
selection or value, such as radio buttons, the default selection or value is
reset.

Use the

```
close
```

Copy to clipboard

icon on the right side of a field, item, or value.

![Example of clear in multiselect dropdown and in a search field](/static/9179b19cfda0dfe4c425b6b2f15e4ebe/3cbba/common-action-2.png)

## Close

Close terminates the current page, window, or menu. Close is also used to
dismiss information, such as notifications.

Use the

```
close
```

Copy to clipboard

icon, which is typically placed on the upper right side of the
element. Do not use close in a button.

![Example of close in a toast notification](/static/320de9e36d4f95091a34a5c29cff4313/3cbba/common-action-3.png)

## Copy

Copy creates a new identical instance of the selected object(s).

Use the

```
copy
```

Copy to clipboard

icon with a confirmation “copied” tooltip appearing post-click or
tap.

![Example of copy in a code snippet](/static/e1e84a8e4deeca8b5bbdaf9a7b51214e/3cbba/common-action-8.png)

## Delete

Delete destroys an object. Delete actions cannot be easily undone and are
typically permanent. Warn the user of any negative consequences if an object is
destroyed, such as loss of data. Use either the

```
delete
```

Copy to clipboard

or

```
trash can
```

Copy to clipboard

icon, a
danger button, or a danger option in a menu. A danger modal is used when a
warning is needed to confirm an action.

![Example of delete in a modal and overflow menu](/static/7fb54926881ee4b5b8eea1a41832525e/3cbba/common-action-4.png)

### Low-impact deletion

Use when it’s trivial to undo deletion or recreate the data. Delete the data
upon click or tap without further warning.

### Moderate-impact deletion

Use when an action cannot be undone or the data cannot be recreated easily. This
pattern is also useful if you’re deleting more than one thing.

Ask for confirmation of the delete, with guidance about what will occur if they
delete.

### High-impact deletion

Use when it would be very expensive or time-consuming to recreate data. Also use
if the action deletes a large amount of data, or if other important items would
be deleted as a result of the action.

In addition to presenting a dialog, have the user type the name of the resource
they are deleting (manual confirmation).

### Post-deletion

After the user deletes data, return to the page that lists the data deleted.
Animate the removal of the data from the list or page and present a success
notification.

If the deletion fails, raise a notification to tell the user that deletion
failed. Send a second notification on another communication channel, like email,
if possible. Animate the data back onto the page if possible.

## Edit

Edit allows data or values to be changed. Edit commonly triggers a state change
to the targeted object or input item.

Offer edit as an option in a menu, or as a button or

```
edit
```

Copy to clipboard

icon.

![Example of edit in a data table cell](/static/d597041eeafe0b5b3aa75ef4ba6aac78/3cbba/common-action-9.png)

![Example of edit in an overflow menu](/static/23e7e4a386315da6cdff45bcdd8c9a9b/3cbba/common-action-10.png)

## Errors

Errors occur when an action or process does not succeed. Error notifications can
occupy full pages, form fields, notifications, and modals. Error notifications
should provide context of what happened and a clear path to continue.

![Form example with inline notification](/static/85c4a7147f4ca9db9f0281374348b18c/3cbba/notification-usage-3.png)

Consider redirecting the user to a previous state, a support page, or offering
recommendations. Be honest and helpful.

Some components, like text input and form field errors, are quite small and
require more thoughtful approaches to the space and placement of error handling.
Consider inline error notifications for these instances.

### Content guidelines

Be brief, honest, and supportive. Explain what happened and what the user can do
to resolve the error.

For full-page and large modals, keep error messages no longer than three
paragraph lines. For form errors, keep error messages no longer than two lines.

## Next

Next advances the user to the next step in a sequence of steps, like in a
wizard.

Represent next with a [button with icon](/components/button/usage) or a
standalone

```
forward
```

Copy to clipboard

icon.

![Example of next as a button with icon](/static/cbf87b3c6a2fd974b60a14820e058320/3cbba/common-action-11.png)

## Refresh

This action reloads the view of an object, list, or data set when the displayed
view has become unsynchronized with the source.

Use the

```
refresh
```

Copy to clipboard

icon or a button.

![Example of edit in a data table cell](/static/5b4534c4a16534ea6d633f846bbe4009/3cbba/common-action-12.png)

## Remove

This action removes an object from a list or item. Remove is distinct from
delete, as a removed item is not destroyed. Multiple objects can be removed at
once.

![Example of remove in a structured list](/static/862afef470a62f46e1063c817c9513ad/3cbba/common-action-5.png)

### Hierarchy and placement

Represent remove as a button or

```
subtract
```

Copy to clipboard

icon or glyph. The remove action is
rarely the primary action on the page and should not be overly emphasized.

### Considerations

- What are the implications of the remove action for the user? Are there
  financial, access, or legal considerations?
- This action can be confused with deleting.
- A user may not have the correct permissions for this action.
- Inform the user if the result is permanent.
- How long will the action take? Seconds, minutes, hours, or days?
- What should the user do if the removal fails?
- Is this a single or bulk action?

## Reset

Reset reverts values back to their last saved state. The last saved state
includes the values stored the last time the user clicked or triggered
**Apply**.

Reset is typically applied as a link.

![Example of reset in a filter](/static/c9989faa9d5705339bb4500f8eac3ee2/3cbba/common-action-6.png)

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/patterns/common-actions/index.mdx)

[Previous

Patterns: Overview](/patterns/overview/)

[Next

Patterns: Dialogs](/patterns/dialog-pattern/)