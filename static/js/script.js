// JS for interactive elements like modals, forms, etc.
// Submit event for the product form

document
	.getElementById("addProductForm")
	.addEventListener("submit", function (e) {
		e.preventDefault();
		// Get product details from the form
		let productName = document.getElementById("productName").value;
		let productImage = document.getElementById("productImage").files[0];
		// TODO: Upload image and product details to server
		// Then update the product list
		let productItem = document.createElement("li");
		productItem.className = "list-group-item";
		productItem.innerHTML = `${productName} 
                <span class="float-right">
                    <a href="#" class="mr-2"><i class="fas fa-edit"></i></a>
                    <a href="#" class="text-danger"><i class="fas fa-trash"></i></a>
                </span>`;
		document.getElementById("productList").appendChild(productItem);
		// Reset form and close modal
		document.getElementById("productName").value = "";
		$("#addProductModal").modal("hide");
	});
