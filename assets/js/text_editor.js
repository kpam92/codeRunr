document.addEventListener('DOMContentLoaded', () => {
  let myCodeMirror = CodeMirror(document.getElementById('editor'), {
    mode: "javascript",
    lineNumbers: true,
    autoCloseBrackets: true
  });
  let windowHeight = window.innerHeight - 20;
  document.getElementById('editor').style.height = `${windowHeight}px`
  document.getElementById('output').style.height = `${windowHeight}px`
  let runButton = document.getElementById('run');
  runButton.addEventListener('click', () => run(myCodeMirror))
});


function run(codemirror) {
  let code = codemirror.getValue();
  let value = eval(code);
  let output = document.getElementById('output');
  output.children[0].innerHTML = value;
}
