class State {

    constructor(context) {
        this.context = context;
    }

    run(event) { throw new Error('unimplemented'); }

    handleMouseup() { throw new Error('unimplemented'); }

    handleMousedown(event) { throw new Error('unimplemented'); }

    handleMousemove(event) { throw new Error('unimplemented'); }

    handleReset(event) { throw new Error('unimplemented'); }

    submitStand(event) { throw new Error('unimplemented'); }

}


export {State}