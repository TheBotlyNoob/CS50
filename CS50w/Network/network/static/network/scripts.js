document.addEventListener("DOMContentLoaded", async () => {
    console.log(
        document.getElementsByClassName("post-edit")[1].parentElement.children
    );
    for (let edit_elem of document.getElementsByClassName("post-edit")) {
        edit_elem.addEventListener("click", () => {
            let content = Array.from(edit_elem.parentElement.children).find(
                (elem) => elem.className == "post-content"
            ).innerHTML;

            let form = document.createElement("form");
            form.setAttribute("method", "POST");

            let textarea = document.createElement("textarea");
            textarea.setAttribute("name", "content");
            textarea.setAttribute("value", content);
            textarea.classList.add("form-control");

            form.appendChild(textarea);

            let submit = document.createElement("input");
            submit.setAttribute("type", "submit");
            submit.setAttribute("value", "Submit");
            submit.classList.add("btn");
            submit.classList.add("btn-primary");

            form.appendChild(submit);

            form.addEventListener("submit", async (e) => {});

            edit_elem.parentElement.replaceChildren(form);
        });
    }
});
