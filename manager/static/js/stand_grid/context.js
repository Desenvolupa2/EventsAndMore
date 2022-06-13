import {clearSelection, getExtrems, getSelectedById, putBorders, sendRequest} from "../utils.js";
import {Default} from "./states/default.js";
import {Selecting} from "./states/selecting.js";

const clone = (items) => items.map(item => Array.isArray(item) ? clone(item) : item.cloneNode());

class Context {

    constructor(cells) {
        this.cells = cells;
        this.cellsCopy = clone(cells);

        this.states = [new Default(this), new Selecting(this)];
        this.current = this.states[0];
        this.eventId = null;
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
        const url = window.location.pathname;
        this.eventId = url.substring(url.lastIndexOf('/') + 1);
        sendRequest('/stand-request-grid/?event=' + this.eventId, 'GET', null).then((response) => {
            const content = response.data['content'];
            for (const stand in content) {
                const positions = content[stand]['positions']
                const isAvailable = content[stand]['available'];
                for (const [x, y] of positions) {
                    const cell = this.cells[x][y]
                    cell.innerText = parseInt(stand) + 1;
                    cell.classList.toggle('empty');
                    cell.classList.toggle(isAvailable ? 'available' : 'unavailable');
                }
                const [minRow, maxRow, minCol, maxCol] = getExtrems(content[stand]['positions']);
                putBorders(_this.cells, content[stand]['positions'].length, minRow, minCol, maxRow, maxCol);
            }
            this.cloneCells();
        })

        // get all the grid positions associated with this event

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
                _this.submitStandRequest();
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

    submitStandRequest() {
        const wholeEvent = document.getElementById('whole-event').checked
        const selectedGrid = getSelectedById(this.cells);
        const data = {
            'wholeEvent': wholeEvent,
            'grid': selectedGrid
        }

        if (!wholeEvent) {
            const initialDate = document.getElementById('id_initial_date').value;
            const finalDate = document.getElementById('id_final_date').value;
            data['initial_date'] = initialDate
            data['final_date'] = finalDate
        }

        sendRequest('/stand-request/' + this.eventId, 'POST', data).then((r) => {
            Swal.fire(
                'Success!',
                'Your stand has been submitted.',
                'success'
            ).then(() => {
                const reservationId = r.data['content']['reservation'];
                window.location.replace('/stand-services/?reservation=' + reservationId);
            })
        }).catch((r) => {
            console.log("response", r);
            Swal.fire({
                icon: 'error',
                title: 'Error submitting your request',
                text: r.response.data['content'],
            })
        });

    }

}

export {Context}