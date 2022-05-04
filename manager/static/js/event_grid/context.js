import {clearSelection} from "../utils.js";
import {Default} from "./states/default.js";
import {Selecting} from "./states/selecting.js";

class Context {
    constructor(cells) {
        this.cells = cells;
        this.states = [new Default(this), new Selecting(this)];
        this.current = this.states[0];
        this.nextId = 1;
    }

    change(state, event, firstTarget = null, previousTarget = null) {
        // console.log(this.current.toString(), " -> ", newState.toString())
        this.current = this.getState(state)
        this.current.run(event, firstTarget, previousTarget);
    };

    getState(state) {
        for (let i = 0; i < this.states.length; i++) {
            if (this.states[i] instanceof state) {
                return this.states[i]
            }
        }
        return this.states[0]
    }

    run() {
        let _this = this;
        document.addEventListener("mouseup", function (event) {
            clearSelection()
            _this.current.handleMouseup(event)
        })

        document.addEventListener("mousedown", function (event) {
            clearSelection()
            _this.current.handleMousedown(event)
        })

        document.addEventListener("mousemove", function (event) {
            _this.current.handleMousemove(event)
        })


        //BUTTON next stand
        document.getElementById("button-all").addEventListener(
            "click",
            (event) => {
                _this.selectAll(event)
            }
        )

        document.getElementById("button-reset").addEventListener(
            "click",
            (event) => {
                _this.current.handleReset(event)
            }
        )

        document.getElementById("id_initial_date").addEventListener('change', () => {
            _this.updateAvailablePositions(_this.cells);
            console.log("HOLA");
        })

        document.getElementById("id_initial_date").addEventListener('change', () => {
            console.log("HOLA");
        })

        _this.current.run();
    };

    updateAvailablePositions() {

    }

    selectAll(event) {
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
}

export {Context}