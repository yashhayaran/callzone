'use strict';

document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();
  });

  inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
      if (inputElement.files[0] != null) {
        inputFileChange(inputElement.files[0]);
      }
      else {
        console.log("error");
        showMessage(
          false,
          true,
          "Input file is null! Please refresh the page, upload the file again."
        );
      }
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      //updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }

    dropZoneElement.classList.remove("drop-zone--over");
  });
});

// Show message to user
function showMessage(resetToNormal = false, isError = false, message = "") {
  let messageArea = document.getElementById("upload-message");

  if (messageArea != null) {
    messageArea.textContent = message;
    if (!resetToNormal && isError) {
      messageArea.className = "upload-message-style error";
    }
    else {
      messageArea.className = "upload-message-style";
    }
  }
  else {
    console.error("ERROR: Couldn't find the return of document.getElementById(upload-message)")
  }

  if (isError) {
    enableUploadButton(false);
  }
}

function enableUploadButton(enable = true) {
  let button = document.getElementById("upload-button");
  if (enable)
    button.removeAttribute("disabled");
  else
    button.setAttribute("disabled", "true");
}

// When user selects a file
function inputFileChange(file) {
  console.log(file);
  const MAX_SIZE_ALLOWED = 20971520;
  let message = "File '" + file.name;

  if (file.size < MAX_SIZE_ALLOWED) {
    message += "' selected. Click upload button for action!";
    showMessage(true, false, message);
    enableUploadButton();
    //updateThumbnail(dropZoneElement, inputElement.files[0]);
  }
  else {
    message += "' size is bigger than allowed size of 20MB";
    showMessage(false, true, message);
  }
}

function uploadFile() {
  let inputElement = document.getElementById("audio_file_input");
  if (inputElement.files.length) {
    let audioFile = inputElement.files[0];
    let form_data = new FormData();
    console.log(form_data);
    form_data.append("audio_file", audioFile);
    postForm(form_data, "/playground/upload_file")
      .then(success => {
        showMessage(false, true, "UPLOADED");
        console.log('result: ', success);
      })
      .catch(error => {
        console.log('request failed', error);
      })
      .finally(function finallyHere(e) {
        console.log(e);
      });
  }
}

{
  let uploadButton = document.getElementById("upload-button");
  if (uploadButton != null) {
    uploadButton.addEventListener("click", (e) => {
      e.preventDefault();
      uploadFile();
    });
  }
}