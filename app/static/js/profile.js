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



function newF(element) {
    const value = element.getAttribute("data-value");

    fetch("/profile", {
        method: "POST",
        body: new URLSearchParams({
            ch: value
        })
    })
    .then(() => {
        window.location.reload();
    });
}


function delF(element) {
    const value = element.getAttribute("data-value");

    fetch("/profile", {
        method: "POST",
        body: new URLSearchParams({
            del: value
        })
    })
    .then(() => {
        window.location.reload();
    });
}


//workouts



function drop2() {
    document.getElementById("s2").classList.toggle("display");
    document.getElementById("options2").classList.remove("display");

}

function filter2() {
    var uInput, f
    document.getElementById("options2").classList.add("display");
    uInput = document.getElementById("search2");
    f = uInput.value.toLowerCase();
    drp = document.getElementById("dropd2");
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

function newE(element) {
    const value = element.getAttribute("data-value");

    fetch("/profile", {
        method: "POST",
        body: new URLSearchParams({
            chE: value
        })
    })
    .then(() => {
        window.location.reload();
    });
}



function delE(element) {
    const value = element.getAttribute("data-value");

    fetch("/profile", {
        method: "POST",
        body: new URLSearchParams({
            delE: value
        })
    })
    .then(() => {
        window.location.reload();
    });
}



