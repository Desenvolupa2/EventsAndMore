import {State} from "./state.js";
import {Default} from "./default.js";
import {isEmpty} from "../utils.js";

class Selecting extends State {

    constructor(context) {
        super(context);

    }

    run(event) {
        if (event) {
            this.drawWalls(event.target).then(_ => {
            })
        }
    }

    handleMouseup() {
        this.context.change(Default);
    }

    handleMousedown(event) {
    }

    handleMousemove(event) {
        this.drawWalls(event.target).then(_ => {
        })
    }

    handleReset(event) {
        super.handleReset(event);
    }

    async drawWalls(target) {
        if (isEmpty(target)) {
            target.innerText = target.classList.contains('empty') ? this.context.nextId : "";
            target.classList.toggle("selected");
            target.classList.toggle("empty");
        }
    }

}


export {Selecting}