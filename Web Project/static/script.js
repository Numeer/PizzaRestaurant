document.addEventListener("DOMContentLoaded", function() {
  
  var addToCartButtons = document.querySelectorAll(".add-to-cart");
  addToCartButtons.forEach(function(button) {
    button.addEventListener("click", addToCart);
  });

  // Function to handle the "Add to Cart" button click
  function addToCart(event) {
    var menuItem = event.target.parentNode;
    var itemName = menuItem.querySelector("h3").textContent;
    var selectedSize = menuItem.querySelector(".size-selection").value;
    var itemPrice = menuItem.querySelector(".size-selection").getAttribute("data-price-" + selectedSize.toLowerCase());

    var cartItem = document.createElement("li");
    cartItem.textContent = itemName + " - " + selectedSize + " - " + itemPrice;

    var removeButton = document.createElement("button");
    removeButton.textContent = "Remove";
    removeButton.classList.add("remove-from-cart");
    removeButton.addEventListener("click", removeFromCart);

    cartItem.appendChild(removeButton);

    var cartItemsList = document.getElementById("cart-items");
    cartItemsList.appendChild(cartItem);

    updateTotalPrice();

    // Send the cart item to the Flask endpoint
    sendCartItemToFlask({
      itemName: itemName,
      itemSize: selectedSize,
      itemPrice: itemPrice
    });
  }

  // Function to handle the "Remove" button click
  function removeFromCart(event) {
    var cartItem = event.target.parentNode;
    var cartItemsList = document.getElementById("cart-items");

    cartItemsList.removeChild(cartItem);
    updateTotalPrice();
  }

  // Function to update the total price in the cart
  function updateTotalPrice() {
    var cartItemsList = document.getElementById("cart-items");
    var cartItems = cartItemsList.getElementsByTagName("li");
    var totalPrice = 0;

    for (var i = 0; i < cartItems.length; i++) {
      var itemPrice = parseFloat(cartItems[i].textContent.split(" - ")[2]);
      totalPrice += itemPrice;
    }

    var totalPriceElement = document.getElementById("total-price");
    totalPriceElement.textContent = "Total Price: Rs " + totalPrice;
  }
});
// Handle checkout button click
var checkoutButton = document.getElementById("checkout");
checkoutButton.addEventListener("click", function () {
  // Create a list of line items for the checkout session
  var lineItems = [];
  var cartItemsList = document.getElementById("cart-items");
  var cartItems = cartItemsList.getElementsByTagName("li");

  for (var i = 0; i < cartItems.length; i++) {
    var item = cartItems[i].textContent.split(" - ");
    var itemName = item[0];
    var itemSize = item[1];
    var itemPrice = parseFloat(item[2]);

    lineItems.push({
      name: itemName,
      size: itemSize,
      price: itemPrice,
    });
  }

  // Send the line items to the Flask endpoint for further processing
  sendLineItemsToFlask(lineItems);
});

// Function to send the line items to the Flask endpoint
function sendLineItemsToFlask(lineItems) {
  fetch("/checkout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ lineItems }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data.message);
      window.location.href = "/confirm";
    })
    .catch(function (error) {
      console.error(error);
    });
}
