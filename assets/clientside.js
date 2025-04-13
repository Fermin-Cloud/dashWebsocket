window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    show_selected_filename: function(value) {
      if (value === 'clear') {
        return "Esperando archivo..."; 
      }
      return value ? `Archivo seleccionado: ${value}` : "Esperando archivo...";
    }
  }
});
