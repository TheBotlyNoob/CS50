// Using React, ReactDOM, and @babel/standalone to use jsx

// not using DOMContentLoaded because babel already waits for it, so it will already be loaded
// Use buttons to toggle between views
document
  .querySelector("#inbox")
  .addEventListener("click", () => load_mailbox("inbox"));
document
  .querySelector("#sent")
  .addEventListener("click", () => load_mailbox("sent"));
document
  .querySelector("#archived")
  .addEventListener("click", () => load_mailbox("archive"));
document.querySelector("#compose").addEventListener("click", compose_email);

// By default, load the inbox
load_mailbox("inbox");

async function compose_email(recipiants, subject, body) {
  // Show compose view and hide other views
  hide_all();

  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value =
    recipiants instanceof Array
      ? recipiants.join(", ")
      : typeof recipiants === "string"
      ? recipiants
      : "";
  document.querySelector("#compose-subject").value = subject ?? "";
  document.querySelector("#compose-body").value = body ?? "";

  // When the send button is clicked, send the email
  document
    .querySelector("#compose-form")
    .addEventListener("submit", async () => {
      // Construct the email object
      const email = {
        recipients: document.querySelector("#compose-recipients").value,
        subject: document.querySelector("#compose-subject").value,
        body: document.querySelector("#compose-body").value,
      };

      console.log(email);

      // POST to /emails
      const response = await fetch("/emails", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(email),
      });

      // If the POST succeeded, load the sent view
      if (response.ok) {
        load_mailbox("sent");
      } else {
        alert((await response.json()).error);
      }
    });
}

async function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  hide_all();

  document.querySelector("#emails-view").style.display = "block";

  let emails = await fetch(`/emails/${mailbox}`).then((res) => res.json());

  function Mailbox() {
    return (
      <>
        <h3>{mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>

        <table className="email-list table">
          <tbody>
            {emails.map((email, key) => (
              <tr
                key={key}
                onClick={() => view_email(email.id)}
                className={email.read ? "read-email" : ""}
              >
                <td>{email.sender}</td>
                <td>{email.subject}</td>
                <td>{email.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </>
    );
  }

  ReactDOM.render(<Mailbox />, document.querySelector("#emails-view"));
}

async function view_email(email_id) {
  // Show the email and hide other views
  hide_all();

  document.querySelector("#email-view").style.display = "block";

  function Email() {
    let [email, setEmail] = React.useState({});

    React.useEffect(
      () =>
        fetch(`/emails/${email_id}`)
          .then((res) => res.json())
          .then(setEmail),
      []
    );

    return (
      <>
        {email.sender === window.user_email ? (
          <></>
        ) : (
          <button
            onClick={() =>
              fetch(`/emails/${email.id}`, {
                method: "PUT",
                body: JSON.stringify({
                  archived: !email.archived,
                }),
              }).then(() => setEmail({ ...email, archived: !email.archived }))
            }
            className="btn btn-primary"
          >
            {email.archived ? <>Unarchive</> : <>Archive</>}
          </button>
        )}

        <br />

        <span>
          <strong>From:</strong> {email.sender}
        </span>

        <br />

        <span>
          <strong>To:</strong> {email.recipients}
        </span>

        <br />

        <span>
          <strong>Subject:</strong> {email.subject}
        </span>

        <br />

        <span>
          <strong>Date:</strong> {email.timestamp}
        </span>

        <hr />

        <pre>{email.body}</pre>

        <hr />

        <button
          className="btn btn-primary"
          onClick={() =>
            compose_email(
              email.sender,
              email.subject.toLowerCase().startsWith("re:")
                ? email.subject
                : `Re: ${email.subject}`,
              `On ${email.timestamp}, ${
                email.sender
              } wrote: \n${email.body.replace(/^/gm, "\t")}`
            )
          }
        >
          Reply
        </button>
      </>
    );
  }

  ReactDOM.render(<Email />, document.querySelector("#email-view"));

  await fetch(`/emails/${email_id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      read: true,
    }),
  });
}

function hide_all() {
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
}
