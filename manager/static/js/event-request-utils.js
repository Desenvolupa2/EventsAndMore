import {sendRequest} from "./utils.js";

export function changeEventDate(eventRequestId) {
    Swal.fire({
        title: "Pick new dates",
        html: `
            <div class="col justify-content-center text-center">
                <div class="row py-2 justify-content-center text-center">
                    <label class="px-2" for=datepicker-initial>Initial date</label><input type="date" id="datepicker-initial">
                </div>
                <div class="row py-2 justify-content-center text-center">
                    <label class="px-2" for=datepicker-final>Final date</label><input type="date" id="datepicker-final">
                </div>
            </div>`,
        showConfirmButton: true,
        showCancelButton: true,
    }).then(function () {
        let initialDate = document.getElementById('datepicker-initial').value;
        let finalDate = document.getElementById('datepicker-final').value;
        if (!initialDate || !finalDate || initialDate === "" || finalDate === "") {
            return
        }
        let data = {};
        data['initial_date'] = initialDate;
        data['final_date'] = finalDate;
        data['status'] = 2;
        sendRequest('/event-requests/' + eventRequestId + "/", 'put', data)
            .then(() => {
                Swal.fire({
                    icon: 'success',
                    title: 'Changes submitted',
                    text: 'Your proposal has been submitted'
                }).then(() => {
                    location.reload();
                })
            })
            .catch(() => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error updating address. There was no change submitted'
                })
            });
    })
    ;
}

export function acceptEvent(eventRequestId) {
    let data = {};
    data['status'] = 3;
    sendRequest('/event-requests/' + eventRequestId + "/", 'put', data)
        .then(() => {
            Swal.fire({
                icon: 'success',
                title: 'Event accepted',
            }).then(() => {
                location.reload();
            })
        })
        .catch(() => {
            Swal.fire({
                icon: 'error',
                title: 'Error accepting the event request.'
            })
        });
}

export function denyEvent(eventRequestId) {
    let data = {};
    data['status'] = 4;
    sendRequest('/event-requests/' + eventRequestId + "/", 'put', data)
        .then(() => {
            Swal.fire({
                icon: 'success',
                title: 'Event denied',
            }).then(() => {
                location.reload();
            })
        })
        .catch(() => {
            Swal.fire({
                icon: 'error',
                title: 'Error denying the event request.'
            })
        });
}

window.acceptEvent = acceptEvent
window.denyEvent = denyEvent
window.changeEventDate = changeEventDate
