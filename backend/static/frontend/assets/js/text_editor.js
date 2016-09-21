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
    let newButton = document.getElementById('new');
    runButton.addEventListener('click', () => run())
    saveButton.addEventListener('click', () => save())
    newButton.addEventListener('click', () => newDoc())
  }
});


function run() {
  let code = myCodeMirror.getValue();
  let value = eval(code);
  let output = document.getElementById('output');
  output.children[0].innerHTML = value;
}

function save() {
  if (window.openDoc) {
    let value = myCodeMirror.getValue();
    $.ajax({
      type: 'GET',
      url: '/editCode',
      data: {value, id: window.openDoc},
    });
  } else {
    let value = myCodeMirror.getValue();
    $.ajax({
      type: 'GET',
      url: '/addCode',
      data: {value},
    });
  }
}

function newDoc () {
  window.openDoc = null;
  myCodeMirror.setValue('');
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

function renameCode(id) {
  $.ajax({
    type: 'GET'
  })
}
