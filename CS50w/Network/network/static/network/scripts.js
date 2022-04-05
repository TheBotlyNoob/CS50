document.addEventListener("DOMContentLoaded", async () => {
  setup_edit_elements();

  setup_like_elements();

  setup_follow_elements();
});

function setup_edit_elements() {
  for (let edit_elem of document.getElementsByClassName("post-edit")) {
    let children = edit_elem.parentElement.children;

    edit_elem.addEventListener("click", () => {
      for (let child of children) {
        child.previous_display = child.style.display;
        child.style.display = "none";
      }

      let content = Array.from(edit_elem.parentElement.children).find(
        (elem) => elem.className == "post-content"
      ).innerHTML;

      let form = document.createElement("form");
      form.setAttribute("method", "POST");

      let textarea = document.createElement("textarea");
      textarea.setAttribute("name", "content");
      textarea.textContent = content;
      textarea.classList.add("form-control");

      form.appendChild(textarea);

      let submit = document.createElement("input");
      submit.setAttribute("type", "submit");
      submit.setAttribute("value", "Submit");
      submit.classList.add("btn");
      submit.classList.add("btn-primary");

      form.appendChild(submit);

      form.addEventListener("submit", async (e) => {
        e.preventDefault();

        let form_data = new FormData(form);
        form_data.append(
          "post_id",
          e.submitter.parentElement.parentElement.dataset.postId
        );

        let res = await fetch("/edit", {
          method: "POST",
          headers: {
            "X-CSRFToken": window.csrf_token,
          },
          body: form_data,
          mode: "same-origin",
        }).then((res) => res.json());

        form.remove();

        for (let child of children) {
          if (child.classList.contains("post-content")) {
            child.innerHTML = res.post.content;
          } else if (child.classList.contains("post-updated-at")) {
            child.innerHTML = `updated ${new Date(res.post.updated_at)
              .toLocaleString("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric",
                timezone: "EST",
                hour: "numeric",
                minute: "numeric",
              })
              .replace(/([AP])M/g, (_, p1) => `${p1.toLowerCase()}.m.`)}`;
          }

          child.style.display = child.previous_display;
        }
      });

      edit_elem.parentElement.appendChild(form);
    });
  }
}

function setup_like_elements() {
  for (let like_elem of document.getElementsByClassName("post-like")) {
    let post_id = like_elem.parentElement.parentElement.dataset.postId;

    let form_data = new FormData();
    form_data.append("post_id", post_id);

    like_elem.addEventListener("click", async (e) => {
      let res = await fetch("/like", {
        method: "POST",
        headers: {
          "X-CSRFToken": window.csrf_token,
        },
        body: form_data,
        mode: "same-origin",
      }).then((res) => res.json());

      let children = Array.from(like_elem.parentElement.children);

      children.find((elem) =>
        elem.classList.contains("post-likes")
      ).innerHTML = `${res.post.liked.length} like(s)`;

      let like_button_elem = children.find((elem) =>
        elem.classList.contains("post-like")
      );

      if (like_button_elem.classList.contains("post-liked")) {
        like_button_elem.innerHTML = "♡";
        like_button_elem.classList.remove("post-liked");
      } else {
        like_button_elem.innerHTML = "♥";
        like_button_elem.classList.add("post-liked");
      }
    });
  }
}

function setup_follow_elements() {
  for (let follow_elem of document.getElementsByClassName("follow-button")) {
    follow_elem.addEventListener("click", async (e) => {
      let form_data = new FormData();
      form_data.append("user_id", window.location.pathname.split("/")[2]);

      let followers = await fetch("/follow", {
        method: "POST",
        headers: {
          "X-CSRFToken": window.csrf_token,
        },
        body: form_data,
        mode: "same-origin",
      })
        .then((res) => res.json())
        .then((res) => res.followers);

      if (follow_elem.classList.contains("following")) {
        follow_elem.innerHTML = "Follow";
        follow_elem.classList.remove("following");
      } else {
        follow_elem.innerHTML = "Unfollow";
        follow_elem.classList.add("following");
      }

      Array.from(follow_elem.parentElement.children).find(
        ({ tagName }) => tagName == "H5"
      ).innerHTML = `${followers} following`;
    });
  }
}
