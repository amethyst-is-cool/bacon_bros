function addP(element) {
    const value = element.getAttribute("data-value");

    fetch("/personalize", {
        method: "POST",
        body: new URLSearchParams({
            pound: value
        })
    })
    .then(() => {
        window.location.reload();
    });
}