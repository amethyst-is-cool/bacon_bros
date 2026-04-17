function drop() {
    document.getElementById("s").classList.toggle("display");
    document.getElementById("options").classList.remove("display");

}



function filter() {
    var uInput, f
    document.getElementById("options").classList.add("display");
    uInput = document.getElementById("search");
    f = uInput.value.toLowerCase();
    drp = document.getElementById("dropd");
    items = drp.getElementsByTagName("p");
    for (i = 0; i < items.length; i++) {
      txt = items[i].textContent;
      if (txt.toLowerCase().indexOf(f) > -1) {
        items[i].style.display = "";
      } else {
        items[i].style.display = "none";
      }
    }
}