const waitForElement = (selector, callback) => {
  const el = document.querySelector(selector);
  if (el) {
    callback(el);
  } else {
    setTimeout(() => waitForElement(selector, callback), 100);
  }
};

waitForElement("#upload-btn", () => {
  const fileInput = document.getElementById("upload-data");
  const uploadBtn = document.getElementById("upload-btn");
  const pauseBtn = document.getElementById("pause-btn");
  const resumeBtn = document.getElementById("resume-btn");
  const cancelBtn = document.getElementById("cancel-btn");
  const progressEl = document.getElementById("upload-progress");
  const outputText = document.getElementById("output-data-upload");

  if (!fileInput || !uploadBtn || !pauseBtn || !resumeBtn || !cancelBtn || !progressEl || !outputText) {
    console.error("Algunos elementos no se encontraron");
    return;
  }

  let file,
    chunkSize = 512 * 1024;
  let currentChunk = 0,
    totalChunks = 0;
  let paused = false,
    cancelled = false;

  const uploadChunk = async () => {
    if (paused || cancelled || currentChunk >= totalChunks) return;

    const start = currentChunk * chunkSize;
    const end = Math.min(file.size, start + chunkSize);
    const chunk = file.slice(start, end);

    await fetch("/upload_chunk", {
      method: "POST",
      headers: {
        "Content-Type": "application/octet-stream",
        "X-Filename": file.name,
        "X-Chunk-Index": currentChunk,
        "X-Total-Chunks": totalChunks,
      },
      body: chunk,
    });

    currentChunk++;
    setTimeout(uploadChunk, 10); // opcional para throttling
  };

  uploadBtn.addEventListener("click", () => {
    if (!fileInput.files[0]) return;

    file = fileInput.files[0];
    totalChunks = Math.ceil(file.size / chunkSize);
    currentChunk = 0;
    paused = false;
    cancelled = false;
    uploadChunk();
  });

  pauseBtn.addEventListener("click", () => (paused = true));

  resumeBtn.addEventListener("click", () => {
    if (paused) {
      paused = false;
      uploadChunk();
    }
  });

  cancelBtn.addEventListener("click", () => {
    paused = true;
    cancelled = true;
    progressEl.value = 0;
    outputText.innerText = "Subida cancelada";
  });

  socket.on("upload_progress", (data) => {
    progressEl.value = data.progress;
    outputText.innerText = `Progreso: ${data.progress}%`;
  });
});
