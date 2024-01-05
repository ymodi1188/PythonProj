// Additional JavaScript to send frames to the backend
// Assuming we are sending frames at a set interval

const video = document.getElementById("video");
let isStreaming = false;

document.getElementById("startButton").addEventListener("click", () => {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
        isStreaming = true;
        streamFrames();
      })
      .catch((err) => {
        console.error("Error accessing the camera: ", err);
      });
  } else {
    alert("Your browser does not support media devices.");
  }
});

function streamFrames() {
  const canvas = document.createElement("canvas");
  canvas.width = 640;
  canvas.height = 480;
  const ctx = canvas.getContext("2d");

  // Function to capture and send frames
  const capture = () => {
    if (!isStreaming) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(sendFrame, "image/jpeg");
    setTimeout(capture, 1000); // capture frame every second
  };

  capture();
}

function sendFrame(blob) {
  const data = new FormData();
  data.append("frame", blob);

  fetch("/analyze", {
    method: "POST",
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Mood:", data.mood);
      // You can update the UI with the mood analysis result
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
