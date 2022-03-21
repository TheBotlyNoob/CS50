class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      command_history: [],
      result: "",
      executing: false,
      shell_id: null,
    };
  }

  componentDidMount() {
    document.body.addEventListener("click", () =>
      document.getElementById("input-area").focus()
    );

    fetch("/command_history")
      .then((res) => res.json())
      .then((res) => {
        this.setState({ ...this.state, command_history: res.commands });
      });

    document
      .getElementById("input-area")
      .addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          if (document.getElementById("input-area").value !== "") {
            this.execute(document.getElementById("input-area").value);
          }

          document.getElementById("input-area").value = "";
        } else if (event.key == "ArrowUp") {
          console.log(this.state);
          if (this.state.command_history.length > 0) {
            document.getElementById("input-area").value =
              this.state.command_history.pop();
          }
        }
      });
  }

  async execute(command) {
    this.state.executing = true;

    let form_data = new FormData();
    form_data.append("command", command);

    let res = await fetch("/execute", {
      method: "POST",
      headers: {
        "X-CSRFToken": window.csrf_token,
      },
      body: form_data,
    }).then((res) => res.json());

    this.setState({
      ...this.state,
      executing: false,
      result: res.output || res.message,
      command_history: res.command_history,
    });
  }

  render() {
    return (
      <>
        <pre id="terminal">{this.state.result}</pre>
        <span id="prompt">&gt;</span>
        <input
          autoCapitalize="off"
          autoComplete="off"
          spellCheck="false"
          type="text"
          id="input-area"
          aria-label="prompt"
        />
      </>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
