document.addEventListener('DOMContentLoaded', () => {
  let myCodeMirror = CodeMirror(document.getElementById('editor'), {
    mode: "javascript",
    lineNumbers: true,
    autoCloseBrackets: true
  });
  window.myCodeMirror = myCodeMirror;
  let windowHeight = window.innerHeight - 20;
  let editor = document.getElementById('editor')
  let output = document.getElementById('output')
  if (editor) {
    editor.style.height = `${windowHeight}px`;
    output.style.height = `${windowHeight}px`;
    let runButton = document.getElementById('run');
    let saveButton = document.getElementById('save');
    runButton.addEventListener('click', () => run())
    saveButton.addEventListener('click', () => save())
  }
});


function run() {
  let code = myCodeMirror.getValue();
  let value = eval(code);
  let output = document.getElementById('output');
  output.children[0].innerHTML = value;
}

function save() {
  let value = myCodeMirror.getValue();
  $.ajax({
    type: 'GET',
    url: '/code',
    data: {value},
  });
}


function receiveCode(id) {
  $.ajax({
    type: 'GET',
    url: '/getCode',
    data: {id},
    success: (code) => {
      myCodeMirror.setValue(code)
    }
  });
}
