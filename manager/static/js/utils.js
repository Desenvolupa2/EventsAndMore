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

export async function updateStand(context, stand) {
    const row = stand['x_position'];
    const col = stand['y_position'];

    if (context.cells[row][col].classList.contains('empty')) {
        context.cells[row][col].classList.toggle(stand['available'] ? 'available' : 'unavailable');
    }

    if (stand['available']) {
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
    context.cellsCopy[row][col] = context.cells[row][col].cloneNode()
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