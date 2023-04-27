//update the year in the footer
document.getElementById("year").innerHTML = new Date().getFullYear();

//color each span.avg depending on the value of innerText
//87.5-100: class a
//62.5-87.5: class b
//37.5-62.5: class c
//12.5-37.5: class d
//0-12.5: class e
let avgSpans = document.querySelectorAll(".avg");
avgSpans.forEach(span => {
    let avg = +span.innerText;
    if (avg >= 87.5) {
        span.classList.add("a");
    } else if (avg >= 62.5) {
        span.classList.add("b");
    } else if (avg >= 37.5) {
        span.classList.add("c");
    } else if (avg >= 12.5) {
        span.classList.add("d");
    } else {
        span.classList.add("e");
    }
});


//sort the order of wrappers in DOM by the avg value
let wrappers = document.querySelectorAll(".canvas-wrapper");
wrappers.forEach(wrapper => {
    let avg = +wrapper.querySelector(".avg").innerText;
    wrapper.setAttribute("avg", avg);
});

let wrapperContainer = document.getElementById("wrapper-container");
let sortedWrappers = Array.from(wrappers).sort((a, b) => {
    return b.getAttribute("avg") - a.getAttribute("avg");
});
sortedWrappers.forEach(wrapper => {
    wrapperContainer.appendChild(wrapper);
});


//count all .canvas-wrapper elements = total number of tasks
let totalCanvas = document.querySelectorAll(".canvas-wrapper").length;
//count all .canvas-wrapper.hidden elements = number of tasks that are filtered out
let hiddenCanvas = document.querySelectorAll(".canvas-wrapper.hidden").length;
updateCounts();

//filter the results if avg score values are changed
const minAvg = document.getElementById("filterMin");
const maxAvg = document.getElementById("filterMax");

minAvg.addEventListener("input", () => {
    filterResults();
});
maxAvg.addEventListener("input", () => {
    filterResults();
});

function filterResults() {
    let min = +minAvg.value;
    let max = +maxAvg.value;

    let values = document.querySelectorAll(".avg");
    values.forEach(value => {
        let avg = +value.innerText;
        if (avg < min || avg > max) {
            value.parentElement.parentElement.classList.add("hidden");
        } else {
            value.parentElement.parentElement.classList.remove("hidden");
        }
    });
    totalCanvas = document.querySelectorAll(".canvas-wrapper").length;
    hiddenCanvas = document.querySelectorAll(".canvas-wrapper.hidden").length;
    updateCounts();
}

function updateCounts() {
    let count = totalCanvas - hiddenCanvas;
    document.getElementById("total").innerText = totalCanvas;
    document.getElementById("actual").innerText = count;
}

//restrict the inputs between 0 and 100
minAvg.addEventListener("change", function () {
    if (minAvg.value < 0) {
        minAvg.value = 0;
    }
    if (minAvg.value > 100) {
        minAvg.value = 100;
    }
});
maxAvg.addEventListener("change", function () {
    if (maxAvg.value < 0) {
        maxAvg.value = 0;
    }
    if (maxAvg.value > 100) {
        maxAvg.value = 100;
    }
});