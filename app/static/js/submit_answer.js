$(document).ready(function () {
    // Handle Submit Answer
    $("#submit-answer").click(function () {
      const currentNumber = parseInt($("#quiz-container").data("current-number"));
      const totalQuestions = parseInt($("#quiz-container").data("total-questions"));
  
      if (currentNumber === totalQuestions) {
        // Check login status via AJAX
        $.ajax({
          url: "/auth/check-login-status",
          method: "GET",
          success: function (response) {
            if (!response.logged_in) {
              // Show login modal
              $("#login-modal").removeClass("hidden").addClass("flex");
  
              // Save action in session storage
              sessionStorage.setItem("pendingAction", "submitLastAnswer");
            } else {
              // User is logged in, submit the form
              $("#answer-form").submit();
            }
          },
          error: function () {
            alert("An error occurred while checking login status.");
          },
        });
      } else {
        // Not the last question, submit directly
        $("#answer-form").submit();
      }
    });
    // Close Modal
    $("#close-modal").click(function () {
      $("#login-modal").removeClass("flex").addClass("hidden");
    });
  });
