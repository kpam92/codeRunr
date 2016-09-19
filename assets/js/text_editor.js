document.addEventListener('DOMContentLoaded', () => {
  let myCodeMirror = CodeMirror(document.getElementById('editor'), {
    mode: "javascript",
    lineNumbers: true
  });
  let runButton = document.getElementById('run');
  runButton.onClick(run);
});


function run() {
  let textarea = document.getElementById('editor');
  let code = textarea.text();
  let functionToRun = putInFunction(code);
  functionToRun();
}

function putInFunction(code) {
  debugger;
  let stuff = () => {
    code
  }
  return stuff;
}
