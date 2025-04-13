window.dash_clientside = Object.assign({}, window.dash_clientside, {
  uploadNS: {
    handleUpload: function (nClicks) {
      if (!nClicks) return window.dash_clientside.no_update;

      const fileInput = document.getElementById("upload-data");
      const progressBar = document.getElementById("upload-progress");
      const pauseBtn = document.getElementById("pause-btn");
      const resumeBtn = document.getElementById("resume-btn");
      const cancelBtn = document.getElementById("cancel-btn");

      if (!fileInput || fileInput.files.length === 0) {
        return "No se seleccionó ningún archivo.";
      }

      const file = fileInput.files[0];
      const chunkSize = 1024 * 1024;
      let offset = 0;
      let chunkIndex = 0;
      const totalChunks = Math.ceil(file.size / chunkSize);
      let isPaused = false;
      let isCancelled = false;

      const sendChunk = () => {
        if (isPaused || isCancelled) return;

        const chunk = file.slice(offset, offset + chunkSize);
        const reader = new FileReader();

        reader.onload = function (event) {
          if (event.target.result) {
            fetch("/upload_chunk", {
              method: "POST",
              headers: {
                "X-Filename": file.name,
                "X-Chunk-Index": chunkIndex,
                "X-Total-Chunks": totalChunks,
                "Content-Type": "application/octet-stream",
              },
              body: event.target.result,
            })
              .then(() => {
                offset += chunk.size;
                chunkIndex++;
                const progress = Math.round((offset / file.size) * 100);
                if (progressBar) progressBar.value = progress;

                if (offset < file.size && !isCancelled) {
                  setTimeout(sendChunk, 100);
                } else if (offset >= file.size) {
                  console.log("Subida completa");
                }
              })
              .catch((error) => {
                console.error("Error en el chunk:", error);
              });
          }
        };

        reader.readAsArrayBuffer(chunk);
      };

      pauseBtn.onclick = () => {
        isPaused = true;
        console.log("⏸ Subida pausada");
      };

      resumeBtn.onclick = () => {
        if (isPaused) {
          isPaused = false;
          console.log("▶ Subida reanudada");
          sendChunk();
        }
      };

      cancelBtn.onclick = () => {
        isCancelled = true;
        offset = 0;
        chunkIndex = 0;
        if (progressBar) progressBar.value = 0;
        console.log("✖ Subida cancelada");
      };

      sendChunk();
      return `Subiendo: ${file.name}`;
    },
  },
});
