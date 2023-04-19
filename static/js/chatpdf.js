$("#uploadForm").on("submit", function (event) {
  event.preventDefault();

  var formData = new FormData();
  formData.append("file", $("#document-file")[0].files[0]);
  $.ajax({
      url: "/chatpdf/upload",
      type: "POST",
      data: formData,
      success: function () {
          alert("File uploaded and training started");
          $("#upload-success-msg").css("display", "block");
      },
      error: function (jqXHR, textStatus, errorThrown) {
          alert("Error: " + errorThrown);
      },
      cache: false,
      contentType: false,
      processData: false,
  });
});


function appendMessage(user, message) {
  var chat = $("#chat");
  chat.val(chat.val() + user + ": " + message + "\n");
  chat.scrollTop(chat[0].scrollHeight);
}


$("#askBtn").click(function () {
  var question = $("#question").val();
  if (question.trim() === "") {
    alert("Please enter a question");
    return;
  }

  $.ajax({
    url: "/ask",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ question: question }),
    success: function (response) {
      if (response.success) {
        appendMessage("User", question);
        appendMessage("Bot", response.answer);
        $("#question").val("");
      } else {
        alert("Error: " + response.message);
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      alert("Error: " + errorThrown);
    },
  });
});
