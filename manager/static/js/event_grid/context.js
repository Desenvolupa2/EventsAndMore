import {clearSelection, dateIsSelected, getPercentageSelected, updateStand} from "../utils.js";
import {Default} from "./states/default.js";
import {Selecting} from "./states/selecting.js";

class Context {
    constructor(cells) {
        this.cells = cells;
        this.cellsCopy = JSON.parse(JSON.stringify(cells)); // deepcopy
        this.states = [new Default(this), new Selecting(this)];
        this.current = this.states[0];
        this.nextId = 1;
    }

    change(state, event) {
        // console.log(this.current.toString(), " -> ", newState.toString())
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


        document.getElementById("button-all").addEventListener(
            "click",
            (event) => {
                _this.selectAll(event);
                getPercentageSelected(_this.cells).then(percentage => {
                    document.getElementById('percentage').innerText = (percentage * 100).toFixed(1);
                });
            }
        )

        document.getElementById("button-left").addEventListener(
            "click",
            (event) => {
                _this.selectLeftHalf(event);
                getPercentageSelected(_this.cells).then(percentage => {
                    document.getElementById('percentage').innerText = (percentage * 100).toFixed(1);
                });
            }
        )

        document.getElementById("button-right").addEventListener(
            "click",
            (event) => {
                _this.selectRightHalf(event);
                getPercentageSelected(_this.cells).then(percentage => {
                    document.getElementById('percentage').innerText = (percentage * 100).toFixed(1);
                });
            }
        )

        document.getElementById("button-reset").addEventListener(
            "click",
            (event) => {
                _this.current.handleReset(event);
            }
        )

        document.getElementById("id_initial_date").addEventListener('change', () => {
            if (dateIsSelected('id_initial_date') && dateIsSelected('id_final_date')) {
                _this.updateAvailablePositions();
            }
        })

        document.getElementById("id_final_date").addEventListener('change', () => {
            if (dateIsSelected('id_initial_date') && dateIsSelected('id_final_date')) {
                _this.updateAvailablePositions();
            }
        })

        _this.current.run();
    };

    updateAvailablePositions() {
        //make request with inital and final date
        const initialDate = document.getElementById('id_initial_date').value;
        const finalDate = document.getElementById('id_final_date').value;
        if (Date.parse(initialDate) > Date.parse(finalDate)) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Final date can\'t be before initial date',
            })
            return;
        }
        const url = '/grid-positions/?initial_date=' + initialDate + '&final_date=' + finalDate;
        sendRequest(url, 'GET', null).then((response) => {
            for (const stand of response.data['content']) {
                updateStand(this, stand).then(_ => {
                })
            }
        })
    }

    selectAll(event) {
        for (let i = 0; i < this.cells.length; i++) {
            for (let j = 0; j < this.cells[0].length; j++) {
                if (this.cells[i][j].classList.contains('available')) {
                    this.cells[i][j].classList.toggle('selected');
                    this.cells[i][j].classList.toggle('available');
                }
            }
        }
    }

    selectLeftHalf(event) {
        for (let i = 0; i < this.cells.length; i++) {
            for (let j = 0; j < this.cells[0].length / 2; j++) {
                if (this.cells[i][j].classList.contains('available')) {
                    this.cells[i][j].classList.toggle('selected');
                    this.cells[i][j].classList.toggle('available');
                }
            }
        }
    }

    selectRightHalf(event) {
        for (let i = 0; i < this.cells.length; i++) {
            for (let j = this.cells[0].length / 2; j < this.cells[0].length; j++) {
                if (this.cells[i][j].classList.contains('available')) {
                    this.cells[i][j].classList.toggle('selected');
                    this.cells[i][j].classList.toggle('available');
                }
            }
        }
    }

}

export {Context}