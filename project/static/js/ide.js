let editor;

window.onload = function() 
{
    editor = ace.edit("editor");
    editor.setTheme("ace/mode/chaos");
}

function changeLanguage() 
{
    let language = document.getElementById("languages").value;  

    if (language == 'c' || language == 'cpp')
    {
        editor.session.setMode("ace/mode/c_cpp");
    } 
    else if (language == 'java') 
    {
        editor.session.setMode("ace/mode/java");
    }
    else if (language == 'python')
    {
        editor.session.setMode("ace/mode/python");
    }
}

function executeCode()
{
    $.ajax({
        url: "/judge",
        method: "POST",
        data: {
            language: $('#languages').val(),
            code: editor.getSession().getValue(),
            problem_id: $('label#problem_id').text().split(' ')[1]
        },
        success: function(response) {
            switch (response['result']) {
                case 'ACCEPTED':
                    $("button.output").text(response['result']).css('background-color', '#3ec487').css('border', '2px solid').css('border-color', '#3e56c4').show();
                    break;
                case 'WRONG ANSWER':
                    $("button.output").text(response['result']).css('background-color', '#f03a5f').show();
                    break;
                case 'COMPILATION ERROR':
                    $("button.output").text(response['result']).css('background-color', '#ffdc7d').show();
                    break;
                case 'RUNTIME ERROR':
                    $("button.output").text(response['result']).css('background-color', '#3488ce').show();
                    break;
                case 'TIME LIMIT EXCEEDED':
                    $("button.output").text(response['result']).css('background-color', '#3e56c4').show();
                    break;
            }
        }
    })
}
