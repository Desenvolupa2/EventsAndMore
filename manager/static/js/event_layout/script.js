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
    sendRequest('/grid-stands/', 'GET', null).then( (response) => {
        let ids = [];
        for (let stand of response.body) {
            ids.push(stand['id']);
            for (let position of stand['positions']) {
                const x = position['x_coordinate'];
                const y = position['y_coordinate'];
            }
        }
    })
    return cells
}

window.onload = () => {
    const ROWS = 10;
    const COLUMNS = 20;
    const cells = initializeGrid(ROWS, COLUMNS);
    let contextState = new Context(cells);
    contextState.run();
}