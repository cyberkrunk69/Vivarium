# JavaScript Grid: Row Sorting | AG Grid

Source: https://www.ag-grid.com/javascript-data-grid/row-sorting/

---

This page describes how to sort row data in the grid and how you can customise that sorting to match your requirements.

## Sorting [Copy Link](#sorting)

Sorting is enabled by default for all columns. You can sort a column by clicking on the column header. To enable / disable sorting per column use the `sortable` column definition attribute.

```
const gridOptions = {
    columnDefs: [
        { field: 'name' },
        { field: 'age' },
        // disable sorting by address
        { field: 'address', sortable: false },
    ],

    // other grid options ...
}
```

To disable sorting for all columns, set sorting in the [default column definition](/javascript-data-grid/column-definitions/).

```
const gridOptions = {
    // disable sorting on all columns
    defaultColDef: {
        sortable: false
    },
    columnDefs: [
        // Override default to enable sorting by name
        { field: 'name', sortable: true },
        { field: 'age' },
        { field: 'address' },
    ],

    // other grid options ...
}
```

## Custom Sorting [Copy Link](#custom-sorting)

Custom sorting is provided at a column level by configuring a comparator on the column definition.

```
const gridOptions = {
    columnDefs: [
        {
            field: 'age',
            // simple number comparator
            comparator: (valueA, valueB, nodeA, nodeB, isDescending) => valueA - valueB
        },
        {
            field: 'name',
            // simple string comparator
            comparator: (valueA, valueB, nodeA, nodeB, isDescending) => {
                if (valueA == valueB) return 0;
                return (valueA > valueB) ? 1 : -1;
            }
        }
    ],

    // other grid options ...
}
```

|  |
| --- |
| comparator[Copy Link](#reference-sort-comparator)  SortComparatorFn | Partial<Record<SortType, SortComparatorFn>>  Override the default sorting order by providing a custom sort comparator, or a map of comparators for different `SortType`s.- `valueA`, `valueB` are the values to compare. - `nodeA`, `nodeB` are the corresponding RowNodes. Useful if additional details are required by the sort. - `isDescending` - `true` if sort direction is `desc`. Not to be used for inverting the return value as the grid already applies `asc` or `desc` ordering. Returns:- `0` valueA is the same as valueB - `> 0` Sort valueA after valueB - `< 0` Sort valueA before valueB |

Example below shows the following:

- Default sorting on the **Athlete** column.
- When the **Year** column is not sorted, it shows a custom icon (up/down arrow).
- The **Date** column has strings as the row data, but has a custom comparator so that when you sort this column it sorts as dates, not as strings.

If you are using a custom column header component see [Custom Components](/javascript-data-grid/column-headers/#custom-component) for how to implement sorting.

## Multi Column Sorting [Copy Link](#multi-column-sorting)

It is possible to sort by multiple columns. The default action for multiple column sorting is for the user to hold down `â§ Shift` while clicking the column header. To change the default action to use the `^ Ctrl` key (or `Command` key on Apple) instead set the property `multiSortKey='ctrl'`.

The example below demonstrates the following:

- The grid sorts by **Country** then **Athlete** by default.
- The property `multiSortKey='ctrl'` is set so multiple column sorting is achieved by holding down `^ Ctrl` (or `Command` on Apple) and selecting multiple columns.

You can suppress the multi sorting behaviour by enabling the `suppressMultiSort` option, or force the behaviour without key press by enabling the `alwaysMultiSort` option.

## Sorting Animation [Copy Link](#sorting-animation)

By default rows will animate after sorting. If you wish to suppress this animation set the grid property `animateRows=false`.

## Sorting Order [Copy Link](#sorting-order)

By default, the sorting order is as follows:

**ascending -> descending -> none**.

In other words, when you click a column that is not sorted, it will sort ascending. The next click will make it sort descending. Another click will remove the sort.

It is possible to override this behaviour by providing your own `sortingOrder` on the `colDef`.

|  |
| --- |
| sortingOrder[Copy Link](#reference-sort-sortingOrder)  (SortDirection | SortDef)[]  An array defining the order in which sorting occurs (if sorting is enabled).    Defaults:- `['asc', 'desc', null]` if no sort type is specified, - `[{ type: 'absolute', direction: 'asc', }, { type: 'absolute', direction: 'desc' }, null]` if 'sort' or 'initialSort' have type 'absolute' |

The example below shows different combinations of sorting orders as follows:

- **Column Athlete:** ascending -> descending
- **Column Age:** descending -> ascending
- **Column Country:** descending -> no sort
- **Column Year:** ascending only
- **Default Columns:** descending -> ascending -> no sort

## Absolute Sorting [Copy Link](#absolute-sorting)

Absolute Sorting enables sorting numeric values based on their magnitude, ignoring their sign. This can be used to rank values by their size ignoring if a value is positive or negative.

In the following example, the column `rankingChange` uses absolute sorting:

```
const gridOptions = {
    columnDefs: [
        // ... other columns 
        {
            field: 'rankingChange',
            sort: { direction: 'asc', type: 'absolute' },
            sortingOrder: [
                { direction: 'asc', type: 'absolute' }, 
                { direction: 'desc', type: 'absolute' },
                null, 
            ],
        },
    ],

    // other grid options ...
}
```

|  |
| --- |
| sort[Copy Link](#reference-sort-sort)  SortDirection | SortDef  Set the default sort. |
| sortingOrder[Copy Link](#reference-sort-sortingOrder)  (SortDirection | SortDef)[]  An array defining the order in which sorting occurs (if sorting is enabled).    Defaults:- `['asc', 'desc', null]` if no sort type is specified, - `[{ type: 'absolute', direction: 'asc', }, { type: 'absolute', direction: 'desc' }, null]` if 'sort' or 'initialSort' have type 'absolute' |

## Sorting API [Copy Link](#sorting-api)

The sort state can be saved and restored as part of [Grid State](/javascript-data-grid/grid-state/).

What sorting is applied is controlled via [Column State](/javascript-data-grid/column-state/). The below examples uses the Column State API to control column sorting.

## Accented Sort [Copy Link](#accented-sort)

By default, sorting doesn't take into consideration locale-specific characters. If you need to make your sort locale-specific you can configure this by setting the grid option `accentedSort = true`.

Please note, accented sort is slower than default sort; the effect is more noticeable when sorting a large number of rows.

The following example is configured to use this feature.

## Post-Sort [Copy Link](#post-sort)

It is also possible to perform some post-sorting if you require additional control over the sorted rows.

This is provided via the `postSortRows` grid callback function as shown below:

|  |
| --- |
| postSortRows[Copy Link](#reference-sort-postSortRows)  Function  Callback to perform additional sorting after the grid has sorted the rows. |

```
const gridOptions = {
    postSortRows: params => {
        let rowNodes = params.nodes;
        // here we put Ireland rows on top while preserving the sort order
        let nextInsertPos = 0;
        for (let i = 0; i < rowNodes.length; i++) {
            const country = rowNodes[i].data.country;
            if (country === 'Ireland') {
                rowNodes.splice(nextInsertPos, 0, rowNodes.splice(i, 1)[0]);
                nextInsertPos++;
            }
        }
    },

    // other grid options ...
}
```

The following example uses this configuration to perform a post-sort on the rows. The custom function puts rows with Ireland at the top always.