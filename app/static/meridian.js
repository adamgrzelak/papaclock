setInterval(function() {
  let myRequest = new Request('/get_map');
  fetch(myRequest).then(response => response.json()).then(function(data) {
    let data_table = document.getElementById("papamap");
    data_table.innerHTML = data.papamap;
  });
}, 30000);
