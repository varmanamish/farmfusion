document.addEventListener("DOMContentLoaded", function () {
    let cart = [];

    // Add event listeners to all "Add to Cart" buttons
    document.querySelectorAll(".btn-cart").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            let productElement = this.closest(".product-item");
            let productId = this.getAttribute("data-product-id");
            let quantityInput = productElement.querySelector(".quantity");
            let quantity = quantityInput ? quantityInput.value : 1;
            let productName = productElement.querySelector("h3").textContent;
            let productPrice = productElement.querySelector(".text-dark").textContent.replace("$", "");

            let product = {
                id: productId,
                name: productName,
                price: parseFloat(productPrice),
                quantity: parseInt(quantity)
            };

            // Send request to Django backend
            fetch("/shop/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: `product_id=${productId}&quantity=${quantity}`
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                document.querySelector(".badge.bg-primary").innerText = data.cart_count;

                // Update frontend cart UI

                cart.push(product);
                updateCartUI();
            })
            .catch(error => console.error("Error:", error));
        });
    });

    function updateCartUI() {
        const cartList = document.querySelector(".list-group");
        const cartTotal = document.querySelector(".list-group-item strong");
        cartList.innerHTML = "";
        let total = 0;

        cart.forEach(item => {
            total += item.price * item.quantity;
            cartList.innerHTML += `
                <li class="list-group-item d-flex justify-content-between lh-sm">
                    <div>
                        <h6 class="my-0">${item.name}</h6>
                        <small class="text-body-secondary">x ${item.quantity}</small>
                    </div>
                    <span class="text-body-secondary">$${(item.price * item.quantity).toFixed(2)}</span>
                </li>
            `;
        });

        cartList.innerHTML += `
            <li class="list-group-item d-flex justify-content-between">
                <span>Total (USD)</span>
                <strong>$${total.toFixed(2)}</strong>
            </li>
        `;
    }

    function getCSRFToken() {
        let tokenElement = document.querySelector("meta[name='csrf-token']");
        return tokenElement ? tokenElement.getAttribute("content") : null;
    }
});
