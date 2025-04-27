$(document).ready(function () {
    // When the user hovers over a book item
    $(".book-list").on("mouseenter", ".book-item", function () {
      const bookDiv = $(this);
      const bookId = bookDiv.data("book-id");
      const resultArea = bookDiv.find(".availability-result");
  
      // Highlight the hovered book
      bookDiv.css("background-color", "#9AC7F3");
  
      // Add "View Details" button if it doesn't exist
      if (bookDiv.find(".extra-info").length === 0) {
        const detailsLink = $(`<a href="/books/${bookId}/" class="extra-info btn">View Details</a>`);
        bookDiv.append(detailsLink);
      }
  
      if (resultArea.text().trim() === "") {
        $.get(`/api/book-availability/${bookId}/`, function (data) {
          const text = data.available
            ? `✅ Available at ${data.location}`
            : `❌ Currently unavailable`;
          resultArea.text(text);
        });
      }
    });
  
    // When the user moves the mouse away
    $(".book-list").on("mouseleave", ".book-item", function () {
      const bookDiv = $(this);
      bookDiv.css("background-color", "");
      bookDiv.find(".extra-info").remove();
      bookDiv.find(".availability-result").text("");
    });
  });
  