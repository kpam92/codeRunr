document.addEventListener('DOMContentLoaded', () => {
  let myCodeMirror = CodeMirror(document.getElementById('editor'), {
    mode: "javascript",
    lineNumbers: true
  });
  let runButton = document.getElementById('run');
  runButton.addEventListener('click', () => run(myCodeMirror))
});


function run(codemirror) {
  let code = codemirror.getValue();
  let value = eval(code);
  let output = document.getElementById('output');
  output.innerHTML = value;
}
