$(document).ready(function () {
  // Handle Borrow Request
  $("body").on("click", ".request-borrow", function () {
      $(this).text("Request Sent!");
      $(this).css("background-color", "#9AC7F3");
      $("#borrow-message").html("<p class='success-msg'>✅ Request submitted! The owner will contact you soon.</p>");
  });

  // Handle Rating Click
  $(".rating-stars .star").click(function () {
      const bookId = $(".rating-stars").data("book-id");
      const selectedRating = $(this).data("value");
  
      $.ajax({
        url: `/api/rate-book/${bookId}/`,
        method: "POST",
        data: {
          rating: selectedRating,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (data) {
          $("#rating-result").text(`You rated this book ${data.new_rating} stars!`);
  
          // Update the stars visually
          $(".rating-stars .star").each(function () {
            const starVal = $(this).data("value");
            $(this).text(starVal <= data.new_rating ? "★" : "☆");
          });
        }
      });
  });

    // Handle submitting a new review
    $("#submit-review").click(function (e) {
      e.preventDefault();

      const bookId = $(".rating-stars").data("book-id");  // Or another hidden field with book id
      const content = $("#review-content").val();
      const rating = $("#review-rating").val();

      $.ajax({
          url: `/api/add-review/${bookId}/`,
          method: "POST",
          data: {
              content: content,
              rating: rating,
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
          },
          success: function (data) {
              if (data.status === "success") {
                const newReviewHtml = `
                <div class="review-item" id="review-${data.review_id}">
                    <p>
                        <span class="timestamp">just now</span> |
                        <a href="/profile/${data.username}/">${data.username}</a> |
                        <span class="stars">
                            ${"★".repeat(data.rating)}${"☆".repeat(5 - data.rating)}
                        <span class="review-text">${data.content}</span>
                        <button class="icon-button edit-review" data-review-id="${data.review_id}" data-current-content="${data.content}" data-current-rating="${data.rating}">✏️</button>
                        <button class="icon-button delete-review" data-review-id="${data.review_id}">🗑️</button>
                    </p>
                </div>
            `;
                  $(".reviews").prepend(newReviewHtml);
                  $("#review-content").val("");  // Clear textarea
                  $("#review-rating").val("5");  // Reset rating to 5 stars
              } else {
                  alert("Failed to add review.");
              }
          }
      });
  });

  // Handle deleting a review
  $("body").on("click", ".delete-review", function () {
      const reviewId = $(this).data("review-id");

      $.ajax({
          url: `/api/delete-review/${reviewId}/`,
          method: "POST",
          data: {
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
          },
          success: function (data) {
              if (data.status === "success") {
                  $(`#review-${reviewId}`).remove();
              } else {
                  alert("Failed to delete review.");
              }
          }
      });
  });

  $("body").on("click", ".edit-review", function () {
    const reviewId = $(this).data("review-id");
    const currentContent = $(this).data("current-content");
    const currentRating = $(this).data("current-rating");

    // Show a prompt to edit (simple version)
    const newContent = prompt("Edit your review:", currentContent);
    const newRating = prompt("Edit your rating (1-5):", currentRating);

    if (newContent !== null && newRating !== null) {
        $.ajax({
            url: `/api/edit-review/${reviewId}/`,
            method: "POST",
            data: {
                content: newContent,
                rating: newRating,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                if (data.status === "success") {
                    // Update the text on the page
                    $(`#review-${reviewId} .review-text`).text(newContent);
                    $(`#review-${reviewId} .stars`).html("★".repeat(data.new_rating) + "☆".repeat(5 - data.new_rating));
                } else {
                    alert("Failed to edit review.");
                }
            }
        });
    }
});

});