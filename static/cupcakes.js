const BASE_URL = "http://localhost:5000/api";


/** given data about a cupcake, generate html */

function CupcakeHTML(cake) {
    return `
    <div cake-id="${cake.id}">
    <div class="col-sm">
    <div class="card" style="width: 14rem;">
        <img class="Cupcake-img" src="${cake.image}" alt="(no image provided)" width="220" height="220">
        <div class=" card-body">
            <li>
                ${cake.id}
            </li>
            <li>
                ${cake.flavor}
            </li>
            <li>
                ${cake.size}
            </li>
            <li>
                ${cake.rating}
            </li>
            <button class="delete-button btn btn-primary" data-id="${cake.id}">Delete</button>
        </div>
    </div>
    <br>
</div>
</div>
  `;
}


/** put initial cupcakes on page. */

async function showInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cake) {
        let newCupcake = $(CupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}


/** handle form for adding of new cupcakes */

$("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(CupcakeHTML(newCupcakeResponse.data.cake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});


/** handle clicking delete: delete cupcake */


$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target.parentNode.parentNode.parentNode.parentNode).closest("div");
    let cupcakeId = $cupcake.attr("cake-id");
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showInitialCupcakes);