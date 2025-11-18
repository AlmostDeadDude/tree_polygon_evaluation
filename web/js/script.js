//check what is the page name, is it index.php
let page = window.location.pathname.split("/").pop();;

//specific for index.php
if (page === "index.php" || page === "") {
    // variables and dom elements
    const values = {};
    const confirmBtn = document.getElementById("confirmBtn");
    const completionBox = document.getElementById("demoComplete");

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

    //when confirmed the values stay local in demo mode, but we still show the proof code
    if (confirmBtn) {
        confirmBtn.addEventListener("click", () => {
            //confirm button should only work if all tasks are rated - otherwise the user gets a warning
            if (Object.keys(values).length < tasks.length) {
                alert("Please rate all tasks!");
                //scroll to the first task that is not rated yet
                let firstUnratedTask = document.querySelector(".task-wrapper:not(.rated)");
                firstUnratedTask.scrollIntoView({
                    behavior: "smooth",
                });
                return;
            }

            confirmBtn.disabled = true;
            confirmBtn.innerText = "Demo completed";

            if (completionBox) {
                completionBox.innerHTML = `
                    <p>Great! Your demo proof code is <strong>${userInfo.proofCode}</strong>. Workers submitted this code on the crowdsourcing platform to confirm completion and receive payment.</p>
                    <div class="demo-actions">
                        <a class="primary-link" href="../visualisation/visu.php" target="_blank" rel="noopener noreferrer">Open visualisation</a>
                        <a class="secondary-link" href="index.php">Rate another job</a>
                    </div>
                `;
                completionBox.classList.add("visible");
                setTimeout(() => {
                    completionBox.scrollIntoView({
                        behavior: "smooth",
                    });
                }, 150);
            }
        });
    }
}
