const socket = io();

socket.on("connect", () => {
  console.log("Conectado al servidor WebSocket");
});

socket.on("command_output", (msg) => {
  const outputDiv = document.getElementById("command-output");
  if (outputDiv) {
    outputDiv.textContent += msg.data;
    outputDiv.scrollTop = outputDiv.scrollHeight;
  }
});

