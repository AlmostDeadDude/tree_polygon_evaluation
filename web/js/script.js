//check what is the page name, is it index.php or results.php
let page = window.location.pathname.split("/").pop();;

//in both cases:
//update the year in the footer
document.getElementById("year").innerHTML = new Date().getFullYear();

//specific for index.php and results.php
if (page === "index.php" || page === "") {
    // variables and dom elements
    const values = {};
    const confirmBtn = document.getElementById("confirmBtn");

    //make rating options selectable (like radio buttons)
    let tasks = document.querySelectorAll(".task-wrapper");
    tasks.forEach(task => {
        let taskID = task.id;
        //TODO: maybe just use the ID, not the whole id string ('task_[ID])
        let ratings = document.getElementById(taskID).querySelectorAll(".rating");
        ratings.forEach(rating => {
            rating.addEventListener("click", () => {
                //add class to the task_wrapper to show that it is rated
                task.classList.add("rated");
                //manage the classes of the rating options
                ratings.forEach(rating_ => {
                    rating_.classList.remove("selected");
                    rating_.classList.add("unfocused");
                });
                rating.classList.add("selected");
                rating.classList.remove("unfocused");
                //add the rating to the values array
                values[taskID] = rating.getAttribute("result-value");

                //after user selects the rating the webpage scrolls down to the next .task-wrapper:not(.rated) or button if there is no more unrated tasks
                let nextTask = document.querySelector(".task-wrapper:not(.rated)") || confirmBtn;
                if (nextTask) {
                    setTimeout(() => {
                        nextTask.scrollIntoView({
                            behavior: "smooth",
                        });
                    }, 300);
                }
            });
        });
    });

    //when confirmed the values are sent to the server = saveResults.php
    //if it returns the success message, the user is redirected to the results page = results.php
    if (confirmBtn) {
        confirmBtn.addEventListener("click", async () => {
            //confirm button should only work if all tasks are rated - otherwise the user gets a warning
            if (Object.keys(values).length < tasks.length) {
                alert("Please rate all tasks!");
                //scroll to the first task that is not rated yet
                let firstUnratedTask = document.querySelector(".task-wrapper:not(.rated)");
                firstUnratedTask.scrollIntoView({
                    behavior: "smooth",
                });

                return;
            } else {
                //send data as json 
                let data = JSON.stringify({
                    userInfo: userInfo,
                    dataInfo: dataInfo,
                    values: values,
                });
                let response = await fetch("saveResults.php", {
                    method: "POST",
                    body: data,
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
                let result = await response.text();
                console.log(result);
                if (result == "success") {
                    window.location.href = "results.php?vcode=" + userInfo.vcode;
                }
            }
        });
    }
} else if (page === "results.php") {
    //the results page onle needs a simple button to copy the vcode to the clipboard
    const copyBtn = document.getElementById("copyVcodeBtn");
    const vcodeEl = document.getElementById("vcodeContainer");
    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(vcodeEl.innerText.trim());
        copyBtn.innerText = "Copied!";
    });
} else {
    //page === "about.php"
    //disable the link to about php - it is not needed
    document.querySelector('header a').remove();
}