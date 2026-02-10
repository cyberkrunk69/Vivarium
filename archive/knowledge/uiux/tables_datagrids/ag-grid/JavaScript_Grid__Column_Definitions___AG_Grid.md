# JavaScript Grid: Column Definitions | AG Grid

Source: https://www.ag-grid.com/javascript-data-grid/column-definitions/

---

Each column in the grid is defined using a Column Definition (`ColDef`). Columns are positioned in the grid according to the order the Column Definitions are specified in the Grid Options.

```
const gridOptions = {
    columnDefs: [
        { field: 'athlete' },
        { field: 'sport' },
        { field: 'age' }
    ],

    // other grid options ...
}
```

See [Column Options](/javascript-data-grid/column-properties/) for all available properties.

## Column Defaults [Copy Link](#default-column-definitions)

Use `defaultColDef` to set properties across ALL Columns.

```
const gridOptions = {
    defaultColDef: {
        width: 150,
        cellStyle: { fontWeight: 'bold' },
    },

    // other grid options ...
}
```

## Column Types [Copy Link](#column-types)

Use `columnTypes` to define a set of Column properties to be applied together. The properties in a column type are applied to a Column by setting its `type` property.

```
const gridOptions = {
    // Define column types
    columnTypes: {
        currency: { 
            width: 150,
            valueFormatter: CurrencyFormatter
        },
        shaded: {
            cellClass: 'shaded-class'
        }
    },

    columnDefs: [
        { field: 'productName'},

        // uses properties from currency type
        { field: 'boughtPrice', type: 'currency'},

        // uses properties from currency AND shaded types
        { field: 'soldPrice', type: ['currency', 'shaded'] },
    ],

    // other grid options ...
}
```

Column Types work on Columns only and not Column Groups.

The below example shows Column Types.

## Provided Column Types [Copy Link](#provided-column-types)

The grid provides the Column Types `rightAligned` and `numericColumn`. Both of these types right align the header and cell contents by applying CSS classes `ag-right-aligned-header` to Column Headers and `ag-right-aligned-cell` to Cells.

```
const gridOptions = {
    columnDefs: [
        { headerName: 'Column A', field: 'a' },
        { headerName: 'Column B', field: 'b', type: 'rightAligned' },
        { headerName: 'Column C', field: 'c', type: 'numericColumn' },
    ],

    // other grid options ...
}
```

## Updating Columns [Copy Link](#updating-columns)

Columns can be controlled by updating the column state, or updating the column definition.

[Column State](/javascript-data-grid/column-state/) should be used when restoring a users grid, for example saving and restoring column widths.

Column Definitions should be updated to modify properties that the user cannot control, and as such are not supported by Column State. Whilst column definitions can be used to change stateful properties, this can cause additional side effects.

### Using Column State [Copy Link](#using-column-state)

The [Grid Api](/javascript-data-grid/grid-api/#reference-state-applyColumnState) function `applyColumnState` can be used to update [Column State](/javascript-data-grid/column-state/).

```
// Sort Athlete column ascending
api.applyColumnState({
    state: [
        {
            colId: 'athlete',
            sort: 'asc'
        }
    ]
});
```

In the example below, use the 'Sort Athlete' button to apply a column state.

### Updating Column Definitions [Copy Link](#updating-column-definitions)

To update an attribute by [Updating Column Definitions](/javascript-data-grid/column-updating-definitions/#changing-column-definition), pass a new array of [Column Definitions](/javascript-data-grid/column-definitions/) to the grid options.

```
// Define new column definitions
const updatedHeaderColumnDefs = [
  { field: 'athlete', headerName: 'C1' },
  { field: 'age', headerName: 'C2' },
  { field: 'country', headerName: 'C3' },
  { field: 'sport', headerName: 'C4' },
]
// Supply new column definitions to the grid
gridApi.setGridOption('columnDefs', updatedHeaderColumnDefs);
```

In the example below, use the 'Update Header Names' button to update the column definitions.

## Next Up [Copy Link](#next-up)

Continue to the next section: [Updating Definitions](/javascript-data-grid/column-updating-definitions/).