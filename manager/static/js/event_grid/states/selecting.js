import {State} from "./state.js";
import {Default} from "./default.js";
import {getPercentageSelected, isAvailable, isEmpty} from "../../utils.js";

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
        if (isAvailable(target)) {
            target.classList.toggle("selected");
            target.classList.toggle("available");
            getPercentageSelected(this.context.cells).then(percentage => {
                document.getElementById('percentage').innerText = (percentage * 100).toFixed(1);
            });
        }
    }

}


export {Selecting}