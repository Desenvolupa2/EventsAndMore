export function clearSelection() {
    if (window.getSelection) {
        window.getSelection().removeAllRanges();
    } else if (document.selection) {
        document.selection.empty();
    }
}

export function isCell(target) {
    return target.classList.contains("cell");
}

export function isEmpty(target) {
    return target.classList.contains("empty");
}

export function isSelected(target) {
    return target.classList.contains("selected");
}

export function isConfirmed(target) {
    return target.classList.contains("confirmed");
}
