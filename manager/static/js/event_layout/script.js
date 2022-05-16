import {Context} from "./context.js";
import {getExtrems, putBorders} from "../utils.js";

async function initializeGrid(rows, columns) {
    let grid = document.getElementById("grid")
    let cells = []
    for (let i = 0; i < rows; i++) {
        let row = grid.insertRow()
        let rows = []
        for (let j = 0; j < columns; j++) {
            let cell = row.insertCell()
            cell.classList.add("cell")
            // cell.classList.add("empty")
            rows.push(cell)
        }
        cells.push(rows)
    }
    let ids = [];
    const nextId = sendRequest('/grid-stands/', 'GET', null).then((response) => {
        let cell = null;
        const content = response.data['content'];
        for (let stand in content) {
            if (stand !== 'unassigned') {
                ids.push(parseInt(stand, 10));
                const [minRow, maxRow, minCol, maxCol] = getExtrems(content[stand]);
                putBorders(cells, content[stand].length, minRow, minCol, maxRow, maxCol);
            }
            for (let position of content[stand]) {
                const [x, y] = position;
                cell = cells[x][y];
                if (stand === 'unassigned') {
                    cell.classList.add("empty")
                } else {
                    cell.classList.add("confirmed")
                    cell.innerText = stand
                }
            }
        }
        return ids.length === 0 ? 1 : Math.max(...ids) + 1;
    })
    return [cells, nextId];
}

window.onload = () => {
    const ROWS = 10;
    const COLUMNS = 20;
    let contextState = null;
    initializeGrid(ROWS, COLUMNS).then((ret_) => {
        const [cells, nextId] = ret_;
        contextState = new Context(cells);
        nextId.then(nId => {
            contextState.nextId = nId
        });
        contextState.run();
    })
}