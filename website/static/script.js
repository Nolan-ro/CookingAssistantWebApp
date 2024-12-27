function sendMessage() {
    var userInput = document.getElementById("user_input").value;
    if (userInput.trim() === "") return;
    
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += "<div><b>You:</b> " + userInput + "</div>";

    fetch("/get_response", {
        method: "POST",
        body: new URLSearchParams("user_input=" + userInput),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json())
    .then(data => {
        var botResponse = "<div><b>Cooking Assistant:</b> " + data.response;
        // Add save button if response contains a recipe (checking for numbered steps)
        if (data.response.includes("1.") && data.response.includes("Ingredients")) {
            botResponse += '<br><button class="btn btn-success mt-2" onclick="save_recipe(this.parentElement)">Save Recipe</button>';
        }
        
        botResponse += "</div>";
        messagesDiv.innerHTML += botResponse;
        document.getElementById("user_input").value = "";
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

function save_recipe(recipe) { 
    console.log("script.js save_recipe called")
    const recipeText = recipe.innerHTML;

    fetch("/save_recipe", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ recipe: recipeText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Recipe saved successfully!");
        }
    });
}

function deleteRecipe(recipeId) {
    console.log("script.js deleteRecipe called")
    if (confirm('Are you sure you want to delete this recipe?')) {
        fetch("/delete_recipe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ recipe_id: recipeId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    }
}




