import {
    clearSelection,
    getSelected,
    sendRequest,
    updateStand
} from "../utils.js";
import {Default} from "./states/default.js";
import {Selecting} from "./states/selecting.js";

const clone = (items) => items.map(item => Array.isArray(item) ? clone(item) : item.cloneNode());

class Context {

    constructor(cells) {
        this.cells = cells;
        this.cellsCopy = clone(cells);

        this.states = [new Default(this), new Selecting(this)];
        this.current = this.states[0];
    }

    change(state, event) {
        this.current = this.getState(state)
        this.current.run(event);
    };

    getState(state) {
        for (let i = 0; i < this.states.length; i++) {
            if (this.states[i] instanceof state) {
                return this.states[i]
            }
        }
        return this.states[0]
    }

    cloneCells() {
        this.cellsCopy = clone(this.cells);
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

        document.getElementById("button-submit").addEventListener(
            "click",
            (event) => {
                _this.submitEventRequest();
            }
        )
        document.getElementById("button-reset").addEventListener(
            "click",
            (event) => {
                _this.current.handleReset(event);
            }
        )

        _this.current.run();
    };

    submitEventRequest() {
        const eventName = document.getElementById('id_name').value;
        const initialDate = document.getElementById('id_initial_date').value;
        const finalDate = document.getElementById('id_final_date').value;
        const selectedGrid = getSelected(this.cells);

        const data = {
            'eventName': eventName,
            'initialDate': initialDate,
            'finalDate': finalDate,
            'grid': selectedGrid
        }

        sendRequest('/event-request/', 'POST', data).then(() => {
            Swal.fire(
                'Success!',
                'Your event request has been submitted.',
                'success'
            ).then(() => { window.location.replace('/event-requests/')})
        }).catch((r) => {
            console.log("response", r.response);
            Swal.fire({
                icon: 'error',
                title: 'Error submitting your request',
                text: r.response.data['content'],
            })
        });

    }

    updateAvailablePositions() {
        const url = '/grid-positions/?initial_date=' + initialDate + '&final_date=' + finalDate;
        sendRequest(url, 'GET', null).then((response) => {
            const content = response.data['content'];
            for (const stand in content) {
                updateStand(this, stand, content[stand]).then(_ => {
                })
            }
        })
    }

}

export {Context}