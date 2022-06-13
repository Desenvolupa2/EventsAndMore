import {sendRequest} from "../utils.js";


let serviceList = {}; // key=standReservationId, values= List of services
let categories = null;

function createForm(parent, standReservationId) {
    const element = document.createElement("div");
    const countId = standReservationId in serviceList ? serviceList[standReservationId].length + 1 : 0;
    parent.insertAdjacentHTML(
        "beforebegin",
        `
                <div class="mb-3" id="service-form-${standReservationId}-${countId}">
                    <div class="row">
                        <div class="col mx-1">
                            <div class="row"><b><label for="category-${standReservationId}-${countId}">Category</label></b>
                            </div>
                            <div class="row">
                                <select class="form-control" name="category" id="category-${standReservationId}-${countId}">
                                    <option value="" selected>----------</option>
                                </select>
                            </div>
                        </div>
                        <div class="col mx-1">
                            <div class="row"><b><label for="subcategory-${standReservationId}">Subcategory</label></b>
                            </div>
                            <div class="row">
                                <select class="form-control" name="subcategory"
                                        id="subcategory-${standReservationId}-${countId}">
                                    <option value="" selected>----------</option>
                                </select>
                            </div>
                        </div>
                        <div class="col mx-1">
                            <div class="row"><b><label for="service-${standReservationId}-${countId}">Service</label></b>
                            </div>
                            <div class="row">
                                <select class="form-control" name="service" id="service-${standReservationId}-${countId}">
                                    <option value="" selected>----------</option>
                                </select>
                            </div>
                        </div>
                        <div class="col mx-1">
                            <div class="row"><b><label for="quantity-${standReservationId}-${countId}">Quantity</label></b>
                            </div>
                            <div class="row">
                                <input type="number" class="form-control" name="quantity"
                                       id="quantity-${standReservationId}-${countId}" min="0" value="0">
                            </div>
                        </div>
                        <div class="col mx-1">
                            <div class="row"><b><label for="comments-${standReservationId}-${countId}">Comments</label></b>
                            </div>
                            <div class="row">
                    <textarea class="form-control" placeholder="Leave a comment here" name="comments"
                              id="comments-${standReservationId}-${countId}"></textarea>
                            </div>
                        </div>
                        <div class="col mx-1 d-flex align-items-center">
                            <button class="btn btn-primary"
                            onclick="addService(${standReservationId}, ${countId})"
                            id="add-button-${standReservationId}-${countId}">Add</button>
                        </div>
                    </div>
                </div>
    `
    )
    for (const cat of categories) {
        let option = document.createElement('option');
        option.text = cat['name'];
        option.value = cat["id"]
        document.getElementById("category-" + standReservationId + "-" + countId).appendChild(option)
    }

    $("#category-" + standReservationId + "-" + countId).change(function () {
        var url = '/load-subcategories/';
        var categoryId = $(this).val();
        $.ajax({
            url: url + categoryId,
            success: function (data) {
                $("#subcategory-" + standReservationId + "-" + countId).html(data);
            }
        });
    });

    $("#subcategory-" + standReservationId + "-" + countId).change(function () {
        var url = '/load-services/';
        var categoryId = $(this).val();
        $.ajax({
            url: url + categoryId,
            success: function (data) {
                $("#service-" + standReservationId + "-" + countId).html(data);
            }
        });
    });
    return element;
}


function addServiceLine(instance, standReservationId) {
    const parent = instance.parentNode.parentNode;
    const form = createForm(parent, standReservationId);
    parent.appendChild(form);
    document.getElementById("add-line-button-" + standReservationId).classList.toggle("invisible");
}

window.addServiceLine = addServiceLine;

function addService(standReservationId, serviceId) {
    if (!(standReservationId in serviceList)) {
        serviceList[standReservationId] = [];
    }
    serviceList[standReservationId].push(getProduct(standReservationId, serviceId))
    document.getElementById("add-line-button-" + standReservationId).classList.toggle("invisible");
    document.getElementById("add-button-" + standReservationId + "-" + serviceId).classList.toggle("invisible");
    document.getElementById("category-" + standReservationId + "-" + serviceId).disabled = true;
    document.getElementById("subcategory-" + standReservationId + "-" + serviceId).disabled = true;
    document.getElementById("service-" + standReservationId + "-" + serviceId).disabled = true;
    document.getElementById("quantity-" + standReservationId + "-" + serviceId).disabled = true;
    document.getElementById("comments-" + standReservationId + "-" + serviceId).disabled = true;
}

window.addService = addService;


function getProduct(standReservationId, serviceId) {
    const product = document.getElementById("service-" + standReservationId + "-" + serviceId).value;
    const quantity = parseInt(document.getElementById("quantity-" + standReservationId + "-" + serviceId).value);
    const comments = document.getElementById("comments-" + standReservationId + "-" + serviceId).value;
    return [product, quantity, comments]
}

function submitServices() {
    const param = window.location.search;
    let data = {
        "reservation": param.substring(param.lastIndexOf('=') + 1),
        "services": serviceList
    }
    sendRequest('/stand-services/', 'POST', data).then(() => {
        Swal.fire(
            'Success!',
            'Your additional services have been submitted.',
            'success'
        ).then(() => {
            window.location.replace('/stand-reservations/')
        })
    })
}

window.submitServices = submitServices;

window.onload = () => {
    sendRequest('/load-categories/', 'GET', null).then(r => {
        categories = r.data["categories"];
    })
}