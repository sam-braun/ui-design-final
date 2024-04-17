document.addEventListener('DOMContentLoaded', function() {
    // The quizForm submission is now handled normally by the browser.
    // Therefore, we don't need any specific JavaScript to handle the quiz form submission.
    // The form action will point to the server's submit route, which will handle the storage of answers and navigation.

    // The displayAlert and createAlertPlaceholder functions can remain in case you want to display messages to the user for other purposes.
});

// Function to display alerts with Bootstrap styling
function displayAlert(message) {
    const alertPlaceholder = document.getElementById('alertPlaceholder') || createAlertPlaceholder();
    const alertDiv = document.createElement('div');
    
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.textContent = message;
    
    const closeButton = document.createElement('button');
    closeButton.className = 'btn-close';
    closeButton.type = 'button';
    closeButton.dataset.bsDismiss = 'alert';
    closeButton.ariaLabel = 'Close';
    alertDiv.appendChild(closeButton);

    alertPlaceholder.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.classList.remove('show');
    }, 5000);
}

// Function to create the alert placeholder if it doesn't exist
function createAlertPlaceholder() {
    const placeholder = document.createElement('div');
    placeholder.id = 'alertPlaceholder';
    document.body.insertBefore(placeholder, document.body.firstChild); // Place at the top
    return placeholder;
}

