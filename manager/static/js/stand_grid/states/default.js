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
        for (let i = 0; i < this.context.cells.length; i++) {
            for (let j = 0; j < this.context.cells[0].length; j++) {
                this.context.cells[i][j].classList = this.context.cellsCopy[i][j].classList;
            }
        }
    }
}

export {Default}