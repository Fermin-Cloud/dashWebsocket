document.addEventListener("DOMContentLoaded", () => {
  const uploadInput = getElementById("upload-data");
  const socket = io();

  if (!uploadInput) return;

  uploadInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const chunkSize = 512 * 1024; // 512 KB
    const totalChunks = Math.ceil(file.size / chunkSize);

    let currentChunk = 0;

    const uploadChunk = async () => {
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
      if (currentChunk < totalChunks) {
        await uploadChunk(); // Recursivo
      }
    };

    uploadChunk(); // Iniciar subida

    socket.on("upload_progress", (data) => {
      document.getElementById(
        "output-data-upload"
      ).innerText = `Progreso: ${data.progress}%`;
    });
  });
});
