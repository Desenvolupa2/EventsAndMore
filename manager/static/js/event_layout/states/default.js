import {Selecting} from './selecting.js';
import {getExtrems, putBorders, sendRequest} from "../../utils.js";



class Default {

    constructor(context) {
        this.context = context
    }

    run(event) {
    }

    toString() {
        return "Default"
    }

    handleMousedown(event) {
        this.context.change(Selecting, event, event.target.cloneNode())
    }

    handleMouseup(event) {
    }

    handleMousemove(event) {
    }

    handleReset(event) {
        const cells = this.context.cells;
        for (let i = 0; i < cells.length; i++) {
            for (let j = 0; j < cells[0].length; j++) {
                if (cells[i][j].classList.contains('selected')) {
                    cells[i][j].classList.toggle('selected');
                    cells[i][j].classList.toggle('empty');
                    cells[i][j].innerText = "";
                }
            }
        }
    }

    submitStand(event) {
        const selected = this.getSelected(this.context.cells);
        const [minRow, maxRow, minCol, maxCol] = getExtrems(selected);
        if ((selected.length === 1 || selected.length === 2 || selected.length === 4) && ((maxRow - minRow) <= 1 && (maxCol - minCol) <= 1)) {
            const data = {
                'positions': selected
            }
            sendRequest('/grid-stands/', 'POST', data)
            this.context.nextId += 1;
            for (const coords of selected) {
                const row = coords[0];
                const col = coords[1];
                this.context.cells[row][col].classList.toggle('selected');
                this.context.cells[row][col].classList.toggle('confirmed');
            }
            putBorders(this.context.cells, selected.length, minRow, minCol, maxRow, maxCol);

        } else {
            for (const coords of selected) {
                const row = coords[0];
                const col = coords[1];
                this.context.cells[row][col].innerText = "";
                this.context.cells[row][col].classList.toggle('selected');
                this.context.cells[row][col].classList.toggle('empty');
            }

        }
    }

    getSelected(cells) {
        let selected = []
        for (let i = 0; i < cells.length; i++) {
            for (let j = 0; j < cells[0].length; j++) {
                if (cells[i][j].classList.contains('selected')) {
                    selected.push([i, j])
                }
            }
        }
        return selected;
    }


}

export {Default}