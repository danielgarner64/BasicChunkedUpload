function loadHtmlToId(url, elmId){
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.open("GET", url, true); // Third parameter True is for asynchronous
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      if(this.status == 200){
        document.getElementById(elmId).innerHTML = xhttp.load();
      }
    }
  };
  xhttp.send(null); // Null as get request.
}
