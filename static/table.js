setInterval(function() {
  let myRequest = new Request('/get_table');
  fetch(myRequest).then(response => response.json()).then(function(data) {
    let data_table = document.getElementById("papatable");
    data_table.innerHTML = data.table;
    let icon = document.getElementById("papaicon")
    icon.innerHTML = data.icon;
  });
}, 100);
