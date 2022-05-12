import {Selecting} from './selecting.js';

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
        const [minRow, maxRow, minCol, maxCol] = this.getExtrems(selected);
        if ((selected.length === 1 || selected.length === 2 || selected.length === 4) && ((maxRow - minRow) <= 1 && (maxCol - minCol) <= 1)) {
            const data = {
                'positions': selected
            }
            console.log(data)
            sendRequest('/grid-stands/', 'POST', data)
            // TODO: make request with selected
            this.context.nextId += 1;
            for (const coords of selected) {
                const row = coords[0];
                const col = coords[1];
                this.context.cells[row][col].classList.toggle('selected');
                this.context.cells[row][col].classList.toggle('confirmed');
            }
            if (selected.length === 1) {
                this.context.cells[minRow][minCol].classList.toggle('border-left');
                this.context.cells[minRow][minCol].classList.toggle('border-right');
                this.context.cells[minRow][minCol].classList.toggle('border-top');
                this.context.cells[minRow][minCol].classList.toggle('border-bottom');
            } else if (selected.length === 2) {
                if (minCol === maxCol) {
                    // same column
                    this.context.cells[minRow][minCol].classList.toggle('border-left');
                    this.context.cells[minRow][minCol].classList.toggle('border-top');
                    this.context.cells[minRow][minCol].classList.toggle('border-right');

                    this.context.cells[maxRow][minCol].classList.toggle('border-left');
                    this.context.cells[maxRow][minCol].classList.toggle('border-bottom');
                    this.context.cells[maxRow][minCol].classList.toggle('border-right');

                } else {
                    // same row
                    this.context.cells[minRow][minCol].classList.toggle('border-left');
                    this.context.cells[minRow][minCol].classList.toggle('border-top');
                    this.context.cells[minRow][minCol].classList.toggle('border-bottom');

                    this.context.cells[minRow][maxCol].classList.toggle('border-top');
                    this.context.cells[minRow][maxCol].classList.toggle('border-right');
                    this.context.cells[minRow][maxCol].classList.toggle('border-bottom');

                }
            } else {
                // square
                this.context.cells[minRow][minCol].classList.toggle('border-left');
                this.context.cells[minRow][minCol].classList.toggle('border-top');

                this.context.cells[minRow][maxCol].classList.toggle('border-top');
                this.context.cells[minRow][maxCol].classList.toggle('border-right');

                this.context.cells[maxRow][minCol].classList.toggle('border-bottom');
                this.context.cells[maxRow][minCol].classList.toggle('border-left');

                this.context.cells[maxRow][maxCol].classList.toggle('border-right');
                this.context.cells[maxRow][maxCol].classList.toggle('border-bottom');
            }

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

    getExtrems(selected) {
        const rows = selected.map((coords) => {
            return coords[0];
        })
        const cols = selected.map((coords) => {
            return coords[1];
        })
        return [Math.min(...rows), Math.max(...rows), Math.min(...cols), Math.max(...cols)];
    }
}

export {Default}