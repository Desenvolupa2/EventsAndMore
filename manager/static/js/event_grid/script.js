import {Context} from "./context.js";

function initializeGrid(rows, columns) {
    let grid = document.getElementById("grid")
    let cells = []
    for (let i = 0; i < rows; i++) {
        let row = grid.insertRow()
        let rows = []
        for (let j = 0; j < columns; j++) {
            let cell = row.insertCell()
            cell.classList.add("cell")
            cell.classList.add("empty")
            rows.push(cell)
        }
        cells.push(rows)
    }
    return cells
}

window.onload = () => {
    const ROWS = 10;
    const COLUMNS = 20;
    const cells = initializeGrid(ROWS, COLUMNS);
    let contextState = new Context(cells);
    contextState.run();
}