export function clearSelection() {
    if (window.getSelection) {
        window.getSelection().removeAllRanges();
    } else if (document.selection) {
        document.selection.empty();
    }
}

export function isCell(target) {
    if ('classList' in target) {
        return target.classList.contains("cell");
    }
    return false;
}

export function isEmpty(target) {
    if ('classList' in target) {
        return target.classList.contains("empty");
    }
    return false;
}

export function isSelected(target) {
    if ('classList' in target) {
        return target.classList.contains("selected");
    }
    return false;
}


export function isAvailable(target) {
    if ('classList' in target) {
        return target.classList.contains("available");
    }
    return false;
}

export function isUnavailable(target) {
    if ('classList' in target) {
        return target.classList.contains("unavailable");
    }
    return false;
}

export function isConfirmed(target) {
    if ('classList' in target) {
        return target.classList.contains("confirmed");
    }
    return false;
}

export function dateIsSelected(element) {
    return document.getElementById(element).value !== "";
}

export async function updateStand(context, stand_id, positions) {
    for (let position of positions) {
        const row = position['x_position'];
        const col = position['y_position'];

        if (context.cells[row][col].classList.contains('empty')) {
            context.cells[row][col].classList.toggle('empty');
            context.cells[row][col].classList.toggle(position['available'] ? 'available' : 'unavailable');
        }

        if (position['available']) {
            // if was unavailable -> set available
            if (context.cells[row][col].classList.contains('unavailable')) {
                context.cells[row][col].classList.toggle('unavailable');
                context.cells[row][col].classList.toggle('available');
            }
        } else {
            // if was available -> set unavailable
            if (context.cells[row][col].classList.contains('available')) {
                context.cells[row][col].classList.toggle('available');
                context.cells[row][col].classList.toggle('unavailable');
            }
        }
        context.cells[row][col].innerText = stand_id;
    }
    const selected = positions.map(function (position) {
        return [position['x_position'], position['y_position']]
    });
    const [minRow, maxRow, minCol, maxCol] = getExtrems(selected);
    putBorders(context.cells, selected.length, minRow, minCol, maxRow, maxCol)
    context.cloneCells()

}


export async function getPercentageSelected(cells) {
    let total = cells.length * cells[0].length;
    let selected = 0;
    for (let i = 0; i < cells.length; i++) {
        for (let j = 0; j < cells[0].length; j++) {
            if (cells[i][j].classList.contains('selected')) {
                selected += 1;
            }
        }
    }
    return selected / total;
}

export function getSelected(cells) {
    let selected = [];
    for (let i = 0; i < cells.length; i++) {
        for (let j = 0; j < cells[0].length; j++) {
            if (cells[i][j].classList.contains('selected')) {
                selected.push([i, j])
            }
        }
    }
    return selected;
}

export function putBorders(cells, selected, minRow, minCol, maxRow, maxCol) {
    if (selected === 1) {
        cells[minRow][minCol].classList.add('border-left');
        cells[minRow][minCol].classList.add('border-right');
        cells[minRow][minCol].classList.add('border-top');
        cells[minRow][minCol].classList.add('border-bottom');
    } else if (selected === 2) {
        if (minCol === maxCol) {
            // same column
            cells[minRow][minCol].classList.add('border-left');
            cells[minRow][minCol].classList.add('border-top');
            cells[minRow][minCol].classList.add('border-right');

            cells[maxRow][minCol].classList.add('border-left');
            cells[maxRow][minCol].classList.add('border-bottom');
            cells[maxRow][minCol].classList.add('border-right');

        } else {
            // same row
            cells[minRow][minCol].classList.add('border-left');
            cells[minRow][minCol].classList.add('border-top');
            cells[minRow][minCol].classList.add('border-bottom');

            cells[minRow][maxCol].classList.add('border-top');
            cells[minRow][maxCol].classList.add('border-right');
            cells[minRow][maxCol].classList.add('border-bottom');

        }
    } else {
        // square
        cells[minRow][minCol].classList.add('border-left');
        cells[minRow][minCol].classList.add('border-top');

        cells[minRow][maxCol].classList.add('border-top');
        cells[minRow][maxCol].classList.add('border-right');

        cells[maxRow][minCol].classList.add('border-bottom');
        cells[maxRow][minCol].classList.add('border-left');

        cells[maxRow][maxCol].classList.add('border-right');
        cells[maxRow][maxCol].classList.add('border-bottom');
    }
}

export function getExtrems(arr) {
    const rows = arr.map((coords) => {
        return coords[0];
    })
    const cols = arr.map((coords) => {
        return coords[1];
    })
    return [Math.min(...rows), Math.max(...rows), Math.min(...cols), Math.max(...cols)];
}