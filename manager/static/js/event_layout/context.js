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
        let _this = this
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
        document.getElementById("button-submit").addEventListener(
            "click",
            (event) => {
                _this.current.submitStand(event)
            }
        )

        document.addEventListener(
            "keypress",
            (event) => {
                if (event.key === "Enter") {
                    document.getElementById("button-submit").click();
                }
            }
        )

        document.getElementById("button-reset").addEventListener(
            "click",
            (event) => {
                _this.current.handleReset(event)
            }
        )

        _this.current.run();
    };
}

export {Context}